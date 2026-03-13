/**
 * Verification API client for test execution
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:3001";

export interface VerificationRequest {
  code: string;
  problem_slug: string;
  test_code?: string;
}

export interface TestResult {
  name: string;
  status: "passed" | "failed" | "error" | "skipped" | "timeout";
  message?: string;
  expected?: string;
  actual?: string;
  hint?: string;
  error_category?: string;
  duration_ms?: number;
}

export interface VerificationSummary {
  total: number;
  passed: number;
  failed: number;
  errors: number;
  skipped?: number;
}

export interface HintSuggestion {
  hint_index: number;
  reason: string;
  confidence: string;
}

export interface VerificationResponse {
  success: boolean;
  summary: VerificationSummary;
  tests: TestResult[];
  stdout: string;
  stderr: string;
  execution_time_ms: number;
  suggested_hints: HintSuggestion[];
  progress_updated: boolean;
  attempts?: number;
}

export interface TestInfo {
  problem_slug: string;
  problem_title: string;
  test_count: number;
  test_names: string[];
  has_tests: boolean;
}

export interface SyntaxValidationResponse {
  valid: boolean;
  error?: string;
  message: string;
}

class VerificationApiError extends Error {
  constructor(
    public status: number,
    message: string,
    public data?: unknown
  ) {
    super(message);
    this.name = "VerificationApiError";
  }
}

async function apiClient<T>(
  endpoint: string,
  options: {
    method?: "GET" | "POST";
    body?: unknown;
    headers?: Record<string, string>;
  } = {}
): Promise<T> {
  const { method = "GET", body, headers = {} } = options;

  const url = `${API_BASE_URL}/api/v1${endpoint}`;

  const config: RequestInit = {
    method,
    headers: {
      "Content-Type": "application/json",
      ...headers,
    },
    credentials: "include",
  };

  if (body) {
    config.body = JSON.stringify(body);
  }

  const response = await fetch(url, config);
  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new VerificationApiError(
      response.status,
      data?.detail || data?.message || `HTTP error! status: ${response.status}`,
      data
    );
  }

  return data as T;
}

/**
 * Verification API methods
 */
export const verificationApi = {
  /**
   * Verify a solution against test cases
   */
  verify: async (request: VerificationRequest): Promise<VerificationResponse> => {
    return apiClient<VerificationResponse>("/verify", {
      method: "POST",
      body: request,
    });
  },

  /**
   * Verify a solution for a specific problem (URL-based)
   */
  verifyForProblem: async (
    problemSlug: string,
    code: string
  ): Promise<VerificationResponse> => {
    return apiClient<VerificationResponse>(`/verify/${problemSlug}`, {
      method: "POST",
      body: { code },
    });
  },

  /**
   * Validate code syntax without running tests
   */
  validateSyntax: async (code: string): Promise<SyntaxValidationResponse> => {
    return apiClient<SyntaxValidationResponse>("/validate-syntax", {
      method: "POST",
      body: { code },
    });
  },

  /**
   * Get test information for a problem
   */
  getTestInfo: async (problemSlug: string): Promise<TestInfo> => {
    return apiClient<TestInfo>(`/test-info/${problemSlug}`);
  },
};

/**
 * React hook for verification
 */
export function useVerification() {
  const verify = async (request: VerificationRequest): Promise<VerificationResponse> => {
    return verificationApi.verify(request);
  };

  const validateSyntax = async (code: string): Promise<SyntaxValidationResponse> => {
    return verificationApi.validateSyntax(code);
  };

  return {
    verify,
    validateSyntax,
  };
}

export { VerificationApiError };
export default verificationApi;
