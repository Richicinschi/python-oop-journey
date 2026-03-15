"use client";

import { Bookmark } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useLocalBookmarks } from "@/hooks/use-bookmarks";
import { cn } from "@/lib/utils";
import { useToast } from "@/components/ui/use-toast";
import type { Bookmark as BookmarkType } from "@repo/types";

interface BookmarkButtonProps {
  item: Omit<BookmarkType, "createdAt" | "notes">;
  variant?: "default" | "ghost" | "outline";
  size?: "default" | "sm" | "lg" | "icon";
  className?: string;
  showLabel?: boolean;
}

export function BookmarkButton({
  item,
  variant = "ghost",
  size = "icon",
  className,
  showLabel = false,
}: BookmarkButtonProps) {
  const { isBookmarked, toggleBookmark } = useLocalBookmarks();
  const { toast } = useToast();
  const bookmarked = isBookmarked(item.id);

  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    const newBookmarkedState = toggleBookmark(item);
    
    // Show toast notification
    if (newBookmarkedState) {
      toast({
        title: "Bookmark added",
        description: `"${item.title}" has been added to your bookmarks.`,
        variant: "success",
        duration: 3000,
      });
    } else {
      toast({
        title: "Bookmark removed",
        description: `"${item.title}" has been removed from your bookmarks.`,
        variant: "default",
        duration: 3000,
      });
    }
  };

  return (
    <Button
      variant={variant}
      size={size}
      className={cn(
        "transition-colors",
        bookmarked && "text-yellow-500 hover:text-yellow-600",
        className
      )}
      onClick={handleClick}
      aria-label={bookmarked ? "Remove bookmark" : "Add bookmark"}
    >
      <Bookmark
        className={cn("h-4 w-4", bookmarked && "fill-current")}
      />
      {showLabel && (
        <span className="ml-2">
          {bookmarked ? "Bookmarked" : "Bookmark"}
        </span>
      )}
    </Button>
  );
}
