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

  return (
    <div className="min-h-screen">
      <Header onSearchClick={() => setSearchOpen(true)} />
      <main>{children}</main>
      <CommandPalette
        searchIndex={searchIndex}
        open={searchOpen}
        onOpenChange={setSearchOpen}
      />
    </div>
  );
}
