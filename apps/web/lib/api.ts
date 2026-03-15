const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';

interface ApiOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  body?: unknown;
  headers?: Record<string, string>;
  token?: string;
  csrfToken?: string;
}

class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
    public data?: unknown
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

/**
 * Get CSRF token from localStorage
 */
function getCsrfToken(): string | null {
  if (typeof window === 'undefined') return null;
  
  try {
    return localStorage.getItem('csrf_token');
  } catch {
    return null;
  }
}

/**
 * State-changing HTTP methods that require CSRF protection
 */
const STATE_CHANGING_METHODS = ['POST', 'PUT', 'DELETE', 'PATCH'];

async function apiClient<T>(
  endpoint: string,
  options: ApiOptions = {}
): Promise<T> {
  const { method = 'GET', body, headers = {}, token, csrfToken } = options;

  const url = `${API_BASE_URL}${endpoint}`;

  const config: RequestInit = {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...headers,
    },
    credentials: 'include',  // Always include cookies for authentication
  };

  // Add auth token if provided (for backward compatibility)
  // Note: With HttpOnly cookies, the browser sends them automatically
  if (token) {
    config.headers = {
      ...config.headers,
      'Authorization': `Bearer ${token}`,
    };
  }

  // Add CSRF token for state-changing requests
  if (STATE_CHANGING_METHODS.includes(method)) {
    const csrf = csrfToken || getCsrfToken();
    if (csrf) {
      config.headers = {
        ...config.headers,
        'X-CSRF-Token': csrf,
      };
    }
  }

  if (body) {
    config.body = JSON.stringify(body);
  }

  try {
    const response = await fetch(url, config);
    
    // Handle 403 CSRF errors - token may have expired
    if (response.status === 403) {
      const data = await response.json().catch(() => null);
      if (data?.error?.toLowerCase().includes('csrf')) {
        // Clear expired token so next request fetches a new one
        try {
          localStorage.removeItem('csrf_token');
          localStorage.removeItem('csrf_token_timestamp');
        } catch {
          // localStorage not available
        }
        throw new ApiError(
          403,
          'CSRF token expired. Please refresh the page and try again.',
          data
        );
      }
    }
    
    // Handle 204 No Content
    if (response.status === 204) {
      return undefined as T;
    }
    
    const data = await response.json().catch(() => null);

    if (!response.ok) {
      throw new ApiError(
        response.status,
        data?.message || data?.error || `HTTP error! status: ${response.status}`,
        data
      );
    }

    return data as T;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(500, error instanceof Error ? error.message : 'Network error');
  }
}

// Types
export interface Problem {
  slug: string;
  title: string;
  description: string;
  difficulty: 'easy' | 'medium' | 'hard';
  weekNumber: number;
  dayNumber: number;
}

export interface SubmissionResult {
  success: boolean;
  message: string;
  testResults: TestResult[];
}

export interface TestResult {
  passed: boolean;
  testCase: number;
  expected: string;
  actual: string;
}

export interface RunResult {
  output: string;
  error?: string;
  executionTime: number;
}

export interface Week {
  slug: string;
  number: number;
  title: string;
  description: string;
}

export interface Theory {
  title: string;
  content: string;
  examples: CodeExample[];
}

export interface CodeExample {
  title: string;
  code: string;
  explanation: string;
}

export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
}

// Progress Types
export type ProblemStatus = 'not_started' | 'in_progress' | 'solved' | 'needs_review';

export interface Progress {
  id: string;
  userId: string;
  problemSlug: string;
  weekSlug: string | null;
  daySlug: string | null;
  status: ProblemStatus;
  attemptsCount: number;
  solvedAt: string | null;
  firstAttemptedAt: string | null;
  lastAttemptedAt: string | null;
  timeSpentSeconds: number;
  createdAt: string;
  updatedAt: string;
}

export interface ProgressUpdate {
  status?: ProblemStatus;
  timeSpentSeconds?: number;
  addAttempt?: boolean;
}

export interface ProgressStats {
  totalProblems: number;
  completed: number;
  inProgress: number;
  notStarted: number;
  completionPercentage: number;
  currentStreak: number;
  longestStreak: number;
  totalTimeSpentSeconds: number;
  lastActiveAt: string | null;
}

