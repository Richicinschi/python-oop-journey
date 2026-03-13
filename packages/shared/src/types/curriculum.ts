/**
 * Curriculum Types
 * Core type definitions for the Python OOP Journey curriculum structure
 */

/**
 * Difficulty level for problems and content
 */
export type Difficulty = 'beginner' | 'easy' | 'medium' | 'hard' | 'challenge';

/**
 * Completion status for tracking progress
 */
export type CompletionStatus = 'not_started' | 'in_progress' | 'completed' | 'locked';

/**
 * Problem type classification
 */
export type ProblemType = 'exercise' | 'quiz' | 'coding' | 'debugging' | 'challenge';

/**
 * Represents a single coding problem or exercise
 */
export interface Problem {
  /** Unique identifier for the problem */
  id: string;
  /** Problem number within the day (e.g., "01", "02") */
  number: string;
  /** Display title */
  title: string;
  /** Problem type classification */
  type: ProblemType;
  /** Difficulty level */
  difficulty: Difficulty;
  /** Brief description */
  description: string;
  /** Detailed instructions (markdown) */
  instructions: string;
  /** Starter code shown to user */
  starterCode: string;
  /** Solution code (for reference/testing) */
  solutionCode: string;
  /** Test cases for verification */
  testCases: TestCase[];
  /** Hints for the user */
  hints: string[];
  /** Expected output for display */
  expectedOutput?: string;
  /** Time estimate in minutes */
  estimatedTime: number;
  /** Tags for categorization */
  tags: string[];
  /** Prerequisites for this problem */
  prerequisites?: string[];
}

/**
 * Individual test case for problem verification
 */
export interface TestCase {
  /** Test case identifier */
  id: string;
  /** Human-readable test name */
  name: string;
  /** Input to provide to the function/code */
  input: string;
  /** Expected output */
  expectedOutput: string;
  /** Whether this is a public or hidden test */
  isPublic: boolean;
  /** Optional description of what this tests */
  description?: string;
}

/**
 * A single day of learning content
 */
export interface Day {
  /** Day number (1-7) */
  number: number;
  /** Display title for the day */
  title: string;
  /** Short description of day's focus */
  description: string;
  /** Learning objectives for this day */
  learningObjectives: string[];
  /** Theory content (markdown) */
  theoryContent: string;
  /** List of problems/exercises */
  problems: Problem[];
  /** Mini-project for the day (optional) */
  miniProject?: Project;
  /** Estimated time to complete in minutes */
  estimatedTime: number;
  /** Key concepts covered */
  keyConcepts: string[];
  /** Path to day's content file */
  contentPath?: string;
}

/**
 * A project (mini or weekly)
 */
export interface Project {
  /** Unique identifier */
  id: string;
  /** Project title */
  title: string;
  /** Project description */
  description: string;
  /** Detailed instructions (markdown) */
  instructions: string;
  /** Difficulty level */
  difficulty: Difficulty;
  /** Starter files/paths */
  starterFiles: ProjectFile[];
  /** Solution files/paths */
  solutionFiles: ProjectFile[];
  /** Success criteria */
  successCriteria: string[];
  /** Estimated time in hours */
  estimatedTime: number;
  /** Rubric for evaluation */
  rubric?: RubricItem[];
}

/**
 * A file in a project
 */
export interface ProjectFile {
  /** File name */
  name: string;
  /** File path relative to project */
  path: string;
  /** File content or reference */
  content?: string;
  /** Whether this is the main file */
  isMain: boolean;
}

/**
 * Rubric item for project evaluation
 */
export interface RubricItem {
  /** Criterion name */
  criterion: string;
  /** Points possible */
  points: number;
  /** Description of requirements */
  description: string;
}

/**
 * A week of curriculum content
 */
export interface Week {
  /** Week number (1-8) */
  number: number;
  /** Week title */
  title: string;
  /** Theme or focus area */
  theme: string;
  /** Brief description */
  description: string;
  /** Weekly learning objectives */
  objectives: string[];
  /** Days in this week */
  days: Day[];
  /** Weekly capstone project */
  capstoneProject: Project;
  /** Prerequisites for this week */
  prerequisites: string[];
  /** Skills gained after completion */
  skillsGained: string[];
  /** Estimated time in hours */
  estimatedTime: number;
  /** Whether week is locked */
  isLocked?: boolean;
}

/**
 * Root curriculum object containing all weeks
 */
