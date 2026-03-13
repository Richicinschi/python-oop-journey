'use client';

import { useState, useEffect, useCallback } from 'react';
import { api, Bookmark, BookmarkCreate, ItemType, BookmarkCheck } from '@/lib/api';

interface UseBookmarksReturn {
  bookmarks: Bookmark[];
  isLoading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}

interface UseToggleBookmarkReturn {
  isBookmarked: boolean;
  bookmarkId: string | null;
  toggle: (notes?: string) => Promise<boolean>;
  isLoading: boolean;
  error: Error | null;
}

interface UseIsBookmarkedReturn {
  isBookmarked: boolean;
  bookmarkId: string | null;
  isLoading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}

// Local storage key for offline support
const BOOKMARKS_STORAGE_KEY = 'oop-journey-bookmarks';

/**
 * Hook to get all bookmarks
 */
export function useBookmarks(itemType?: ItemType): UseBookmarksReturn {
  const [bookmarks, setBookmarks] = useState<Bookmark[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchBookmarks = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await api.bookmarks.list(itemType);
      setBookmarks(data.items);
      
      // Cache to localStorage
      localStorage.setItem(BOOKMARKS_STORAGE_KEY, JSON.stringify(data.items));
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to fetch bookmarks'));
      
      // Try to load from cache on error
      const cached = localStorage.getItem(BOOKMARKS_STORAGE_KEY);
      if (cached) {
        try {
          const parsed: Bookmark[] = JSON.parse(cached);
          if (itemType) {
            setBookmarks(parsed.filter(b => b.itemType === itemType));
          } else {
            setBookmarks(parsed);
          }
        } catch {
          // Ignore parse errors
        }
      }
    } finally {
      setIsLoading(false);
    }
  }, [itemType]);

  useEffect(() => {
    fetchBookmarks();
  }, [fetchBookmarks]);

  return {
    bookmarks,
    isLoading,
    error,
    refetch: fetchBookmarks,
  };
}

/**
 * Hook to toggle a bookmark
 */
