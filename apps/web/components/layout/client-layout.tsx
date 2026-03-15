"use client";

import * as React from "react";
import { Header } from "./header";
import { CommandPalette } from "@/components/search";
import searchIndexRaw from "@/data/search-index.json";
import type { SearchIndexItem } from "@/lib/search";
const searchIndex = searchIndexRaw as SearchIndexItem[];

interface ClientLayoutProps {
  children: React.ReactNode;
}

export function ClientLayout({ children }: ClientLayoutProps) {
  const [searchOpen, setSearchOpen] = React.useState(false);

  // Open command palette when search button is clicked
  const handleSearchClick = () => {
    setSearchOpen(true);
  };

  return (
    <div className="min-h-screen">
      {/* 
        This Header is used in layouts without a sidebar (like auth pages).
        The menu button is only shown when onMenuClick is provided.
      */}
      <Header onSearchClick={handleSearchClick} />
      <main>{children}</main>
      <CommandPalette
        searchIndex={searchIndex}
        open={searchOpen}
        onOpenChange={setSearchOpen}
      />
    </div>
  );
}
