'use client';

import { useState, useCallback, useRef } from 'react';
import { api, AIHint, AIErrorExplanation } from '@/lib/api';

interface UseAIHintsOptions {
  problemSlug: string;
  code: string;
  testResults?: Record<string, unknown> | null;
}

interface UseAIHintsReturn {
  // Hint generation
  hint: AIHint | null;
  isLoadingHint: boolean;
  hintError: string | null;
  generateHint: (level?: number) => Promise<void>;
  requestNextLevelHint: () => Promise<void>;
  clearHint: () => void;

  // Error explanation
  errorExplanation: AIErrorExplanation | null;
  isExplainingError: boolean;
  errorExplanationError: string | null;
  explainError: (errorMessage: string) => Promise<void>;
  clearErrorExplanation: () => void;

  // Feedback
  submitFeedback: (wasHelpful: boolean, feedbackText?: string) => Promise<void>;
  isSubmittingFeedback: boolean;

  // Reporting
  reportHint: (reason: string) => Promise<void>;
  isReporting: boolean;
}

export function useAIHints({
  problemSlug,
  code,
  testResults,
}: UseAIHintsOptions): UseAIHintsReturn {
  // Hint state
  const [hint, setHint] = useState<AIHint | null>(null);
  const [isLoadingHint, setIsLoadingHint] = useState(false);
  const [hintError, setHintError] = useState<string | null>(null);
  const previousHintsRef = useRef<string[]>([]);
  const currentLevelRef = useRef<number>(1);

  // Error explanation state
  const [errorExplanation, setErrorExplanation] = useState<AIErrorExplanation | null>(null);
  const [isExplainingError, setIsExplainingError] = useState(false);
  const [errorExplanationError, setErrorExplanationError] = useState<string | null>(null);

  // Feedback state
  const [isSubmittingFeedback, setIsSubmittingFeedback] = useState(false);
  const [isReporting, setIsReporting] = useState(false);

  /**
   * Generate an AI hint at the specified level
   */
  const generateHint = useCallback(
    async (level: number = 1) => {
      if (!code || code.trim().length < 10) {
        setHintError('Write some code first to get a meaningful hint!');
        return;
      }

      setIsLoadingHint(true);
      setHintError(null);
      currentLevelRef.current = level;

      try {
        const result = await api.ai.generateHint({
          problemSlug,
          code,
          testResults: testResults || null,
          hintLevel: level,
          previousHints: previousHintsRef.current,
        });

        setHint(result);
        
        // Add this hint to previous hints for context
        if (!previousHintsRef.current.includes(result.hint)) {
          previousHintsRef.current.push(result.hint);
        }
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to generate hint';
        setHintError(message);
      } finally {
        setIsLoadingHint(false);
      }
    },
    [problemSlug, code, testResults]
  );

  /**
   * Request a more specific hint (next level)
   */
  const requestNextLevelHint = useCallback(async () => {
    const nextLevel = currentLevelRef.current + 1;
    if (nextLevel <= 3) {
      await generateHint(nextLevel);
    }
  }, [generateHint]);

  /**
   * Clear the current hint
   */
  const clearHint = useCallback(() => {
    setHint(null);
    setHintError(null);
  }, []);

  /**
   * Clear error explanation
   */
  const clearErrorExplanation = useCallback(() => {
    setErrorExplanation(null);
    setErrorExplanationError(null);
  }, []);

  /**
   * Explain an error using AI
   */
  const explainError = useCallback(
    async (errorMessage: string) => {
      if (!errorMessage) return;

      setIsExplainingError(true);
      setErrorExplanationError(null);

      try {
        const result = await api.ai.explainError({
          errorMessage,
          code,
          problemSlug,
        });

        setErrorExplanation(result);
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to explain error';
        setErrorExplanationError(message);
      } finally {
        setIsExplainingError(false);
      }
    },
    [problemSlug, code]
  );

  /**
   * Submit feedback about the current hint
   */
  const submitFeedback = useCallback(
    async (wasHelpful: boolean, feedbackText?: string) => {
      if (!hint) return;

      setIsSubmittingFeedback(true);

      try {
        await api.ai.submitFeedback({
          problemSlug,
          hintLevel: hint.hintLevel,
          wasHelpful,
          feedbackText,
        });
      } catch (err) {
        // Silently fail - feedback is not critical
        console.error('Failed to submit feedback:', err);
      } finally {
        setIsSubmittingFeedback(false);
      }
    },
    [hint, problemSlug]
  );

  /**
   * Report the current hint as problematic
   */
  const reportHint = useCallback(
    async (reason: string) => {
      if (!hint) return;

      setIsReporting(true);

      try {
        await api.ai.reportHint({
          problemSlug,
          hintLevel: hint.hintLevel,
          hintText: hint.hint,
          reason,
          userCode: code,
        });
      } catch (err) {
        // Silently fail - reporting is not critical
        console.error('Failed to report hint:', err);
      } finally {
        setIsReporting(false);
      }
    },
    [hint, problemSlug, code]
  );

  return {
    // Hint generation
    hint,
    isLoadingHint,
    hintError,
    generateHint,
    requestNextLevelHint,
    clearHint,

    // Error explanation
    errorExplanation,
    isExplainingError,
    errorExplanationError,
    explainError,
    clearErrorExplanation,

    // Feedback
    submitFeedback,
    isSubmittingFeedback,

    // Reporting
    reportHint,
    isReporting,
  };
}
