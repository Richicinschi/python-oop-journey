"use client";

import { useState, useCallback, useMemo, useEffect } from "react";
import type { SearchIndexItem, SearchFilters, SearchResult } from "@repo/types";

interface UseSearchOptions {
  searchIndex: SearchIndexItem[];
  debounceMs?: number;
  minQueryLength?: number;
  maxResults?: number;
}

interface UseSearchReturn {
  query: string;
  setQuery: (query: string) => void;
  results: SearchResult[];
  filters: SearchFilters;
  setFilters: (filters: SearchFilters | ((prev: SearchFilters) => SearchFilters)) => void;
  isSearching: boolean;
  totalResults: number;
  clearSearch: () => void;
}

// Simple fuzzy search implementation (fallback when Fuse.js is not available)
function fuzzySearch(
  items: SearchIndexItem[],
  query: string,
  filters: SearchFilters
): SearchResult[] {
  const normalizedQuery = query.toLowerCase().trim();
  const queryWords = normalizedQuery.split(/\s+/);

  return items
    .filter((item) => {
      // Apply filters
      if (filters.week !== undefined && item.week !== filters.week) {
        return false;
      }
      if (filters.difficulty && item.difficulty !== filters.difficulty) {
        return false;
      }
      if (filters.topic && !item.topics.includes(filters.topic)) {
        return false;
      }
      if (filters.type && item.type !== filters.type) {
        return false;
      }

      // Apply search query
      if (!normalizedQuery) return true;

      const searchFields = [
        item.title,
        item.description,
        item.content,
        ...item.topics,
        ...item.keywords,
      ]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();

      // All query words must match somewhere
      return queryWords.every((word) => searchFields.includes(word));
    })
    .map((item) => {
      // Calculate relevance score
      let score = 0;
      const titleLower = item.title.toLowerCase();
      const descLower = item.description.toLowerCase();

      // Exact title match gets highest score
      if (titleLower === normalizedQuery) {
        score += 100;
      }
      // Title contains query
      else if (titleLower.includes(normalizedQuery)) {
        score += 50;
      }
      // Title contains all query words
      else if (queryWords.every((word) => titleLower.includes(word))) {
        score += 40;
      }

      // Description contains query
      if (descLower.includes(normalizedQuery)) {
        score += 20;
      }

      // Keywords match
      const keywordMatches = item.keywords.filter((k) =>
        normalizedQuery.includes(k.toLowerCase())
      ).length;
      score += keywordMatches * 5;

      // Prefer problems over other types when searching
      if (item.type === "problem") {
        score += 10;
      }

      return {
        item,
        score: 1 / (score + 1), // Lower score = better match (Fuse.js style)
        matches: [],
      };
    })
    .sort((a, b) => a.score - b.score);
}

export function useSearch(options: UseSearchOptions): UseSearchReturn {
  const { searchIndex, minQueryLength = 1, maxResults = 50 } = options;

  const [query, setQuery] = useState("");
  const [filters, setFilters] = useState<SearchFilters>({});
  const [isSearching, setIsSearching] = useState(false);
  const [results, setResults] = useState<SearchResult[]>([]);

  // Debounced search
  useEffect(() => {
    setIsSearching(true);

    const timeoutId = setTimeout(() => {
      if (query.length < minQueryLength) {
        setResults([]);
        setIsSearching(false);
        return;
      }

      const searchResults = fuzzySearch(searchIndex, query, filters);
      setResults(searchResults.slice(0, maxResults));
      setIsSearching(false);
    }, options.debounceMs ?? 150);

    return () => clearTimeout(timeoutId);
  }, [query, filters, searchIndex, minQueryLength, maxResults, options.debounceMs]);

  const clearSearch = useCallback(() => {
    setQuery("");
    setFilters({});
    setResults([]);
  }, []);

  return {
    query,
    setQuery,
    results,
    filters,
    setFilters,
    isSearching,
    totalResults: results.length,
    clearSearch,
  };
}
