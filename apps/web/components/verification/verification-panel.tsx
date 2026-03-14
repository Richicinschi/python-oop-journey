"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Separator } from "@/components/ui/separator";
import { 
  CheckCircle2, 
  XCircle, 
  AlertCircle, 
  Play, 
  RotateCcw, 
  Lightbulb,
  ChevronDown,
  ChevronUp,
  Terminal,
  Clock,
  Trophy
} from "lucide-react";
import { cn } from "@/lib/utils";
import { ErrorExplainer } from "@/components/ai/error-explainer";
import { useAIHints } from "@/hooks/use-ai-hints";
import { TestResultItem } from "./test-result-item";
import { FailureExplanation } from "./failure-explanation";

// Types
export interface TestResult {
  name: string;
  status: "passed" | "failed" | "error" | "skipped" | "timeout";
  message?: string;
  expected?: string;
  actual?: string;
  hint?: string;
  error_category?: string;
  duration_ms?: number;
}

export interface VerificationSummary {
  total: number;
  passed: number;
  failed: number;
  errors: number;
  skipped?: number;
}

export interface VerificationData {
  success: boolean;
  summary: VerificationSummary;
  tests: TestResult[];
  stdout?: string;
  stderr?: string;
  execution_time_ms: number;
  all_tests_passed?: boolean;
  next_steps?: string[];
  suggested_hints?: HintSuggestion[];
}

export interface HintSuggestion {
  hint_index: number;
  reason: string;
  confidence: string;
}

export interface VerificationPanelProps {
  verification: VerificationData | null;
  isLoading?: boolean;
  onRetry?: () => void;
  onGetHelp?: (hintIndex: number) => void;
  className?: string;
  code?: string;
  problemSlug?: string;
  onHighlightLines?: (lines: number[]) => void;
}