export interface WeekProgress {
  weekSlug: string;
  totalProblems: number;
  completed: number;
  inProgress: number;
  notStarted: number;
  completionPercentage: number;
}

export interface ProgressList {
  items: Progress[];
  total: number;
}

// Draft Types
export interface Draft {
  id: string;
  userId: string;
  problemSlug: string;
  code: string;
  savedAt: string;
  isAutoSave: boolean;
  createdAt: string;
}

export interface DraftUpdate {
  code: string;
  isAutoSave?: boolean;
}

export interface DraftList {
  items: Draft[];
  total: number;
}

// Bookmark Types
export type ItemType = 'problem' | 'day' | 'week' | 'theory';

export interface Bookmark {
  id: string;
  userId: string;
  itemType: ItemType;
  itemSlug: string;
  title: string;
  notes: string | null;
  createdAt: string;
}

export interface BookmarkCreate {
  itemType: ItemType;
  itemSlug: string;
  notes?: string;
}

export interface BookmarkUpdate {
  notes?: string;
}

export interface BookmarkCheck {
  isBookmarked: boolean;
  bookmarkId: string | null;
}

export interface BookmarkList {
  items: Bookmark[];
  total: number;
}

// Activity Types
export type ActivityType = 
  | 'started_problem'
  | 'solved_problem'
  | 'attempted_problem'
  | 'viewed_theory'
  | 'viewed_week'
  | 'viewed_day'
  | 'saved_draft'
  | 'created_bookmark'
  | 'deleted_bookmark'
  | 'login'
  | 'logout';

export interface Activity {
  id: string;
  userId: string;
  activityType: ActivityType;
  itemSlug: string | null;
  metadata: Record<string, unknown> | null;
  createdAt: string;
}

export interface ActivityCreate {
  activityType: ActivityType;
  itemSlug?: string;
  metadata?: Record<string, unknown>;
}

export interface ActivityList {
  items: Activity[];
  total: number;
}

export interface ActivitySummary {
  periodDays: number;
  totalActivities: number;
  problemsStarted: number;
  problemsSolved: number;
  problemsAttempted: number;
  theoryViews: number;
  uniqueDaysActive: number;
}

// Submission Types
export type SubmissionStatus = 'pending_review' | 'approved' | 'needs_work' | 'exemplary';

export interface TestResult {
  name: string;
  passed: boolean;
  durationMs: number;
  output?: string;
  error?: string;
}

export interface TestResults {
  total: number;
  passed: number;
  failed: number;
  successRate: number;
  tests: TestResult[];
  stdout?: string;
  stderr?: string;
  executionTimeMs: number;
}

export interface CodeMetrics {
  linesOfCode: number;
  totalLines: number;
  blankLines: number;
  commentLines: number;
  functionCount: number;
  classCount: number;
  averageFunctionLength: number;
  docstringCoverage: number;
  complexityScore?: number;
  lintErrors: number;
  lintWarnings: number;
}

export interface Submission {
  id: string;
  userId: string;
  projectSlug: string;
  projectName?: string;
  weekSlug?: string;
  daySlug?: string;
  files: Record<string, string>;
  submittedAt: string;
  status: SubmissionStatus;
  reviewerNotes?: string;
  reviewedAt?: string;
  reviewedBy?: string;
  reviewerName?: string;
  testResults: TestResults;
  metrics: CodeMetrics;
  isExemplary: boolean;
  showcaseOptIn: boolean;
}

export interface SubmissionListItem {
  id: string;
  projectSlug: string;
  projectName?: string;
  weekSlug?: string;
  daySlug?: string;
  submittedAt: string;
  status: SubmissionStatus;
  testSummary: { total: number; passed: number; failed: number };
  metricsSummary: { linesOfCode: number; functionCount: number };
  isExemplary: boolean;
}

export interface SubmissionList {
  items: SubmissionListItem[];
  total: number;
  page: number;
  pageSize: number;
}

