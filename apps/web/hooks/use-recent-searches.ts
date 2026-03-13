"use client";

import { useLocalStorage } from "./use-local-storage";

const MAX_RECENT_SEARCHES = 10;
const STORAGE_KEY = "recent-searches";

export interface RecentSearch {
  query: string;
  timestamp: string;
}

export function useRecentSearches() {
  const [recentSearches, setRecentSearches] = useLocalStorage<RecentSearch[]>(
    STORAGE_KEY,
    []
  );

  const addRecentSearch = (query: string) => {
    if (!query.trim()) return;

    setRecentSearches((prev) => {
      // Remove existing entry if present
      const filtered = prev.filter(
        (s) => s.query.toLowerCase() !== query.toLowerCase()
      );

      // Add new entry at the beginning
      const newEntry: RecentSearch = {
        query: query.trim(),
        timestamp: new Date().toISOString(),
      };

      // Keep only the most recent searches
      return [newEntry, ...filtered].slice(0, MAX_RECENT_SEARCHES);
    });
  };

  const removeRecentSearch = (query: string) => {
    setRecentSearches((prev) =>
      prev.filter((s) => s.query !== query)
    );
  };

  const clearRecentSearches = () => {
    setRecentSearches([]);
  };

  return {
    recentSearches,
    addRecentSearch,
    removeRecentSearch,
    clearRecentSearches,
  };
}
