"use client";

import {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  ReactNode,
} from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface User {
  id: string;
  email: string;
  display_name: string | null;
  created_at: string;
  updated_at: string;
  last_login_at: string | null;
  last_seen: string;
  is_active: boolean;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string) => Promise<{ success: boolean; message: string }>;
  verifyToken: (token: string) => Promise<boolean>;
  logout: () => Promise<void>;
  refresh: () => Promise<boolean>;
  updateProfile: (data: { display_name: string }) => Promise<boolean>;
  setToken: (token: string) => Promise<boolean>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Storage key for JWT
const TOKEN_KEY = "auth_token";
const USER_KEY = "auth_user";

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Initialize auth state from storage
  useEffect(() => {
    const initAuth = () => {
      try {
        const storedUser = localStorage.getItem(USER_KEY);
        const token = localStorage.getItem(TOKEN_KEY);

        if (storedUser && token) {
          const parsedUser = JSON.parse(storedUser);
          setUser(parsedUser);
        }
      } catch (error) {
        console.error("Failed to restore auth state:", error);
      } finally {
        setIsLoading(false);
      }
    };

    initAuth();
  }, []);

  // Store user in localStorage when it changes
  useEffect(() => {
    if (user) {
      localStorage.setItem(USER_KEY, JSON.stringify(user));
    } else {
      localStorage.removeItem(USER_KEY);
    }
  }, [user]);

  const login = useCallback(
    async (email: string): Promise<{ success: boolean; message: string }> => {
      try {
        const response = await fetch(`${API_URL}/api/v1/auth/magic-link`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email }),
        });

        const data = await response.json();

        if (response.ok) {
          return {
            success: true,
            message: data.message || "Check your email for the magic link",
          };
        }

        return {
          success: false,
          message: data.detail || "Failed to send magic link",
        };
      } catch (error) {
        console.error("Login error:", error);
        return {
          success: false,
          message: "Network error. Please try again.",
        };
      }
    },
    []
  );

  const verifyToken = useCallback(async (token: string): Promise<boolean> => {
    try {
      const response = await fetch(
        `${API_URL}/api/v1/auth/verify?token=${encodeURIComponent(token)}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        return false;
      }

      const data = await response.json();

      if (data.access_token) {
        localStorage.setItem(TOKEN_KEY, data.access_token);

        // Fetch user profile
        const userResponse = await fetch(`${API_URL}/api/v1/auth/me`, {
          headers: {
            Authorization: `Bearer ${data.access_token}`,
          },
        });

        if (userResponse.ok) {
          const userData = await userResponse.json();
          setUser(userData);
          return true;
        }
      }

      return false;
    } catch (error) {
      console.error("Token verification error:", error);
      return false;
    }
  }, []);

  const logout = useCallback(async (): Promise<void> => {
    try {
      const token = localStorage.getItem(TOKEN_KEY);

      if (token) {
        await fetch(`${API_URL}/api/v1/auth/logout`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
      }
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(USER_KEY);
      setUser(null);
    }
  }, []);

  const refresh = useCallback(async (): Promise<boolean> => {
    try {
      const token = localStorage.getItem(TOKEN_KEY);

      if (!token) {
        return false;
      }

      const response = await fetch(`${API_URL}/api/v1/auth/refresh`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        // Token is invalid, logout
        await logout();
        return false;
      }

      const data = await response.json();

      if (data.access_token) {
        localStorage.setItem(TOKEN_KEY, data.access_token);
        return true;
      }

      return false;
    } catch (error) {
      console.error("Token refresh error:", error);
      return false;
    }
  }, [logout]);

  const updateProfile = useCallback(
    async (data: { display_name: string }): Promise<boolean> => {
      try {
        const token = localStorage.getItem(TOKEN_KEY);

        if (!token) {
          return false;
        }

        const response = await fetch(`${API_URL}/api/v1/auth/me`, {
          method: "PATCH",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        });

        if (response.ok) {
          const updatedUser = await response.json();
          setUser(updatedUser);
          return true;
        }

        return false;
      } catch (error) {
        console.error("Profile update error:", error);
        return false;
      }
    },
    []
  );

  // Set token from OAuth callback
  const setToken = useCallback(async (token: string): Promise<boolean> => {
    try {
      localStorage.setItem(TOKEN_KEY, token);
      
      // Fetch user with the token
      const response = await fetch(`${API_URL}/api/v1/auth/me`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      
      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
        return true;
      }
      
      // If fetching user fails, clear token
      localStorage.removeItem(TOKEN_KEY);
      return false;
    } catch (error) {
      console.error("Set token error:", error);
      localStorage.removeItem(TOKEN_KEY);
      return false;
    }
  }, []);

  const value: AuthContextType = {
    user,
    isLoading,
    isAuthenticated: !!user,
    login,
    verifyToken,
    logout,
    refresh,
    updateProfile,
    setToken,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }

  return context;
}

// Helper function to get auth token for API calls
export function getAuthToken(): string | null {
  if (typeof window === "undefined") {
    return null;
  }
  return localStorage.getItem(TOKEN_KEY);
}

// Helper function to make authenticated API calls
export async function fetchWithAuth(
  url: string,
  options: RequestInit = {}
): Promise<Response> {
  const token = getAuthToken();

  const headers = {
    ...options.headers,
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };

  return fetch(url, {
    ...options,
    headers,
  });
}