export interface SubmissionChecklist {
  allTestsPass: boolean;
  requiredFilesPresent: boolean;
  codeReviewed: boolean;
  meetsMinQuality: boolean;
  canSubmit: boolean;
  warnings: string[];
}

export interface SubmissionResponse {
  submissionId: string;
  status: SubmissionStatus;
  message: string;
  checklist: SubmissionChecklist;
  estimatedReviewTime: string;
}

export interface SubmissionComment {
  id: string;
  submissionId: string;
  userId: string;
  userName?: string;
  filePath: string;
  lineNumber: number;
  content: string;
  createdAt: string;
  updatedAt: string;
  isResolved: boolean;
}

export interface SubmissionCommentList {
  items: SubmissionComment[];
  total: number;
}

export interface ReviewQueueItem {
  id: string;
  projectSlug: string;
  projectName?: string;
  userId: string;
  userName?: string;
  submittedAt: string;
  waitingHours: number;
  testSummary: { total: number; passed: number };
  metricsSummary: { linesOfCode: number };
  priorityScore: number;
}

export interface ReviewQueue {
  pendingCount: number;
  items: ReviewQueueItem[];
  myReviewsToday: number;
  avgReviewTimeHours?: number;
}

export interface GamificationStats {
  totalSubmissions: number;
  approvedCount: number;
  exemplaryCount: number;
  currentStreak: number;
  longestStreak: number;
  badges: Array<{
    id: string;
    name: string;
    description: string;
    icon: string;
    earnedAt?: string;
  }>;
  recentAchievements: Array<{
    type: string;
    title: string;
    date: string;
  }>;
}

// Smart Recommendations Types
export interface Recommendation {
  type: 'next_problem' | 'review' | 'theory' | 'practice' | 'difficulty_adjustment' | 'remedial' | 'challenge';
  itemType: 'problem' | 'day' | 'week' | 'theory' | 'suggestion';
  itemSlug: string;
  itemTitle: string;
  reason: string;
  priority: number;
  estimatedTimeMinutes: number;
  context: {
    difficulty?: string;
    weekSlug?: string;
    daySlug?: string;
    easeFactor?: number;
    interval?: number;
    repetitions?: number;
    daysOverdue?: number;
    currentDifficulty?: string;
    suggestedDifficulty?: string;
    successRate?: number;
    masteryScore?: number;
    problemsStruggled?: string[];
  };
}

export interface ReviewItem {
  problemSlug: string;
  problemTitle: string;
  easeFactor: number;
  interval: number;
  repetitions: number;
  nextReview: string | null;
  daysOverdue: number;
  priority: number;
}

export interface ReviewQueueResponse {
  items: ReviewItem[];
  total: number;
  dueToday: number;
  dueThisWeek: number;
}

export interface ReviewStats {
  totalItems: number;
  dueNow: number;
  dueToday: number;
  dueThisWeek: number;
  averageEaseFactor: number;
  completedReviews: number;
}

export interface WeakArea {
  topicSlug: string;
  topicName: string;
  masteryScore: number;
  level: string;
  problemsStruggled: string[];
  suggestedRemediation: string;
  priority: number;
}

export interface LearningPath {
  steps: {
    type: string;
    weekSlug: string;
    weekTitle: string;
    reason: string;
    estimatedDays?: number;
  }[];
  estimatedWeeks: number;
  focusAreas: string[];
  skippedTopics: string[];
  reasoning: string;
}

export interface DifficultySuggestion {
  currentDifficulty: string;
  suggestedDifficulty: string;
  successRate: number;
  message: string;
}

export interface SuccessRate {
  attempted: number;
  solved: number;
  abandoned: number;
  successRate: number;
  abandonRate: number;
}

export interface TopicMastery {
  score: number;
  level: string;
  solved: number;
  total: number;
  completionPct: number;
  name: string;
}

export interface LearningStats {
  problemsAttempted: number;
  problemsSolved: number;
  averageTimePerProblem: number;
  successRateByDifficulty: Record<string, SuccessRate>;
  topicMastery: Record<string, TopicMastery>;
  streakDays: number;
  velocity: number;
}

export interface StreakInfo {
  currentStreak: number;
  longestStreak: number;
  lastReview: string | null;
}

