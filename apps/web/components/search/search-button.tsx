"use client";

import { Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface SearchButtonProps {
  onClick: () => void;
  className?: string;
  showShortcut?: boolean;
}

export function SearchButton({
  onClick,
  className,
  showShortcut = true,
}: SearchButtonProps) {
  return (
    <Button
      variant="outline"
      className={cn(
        "relative h-9 w-full justify-start rounded-md bg-muted/50 text-sm font-normal text-muted-foreground shadow-none hover:bg-muted hover:text-foreground sm:pr-12",
        className
      )}
      onClick={onClick}
    >
      <Search className="mr-2 h-4 w-4" />
      Search...
      {showShortcut && (
        <kbd className="pointer-events-none absolute right-1.5 top-1.5 hidden h-6 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium opacity-100 sm:flex">
          <span className="text-xs">⌘</span>K
        </kbd>
      )}
    </Button>
  );
}

export function MobileSearchButton({
  onClick,
  className,
}: Omit<SearchButtonProps, "showShortcut">) {
  return (
    <Button
      variant="ghost"
      size="icon"
      className={cn("h-9 w-9", className)}
      onClick={onClick}
    >
      <Search className="h-5 w-5" />
      <span className="sr-only">Search</span>
    </Button>
  );
}
