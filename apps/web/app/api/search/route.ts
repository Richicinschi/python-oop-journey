import { NextRequest, NextResponse } from "next/server";
import searchIndex from "@/data/search-index.json";
import type { SearchIndexItem, SearchFilters, SearchResult } from "@repo/types";

const index = searchIndex as SearchIndexItem[];

// Search configuration
const FUSE_OPTIONS = {
  keys: [
    { name: "title", weight: 0.4 },
    { name: "description", weight: 0.3 },
    { name: "content", weight: 0.2 },
    { name: "keywords", weight: 0.1 },
  ],
  threshold: 0.4,
  includeScore: true,
  includeMatches: true,
  minMatchCharLength: 2,
};

// Simple search implementation (without Fuse.js for now)
function searchItems(
  query: string,
  filters: SearchFilters
): SearchResult[] {
  const normalizedQuery = query.toLowerCase().trim();
  const queryWords = normalizedQuery.split(/\s+/).filter(Boolean);

  let results = index.filter((item) => {
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

    return true;
  });

  // If no query, return all (filtered) results
  if (!normalizedQuery) {
    return results.map((item) => ({
      item,
      score: 0,
      matches: [],
    }));
  }

  // Score and filter by search query
  const scored = results
    .map((item) => {
      let score = 0;
      const matches: SearchResult["matches"] = [];

      const titleLower = item.title.toLowerCase();
      const descLower = item.description.toLowerCase();
      const contentLower = item.content.toLowerCase();
      const keywordsLower = item.keywords.map((k) => k.toLowerCase());

      // Exact title match
      if (titleLower === normalizedQuery) {
        score += 100;
        matches.push({ key: "title", value: item.title, indices: [[0, item.title.length - 1]] });
      }
      // Title contains query
      else if (titleLower.includes(normalizedQuery)) {
        score += 50;
        const idx = titleLower.indexOf(normalizedQuery);
        matches.push({ key: "title", value: item.title, indices: [[idx, idx + normalizedQuery.length - 1]] });
      }
      // Title contains all words
      else if (queryWords.every((w) => titleLower.includes(w))) {
        score += 40;
      }

      // Description contains query
      if (descLower.includes(normalizedQuery)) {
        score += 20;
        const idx = descLower.indexOf(normalizedQuery);
        matches.push({ key: "description", value: item.description.slice(0, 100), indices: [[idx, idx + normalizedQuery.length - 1]] });
      }

      // Content contains query
      if (contentLower.includes(normalizedQuery)) {
        score += 10;
      }

      // Keyword matches
      const keywordMatches = keywordsLower.filter((k) =>
        normalizedQuery.includes(k) || k.includes(normalizedQuery)
      ).length;
      score += keywordMatches * 5;

      // Boost problems
      if (item.type === "problem") {
        score += 15;
      }

      return {
        item,
        score: score > 0 ? 1 / score : Infinity,
        matches,
      };
    })
    .filter((r) => r.score !== Infinity)
    .sort((a, b) => a.score - b.score);

  return scored;
}

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);

  const query = searchParams.get("q") || "";
  const week = searchParams.get("week");
  const difficulty = searchParams.get("difficulty");
  const topic = searchParams.get("topic");
  const type = searchParams.get("type") as SearchIndexItem["type"] | null;
  const limit = parseInt(searchParams.get("limit") || "20", 10);

  const filters: SearchFilters = {
    ...(week && { week: parseInt(week, 10) }),
    ...(difficulty && { difficulty }),
    ...(topic && { topic }),
    ...(type && { type }),
  };

  const startTime = Date.now();
  const results = searchItems(query, filters);
  const searchTime = Date.now() - startTime;

  // Limit results
  const limitedResults = results.slice(0, limit);

  return NextResponse.json({
    results: limitedResults,
    total: results.length,
    query,
    filters,
    searchTime,
  });
}
