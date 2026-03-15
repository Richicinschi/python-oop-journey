/**
 * Hook for making API calls with automatic CSRF token handling.
 *
 * This hook wraps the api client and automatically includes CSRF tokens
 * for state-changing requests. It also provides loading and error states.
 */

import { useState, useCallback, useRef } from 'react';
import { useCsrf } from '@/contexts/csrf-context';
import api, { ApiError } from '@/lib/api';

interface UseApiState<T> {
  data: T | null;
  isLoading: boolean;
  error: ApiError | null;
}

interface UseApiReturn<T> extends UseApiState<T> {
  execute: (...args: unknown[]) => Promise<T | null>;
  reset: () => void;
}

type ApiFunction<T> = (...args: unknown[]) => Promise<T>;

/**
 * Hook for making API calls with automatic CSRF handling
 * 
 * @param apiFunction - The API function to call
 * @returns Object with data, loading state, error, execute function, and reset function
 * 
 * @example
 * ```tsx
 * const { data, isLoading, error, execute } = useApi(api.progress.getAll);
 * 
 * useEffect(() => {
 *   execute();
 * }, [execute]);
 * ```
 */
export function useApi<T>(apiFunction: ApiFunction<T>): UseApiReturn<T> {
  const [state, setState] = useState<UseApiState<T>>({
    data: null,
    isLoading: false,
    error: null,
  });

  const abortControllerRef = useRef<AbortController | null>(null);

  const execute = useCallback(
    async (...args: unknown[]): Promise<T | null> => {
      // Cancel previous request if exists
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }

      // Create new abort controller for this request
      abortControllerRef.current = new AbortController();

      setState((prev) => ({ ...prev, isLoading: true, error: null }));

      try {
        const result = await apiFunction(...args);
        setState({ data: result, isLoading: false, error: null });
        return result;
      } catch (err) {
        const error = err instanceof ApiError ? err : new ApiError(500, 'Unknown error');
        setState((prev) => ({ ...prev, isLoading: false, error }));
        return null;
      }
    },
    [apiFunction]
  );

  const reset = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
    setState({ data: null, isLoading: false, error: null });
  }, []);

  return {
    ...state,
    execute,
    reset,
  };
}

/**
 * Hook for making authenticated API calls with CSRF protection
 * 
 * This hook is specifically designed for state-changing operations
 * that require CSRF tokens. It waits for the CSRF token to be available
 * before making the request.
 * 
 * @example
 * ```tsx
 * const { execute, isLoading } = useApiWithCsrf();
 * 
 * const handleSubmit = async (data: FormData) => {
 *   await execute(() => api.submissions.submit(projectSlug, data));
 * };
 * ```
 */
export function useApiWithCsrf() {
  const { getToken, refreshToken } = useCsrf();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);

  const execute = useCallback(
    async <T,>(apiCall: () => Promise<T>): Promise<T | null> => {
      setIsLoading(true);
      setError(null);

      try {
        // Ensure CSRF token is available
        const csrfToken = await getToken();
        
        if (!csrfToken) {
          throw new ApiError(403, 'CSRF token not available');
        }

        const result = await apiCall();
        setIsLoading(false);
        return result;
      } catch (err) {
        const apiError = err instanceof ApiError ? err : new ApiError(500, 'Request failed');
        
        // Handle CSRF token expiration
        if (apiError.status === 403 && apiError.message.toLowerCase().includes('csrf')) {
          // Try to refresh token once
          try {
            await refreshToken();
            const newToken = await getToken();
            
            if (newToken) {
              // Retry the request
              const result = await apiCall();
              setIsLoading(false);
              return result;
            }
          } catch {
            // Refresh failed
          }
        }

        setError(apiError);
        setIsLoading(false);
        return null;
      }
    },
    [getToken, refreshToken]
  );

  return {
    execute,
    isLoading,
    error,
  };
}

/**
 * Hook for making CSRF-protected mutations
 * 
 * Simplified hook for POST/PUT/DELETE operations with automatic
 * CSRF token handling and optimistic updates support.
 * 
 * @example
 * ```tsx
 * const mutation = useMutation(api.bookmarks.create);
 * 
 * const handleCreate = async (data) => {
 *   await mutation.mutate(data);
 * };
 * ```
 */
export function useMutation<T, V = unknown>(
  mutationFn: (variables: V) => Promise<T>
) {
  const { getToken } = useCsrf();
  const [isPending, setIsPending] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [isError, setIsError] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);
  const [data, setData] = useState<T | null>(null);

  const mutate = useCallback(
    async (
      variables: V,
      options?: {
        onSuccess?: (data: T) => void;
        onError?: (error: ApiError) => void;
      }
    ): Promise<T | null> => {
      setIsPending(true);
      setIsSuccess(false);
      setIsError(false);
      setError(null);

      try {
        // Ensure token is available
        await getToken();
        
        const result = await mutationFn(variables);
        setData(result);
        setIsSuccess(true);
        options?.onSuccess?.(result);
        return result;
      } catch (err) {
        const apiError = err instanceof ApiError ? err : new ApiError(500, 'Mutation failed');
        setError(apiError);
        setIsError(true);
        options?.onError?.(apiError);
        return null;
      } finally {
        setIsPending(false);
      }
    },
    [getToken, mutationFn]
  );

  const reset = useCallback(() => {
    setIsPending(false);
    setIsSuccess(false);
    setIsError(false);
    setError(null);
    setData(null);
  }, []);

  return {
    mutate,
    reset,
    isPending,
    isSuccess,
    isError,
    error,
    data,
  };
}

export default useApi;
