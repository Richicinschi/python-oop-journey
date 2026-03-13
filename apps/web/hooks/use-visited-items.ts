"use client";

import { useLocalStorage } from "./use-local-storage";
import type { VisitedItem } from "@repo/types";

const MAX_VISITED_ITEMS = 100;
const STORAGE_KEY = "visited-items";

export function useVisitedItems() {
  const [visitedItems, setVisitedItems] = useLocalStorage<VisitedItem[]>(
    STORAGE_KEY,
    []
  );

  const addVisitedItem = (item: Omit<VisitedItem, "visitedAt">) => {
    setVisitedItems((prev) => {
      // Remove existing entry if present
      const filtered = prev.filter((i) => i.id !== item.id);

      // Add new entry at the beginning
      const newEntry: VisitedItem = {
        ...item,
        visitedAt: new Date().toISOString(),
      };

      // Keep only the most recent items
      return [newEntry, ...filtered].slice(0, MAX_VISITED_ITEMS);
    });
  };

  const removeVisitedItem = (id: string) => {
    setVisitedItems((prev) => prev.filter((i) => i.id !== id));
  };

  const clearVisitedItems = () => {
    setVisitedItems([]);
  };

  const getLastVisited = () => {
    return visitedItems[0] || null;
  };

  return {
    visitedItems,
    addVisitedItem,
    removeVisitedItem,
    clearVisitedItems,
    getLastVisited,
  };
}
