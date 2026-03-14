// AI Hints hooks
export { useAIHints } from './use-ai-hints';

// Progress and tracking hooks
export {
  useProgress,
  useProblemProgress,
  useUpdateProgress,
  useWeekProgress,
  useProgressStats,
  useLocalProgress,
} from './use-progress';

export type {
  ProblemStatus,
} from './use-progress';

// Draft hooks
export {
  useDraft,
  useSaveDraft,
  useDeleteDraft,
  useDraftManager,
} from './use-draft';

// Bookmark hooks
export {
  useBookmarks,
  useToggleBookmark,
  useIsBookmarked,
  useDeleteBookmark,
  useUpdateBookmarkNotes,
  useLocalBookmarks,
} from './use-bookmarks';

export type {
  ItemType,
} from './use-bookmarks';

// Progress sync hooks
export {
  useProgressSync,
  useProgressWebSocket,
} from './use-progress-sync';

// Multi-file project hooks (Agent 16)
export {
  useProjectFiles,
  type UseProjectFilesOptions,
  type UseProjectFilesReturn,
} from './use-project-files';

// Phase 5 Project hooks
export {
  useProjectStore,
} from './use-project-store';

// Editor store hooks
export {
  useEditorStore,
  useEditorKeyboardShortcuts,
} from './use-editor-store';

// Smart Recommendations hooks (Agent 22)
export {
  useNextRecommendation,
  useRecommendations,
  useReviewQueue,
  useReviewStats,
  useRecordReview,
  useWeakAreas,
  useLearningPath,
  useDifficultySuggestion,
  useLearningStats,
  useStreakInfo,
  useSmartDashboard,
} from './use-recommendations';

export type {
  Recommendation,
  ReviewItem,
  ReviewQueue,
  ReviewStats,
  WeakArea,
  LearningPath,
  DifficultySuggestion,
  LearningStats,
  LearningVelocity,
} from './use-recommendations';

// Other hooks
export { useAuth } from './use-auth';
// Curriculum hooks
export {
  useWeeks,
  useWeek,
  useDay,
  useProblems,
  useProblem,
} from './use-curriculum';
export { useDashboardData } from './use-dashboard-data';
export { useLocalStorage } from './use-local-storage';
export { useRecentSearches } from './use-recent-searches';
export { useSearch } from './use-search';
export { useVerification } from './use-verification';
export { useVisitedItems } from './use-visited-items';

// Online/Offline and Sync hooks
export { useOnlineStatus, useIsOnline, useConnectionToast } from './use-online-status';
export type { ConnectionStatus, OnlineStatusState } from './use-online-status';

export { useSync } from './use-sync';
export type { UseSyncReturn } from './use-sync';

// Submissions hooks (from lib/hooks)
export {
  useSubmissions,
  useSubmission,
  useSubmissionFiles,
  useGamificationStats,
  useSubmitProject,
  useSubmissionChecklist,
  useSubmissionComments,
  useAddComment,
  useReviewSubmission,
} from '@/lib/hooks/use-submissions';