export interface Curriculum {
  /** Curriculum version */
  version: string;
  /** Curriculum title */
  title: string;
  /** Description of the curriculum */
  description: string;
  /** Target audience */
  targetAudience: string;
  /** Total weeks */
  totalWeeks: number;
  /** All weeks in the curriculum */
  weeks: Week[];
  /** Learning path description */
  learningPath: LearningPathStage[];
  /** Estimated total time in hours */
  totalEstimatedTime: number;
}

/**
 * Stage in the learning path
 */
export interface LearningPathStage {
  /** Stage name */
  name: string;
  /** Stage description */
  description: string;
  /** Weeks included in this stage */
  weeks: number[];
  /** Skills focus */
  skillsFocus: string[];
}

/**
 * User profile
 */
export interface User {
  /** Unique user ID */
  id: string;
  /** Display name */
  displayName: string;
  /** Email address */
  email: string;
  /** Avatar URL */
  avatarUrl?: string;
  /** Account creation date */
  createdAt: string;
  /** Last active timestamp */
  lastActiveAt: string;
  /** User preferences */
  preferences: UserPreferences;
  /** Current skill level */
  skillLevel: 'beginner' | 'intermediate' | 'advanced';
}

/**
 * User preferences
 */
export interface UserPreferences {
  /** UI theme preference */
  theme: 'light' | 'dark' | 'system';
  /** Default code editor settings */
  editorSettings: EditorSettings;
  /** Email notification preferences */
  notifications: NotificationPreferences;
  /** Accessibility settings */
  accessibility: AccessibilitySettings;
}

/**
 * Code editor settings
 */
export interface EditorSettings {
  /** Font size */
  fontSize: number;
  /** Tab size */
  tabSize: number;
  /** Use spaces instead of tabs */
  useSpaces: boolean;
  /** Word wrap enabled */
  wordWrap: boolean;
  /** Minimap enabled */
  minimap: boolean;
  /** Line numbers display */
  lineNumbers: 'on' | 'off' | 'relative';
}

/**
 * Notification preferences
 */
export interface NotificationPreferences {
  /** Email notifications enabled */
  emailEnabled: boolean;
  /** Weekly progress summary */
  weeklySummary: boolean;
  /** Achievement notifications */
  achievements: boolean;
  /** Reminder notifications */
  reminders: boolean;
}

/**
 * Accessibility settings
 */
export interface AccessibilitySettings {
  /** High contrast mode */
  highContrast: boolean;
  /** Reduced motion */
  reducedMotion: boolean;
  /** Font scale */
  fontScale: number;
  /** Screen reader optimizations */
  screenReaderOptimized: boolean;
}

/**
 * User progress tracking
 */
export interface Progress {
  /** User ID */
  userId: string;
  /** Week progress records */
  weekProgress: WeekProgress[];
  /** Overall statistics */
  statistics: ProgressStatistics;
  /** Current streak */
  currentStreak: number;
  /** Longest streak */
  longestStreak: number;
  /** Last activity date */
  lastActivityDate: string;
  /** Achievements earned */
  achievements: Achievement[];
}

/**
 * Progress for a specific week
 */
export interface WeekProgress {
  /** Week number */
  weekNumber: number;
  /** Completion status */
  status: CompletionStatus;
  /** Day progress records */
  dayProgress: DayProgress[];
  /** Capstone project status */
  capstoneStatus: CompletionStatus;
  /** Start date */
  startedAt?: string;
  /** Completion date */
  completedAt?: string;
  /** Time spent in minutes */
  timeSpent: number;
}

/**
 * Progress for a specific day
 */
export interface DayProgress {
  /** Day number */
  dayNumber: number;
  /** Completion status */
  status: CompletionStatus;
  /** Problem completion records */
  problemProgress: ProblemProgress[];
  /** Mini-project status */
  miniProjectStatus?: CompletionStatus;
  /** Start date */
  startedAt?: string;
  /** Completion date */
  completedAt?: string;
  /** Time spent in minutes */
  timeSpent: number;
}

/**
 * Progress for a specific problem
 */
export interface ProblemProgress {
  /** Problem ID */
  problemId: string;
  /** Completion status */
  status: CompletionStatus;
  /** Number of attempts */
  attempts: number;
  /** Successfully completed */
  completed: boolean;
  /** Completion date */
  completedAt?: string;
  /** Code saved at completion */
  solutionCode?: string;
  /** Time spent in minutes */
  timeSpent: number;
}

/**
 * Progress statistics
 */
