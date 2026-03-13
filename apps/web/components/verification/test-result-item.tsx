"use client";

import { CheckCircle2, XCircle, AlertCircle, Clock, ChevronDown, ChevronUp } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { InlineErrorExplainer } from "@/components/ai/error-explainer";
import type { TestResult } from "./verification-panel";

interface TestResultItemProps {
  test: TestResult;
  isExpanded: boolean;
  onToggle: () => void;
  testNumber: number;
  code?: string;
  problemSlug?: string;
  onExplainError?: (errorMessage: string) => Promise<{ explanation: string; suggestion: string; relevantLines: number[] }>;
}

const statusConfig = {
  passed: {
    icon: CheckCircle2,
    bgColor: "bg-green-50 dark:bg-green-900/20",
    borderColor: "border-green-200 dark:border-green-800",
    iconColor: "text-green-600 dark:text-green-400",
    label: "Passed",
  },
  failed: {
    icon: XCircle,
    bgColor: "bg-red-50 dark:bg-red-900/20",
    borderColor: "border-red-200 dark:border-red-800",
    iconColor: "text-red-600 dark:text-red-400",
    label: "Failed",
  },
  error: {
    icon: AlertCircle,
    bgColor: "bg-orange-50 dark:bg-orange-900/20",
    borderColor: "border-orange-200 dark:border-orange-800",
    iconColor: "text-orange-600 dark:text-orange-400",
    label: "Error",
  },
  skipped: {
    icon: Clock,
    bgColor: "bg-gray-50 dark:bg-gray-900/20",
    borderColor: "border-gray-200 dark:border-gray-800",
    iconColor: "text-gray-500 dark:text-gray-400",
    label: "Skipped",
  },
  timeout: {
    icon: Clock,
    bgColor: "bg-yellow-50 dark:bg-yellow-900/20",
    borderColor: "border-yellow-200 dark:border-yellow-800",
    iconColor: "text-yellow-600 dark:text-yellow-400",
    label: "Timeout",
  },
};

export function TestResultItem({
  test,
  isExpanded,
  onToggle,
  testNumber,
  code,
  problemSlug,
  onExplainError,
}: TestResultItemProps) {
  const config = statusConfig[test.status];
  const Icon = config.icon;
  const hasDetails = test.message || test.hint || test.expected || test.actual;

  // Format test name for display
  const displayName = test.name
    .replace(/^test_/, "")
    .replace(/_/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());

  return (
    <div
      className={cn(
        "rounded-lg border transition-colors",
        config.bgColor,
        config.borderColor,
        hasDetails && "cursor-pointer hover:opacity-80"
      )}
    >
      <div
        className="flex items-center justify-between p-3"
        onClick={hasDetails ? onToggle : undefined}
      >
        <div className="flex items-center gap-3">
          <Icon className={cn("h-5 w-5 shrink-0", config.iconColor)} />
          <div>
            <p className="text-sm font-medium">
              Test {testNumber}: {displayName}
            </p>
            {test.duration_ms !== undefined && test.duration_ms > 0 && (
              <p className="text-xs text-muted-foreground">
                {test.duration_ms.toFixed(0)}ms
              </p>
            )}
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span
            className={cn(
              "text-xs font-medium px-2 py-0.5 rounded-full",
              test.status === "passed"
                ? "bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300"
                : test.status === "failed"
                ? "bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300"
                : "bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300"
            )}
          >
            {config.label}
          </span>
          {hasDetails && (
            <Button variant="ghost" size="sm" className="h-6 w-6 p-0">
              {isExpanded ? (
                <ChevronUp className="h-4 w-4" />
              ) : (
                <ChevronDown className="h-4 w-4" />
              )}
            </Button>
          )}
        </div>
      </div>

      {isExpanded && hasDetails && (
        <div className="px-3 pb-3 pt-0 space-y-2">
          {/* Error Message */}
          {test.message && (
            <div className="bg-background/80 rounded p-2">
              <p className="text-xs font-medium text-muted-foreground mb-1">Message</p>
              <p className="text-sm text-foreground">{test.message}</p>
            </div>
          )}

          {/* Expected vs Actual */}
          {(test.expected || test.actual) && (
            <div className="grid grid-cols-2 gap-2">
              {test.expected !== undefined && (
                <div className="bg-green-100/50 dark:bg-green-900/30 rounded p-2">
                  <p className="text-xs font-medium text-green-700 dark:text-green-400 mb-1">
                    Expected
                  </p>
                  <pre className="text-sm font-mono text-green-800 dark:text-green-300 whitespace-pre-wrap">
                    {test.expected}
                  </pre>
                </div>
              )}
              {test.actual !== undefined && (
                <div className="bg-red-100/50 dark:bg-red-900/30 rounded p-2">
                  <p className="text-xs font-medium text-red-700 dark:text-red-400 mb-1">
                    Actual
                  </p>
                  <pre className="text-sm font-mono text-red-800 dark:text-red-300 whitespace-pre-wrap">
                    {test.actual}
                  </pre>
                </div>
              )}
            </div>
          )}

          {/* Hint */}
          {test.hint && (
            <div className="bg-blue-50 dark:bg-blue-900/20 rounded p-2 border border-blue-200 dark:border-blue-800">
              <p className="text-xs font-medium text-blue-700 dark:text-blue-400 mb-1">
                💡 Hint
              </p>
              <p className="text-sm text-blue-800 dark:text-blue-300">{test.hint}</p>
            </div>
          )}

          {/* Error Category */}
          {test.error_category && test.status !== "passed" && (
            <div className="text-xs text-muted-foreground">
              Error type: <span className="font-mono">{test.error_category}</span>
            </div>
          )}

          {/* AI Error Explanation */}
          {(test.status === "failed" || test.status === "error") && test.message && onExplainError && (
            <div className="pt-2 border-t border-border/50">
              <InlineErrorExplainer
                errorMessage={test.message}
                onExplain={() => onExplainError(test.message || "")}
              />
            </div>
          )}
        </div>
      )}
    </div>
  );
}
