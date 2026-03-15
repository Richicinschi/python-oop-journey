"use client";

import { Suspense } from "react";
import { useState, useMemo } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Link from "next/link";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { getCurriculum, getWeeks, formatWeekNumber } from "@/lib/curriculum-loader";
import { Problem, Week, Day } from "@/types/curriculum";
import { Search, Grid, List, X, FileCode, Calendar, Layers, ArrowRight, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface SearchFilters {
  query: string;
  week: string;
  difficulty: string;
  topic: string;
}

interface ProblemWithContext extends Problem {
  weekSlug: string;
  weekTitle: string;
  weekOrder: number;
  daySlug: string;
  dayTitle: string;
  dayOrder: number;
}

function SearchContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const initialQuery = searchParams.get("q") || "";

  const [filters, setFilters] = useState<SearchFilters>({
    query: initialQuery,
    week: "all",
    difficulty: "all",
    topic: "all",
  });

  const [viewMode, setViewMode] = useState<"grid" | "list">("grid");

  // Get curriculum data
  const curriculumData = useMemo(() => getCurriculum(), []);
  const weeks = useMemo(() => getWeeks(), []);

  // Extract all problems from curriculum with context
  const allProblems = useMemo<ProblemWithContext[]>(() => {
    const problems: ProblemWithContext[] = [];
    
    curriculumData.weeks.forEach((week: Week) => {
      week.days.forEach((day: Day) => {
        day.problems.forEach((problem: Problem) => {
          problems.push({
            ...problem,
            weekSlug: week.slug,
            weekTitle: week.title,
            weekOrder: week.order,
            daySlug: day.slug,
            dayTitle: day.title,
            dayOrder: day.order,
          });
        });
      });
    });
    
    return problems;
  }, [curriculumData]);

  // Extract unique topics
  const topics = useMemo(() => {
    const topicSet = new Set<string>();
    allProblems.forEach((p) => {
      if (p.topic) {
        topicSet.add(p.topic);
      }
    });
    return Array.from(topicSet).sort();
  }, [allProblems]);

  // Extract unique difficulties
  const difficulties = useMemo(() => {
    const diffSet = new Set<string>();
    allProblems.forEach((p) => {
      if (p.difficulty) {
        diffSet.add(p.difficulty);
      }
    });
    return Array.from(diffSet).sort();
  }, [allProblems]);

  // Filter problems
  const results = useMemo<ProblemWithContext[]>(() => {
    let filtered = allProblems;

    if (filters.query) {
      const query = filters.query.toLowerCase();
      filtered = filtered.filter(
        (p) =>
          p.title.toLowerCase().includes(query) ||
          (p.topic && p.topic.toLowerCase().includes(query)) ||
          (p.instructions && p.instructions.toLowerCase().includes(query))
      );
    }

    if (filters.week !== "all") {
      filtered = filtered.filter((p) => p.weekSlug === filters.week);
    }

    if (filters.difficulty !== "all") {
      filtered = filtered.filter((p) => p.difficulty === filters.difficulty);
    }

    if (filters.topic !== "all") {
      filtered = filtered.filter((p) => p.topic === filters.topic);
    }

    return filtered;
  }, [filters, allProblems]);

  const clearFilters = () => {
    setFilters({
      query: "",
      week: "all",
      difficulty: "all",
      topic: "all",
    });
    router.replace("/search");
  };

  const hasActiveFilters =
    filters.week !== "all" ||
    filters.difficulty !== "all" ||
    filters.topic !== "all";

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case "easy":
      case "beginner":
        return "bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300";
      case "medium":
        return "bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300";
      case "hard":
        return "bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300";
      default:
        return "bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300";
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Search Problems</h1>
        <p className="text-muted-foreground">
          Find problems by keyword, difficulty, topic, or week
        </p>
      </div>

      {/* Search Bar */}
      <div className="flex gap-4">
        <div className="relative flex-1 max-w-2xl">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search problems..."
            value={filters.query}
            onChange={(e) =>
              setFilters((f) => ({ ...f, query: e.target.value }))
            }
            className="pl-10"
          />
          {filters.query && (
            <button
              onClick={() => setFilters((f) => ({ ...f, query: "" }))}
              className="absolute right-3 top-1/2 -translate-y-1/2"
            >
              <X className="h-4 w-4 text-muted-foreground hover:text-foreground" />
            </button>
          )}
        </div>

        {/* View Toggle */}
        <div className="flex border rounded-md">
          <Button
            variant={viewMode === "grid" ? "default" : "ghost"}
            size="icon"
            onClick={() => setViewMode("grid")}
            aria-label="Grid view"
            aria-pressed={viewMode === "grid"}
          >
            <Grid className="h-4 w-4" />
          </Button>
          <Button
            variant={viewMode === "list" ? "default" : "ghost"}
            size="icon"
            onClick={() => setViewMode("list")}
            aria-label="List view"
            aria-pressed={viewMode === "list"}
          >
            <List className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-4">
        <Select
          value={filters.week}
          onValueChange={(v) => setFilters((f) => ({ ...f, week: v }))}
        >
          <SelectTrigger className="w-[200px]">
            <SelectValue placeholder="All Weeks" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Weeks</SelectItem>
            {weeks.map((week) => (
              <SelectItem key={week.slug} value={week.slug}>
                {formatWeekNumber(week.order)}: {week.title.replace(`Week ${week.order}: `, '').replace('Week 0: ', '')}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        <Select
          value={filters.difficulty}
          onValueChange={(v) => setFilters((f) => ({ ...f, difficulty: v }))}
        >
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="All Difficulties" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Difficulties</SelectItem>
            {difficulties.map((d) => (
              <SelectItem key={d} value={d}>
                {d.charAt(0).toUpperCase() + d.slice(1)}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        <Select
          value={filters.topic}
          onValueChange={(v) => setFilters((f) => ({ ...f, topic: v }))}
        >
          <SelectTrigger className="w-[200px]">
            <SelectValue placeholder="All Topics" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Topics</SelectItem>
            {topics.map((topic) => (
              <SelectItem key={topic} value={topic}>
                {topic}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        {hasActiveFilters && (
          <Button variant="ghost" onClick={clearFilters}>
            <X className="h-4 w-4 mr-2" />
            Clear Filters
          </Button>
        )}
      </div>

      {/* Results Count */}
      <div className="flex items-center justify-between">
        <p className="text-sm text-muted-foreground">
          Found <strong>{results.length}</strong> problems
        </p>
        {filters.query && (
          <Badge variant="secondary">
            Searching for &quot;{filters.query}&quot;
          </Badge>
        )}
      </div>

      {/* Results Grid/List */}
      {results.length === 0 ? (
        <div className="text-center py-12">
          <Search className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
          <h3 className="text-lg font-medium mb-2">No problems found</h3>
          <p className="text-muted-foreground mb-4">
            Try adjusting your search or filters
          </p>
          <Button onClick={clearFilters}>Clear All Filters</Button>
        </div>
      ) : (
        <div
          className={cn(
            viewMode === "grid"
              ? "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
              : "flex flex-col gap-4"
          )}
        >
          {results.map((problem) => (
            <Card
              key={problem.slug}
              className={cn(
                "group transition-all hover:shadow-md",
                viewMode === "list" && "flex flex-row items-center"
              )}
            >
              <CardHeader className={cn("pb-3", viewMode === "list" && "flex-1")}>
                <div className="flex items-start justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <div className="p-2 rounded-lg bg-primary/10">
                      <FileCode className="h-4 w-4 text-primary" />
                    </div>
                    <div>
                      <Badge variant="outline" className="mb-1 text-xs">
                        {problem.topic || "General"}
                      </Badge>
                      <CardTitle className="text-base group-hover:text-primary transition-colors">
                        {problem.title}
                      </CardTitle>
                    </div>
                  </div>
                  <Badge
                    variant="secondary"
                    className={cn("text-xs capitalize", getDifficultyColor(problem.difficulty))}
                  >
                    {problem.difficulty}
                  </Badge>
                </div>
              </CardHeader>

              <CardContent className={cn("pt-0", viewMode === "list" && "flex items-center gap-4 border-l")}>
                {viewMode === "grid" && (
                  <CardDescription className="line-clamp-2 mb-4">
                    {problem.instructions?.split('\n')[0]?.replace(/#{1,6}\s*/g, '') || "No description available"}
                  </CardDescription>
                )}

                <div className="flex items-center gap-4 text-xs text-muted-foreground mb-4">
                  <div className="flex items-center gap-1">
                    <Layers className="h-3 w-3" />
                    <span>{formatWeekNumber(problem.weekOrder)}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Calendar className="h-3 w-3" />
                    <span>Day {problem.dayOrder}</span>
                  </div>
                </div>

                <Link
                  href={`/problems/${problem.slug}`}
                  className="block"
                >
                  <Button variant="secondary" size="sm" className="w-full">
                    Open Problem
                    <ArrowRight className="ml-2 h-3 w-3" />
                  </Button>
                </Link>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}

export default function SearchPage() {
  return (
    <Suspense fallback={
      <div className="flex items-center justify-center py-20">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="h-10 w-10 animate-spin text-primary" />
          <p className="text-muted-foreground">Loading search...</p>
        </div>
      </div>
    }>
      <SearchContent />
    </Suspense>
  );
}
