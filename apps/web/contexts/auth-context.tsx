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
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Initialize auth state by checking if user is authenticated via cookies
  useEffect(() => {
    const initAuth = async () => {
      try {
        // Try to fetch current user - cookies are sent automatically
        const response = await fetch(`${API_URL}/api/v1/auth/me`, {
          credentials: "include",
        });

        if (response.ok) {
          const userData = await response.json();
          setUser(userData);
        }
      } catch (error) {
        console.error("Failed to restore auth state:", error);
      } finally {
        setIsLoading(false);
      }
    };

    initAuth();
  }, []);

  const login = useCallback(
    async (email: string): Promise<{ success: boolean; message: string }> => {
      try {
        const response = await fetch(`${API_URL}/api/v1/auth/magic-link`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
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

  // verifyToken is now handled by the backend setting cookies
  // This method is kept for backward compatibility with magic link callbacks
  const verifyToken = useCallback(async (token: string): Promise<boolean> => {
    try {
      const response = await fetch(
        `${API_URL}/api/v1/auth/verify?token=${encodeURIComponent(token)}`,
        {
          method: "GET",
          credentials: "include",
        }
      );

      if (!response.ok) {
        return false;
      }

      // Cookies are set by backend, now fetch user
      const userResponse = await fetch(`${API_URL}/api/v1/auth/me`, {
        credentials: "include",
      });

      if (userResponse.ok) {
        const userData = await userResponse.json();
        setUser(userData);
        return true;
      }

      return false;
    } catch (error) {
      console.error("Token verification error:", error);
      return false;
    }
  }, []);

  const logout = useCallback(async (): Promise<void> => {
    try {
      await fetch(`${API_URL}/api/v1/auth/logout`, {
        method: "POST",
        credentials: "include",
      });
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      setUser(null);
    }
  }, []);

  const refresh = useCallback(async (): Promise<boolean> => {
    try {
      const response = await fetch(`${API_URL}/api/v1/auth/refresh`, {
        method: "POST",
        credentials: "include",
      });

      if (!response.ok) {
        // Token is invalid, logout
        await logout();
        return false;
      }

      // Cookies are refreshed by backend, fetch user to update state
      const userResponse = await fetch(`${API_URL}/api/v1/auth/me`, {
        credentials: "include",
      });

      if (userResponse.ok) {
        const userData = await userResponse.json();
        setUser(userData);
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
        const response = await fetch(`${API_URL}/api/v1/auth/me`, {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
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

  const value: AuthContextType = {
    user,
    isLoading,
    isAuthenticated: !!user,
    login,
    verifyToken,
    logout,
    refresh,
    updateProfile,
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

// Helper function to make authenticated API calls
// Note: With HttpOnly cookies, we just need to include credentials
export async function fetchWithAuth(
  url: string,
  options: RequestInit = {}
): Promise<Response> {
  return fetch(url, {
    ...options,
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });
}