export function useToggleBookmark(
  itemType: ItemType,
  itemSlug: string
): UseToggleBookmarkReturn {
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [bookmarkId, setBookmarkId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  // Check initial status
  const checkStatus = useCallback(async () => {
    if (!itemSlug) return;
    
    try {
      const result = await api.bookmarks.check(itemType, itemSlug);
      setIsBookmarked(result.isBookmarked);
      setBookmarkId(result.bookmarkId);
    } catch {
      // Ignore errors on initial check
    }
  }, [itemType, itemSlug]);

  useEffect(() => {
    checkStatus();
  }, [checkStatus]);

  const toggle = useCallback(async (notes?: string) => {
    if (!itemSlug) return false;
    
    try {
      setIsLoading(true);
      setError(null);
      
      const data: BookmarkCreate = { itemType, itemSlug, notes };
      const result = await api.bookmarks.toggle(data);
      
      setIsBookmarked(result.isBookmarked);
      setBookmarkId(result.bookmarkId);
      
      // Update cache
      if (result.isBookmarked && result.bookmarkId) {
        const cached = localStorage.getItem(BOOKMARKS_STORAGE_KEY);
        const bookmarks: Bookmark[] = cached ? JSON.parse(cached) : [];
        bookmarks.push({
          id: result.bookmarkId,
          userId: '',
          itemType,
          itemSlug,
          notes: notes || null,
          createdAt: new Date().toISOString(),
        });
        localStorage.setItem(BOOKMARKS_STORAGE_KEY, JSON.stringify(bookmarks));
      } else {
        const cached = localStorage.getItem(BOOKMARKS_STORAGE_KEY);
        if (cached) {
          const bookmarks: Bookmark[] = JSON.parse(cached);
          const filtered = bookmarks.filter(
            b => !(b.itemType === itemType && b.itemSlug === itemSlug)
          );
          localStorage.setItem(BOOKMARKS_STORAGE_KEY, JSON.stringify(filtered));
        }
      }
      
      return result.isBookmarked;
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to toggle bookmark'));
      return isBookmarked; // Return current state on error
    } finally {
      setIsLoading(false);
    }
  }, [itemType, itemSlug, isBookmarked]);

  return {
    isBookmarked,
    bookmarkId,
    toggle,
    isLoading,
    error,
  };
}

/**
 * Hook to check if an item is bookmarked
 */
export function useIsBookmarked(
  itemType: ItemType,
  itemSlug: string
): UseIsBookmarkedReturn {
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [bookmarkId, setBookmarkId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const checkBookmark = useCallback(async () => {
    if (!itemSlug) {
      setIsLoading(false);
      return;
    }
    
    try {
      setIsLoading(true);
      setError(null);
      const result = await api.bookmarks.check(itemType, itemSlug);
      setIsBookmarked(result.isBookmarked);
      setBookmarkId(result.bookmarkId);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to check bookmark'));
    } finally {
      setIsLoading(false);
    }
  }, [itemType, itemSlug]);

  useEffect(() => {
    checkBookmark();
  }, [checkBookmark]);

  return {
    isBookmarked,
    bookmarkId,
    isLoading,
    error,
    refetch: checkBookmark,
  };
}

/**
 * Hook to delete a bookmark by ID
 */
export function useDeleteBookmark() {
  const [isDeleting, setIsDeleting] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const deleteBookmark = useCallback(async (bookmarkId: string) => {
    try {
      setIsDeleting(true);
      setError(null);
      await api.bookmarks.delete(bookmarkId);
      
      // Update cache
      const cached = localStorage.getItem(BOOKMARKS_STORAGE_KEY);
      if (cached) {
        const bookmarks: Bookmark[] = JSON.parse(cached);
        const filtered = bookmarks.filter(b => b.id !== bookmarkId);
        localStorage.setItem(BOOKMARKS_STORAGE_KEY, JSON.stringify(filtered));
      }
      
      return true;
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to delete bookmark'));
      return false;
    } finally {
      setIsDeleting(false);
    }
  }, []);

  return {
    deleteBookmark,
    isDeleting,
    error,
  };
}

/**
 * Hook to update bookmark notes
 */
export function useUpdateBookmarkNotes() {
  const [isUpdating, setIsUpdating] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const updateNotes = useCallback(async (bookmarkId: string, notes: string) => {
    try {
      setIsUpdating(true);
      setError(null);
      const updated = await api.bookmarks.update(bookmarkId, { notes });
      
      // Update cache
      const cached = localStorage.getItem(BOOKMARKS_STORAGE_KEY);
      if (cached) {
        const bookmarks: Bookmark[] = JSON.parse(cached);
        const index = bookmarks.findIndex(b => b.id === bookmarkId);
        if (index !== -1) {
          bookmarks[index] = { ...bookmarks[index], notes };
          localStorage.setItem(BOOKMARKS_STORAGE_KEY, JSON.stringify(bookmarks));
        }
      }
      
      return updated;
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to update bookmark notes'));
      return null;
    } finally {
      setIsUpdating(false);
    }
  }, []);

  return {
    updateNotes,
    isUpdating,
    error,
  };
}

// Legacy types for backward compatibility
export interface LegacyBookmark {
  id: string;
  type: 'problem' | 'week' | 'day';
  title: string;
  path: string;
  notes?: string;
  createdAt: string;
}

const LEGACY_BOOKMARKS_KEY = 'bookmarks';

/**
 * Legacy hook for backward compatibility with localStorage
 * @deprecated Use useBookmarks() for server-side bookmarks
 */
export function useLocalBookmarks() {
  const [bookmarks, setBookmarks] = useState<LegacyBookmark[]>([]);

  useEffect(() => {
    const stored = localStorage.getItem(LEGACY_BOOKMARKS_KEY);
    if (stored) {
      try {
        setBookmarks(JSON.parse(stored));
      } catch {
        // Ignore parse errors
      }
    }
  }, []);

  const addBookmark = useCallback((item: Omit<LegacyBookmark, 'createdAt'>) => {
    setBookmarks((prev) => {
      if (prev.some((b) => b.id === item.id)) {
        return prev;
      }

      const newBookmark: LegacyBookmark = {
        ...item,
        createdAt: new Date().toISOString(),
      };

      const updated = [...prev, newBookmark];
      localStorage.setItem(LEGACY_BOOKMARKS_KEY, JSON.stringify(updated));
      return updated;
    });
  }, []);

  const removeBookmark = useCallback((id: string) => {
    setBookmarks((prev) => {
      const updated = prev.filter((b) => b.id !== id);
      localStorage.setItem(LEGACY_BOOKMARKS_KEY, JSON.stringify(updated));
      return updated;
    });
  }, []);

  const toggleBookmark = useCallback((item: Omit<LegacyBookmark, 'createdAt'>) => {
    const exists = bookmarks.some((b) => b.id === item.id);
    if (exists) {
      removeBookmark(item.id);
    } else {
      addBookmark(item);
    }
  }, [bookmarks, addBookmark, removeBookmark]);

  const isBookmarked = useCallback((id: string) => {
    return bookmarks.some((b) => b.id === id);
  }, [bookmarks]);

  const updateBookmarkNotes = useCallback((id: string, notes: string) => {
    setBookmarks((prev) => {
      const updated = prev.map((b) => (b.id === id ? { ...b, notes } : b));
      localStorage.setItem(LEGACY_BOOKMARKS_KEY, JSON.stringify(updated));
      return updated;
    });
  }, []);

  const clearBookmarks = useCallback(() => {
    setBookmarks([]);
    localStorage.removeItem(LEGACY_BOOKMARKS_KEY);
  }, []);

  const groupedBookmarks = bookmarks.reduce((acc, bookmark) => {
    const type = bookmark.type;
    if (!acc[type]) {
      acc[type] = [];
    }
    acc[type].push(bookmark);
    return acc;
  }, {} as Record<LegacyBookmark['type'], LegacyBookmark[]>);

  return {
    bookmarks,
    groupedBookmarks,
    addBookmark,
    removeBookmark,
    toggleBookmark,
    isBookmarked,
    updateBookmarkNotes,
    clearBookmarks,
  };
}
