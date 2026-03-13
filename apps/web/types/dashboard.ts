export interface ActivityItem {
  id: string;
  problemSlug: string;
  problemTitle: string;
  weekNumber: number;
  dayNumber: number;
  status: 'completed' | 'attempted' | 'failed';
  timestamp: string;
  timeSpent?: number; // in seconds
}

export interface WeekProgress {
  weekNumber: number;
  weekSlug: string;
  weekTitle: string;
  totalProblems: number;
  completedProblems: number;
  isStarted: boolean;
  isCompleted: boolean;
  lastAccessed?: string;
}

export interface ProblemStatus {
  slug: string;
  status: 'not_started' | 'in_progress' | 'completed';
  attempts: number;
  lastAttempt?: string;
  timeSpent: number;
}

export interface UserStats {
  totalProblems: number;
  solvedProblems: number;
  currentStreak: number;
  longestStreak: number;
  totalTimeSpent: number; // in seconds
  averageSessionLength: number; // in seconds
  timeThisWeek: number; // in seconds
  lastActive: string | null;
}

export interface Recommendation {
  type: 'continue' | 'review' | 'practice' | 'project' | 'start';
  title: string;
  description: string;
  weekNumber?: number;
  dayNumber?: number;
  problemSlug?: string;
  actionLabel: string;
  priority: 'high' | 'medium' | 'low';
}

export interface DashboardData {
  userName?: string;
  isLoggedIn: boolean;
  stats: UserStats;
  weeksProgress: WeekProgress[];
  recentActivity: ActivityItem[];
  recommendations: Recommendation[];
  currentPosition: {
    weekNumber: number;
    dayNumber: number;
    problemSlug?: string;
  } | null;
}

export const TOTAL_PROBLEMS = 453; // Total from curriculum
export const TOTAL_WEEKS = 8;

export const WEEKS_DATA = [
  { number: 1, slug: 'week-01-foundations', title: 'Foundations', problemCount: 63 },
  { number: 2, slug: 'week-02-classes-objects', title: 'Classes & Objects', problemCount: 54 },
  { number: 3, slug: 'week-03-encapsulation', title: 'Encapsulation', problemCount: 52 },
  { number: 4, slug: 'week-04-inheritance', title: 'Inheritance', problemCount: 38 },
  { number: 5, slug: 'week-05-polymorphism', title: 'Polymorphism', problemCount: 51 },
  { number: 6, slug: 'week-06-special-methods', title: 'Special Methods', problemCount: 30 },
  { number: 7, slug: 'week-07-design-patterns', title: 'Design Patterns', problemCount: 30 },
  { number: 8, slug: 'week-08-capstone', title: 'Capstone Project', problemCount: 135 },
];
