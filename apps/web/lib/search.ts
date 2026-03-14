// Local type definitions (previously imported from '@repo/types')
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

export interface SearchFilters {
  week?: number;
  difficulty?: string;
  topic?: string;
  type?: SearchIndexItem['type'];
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

let searchIndexCache: SearchIndexItem[] | null = null;

export async function getSearchIndex(): Promise<SearchIndexItem[]> {
  if (searchIndexCache) {
    return searchIndexCache;
  }

  // In a real app, this would fetch from the API or load the JSON
  const index = await import("@/data/search-index.json");
  searchIndexCache = index.default as SearchIndexItem[];
  return searchIndexCache;
}

export async function search(
  query: string,
  filters: SearchFilters = {},
  limit: number = 20
): Promise<{ results: SearchResult[]; total: number; searchTime: number }> {
  const params = new URLSearchParams();
  
  if (query) params.set("q", query);
  if (filters.week !== undefined) params.set("week", filters.week.toString());
  if (filters.difficulty) params.set("difficulty", filters.difficulty);
  if (filters.topic) params.set("topic", filters.topic);
  if (filters.type) params.set("type", filters.type);
  params.set("limit", limit.toString());

  const response = await fetch(`/api/search?${params.toString()}`);
  
  if (!response.ok) {
    throw new Error("Search failed");
  }

  return response.json();
}

export function getAllTopics(index: SearchIndexItem[]): string[] {
  const topics = new Set<string>();
  index.forEach((item) => {
    item.topics.forEach((topic) => topics.add(topic));
  });
  return Array.from(topics).sort();
}

export function getAllDifficulties(index: SearchIndexItem[]): string[] {
  const difficulties = new Set<string>();
  index.forEach((item) => {
    if (item.difficulty) {
      difficulties.add(item.difficulty);
    }
  });
  return Array.from(difficulties).sort();
}

export function getAllWeeks(index: SearchIndexItem[]): number[] {
  const weeks = new Set<number>();
  index.forEach((item) => {
    if (item.week !== undefined) {
      weeks.add(item.week);
    }
  });
  return Array.from(weeks).sort((a, b) => a - b);
}

export function getProblems(index: SearchIndexItem[]): SearchIndexItem[] {
  return index.filter((item) => item.type === "problem");
}

// Aliases for backward compatibility
export { getSearchIndex as buildSearchIndex, search as searchCurriculum };