export interface RecordReviewResponse {
  problemSlug: string;
  quality: number;
  nextReview: string;
  interval: number;
  easeFactor: number;
}

// AI Hint Types
export interface AIHint {
  hint: string;
  relevantLines: number[];
  explanation: string;
  hintLevel: number;
}

export interface AIHintRequest {
  problemSlug: string;
  code: string;
  testResults?: Record<string, unknown> | null;
  hintLevel: number;
  previousHints?: string[];
}

export interface AIErrorRequest {
  errorMessage: string;
  code: string;
  problemSlug?: string | null;
}

export interface AIErrorExplanation {
  explanation: string;
  suggestion: string;
  relevantLines: number[];
}

export interface CodeReviewRequest {
  files: Record<string, string>;
  projectSlug: string;
  rubric?: Array<Record<string, unknown>> | null;
}

export interface CodeReviewResult {
  overallFeedback: string;
  strengths: string[];
  improvements: string[];
  rubricAssessment: Record<string, string>;
  encouragement: string;
}

export interface AIHintFeedback {
  hintId?: string | null;
  problemSlug: string;
  hintLevel: number;
  wasHelpful: boolean;
  feedbackText?: string | null;
}

export interface AIReportRequest {
  problemSlug: string;
  hintLevel: number;
  hintText: string;
  reason: string;
  userCode?: string | null;
}