export interface ProgressStatistics {
  /** Total problems completed */
  totalProblemsCompleted: number;
  /** Total problems available */
  totalProblems: number;
  /** Total days completed */
  daysCompleted: number;
  /** Weeks completed */
  weeksCompleted: number;
  /** Total time spent in minutes */
  totalTimeSpent: number;
  /** Average problem time in minutes */
  averageProblemTime: number;
  /** Current week */
  currentWeek: number;
  /** Current day */
  currentDay: number;
}

/**
 * Achievement badge
 */
export interface Achievement {
  /** Achievement ID */
  id: string;
  /** Achievement name */
  name: string;
  /** Description */
  description: string;
  /** Icon identifier */
  icon: string;
  /** Date earned */
  earnedAt: string;
  /** Category */
  category: 'milestone' | 'streak' | 'skill' | 'social' | 'special';
}

/**
 * Saved code draft
 */
export interface Draft {
  /** Draft ID */
  id: string;
  /** User ID */
  userId: string;
  /** Associated problem ID */
  problemId: string;
  /** Saved code content */
  code: string;
  /** Date saved */
  savedAt: string;
  /** Auto-save flag */
  isAutoSave: boolean;
  /** Draft name/label */
  label?: string;
}

/**
 * Bookmarked content
 */
export interface Bookmark {
  /** Bookmark ID */
  id: string;
  /** User ID */
  userId: string;
  /** Type of bookmarked content */
  contentType: 'problem' | 'day' | 'week' | 'concept' | 'resource';
  /** Content identifier */
  contentId: string;
  /** Custom title/label */
  label?: string;
  /** Notes added by user */
  notes?: string;
  /** Date bookmarked */
  createdAt: string;
  /** Position within content (for problems) */
  position?: CodePosition;
}

/**
 * Code position for bookmarks
 */
export interface CodePosition {
  /** Line number */
  line: number;
  /** Column number */
  column: number;
  /** Selected text */
  selectedText?: string;
}

/**
 * Code execution result
 */
export interface ExecutionResult {
  /** Execution ID */
  id: string;
  /** Success status */
  success: boolean;
  /** Standard output */
  stdout: string;
  /** Standard error */
  stderr: string;
  /** Exit code */
  exitCode: number;
  /** Execution time in milliseconds */
  executionTime: number;
  /** Memory usage in bytes */
  memoryUsage?: number;
  /** Any errors that occurred */
  error?: ExecutionError;
  /** Timestamp */
  timestamp: string;
}

/**
 * Execution error details
 */
export interface ExecutionError {
  /** Error type */
  type: 'syntax' | 'runtime' | 'timeout' | 'memory' | 'system';
  /** Error message */
  message: string;
  /** Line number where error occurred */
  lineNumber?: number;
  /** Column number */
  columnNumber?: number;
  /** Full traceback */
  traceback?: string;
}

/**
 * Test verification result
 */
export interface VerificationResult {
  /** Verification ID */
  id: string;
  /** Problem ID being verified */
  problemId: string;
  /** Overall success */
  success: boolean;
  /** Individual test results */
  testResults: TestResult[];
  /** Summary statistics */
  summary: VerificationSummary;
  /** Timestamp */
  timestamp: string;
}

/**
 * Individual test result
 */
export interface TestResult {
  /** Test case ID */
  testId: string;
  /** Test name */
  name: string;
  /** Whether test passed */
  passed: boolean;
  /** Input used */
  input: string;
  /** Expected output */
  expectedOutput: string;
  /** Actual output */
  actualOutput: string;
  /** Error message if failed */
  errorMessage?: string;
  /** Execution time */
  executionTime: number;
}

/**
 * Verification summary statistics
 */
export interface VerificationSummary {
  /** Total tests run */
  totalTests: number;
  /** Tests passed */
  passedTests: number;
  /** Tests failed */
  failedTests: number;
  /** Total execution time */
  totalExecutionTime: number;
  /** Pass rate percentage */
  passRate: number;
}

/**
 * API Response wrapper
 */
export interface ApiResponse<T> {
  /** Success flag */
  success: boolean;
  /** Response data */
  data?: T;
  /** Error information */
  error?: ApiError;
  /** Response timestamp */
  timestamp: string;
}

/**
 * API Error structure
 */
export interface ApiError {
  /** Error code */
  code: string;
  /** Error message */
  message: string;
  /** Additional error details */
  details?: Record<string, unknown>;
}
