'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { api, Draft, DraftUpdate } from '@/lib/api';

interface UseDraftReturn {
  draft: Draft | null;
  isLoading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}

interface UseSaveDraftReturn {
  saveDraft: (code: string, isAutoSave?: boolean) => Promise<Draft | null>;
  isSaving: boolean;
  error: Error | null;
}

interface UseDeleteDraftReturn {
  deleteDraft: () => Promise<boolean>;
  isDeleting: boolean;
  error: Error | null;
}

// Local storage key for offline support
const DRAFT_STORAGE_PREFIX = 'oop-journey-draft-';

/**
 * Hook to get draft for a specific problem
 */
export function useDraft(problemSlug: string): UseDraftReturn {
  const [draft, setDraft] = useState<Draft | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchDraft = useCallback(async () => {
    if (!problemSlug) return;
    
    try {
      setIsLoading(true);
      setError(null);
      const data = await api.drafts.get(problemSlug);
      setDraft(data);
      
      // Cache to localStorage
      localStorage.setItem(`${DRAFT_STORAGE_PREFIX}${problemSlug}`, JSON.stringify(data));
    } catch (err) {
      // If 404, it means no draft yet - that's ok
      if (err instanceof Error && err.message.includes('404')) {
        setDraft(null);
      } else {
        setError(err instanceof Error ? err : new Error('Failed to fetch draft'));
        
        // Try to load from cache on error
        const cached = localStorage.getItem(`${DRAFT_STORAGE_PREFIX}${problemSlug}`);
        if (cached) {
          try {
            setDraft(JSON.parse(cached));
          } catch {
            // Ignore parse errors
          }
        }
      }
    } finally {
      setIsLoading(false);
    }
  }, [problemSlug]);

  useEffect(() => {
    fetchDraft();
  }, [fetchDraft]);

  return {
    draft,
    isLoading,
    error,
    refetch: fetchDraft,
  };
}

/**
 * Hook to save draft with debounce
 */
export function useSaveDraft(problemSlug: string): UseSaveDraftReturn {
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const debounceTimerRef = useRef<NodeJS.Timeout | null>(null);

  const saveDraft = useCallback(async (code: string, isAutoSave: boolean = false) => {
    if (!problemSlug) return null;
    
    // Clear any pending debounced save
    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
    }

    // Save immediately if not auto-save, otherwise debounce
    const doSave = async () => {
      try {
        setIsSaving(true);
        setError(null);
        
        const data: DraftUpdate = { code, isAutoSave };
        const saved = await api.drafts.save(problemSlug, data);
        
        // Update cache
        localStorage.setItem(`${DRAFT_STORAGE_PREFIX}${problemSlug}`, JSON.stringify(saved));
        
        return saved;
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Failed to save draft'));
        
        // Save to localStorage as fallback
        const fallbackDraft = {
          id: `local-${problemSlug}`,
          userId: 'local',
          problemSlug,
          code,
          savedAt: new Date().toISOString(),
          isAutoSave,
          createdAt: new Date().toISOString(),
        };
        localStorage.setItem(`${DRAFT_STORAGE_PREFIX}${problemSlug}`, JSON.stringify(fallbackDraft));
        
        return null;
      } finally {
        setIsSaving(false);
      }
    };

    if (isAutoSave) {
      // Debounce auto-saves
      return new Promise<Draft | null>((resolve) => {
        debounceTimerRef.current = setTimeout(async () => {
          const result = await doSave();
          resolve(result);
        }, 2000); // 2 second debounce for auto-save
      });
    } else {
      // Save immediately for manual saves
      return doSave();
    }
  }, [problemSlug]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }
    };
  }, []);

  return {
    saveDraft,
    isSaving,
    error,
  };
}

/**
 * Hook to delete draft
 */
export function useDeleteDraft(problemSlug: string): UseDeleteDraftReturn {
  const [isDeleting, setIsDeleting] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const deleteDraft = useCallback(async () => {
    if (!problemSlug) return false;
    
    try {
      setIsDeleting(true);
      setError(null);
      await api.drafts.delete(problemSlug);
      
      // Clear from localStorage
      localStorage.removeItem(`${DRAFT_STORAGE_PREFIX}${problemSlug}`);
      
      return true;
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to delete draft'));
      return false;
    } finally {
      setIsDeleting(false);
    }
  }, [problemSlug]);

  return {
    deleteDraft,
    isDeleting,
    error,
  };
}

/**
 * Combined hook for draft management
 */
export function useDraftManager(problemSlug: string) {
  const { draft, isLoading, error: fetchError, refetch } = useDraft(problemSlug);
  const { saveDraft, isSaving, error: saveError } = useSaveDraft(problemSlug);
  const { deleteDraft, isDeleting, error: deleteError } = useDeleteDraft(problemSlug);

  const getLocalDraft = useCallback(() => {
    const cached = localStorage.getItem(`${DRAFT_STORAGE_PREFIX}${problemSlug}`);
    if (cached) {
      try {
        const parsed = JSON.parse(cached);
        return parsed.code || '';
      } catch {
        return '';
      }
    }
    return '';
  }, [problemSlug]);

  return {
    // Data
    draft,
    code: draft?.code || getLocalDraft(),
    
    // Loading states
    isLoading,
    isSaving,
    isDeleting,
    
    // Errors
    error: fetchError || saveError || deleteError,
    
    // Actions
    saveDraft,
    deleteDraft,
    refetch,
    
    // Helpers
    hasDraft: !!draft || !!getLocalDraft(),
    lastSaved: draft?.savedAt || null,
  };
}
