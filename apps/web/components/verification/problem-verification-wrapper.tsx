"use client";

import { useState, useCallback } from "react";
import { VerificationPanel } from "./verification-panel";
import { useVerification } from "@/hooks/use-verification";
import { Button } from "@/components/ui/button";
import { Play, CheckCircle2, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface ProblemVerificationWrapperProps {
  problemSlug: string;
  code: string;
  onGetHint?: (hintIndex: number) => void;
  className?: string;
}

/**
 * Wrapper component that handles verification logic for a problem page
 * 
 * @example
 * ```tsx
 * <ProblemVerificationWrapper
 *   problemSlug="w01d01-hello-object"
 *   code={editorCode}
 *   onGetHint={(index) => showHint(index)}
 * />
 * ```
 */
export function ProblemVerificationWrapper({
  problemSlug,
  code,
  onGetHint,
  className,
}: ProblemVerificationWrapperProps) {
  const { data, isLoading, error, verify, retry } = useVerification();
  const [hasRunOnce, setHasRunOnce] = useState(false);

  const handleVerify = useCallback(async () => {
    setHasRunOnce(true);
    await verify({
      code,
      problem_slug: problemSlug,
    });
  }, [code, problemSlug, verify]);

  const handleRetry = useCallback(() => {
    retry();
  }, [retry]);

  const handleGetHelp = useCallback(
    (hintIndex: number) => {
      onGetHint?.(hintIndex);
    },
    [onGetHint]
  );

  return (
    <div className={cn("space-y-4", className)}>
      {/* Run Button */}
      <Button
        onClick={handleVerify}
        disabled={isLoading || !code.trim()}
        className={cn(
          "w-full gap-2 transition-all",
          data?.all_tests_passed
            ? "bg-green-600 hover:bg-green-700"
            : "bg-primary hover:bg-primary/90"
        )}
        size="lg"
      >
        {isLoading ? (
          <>
            <Loader2 className="h-4 w-4 animate-spin" />
            Running Tests...
          </>
        ) : data?.all_tests_passed ? (
          <>
            <CheckCircle2 className="h-4 w-4" />
            All Tests Passed!
          </>
        ) : (
          <>
            <Play className="h-4 w-4" />
            Run Tests
          </>
        )}
      </Button>

      {/* Error Message */}
      {error && (
        <div className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
          <p className="text-sm text-red-700 dark:text-red-300">
            <span className="font-medium">Error:</span> {error}
          </p>
          <p className="text-xs text-red-600 dark:text-red-400 mt-1">
            Please try again or contact support if the problem persists.
          </p>
        </div>
      )}

      {/* Verification Results */}
      <VerificationPanel
        verification={data}
        isLoading={isLoading}
        onRetry={hasRunOnce && !data?.all_tests_passed ? handleRetry : undefined}
        onGetHelp={onGetHint ? handleGetHelp : undefined}
      />
    </div>
  );
}

export default ProblemVerificationWrapper;
