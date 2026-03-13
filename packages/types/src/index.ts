// Search Types
export interface SearchIndexItem {
  id: string;
  type: 'week' | 'day' | 'problem' | 'topic' | 'keyword';
  title: string;
  slug: string;
  description: string;
  content: string;
  week?: number;
  day?: number;
  difficulty?: 'beginner' | 'easy' | 'medium' | 'hard' | 'expert';
  topics: string[];
  keywords: string[];
  url: string;
}

export interface SearchResult {
  item: SearchIndexItem;
  score: number;
  matches: Array<{
    key: string;
    indices: Array<[number, number]>;
    value: string;
  }>;
}

export interface SearchFilters {
  week?: number;
  difficulty?: string;
  topic?: string;
  type?: SearchIndexItem['type'];
}

export interface SearchResponse {
  results: SearchResult[];
  total: number;
  query: string;
  filters: SearchFilters;
}

// Curriculum Types
export interface Week {
  id: string;
  number: number;
  title: string;
  description: string;
  slug: string;
  days: Day[];
  topics: string[];
  difficulty: 'beginner' | 'intermediate' | 'advanced';
}

export interface Day {
  id: string;
  number: number;
  title: string;
  description: string;
  slug: string;
  weekId: string;
  weekNumber: number;
  problems: Problem[];
  topics: string[];
}

export interface Problem {
  id: string;
  number: number;
  title: string;
  slug: string;
  description: string;
  difficulty: 'beginner' | 'easy' | 'medium' | 'hard' | 'expert';
  weekId: string;
  weekNumber: number;
  dayId: string;
  dayNumber: number;
  topics: string[];
  keywords: string[];
  url: string;
  estimatedTime?: number; // in minutes
}

// User Activity Types
export interface VisitedItem {
  id: string;
  type: 'week' | 'day' | 'problem' | 'theory';
  title: string;
  slug: string;
  url: string;
  visitedAt: string;
  week?: number;
  day?: number;
}

export interface Bookmark {
  id: string;
  type: 'week' | 'day' | 'problem' | 'theory';
  title: string;
  slug: string;
  url: string;
  createdAt: string;
  week?: number;
  day?: number;
  notes?: string;
}

export interface ContinueLearningItem {
  type: 'week' | 'day' | 'problem';
  title: string;
  slug: string;
  url: string;
  lastVisitedAt: string;
  progress?: number;
  week?: number;
  day?: number;
}

// Filter and Sort Types
export type ProblemSortOption = 
  | 'order' 
  | 'difficulty-asc' 
  | 'difficulty-desc' 
  | 'completion' 
  | 'recent';

export type ViewMode = 'grid' | 'list';

export interface ProblemFilters {
  week?: number;
  difficulty?: string[];
  topic?: string[];
  status?: 'completed' | 'in-progress' | 'not-started'[];
  search?: string;
}