export function VerificationPanel({
  verification,
  isLoading = false,
  onRetry,
  onGetHelp,
  className,
  code,
  problemSlug,
  onHighlightLines,
}: VerificationPanelProps) {
  const [showOutput, setShowOutput] = useState(false);
  const [expandedTests, setExpandedTests] = useState<Set<string>>(new Set());
  
  const { explainError } = useAIHints({
    problemSlug: problemSlug || '',
    code: code || '',
  });

  if (isLoading) {
    return (
      <Card className={cn("border-dashed", className)}>
        <CardContent className="p-8">
          <div className="flex flex-col items-center justify-center space-y-4">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
            <p className="text-muted-foreground">Running tests...</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!verification) {
    return (
      <Card className={cn("border-dashed", className)}>
        <CardContent className="p-8">
          <div className="flex flex-col items-center justify-center space-y-4 text-center">
            <div className="p-3 rounded-full bg-muted">
              <Play className="h-6 w-6 text-muted-foreground" />
            </div>
            <div>
              <p className="font-medium">Run your code to see results</p>
              <p className="text-sm text-muted-foreground mt-1">
                Click the Run button to execute tests against your solution
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  const { summary, tests, all_tests_passed, next_steps, suggested_hints } = verification;
  const passRate = summary.total > 0 ? (summary.passed / summary.total) * 100 : 0;
  const hasFailures = summary.failed > 0 || summary.errors > 0;

  const toggleTestExpand = (testName: string) => {
    const newExpanded = new Set(expandedTests);
    if (newExpanded.has(testName)) {
      newExpanded.delete(testName);
    } else {
      newExpanded.add(testName);
    }
    setExpandedTests(newExpanded);
  };

  return (
    <Card className={className}>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            {all_tests_passed ? (
              <div className="p-2 rounded-full bg-green-100 dark:bg-green-900/30">
                <Trophy className="h-5 w-5 text-green-600 dark:text-green-400" />
              </div>
            ) : hasFailures ? (
              <div className="p-2 rounded-full bg-red-100 dark:bg-red-900/30">
                <XCircle className="h-5 w-5 text-red-600 dark:text-red-400" />
              </div>
            ) : (
              <div className="p-2 rounded-full bg-yellow-100 dark:bg-yellow-900/30">
                <AlertCircle className="h-5 w-5 text-yellow-600 dark:text-yellow-400" />
              </div>
            )}
            <div>
              <CardTitle className="text-base">
                {all_tests_passed
                  ? "All Tests Passed! 🎉"
                  : `${summary.passed}/${summary.total} Tests Passed`}
              </CardTitle>
              <div className="flex items-center gap-2 text-sm text-muted-foreground mt-0.5">
                <Clock className="h-3.5 w-3.5" />
                <span>{verification.execution_time_ms.toFixed(0)}ms</span>
              </div>
            </div>
          </div>
          <Badge
            variant={all_tests_passed ? "default" : hasFailures ? "destructive" : "secondary"}
            className="font-medium"
          >
            {passRate.toFixed(0)}%
          </Badge>
        </div>
        <Progress value={passRate} className="h-2 mt-3" />
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Test Results */}
        <div className="space-y-2">
          {tests.map((test, index) => (
            <TestResultItem
              key={`${test.name}-${index}`}
              test={test}
              isExpanded={expandedTests.has(test.name)}
              onToggle={() => toggleTestExpand(test.name)}
              testNumber={index + 1}
              code={code}
              problemSlug={problemSlug}
              onExplainError={explainError}
            />
          ))}
        </div>

        {/* Failure Explanation */}
        {hasFailures && (
          <FailureExplanation
            failedTests={tests.filter((t) => t.status === "failed" || t.status === "error")}
            suggestedHints={suggested_hints}
            onGetHelp={onGetHelp}
          />
        )}

        {/* Next Steps */}
        {next_steps && next_steps.length > 0 && (
          <div className="bg-muted/50 rounded-lg p-4">
            <h4 className="text-sm font-medium mb-2">Next Steps</h4>
            <ul className="space-y-1.5">
              {next_steps.map((step, index) => (
                <li key={index} className="text-sm text-muted-foreground flex items-start gap-2">
                  <span className="text-primary mt-0.5">•</span>
                  {step}
                </li>
              ))}
            </ul>
          </div>
        )}

        <Separator />

        {/* Console Output */}
        <div>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setShowOutput(!showOutput)}
            className="w-full justify-between"
          >
            <div className="flex items-center gap-2">
              <Terminal className="h-4 w-4" />
              <span>Console Output</span>
            </div>
            {showOutput ? (
              <ChevronUp className="h-4 w-4" />
            ) : (
              <ChevronDown className="h-4 w-4" />
            )}
          </Button>
          
          {showOutput && (
            <div className="mt-2 space-y-2">
              {verification.stdout && (
                <div className="bg-muted rounded-lg p-3">
                  <p className="text-xs font-medium text-muted-foreground mb-1">stdout</p>
                  <pre className="text-xs font-mono text-foreground whitespace-pre-wrap">
                    {verification.stdout}
                  </pre>
                </div>
              )}
              {verification.stderr && (
                <div className="bg-red-50 dark:bg-red-900/20 rounded-lg p-3">
                  <p className="text-xs font-medium text-red-600 dark:text-red-400 mb-1">stderr</p>
                  <pre className="text-xs font-mono text-red-700 dark:text-red-300 whitespace-pre-wrap">
                    {verification.stderr}
                  </pre>
                  {problemSlug && code && (
                    <div className="mt-3 pt-3 border-t border-red-200 dark:border-red-800">
                      <ErrorExplainer
                        errorMessage={verification.stderr}
                        code={code}
                        problemSlug={problemSlug}
                        onExplain={() => explainError(verification.stderr || '')}
                        onHighlightLines={onHighlightLines}
                      />
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Action Buttons */}
        <div className="flex gap-2">
          {hasFailures && onRetry && (
            <Button variant="outline" onClick={onRetry} className="flex-1 gap-2">
              <RotateCcw className="h-4 w-4" />
              Try Again
            </Button>
          )}
          {hasFailures && onGetHelp && suggested_hints && suggested_hints.length > 0 && (
            <Button
              variant="secondary"
              onClick={() => onGetHelp(suggested_hints[0].hint_index)}
              className="flex-1 gap-2"
            >
              <Lightbulb className="h-4 w-4" />
              Get Help
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