// API endpoints
export const api = {
  // Problems
  problems: {
    list: () => apiClient<Problem[]>('/api/v1/problems'),
    get: (slug: string) => apiClient<Problem>(`/api/v1/problems/${slug}`),
    submit: (slug: string, code: string) =>
      apiClient<SubmissionResult>(`/api/v1/problems/${slug}/submit`, {
        method: 'POST',
        body: { code },
      }),
    run: (slug: string, code: string) =>
      apiClient<RunResult>(`/api/v1/problems/${slug}/run`, {
        method: 'POST',
        body: { code },
      }),
  },

  // Progress
  progress: {
    getAll: () => apiClient<ProgressList>('/api/v1/progress'),
    get: (problemSlug: string) => 
      apiClient<Progress>(`/api/v1/progress/${problemSlug}`),
    update: (problemSlug: string, data: ProgressUpdate) =>
      apiClient<Progress>(`/api/v1/progress/${problemSlug}`, {
        method: 'POST',
        body: data,
      }),
    recordAttempt: (problemSlug: string) =>
      apiClient<Progress>(`/api/v1/progress/${problemSlug}/attempt`, {
        method: 'POST',
      }),
    getStats: () => 
      apiClient<ProgressStats>('/api/v1/progress/stats/overall'),
    getWeekProgress: (weekSlug: string) =>
      apiClient<WeekProgress>(`/api/v1/progress/week/${weekSlug}`),
  },

  // Drafts
  drafts: {
    list: (limit?: number, offset?: number) => 
      apiClient<DraftList>(`/api/v1/drafts?limit=${limit || 100}&offset=${offset || 0}`),
    get: (problemSlug: string) =>
      apiClient<Draft>(`/api/v1/drafts/${problemSlug}`),
    save: (problemSlug: string, data: DraftUpdate) =>
      apiClient<Draft>(`/api/v1/drafts/${problemSlug}`, {
        method: 'POST',
        body: data,
      }),
    delete: (problemSlug: string) =>
      apiClient<void>(`/api/v1/drafts/${problemSlug}`, {
        method: 'DELETE',
      }),
  },

  // Bookmarks
  bookmarks: {
    list: (itemType?: ItemType, limit?: number, offset?: number) => {
      const params = new URLSearchParams();
      if (itemType) params.append('item_type', itemType);
      if (limit) params.append('limit', limit.toString());
      if (offset) params.append('offset', offset.toString());
      return apiClient<BookmarkList>(`/api/v1/bookmarks?${params.toString()}`);
    },
    create: (data: BookmarkCreate) =>
      apiClient<Bookmark>('/api/v1/bookmarks', {
        method: 'POST',
        body: data,
      }),
    delete: (bookmarkId: string) =>
      apiClient<void>(`/api/v1/bookmarks/${bookmarkId}`, {
        method: 'DELETE',
      }),
    check: (itemType: ItemType, itemSlug: string) =>
      apiClient<BookmarkCheck>(`/api/v1/bookmarks/check?item_type=${itemType}&item_slug=${itemSlug}`),
    update: (bookmarkId: string, data: BookmarkUpdate) =>
      apiClient<Bookmark>(`/api/v1/bookmarks/${bookmarkId}`, {
        method: 'PATCH',
        body: data,
      }),
    toggle: (data: BookmarkCreate) =>
      apiClient<BookmarkCheck>('/api/v1/bookmarks/toggle', {
        method: 'POST',
        body: data,
      }),
  },

  // Activity
  activity: {
    list: (limit?: number, activityType?: ActivityType) => {
      const params = new URLSearchParams();
      if (limit) params.append('limit', limit.toString());
      if (activityType) params.append('activity_type', activityType);
      return apiClient<ActivityList>(`/api/v1/activity?${params.toString()}`);
    },
    log: (data: ActivityCreate) =>
      apiClient<Activity>('/api/v1/activity', {
        method: 'POST',
        body: data,
      }),
    getSummary: (days?: number) =>
      apiClient<ActivitySummary>(`/api/v1/activity/summary?days=${days || 7}`),
    getStats: (days?: number) =>
      apiClient<{ periodDays: number; byType: Record<string, number>; dailyActivity: { date: string; count: number }[]; total: number }>(
        `/api/v1/activity/stats?days=${days || 30}`
      ),
  },

  // Curriculum
  curriculum: {
    weeks: () => apiClient<Week[]>('/api/v1/curriculum/weeks'),
    week: (slug: string) => apiClient<Week>(`/api/v1/curriculum/weeks/${slug}`),
    theory: (weekSlug: string, daySlug: string) =>
      apiClient<Theory>(`/api/v1/curriculum/weeks/${weekSlug}/days/${daySlug}/theory`),
  },

  // Auth
  auth: {
    me: () => apiClient<User>('/api/v1/auth/me'),
    logout: () => apiClient<void>('/api/v1/auth/logout', { 
      method: 'POST',
    }),
    magicLink: (email: string) =>
      apiClient<{ message: string; debugToken?: string }>('/api/v1/auth/magic-link', {
        method: 'POST',
        body: { email },
      }),
    verifyMagicLink: (token: string) =>
      apiClient<{ accessToken: string; refreshToken: string; tokenType: string; expiresIn: number }>(
        `/api/v1/auth/verify?token=${encodeURIComponent(token)}`,
        {
          method: 'GET',
        }
      ),
    verifyMagicLinkPost: (token: string) =>
      apiClient<{ accessToken: string; refreshToken: string; tokenType: string; expiresIn: number }>(
        '/api/v1/auth/verify',
        {
          method: 'POST',
          body: { token },
        }
      ),
    refresh: () =>
      apiClient<{ accessToken: string; refreshToken: string; tokenType: string; expiresIn: number }>(
        '/api/v1/auth/refresh',
        {
          method: 'POST',
        }
      ),
  },

  // Submissions
  submissions: {
    list: (status?: SubmissionStatus, limit?: number, offset?: number) => {
      const params = new URLSearchParams();
      if (status) params.append('status', status);
      if (limit) params.append('limit', limit.toString());
      if (offset) params.append('offset', offset.toString());
      return apiClient<SubmissionList>(`/api/v1/submissions?${params.toString()}`);
    },
    get: (id: string) => apiClient<Submission>(`/api/v1/submissions/${id}`),
    getFiles: (id: string) => apiClient<Record<string, string>>(`/api/v1/submissions/${id}/files`),
    submit: (projectSlug: string, files: Record<string, string>, options?: { weekSlug?: string; daySlug?: string; showcaseOptIn?: boolean }) =>
      apiClient<SubmissionResponse>(`/api/v1/projects/${projectSlug}/submit`, {
        method: 'POST',
        body: {
          projectSlug,
          files,
          weekSlug: options?.weekSlug,
          daySlug: options?.daySlug,
          showcaseOptIn: options?.showcaseOptIn ?? false,
        },
      }),
    getChecklist: (projectSlug: string, files: Record<string, string>) =>
      apiClient<SubmissionChecklist>(`/api/v1/projects/${projectSlug}/checklist`, {
        method: 'POST',
        body: { files },
      }),
    getComments: (submissionId: string, filePath?: string) => {
      const params = new URLSearchParams();
      if (filePath) params.append('file_path', filePath);
      return apiClient<SubmissionCommentList>(`/api/v1/submissions/${submissionId}/comments?${params.toString()}`);
    },
    addComment: (submissionId: string, data: { filePath: string; lineNumber: number; content: string }) =>
      apiClient<SubmissionComment>(`/api/v1/submissions/${submissionId}/comments`, {
        method: 'POST',
        body: data,
      }),
    getGamificationStats: () => apiClient<GamificationStats>('/api/v1/submissions/gamification/stats'),
  },

  // Admin / Reviewer endpoints
  admin: {
    getReviewQueue: (limit?: number) =>
      apiClient<ReviewQueue>(`/api/v1/admin/reviews/queue?limit=${limit || 50}`),
    reviewSubmission: (submissionId: string, data: { status: SubmissionStatus; reviewerNotes?: string; isExemplary?: boolean }) =>
      apiClient<Submission>(`/api/v1/admin/submissions/${submissionId}/review`, {
        method: 'POST',
        body: data,
      }),
    batchReview: (data: { submissionIds: string[]; status: SubmissionStatus; reviewerNotes?: string }) =>
      apiClient<{ processed: number; failed: number; errors: string[] }>('/api/v1/admin/reviews/batch', {
        method: 'POST',
        body: data,
      }),
  },

  // AI Hints and Assistance
  ai: {
    generateHint: (data: AIHintRequest) =>
      apiClient<AIHint>('/api/v1/ai/hint', {
        method: 'POST',
        body: data,
      }),
    explainError: (data: AIErrorRequest) =>
      apiClient<AIErrorExplanation>('/api/v1/ai/explain-error', {
        method: 'POST',
        body: data,
      }),
    reviewCode: (data: CodeReviewRequest) =>
      apiClient<CodeReviewResult>('/api/v1/ai/code-review', {
        method: 'POST',
        body: data,
      }),
    submitFeedback: (data: AIHintFeedback) =>
      apiClient<void>('/api/v1/ai/hint-feedback', {
        method: 'POST',
        body: data,
      }),
    reportHint: (data: AIReportRequest) =>
      apiClient<void>('/api/v1/ai/report-hint', {
        method: 'POST',
        body: data,
      }),
    healthCheck: () =>
      apiClient<{ status: string; providers: Record<string, boolean>; models: Record<string, string> }>(
        '/api/v1/ai/health'
      ),
  },

  // Smart Recommendations
  recommendations: {
    getNext: () => apiClient<Recommendation>('/api/v1/recommendations/next'),
    getAll: (limit?: number) => 
      apiClient<Recommendation[]>(`/api/v1/recommendations/all?limit=${limit || 10}`),
    getReviewQueue: (limit?: number) => 
      apiClient<ReviewQueue>(`/api/v1/recommendations/review?limit=${limit || 10}`),
    getReviewStats: () => apiClient<ReviewStats>('/api/v1/recommendations/review/stats'),
    recordReview: (problemSlug: string, quality: number) =>
      apiClient<RecordReviewResponse>(`/api/v1/recommendations/review/${problemSlug}`, {
        method: 'POST',
        body: { quality },
      }),
    getWeakAreas: (limit?: number) => 
      apiClient<WeakArea[]>(`/api/v1/recommendations/weak-areas?limit=${limit || 5}`),
    getLearningPath: () => apiClient<LearningPath>('/api/v1/recommendations/path'),
    getDifficultySuggestion: () => apiClient<DifficultySuggestion | null>('/api/v1/recommendations/difficulty'),
    getStats: () => apiClient<LearningStats>('/api/v1/recommendations/stats'),
    getStreak: () => apiClient<StreakInfo>('/api/v1/recommendations/streak'),
  },
};

export { ApiError };
export default api;
