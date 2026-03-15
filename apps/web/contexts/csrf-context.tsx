/**
 * CSRF Protection Context.
 *
 * Provides CSRF token management for the application.
 * Fetches tokens from the backend and includes them in state-changing requests.
 */

import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  ReactNode,
} from 'react';

// CSRF token response from backend
interface CsrfTokenResponse {
  csrf_token: string;
  token_name: string;
  header_name: string;
  refreshed: boolean;
}

// Context value type
interface CsrfContextValue {
  /** The current CSRF token */
  token: string | null;
  /** Whether the token is being fetched */
  isLoading: boolean;
  /** Error if token fetch failed */
  error: Error | null;
  /** Manually refresh the CSRF token */
  refreshToken: () => Promise<void>;
  /** Get the token (fetches if not available) */
  getToken: () => Promise<string | null>;
  /** Clear the current token */
  clearToken: () => void;
}

const CsrfContext = createContext<CsrfContextValue | undefined>(undefined);

// API base URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';

// Storage key for CSRF token
const CSRF_STORAGE_KEY = 'csrf_token';
const CSRF_STORAGE_TIMESTAMP = 'csrf_token_timestamp';
const TOKEN_LIFETIME_MS = 23 * 60 * 60 * 1000; // 23 hours (token expires at 24)

interface CsrfProviderProps {
  children: ReactNode;
}

/**
 * Check if we're in a browser environment
 */
const isBrowser = typeof window !== 'undefined';

/**
 * Get stored token from localStorage
 */
function getStoredToken(): { token: string | null; isValid: boolean } {
  if (!isBrowser) return { token: null, isValid: false };
  
  try {
    const token = localStorage.getItem(CSRF_STORAGE_KEY);
    const timestamp = localStorage.getItem(CSRF_STORAGE_TIMESTAMP);
    
    if (!token || !timestamp) {
      return { token: null, isValid: false };
    }
    
    const age = Date.now() - parseInt(timestamp, 10);
    const isValid = age < TOKEN_LIFETIME_MS;
    
    return { token, isValid };
  } catch {
    // localStorage not available
    return { token: null, isValid: false };
  }
}

/**
 * Store token in localStorage
 */
function storeToken(token: string): void {
  if (!isBrowser) return;
  
  try {
    localStorage.setItem(CSRF_STORAGE_KEY, token);
    localStorage.setItem(CSRF_STORAGE_TIMESTAMP, Date.now().toString());
  } catch {
    // localStorage not available
  }
}

/**
 * Clear stored token
 */
function clearStoredToken(): void {
  if (!isBrowser) return;
  
  try {
    localStorage.removeItem(CSRF_STORAGE_KEY);
    localStorage.removeItem(CSRF_STORAGE_TIMESTAMP);
  } catch {
    // localStorage not available
  }
}

/**
 * CSRF Provider Component
 * 
 * Wraps the application to provide CSRF token management.
 * Automatically fetches a token on mount and provides methods
 * to refresh or retrieve the token.
 * 
 * @example
 * ```tsx
 * <CsrfProvider>
 *   <App />
 * </CsrfProvider>
 * ```
 */
export function CsrfProvider({ children }: CsrfProviderProps): JSX.Element {
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [initialized, setInitialized] = useState(false);

  /**
   * Fetch a new CSRF token from the backend
   */
  const fetchToken = useCallback(async (): Promise<string | null> => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/csrf-token`, {
        method: 'GET',
        credentials: 'include', // Include cookies for session identification
        headers: {
          'Accept': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.error || `Failed to fetch CSRF token: ${response.status}`
        );
      }

      const data: CsrfTokenResponse = await response.json();
      
      if (!data.csrf_token) {
        throw new Error('Invalid CSRF token response');
      }

      storeToken(data.csrf_token);
      setToken(data.csrf_token);
      setError(null);
      
      return data.csrf_token;
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to fetch CSRF token');
      setError(error);
      console.error('[CSRF] Failed to fetch token:', error);
      return null;
    }
  }, []);

  /**
   * Refresh the CSRF token (force new token)
   */
  const refreshToken = useCallback(async (): Promise<void> => {
    setIsLoading(true);
    clearStoredToken();
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/csrf-refresh`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Accept': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to refresh CSRF token: ${response.status}`);
      }

      const data: CsrfTokenResponse = await response.json();
      storeToken(data.csrf_token);
      setToken(data.csrf_token);
      setError(null);
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to refresh CSRF token');
      setError(error);
      console.error('[CSRF] Failed to refresh token:', error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Get the current token or fetch a new one
   */
  const getToken = useCallback(async (): Promise<string | null> => {
    // Check if we have a valid token in memory
    if (token) {
      return token;
    }

    // Check localStorage for cached token
    const { token: storedToken, isValid } = getStoredToken();
    if (storedToken && isValid) {
      setToken(storedToken);
      return storedToken;
    }

    // Fetch new token
    setIsLoading(true);
    const newToken = await fetchToken();
    setIsLoading(false);
    return newToken;
  }, [token, fetchToken]);

  /**
   * Clear the current token
   */
  const clearToken = useCallback((): void => {
    setToken(null);
    clearStoredToken();
  }, []);

  // Initialize: try to load cached token or fetch new one
  useEffect(() => {
    if (initialized) return;
    
    const init = async (): Promise<void> => {
      // First check localStorage
      const { token: storedToken, isValid } = getStoredToken();
      
      if (storedToken && isValid) {
        setToken(storedToken);
        setInitialized(true);
        return;
      }

      // Fetch new token
      setIsLoading(true);
      await fetchToken();
      setIsLoading(false);
      setInitialized(true);
    };

    init();
  }, [initialized, fetchToken]);

  const value: CsrfContextValue = {
    token,
    isLoading,
    error,
    refreshToken,
    getToken,
    clearToken,
  };

  return (
    <CsrfContext.Provider value={value}>
      {children}
    </CsrfContext.Provider>
  );
}

/**
 * Hook to access CSRF context
 * 
 * @throws Error if used outside of CsrfProvider
 * 
 * @example
 * ```tsx
 * const { token, getToken } = useCsrf();
 * 
 * // In a form submission:
 * const handleSubmit = async () => {
 *   const csrfToken = await getToken();
 *   await fetch('/api/submit', {
 *     method: 'POST',
 *     headers: {
 *       'X-CSRF-Token': csrfToken,
 *     },
 *   });
 * };
 * ```
 */
export function useCsrf(): CsrfContextValue {
  const context = useContext(CsrfContext);
  if (context === undefined) {
    throw new Error('useCsrf must be used within a CsrfProvider');
  }
  return context;
}

/**
 * Hook to get CSRF token synchronously (may be null if not loaded)
 * Use getToken() from useCsrf() if you need to ensure token is available
 * 
 * @example
 * ```tsx
 * const token = useCsrfToken();
 * ```
 */
export function useCsrfToken(): string | null {
  const context = useContext(CsrfContext);
  if (context === undefined) {
    throw new Error('useCsrfToken must be used within a CsrfProvider');
  }
  return context.token;
}

export default CsrfContext;
