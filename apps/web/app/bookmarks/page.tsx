"use client";

import * as React from "react";
import Link from "next/link";
import { Bookmark, Trash2, ArrowRight, BookOpen, Calendar, FileCode, Hash, Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useBookmarks } from "@/hooks/use-bookmarks";
import { formatDate, cn } from "@/lib/utils";
import type { Bookmark as BookmarkType } from "@repo/types";

const typeIcons = {
  week: BookOpen,
  day: Calendar,
  problem: FileCode,
  theory: Hash,
};

const typeLabels = {
  week: "Weeks",
  day: "Days",
  problem: "Problems",
  theory: "Theory",
};

export default function BookmarksPage() {
  const { bookmarks, groupedBookmarks, removeBookmark, clearBookmarks } = useBookmarks();
  const [searchQuery, setSearchQuery] = React.useState("");

  const filteredBookmarks = React.useMemo(() => {
    if (!searchQuery) return bookmarks;
    const query = searchQuery.toLowerCase();
    return bookmarks.filter(
      (b) =>
        b.title.toLowerCase().includes(query) ||
        b.notes?.toLowerCase().includes(query)
    );
  }, [bookmarks, searchQuery]);

  const filteredGrouped = React.useMemo(() => {
    const result: Record<string, BookmarkType[]> = {};
    Object.entries(groupedBookmarks).forEach(([type, items]) => {
      if (searchQuery) {
        const query = searchQuery.toLowerCase();
        result[type] = items.filter(
          (b) =>
            b.title.toLowerCase().includes(query) ||
            b.notes?.toLowerCase().includes(query)
        );
      } else {
        result[type] = items;
      }
    });
    return result;
  }, [groupedBookmarks, searchQuery]);

  if (bookmarks.length === 0) {
    return (
      <div className="container mx-auto px-4 py-12 max-w-4xl">
        <div className="text-center">
          <Bookmark className="h-12 w-12 mx-auto text-muted-foreground/50 mb-4" />
          <h1 className="text-2xl font-bold mb-2">No Bookmarks</h1>
          <p className="text-muted-foreground mb-6">
            Bookmark your favorite problems, days, or weeks to find them easily later.
          </p>
          <Button asChild>
            <Link href="/problems">Browse Problems</Link>
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold mb-2">Your Bookmarks</h1>
          <p className="text-muted-foreground">
            {bookmarks.length} saved items
          </p>
        </div>
        <Button variant="destructive" size="sm" onClick={clearBookmarks}>
          <Trash2 className="h-4 w-4 mr-2" />
          Clear All
        </Button>
      </div>

      {/* Search */}
      <div className="relative mb-6">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Search bookmarks..."
          className="pl-10"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      {/* Tabs by Type */}
      <Tabs defaultValue="all" className="space-y-6">
        <TabsList className="flex-wrap h-auto">
          <TabsTrigger value="all">
            All ({filteredBookmarks.length})
          </TabsTrigger>
          {Object.entries(filteredGrouped).map(([type, items]) => (
            items.length > 0 && (
              <TabsTrigger key={type} value={type}>
                {typeLabels[type as keyof typeof typeLabels]} ({items.length})
              </TabsTrigger>
            )
          ))}
        </TabsList>

        <TabsContent value="all" className="space-y-4">
          {filteredBookmarks.length === 0 ? (
            <EmptyState query={searchQuery} />
          ) : (
            filteredBookmarks.map((bookmark) => (
              <BookmarkCard
                key={bookmark.id}
                bookmark={bookmark}
                onRemove={() => removeBookmark(bookmark.id)}
              />
            ))
          )}
        </TabsContent>

        {Object.entries(filteredGrouped).map(([type, items]) => (
          <TabsContent key={type} value={type} className="space-y-4">
            {items.length === 0 ? (
              <EmptyState query={searchQuery} />
            ) : (
              items.map((bookmark) => (
                <BookmarkCard
                  key={bookmark.id}
                  bookmark={bookmark}
                  onRemove={() => removeBookmark(bookmark.id)}
                />
              ))
            )}
          </TabsContent>
        ))}
      </Tabs>
    </div>
  );
}

function BookmarkCard({
  bookmark,
  onRemove,
}: {
  bookmark: BookmarkType;
  onRemove: () => void;
}) {
  const Icon = typeIcons[bookmark.type];

  return (
    <Card className="group hover:shadow-sm transition-shadow">
      <CardContent className="p-4">
        <div className="flex items-start gap-4">
          <div className="p-2 rounded-lg bg-primary/10 text-primary">
            <Icon className="h-4 w-4" />
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <h3 className="font-medium">{bookmark.title}</h3>
              <Badge variant="secondary" className="text-[10px]">
                {bookmark.type}
              </Badge>
            </div>
            {bookmark.notes && (
              <p className="text-sm text-muted-foreground mt-1">
                {bookmark.notes}
              </p>
            )}
            <div className="flex items-center gap-3 mt-2 text-sm text-muted-foreground">
              <span>Bookmarked {formatDate(bookmark.createdAt)}</span>
              {bookmark.week !== undefined && (
                <>
                  <span>·</span>
                  <span>Week {bookmark.week}</span>
                  {bookmark.day && <span>· Day {bookmark.day}</span>}
                </>
              )}
            </div>
          </div>
          <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
            <Button variant="ghost" size="sm" onClick={onRemove}>
              <Trash2 className="h-4 w-4" />
            </Button>
            <Button asChild size="sm">
              <Link href={bookmark.url}>
                View
                <ArrowRight className="ml-1 h-4 w-4" />
              </Link>
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

function EmptyState({ query }: { query: string }) {
  return (
    <div className="text-center py-12">
      <Search className="h-12 w-12 mx-auto text-muted-foreground/50 mb-4" />
      <h3 className="text-lg font-medium mb-2">
        {query ? "No matches found" : "No bookmarks in this category"}
      </h3>
      <p className="text-muted-foreground">
        {query
          ? "Try a different search term"
          : "Start bookmarking content to see it here"}
      </p>
    </div>
  );
}
