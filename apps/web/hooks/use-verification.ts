"use client";

import { useState, useCallback } from "react";
import {
  verificationApi,
  VerificationRequest,
  VerificationResponse,
  SyntaxValidationResponse,
  VerificationApiError,
} from "@/lib/verification-api";

interface UseVerificationState {
  data: VerificationResponse | null;
  isLoading: boolean;
  error: string | null;
}

interface UseVerificationReturn extends UseVerificationState {
  verify: (request: VerificationRequest) => Promise<void>;
  validateSyntax: (code: string) => Promise<SyntaxValidationResponse>;
  reset: () => void;
  retry: () => void;
}

// Store last request for retry functionality
let lastRequest: VerificationRequest | null = null;

/**
 * React hook for code verification
 * 
 * @example
 * ```tsx
 * const { verify, data, isLoading, error } = useVerification();
 * 
 * const handleSubmit = async (code: string) => {
 *   await verify({ code, problem_slug: "w01d01-hello-object" });
 * };
 * ```
 */
export function useVerification(): UseVerificationReturn {
  const [state, setState] = useState<UseVerificationState>({
    data: null,
    isLoading: false,
    error: null,
  });

  const verify = useCallback(async (request: VerificationRequest) => {
    // Store request for potential retry
    lastRequest = request;

    setState((prev) => ({ ...prev, isLoading: true, error: null }));

    try {
      const response = await verificationApi.verify(request);
      setState({
        data: response,
        isLoading: false,
        error: null,
      });
    } catch (err) {
      const errorMessage =
        err instanceof VerificationApiError
          ? err.message
          : err instanceof Error
          ? err.message
          : "An unexpected error occurred";

      setState({
        data: null,
        isLoading: false,
        error: errorMessage,
      });
    }
  }, []);

  const validateSyntax = useCallback(async (code: string) => {
    return verificationApi.validateSyntax(code);
  }, []);

  const reset = useCallback(() => {
    setState({
      data: null,
      isLoading: false,
      error: null,
    });
    lastRequest = null;
  }, []);

  const retry = useCallback(async () => {
    if (lastRequest) {
      await verify(lastRequest);
    }
  }, [verify]);

  return {
    ...state,
    verify,
    validateSyntax,
    reset,
    retry,
  };
}

/**
 * Hook for pre-fetching test information
 */
export function useTestInfo(problemSlug: string | null) {
  const [testInfo, setTestInfo] = useState<{
    data: { test_count: number; test_names: string[] } | null;
    isLoading: boolean;
    error: string | null;
  }>({
    data: null,
    isLoading: false,
    error: null,
  });

  const fetchTestInfo = useCallback(async () => {
    if (!problemSlug) return;

    setTestInfo((prev) => ({ ...prev, isLoading: true, error: null }));

    try {
      const data = await verificationApi.getTestInfo(problemSlug);
      setTestInfo({
        data: {
          test_count: data.test_count,
          test_names: data.test_names,
        },
        isLoading: false,
        error: null,
      });
    } catch (err) {
      setTestInfo({
        data: null,
        isLoading: false,
        error: "Failed to load test information",
      });
    }
  }, [problemSlug]);

  return {
    ...testInfo,
    fetchTestInfo,
  };
}

export default useVerification;
