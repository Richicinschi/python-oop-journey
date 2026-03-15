"use client";

import React from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import {
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
  CommandShortcut,
} from "@/components/ui/command";
import { useSearch } from "@/hooks/use-search";
import { useRecentSearches } from "@/hooks/use-recent-searches";
import { useVisitedItems } from "@/hooks/use-visited-items";
import type { SearchIndexItem, SearchResult } from "@repo/types";
import {
  Search,
  Clock,
  FileCode,
  Calendar,
  Layers,
  Hash,
  ArrowRight,
  X,
  ExternalLink,
} from "lucide-react";
import { cn, formatRelativeTime } from "@/lib/utils";

interface CommandPaletteProps {
  searchIndex: SearchIndexItem[];
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

function getTypeIcon(type: SearchIndexItem["type"]) {
  switch (type) {
    case "week":
      return <Layers className="h-4 w-4" />;
    case "day":
      return <Calendar className="h-4 w-4" />;
    case "problem":
      return <FileCode className="h-4 w-4" />;
    case "topic":
      return <Hash className="h-4 w-4" />;
    case "keyword":
      return <Search className="h-4 w-4" />;
    default:
      return <FileCode className="h-4 w-4" />;
  }
}

function getTypeLabel(type: SearchIndexItem["type"]) {
  switch (type) {
    case "week":
      return "Week";
    case "day":
      return "Day";
    case "problem":
      return "Problem";
    case "topic":
      return "Topic";
    case "keyword":
      return "Keyword";
    default:
      return type;
  }
}

function highlightText(text: string, query: string) {
  if (!query.trim()) return text;

  const parts = text.split(new RegExp(`(${query})`, "gi"));
  return parts.map((part, i) =>
    part.toLowerCase() === query.toLowerCase() ? (
      <mark
        key={i}
        className="bg-primary/20 text-primary font-semibold rounded px-0.5"
      >
        {part}
      </mark>
    ) : (
      part
    )
  );
}

function SearchResultItem({
  result,
  query,
  onSelect,
}: {
  result: SearchResult;
  query: string;
  onSelect: () => void;
}) {
  const { item } = result;

  return (
    <CommandItem
      onSelect={onSelect}
      className="flex items-start gap-3 px-2 py-2 cursor-pointer"
    >
      <div className="mt-0.5 flex-shrink-0 text-muted-foreground">
        {getTypeIcon(item.type)}
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2">
          <span className="font-medium truncate">
            {highlightText(item.title, query)}
          </span>
          <span className="text-xs text-muted-foreground whitespace-nowrap">
            {getTypeLabel(item.type)}
          </span>
          {item.difficulty && (
            <span
              className={cn(
                "text-[10px] px-1.5 py-0.5 rounded-full capitalize",
                item.difficulty === "easy" &&
                  "bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300",
                item.difficulty === "medium" &&
                  "bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300",
                item.difficulty === "hard" &&
                  "bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300"
              )}
            >
              {item.difficulty}
            </span>
          )}
        </div>
        {item.description && (
          <p className="text-sm text-muted-foreground truncate">
            {highlightText(item.description, query)}
          </p>
        )}
        {item.week !== undefined && (
          <p className="text-xs text-muted-foreground mt-0.5">
            Week {item.week}
            {item.day !== undefined && ` · Day ${item.day}`}
          </p>
        )}
      </div>
      <ArrowRight className="h-4 w-4 opacity-0 group-data-[selected=true]:opacity-100 text-muted-foreground" />
    </CommandItem>
  );
}

export const CommandPalette = React.memo(function CommandPalette({
  searchIndex,
  open,
  onOpenChange,
}: CommandPaletteProps) {
  const router = useRouter();
  const { query, setQuery, results, isSearching, clearSearch } = useSearch({
    searchIndex,
    debounceMs: 150,
  });
  const { recentSearches, addRecentSearch, removeRecentSearch } =
    useRecentSearches();
  const { visitedItems } = useVisitedItems();

  const handleSelect = (item: SearchIndexItem) => {
    addRecentSearch(item.title);
    onOpenChange(false);
    router.push(item.url);
    clearSearch();
  };

  // Group results by type
  const groupedResults = React.useMemo(() => {
    const groups: Record<string, SearchResult[]> = {
      problem: [],
      day: [],
      week: [],
      topic: [],
      keyword: [],
    };

    results.forEach((result) => {
      const type = result.item.type;
      if (!groups[type]) groups[type] = [];
      groups[type].push(result);
    });

    return groups;
  }, [results]);

  // Keyboard shortcut to open
  React.useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if ((e.key === "k" && (e.metaKey || e.ctrlKey)) || e.key === "/") {
        e.preventDefault();
        onOpenChange(true);
      }
    };

    document.addEventListener("keydown", down);
    return () => document.removeEventListener("keydown", down);
  }, [onOpenChange]);

  return (
    <CommandDialog open={open} onOpenChange={onOpenChange}>
      <CommandInput
        placeholder="Search weeks, days, problems, topics..."
        value={query}
        onValueChange={setQuery}
      />
      <CommandList>
        {isSearching ? (
          <div className="py-6 text-center text-sm text-muted-foreground">
            <div className="animate-spin inline-block w-4 h-4 border-2 border-current border-t-transparent rounded-full mr-2" />
            Searching...
          </div>
        ) : (
          <>
            <CommandEmpty>
              <div className="py-6 text-center">
                <p className="text-muted-foreground">No results found.</p>
                <p className="text-xs text-muted-foreground mt-1">
                  Try a different search term or filter
                </p>
              </div>
            </CommandEmpty>

            {/* Recent searches when query is empty */}
            {!query && recentSearches.length > 0 && (
              <CommandGroup heading="Recent Searches">
                {recentSearches.slice(0, 5).map((search) => (
                  <CommandItem
                    key={search.query}
                    onSelect={() => setQuery(search.query)}
                    className="flex items-center gap-2"
                  >
                    <Clock className="h-4 w-4 text-muted-foreground" />
                    <span>{search.query}</span>
                    <span className="text-xs text-muted-foreground ml-auto">
                      {formatRelativeTime(search.timestamp)}
                    </span>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        removeRecentSearch(search.query);
                      }}
                      className="p-1 hover:bg-accent rounded"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  </CommandItem>
                ))}
              </CommandGroup>
            )}

            {/* Recently visited when query is empty */}
            {!query && visitedItems.length > 0 && (
              <>
                <CommandSeparator />
                <CommandGroup heading="Recently Visited">
                  {visitedItems.slice(0, 5).map((item) => (
                    <CommandItem
                      key={item.id}
                      onSelect={() => {
                        onOpenChange(false);
                        router.push(item.url);
                      }}
                      className="flex items-center gap-2"
                    >
                      {getTypeIcon(item.type as SearchIndexItem["type"])}
                      <span>{item.title}</span>
                      <span className="text-xs text-muted-foreground ml-auto">
                        {formatRelativeTime(item.visitedAt)}
                      </span>
                    </CommandItem>
                  ))}
                </CommandGroup>
              </>
            )}

            {/* Search results */}
            {query && (
              <>
                {groupedResults.problem.length > 0 && (
                  <CommandGroup heading="Problems">
                    {groupedResults.problem.slice(0, 6).map((result) => (
                      <SearchResultItem
                        key={result.item.id}
                        result={result}
                        query={query}
                        onSelect={() => handleSelect(result.item)}
                      />
                    ))}
                  </CommandGroup>
                )}

                {groupedResults.day.length > 0 && (
                  <>
                    <CommandSeparator />
                    <CommandGroup heading="Days">
                      {groupedResults.day.slice(0, 4).map((result) => (
                        <SearchResultItem
                          key={result.item.id}
                          result={result}
                          query={query}
                          onSelect={() => handleSelect(result.item)}
                        />
                      ))}
                    </CommandGroup>
                  </>
                )}

                {groupedResults.week.length > 0 && (
                  <>
                    <CommandSeparator />
                    <CommandGroup heading="Weeks">
                      {groupedResults.week.map((result) => (
                        <SearchResultItem
                          key={result.item.id}
                          result={result}
                          query={query}
                          onSelect={() => handleSelect(result.item)}
                        />
                      ))}
                    </CommandGroup>
                  </>
                )}

                {groupedResults.topic.length > 0 && (
                  <>
                    <CommandSeparator />
                    <CommandGroup heading="Topics">
                      {groupedResults.topic.slice(0, 4).map((result) => (
                        <SearchResultItem
                          key={result.item.id}
                          result={result}
                          query={query}
                          onSelect={() => handleSelect(result.item)}
                        />
                      ))}
                    </CommandGroup>
                  </>
                )}

                {/* View All Results */}
                {query && results.length > 0 && (
                  <>
                    <CommandSeparator />
                    <CommandGroup>
                      <CommandItem
                        onSelect={() => {
                          onOpenChange(false);
                          router.push(`/search?q=${encodeURIComponent(query)}`);
                        }}
                        className="flex items-center justify-center gap-2 text-primary cursor-pointer"
                      >
                        <Search className="h-4 w-4" />
                        <span>View All Results</span>
                        <ArrowRight className="h-4 w-4" />
                      </CommandItem>
                    </CommandGroup>
                  </>
                )}
              </>
            )}
          </>
        )}
      </CommandList>
      <div className="flex items-center justify-between px-3 py-2 border-t text-xs text-muted-foreground">
        <div className="flex items-center gap-3">
          <span className="flex items-center gap-1">
            <kbd className="bg-muted px-1.5 py-0.5 rounded">↑↓</kbd>
            Navigate
          </span>
          <span className="flex items-center gap-1">
            <kbd className="bg-muted px-1.5 py-0.5 rounded">↵</kbd>
            Select
          </span>
        </div>
        <div className="flex items-center gap-3">
          <span className="flex items-center gap-1">
            <kbd className="bg-muted px-1.5 py-0.5 rounded">Esc</kbd>
            Close
          </span>
          <span className="flex items-center gap-1">
            <kbd className="bg-muted px-1.5 py-0.5 rounded">⌘K</kbd>
            Open
          </span>
        </div>
      </div>
    </CommandDialog>
  );
});

CommandPalette.displayName = 'CommandPalette';
