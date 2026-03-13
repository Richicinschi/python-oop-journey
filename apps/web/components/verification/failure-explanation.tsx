"use client";

import { Lightbulb, AlertTriangle, Target } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import type { TestResult, HintSuggestion } from "./verification-panel";

interface FailureExplanationProps {
  failedTests: TestResult[];
  suggestedHints?: HintSuggestion[];
  onGetHelp?: (hintIndex: number) => void;
}

// Map error categories to learner-friendly explanations
const errorExplanations: Record<string, { title: string; explanation: string; tip: string }> = {
  wrong_return_value: {
    title: "Wrong Return Value",
    explanation: "Your function returned a different value than expected.",
    tip: "Double-check your logic, calculations, and make sure you're returning the correct value.",
  },
  unexpected_exception: {
    title: "Unexpected Error",
    explanation: "Your code raised an exception that wasn't expected.",
    tip: "Check for edge cases like empty inputs, None values, or invalid types.",
  },
  missing_implementation: {
    title: "Not Implemented",
    explanation: "You need to implement this function to make the tests pass.",
    tip: "Remove 'raise NotImplementedError' and write your solution.",
  },
  timeout: {
    title: "Timeout",
    explanation: "Your code took too long to execute.",
    tip: "Check for infinite loops or very slow operations. Make sure your solution is efficient.",
  },
  syntax_error: {
    title: "Syntax Error",
    explanation: "There's a syntax error in your code.",
    tip: "Check for missing colons, parentheses, quotes, or incorrect indentation.",
  },
  import_error: {
    title: "Import Error",
    explanation: "There was a problem importing modules.",
    tip: "Make sure all module names are spelled correctly and the modules exist.",
  },
  assertion_error: {
    title: "Assertion Failed",
    explanation: "A test assertion failed.",
    tip: "Review the test requirements and make sure your code meets all conditions.",
  },
  unknown_error: {
    title: "Unknown Error",
    explanation: "Something unexpected happened.",
    tip: "Try running your code locally to debug the issue.",
  },
};

// Get common error patterns from test names
function getErrorPatternFromTestName(testName: string): string | null {
  const name = testName.toLowerCase();
  
  if (name.includes("empty") || name.includes("none")) {
    return "Make sure to handle empty or None inputs";
  }
  if (name.includes("negative") || name.includes("zero")) {
    return "Check how you handle edge cases like negative numbers or zero";
  }
  if (name.includes("type") || name.includes("invalid")) {
    return "Ensure your function handles different input types correctly";
  }
  if (name.includes("large") || name.includes("performance")) {
    return "Your solution might be too slow for large inputs";
  }
  
  return null;
}

export function FailureExplanation({
  failedTests,
  suggestedHints,
  onGetHelp,
}: FailureExplanationProps) {
  // Count error categories
  const categoryCounts: Record<string, number> = {};
  failedTests.forEach((test) => {
    const category = test.error_category || "unknown_error";
    categoryCounts[category] = (categoryCounts[category] || 0) + 1;
  });

  // Get the most common error category
  const mostCommonCategory = Object.entries(categoryCounts).sort(
    (a, b) => b[1] - a[1]
  )[0]?.[0];

  const errorInfo = mostCommonCategory
    ? errorExplanations[mostCommonCategory] || errorExplanations.unknown_error
    : null;

  // Get specific test patterns
  const testPatterns = failedTests
    .map((t) => getErrorPatternFromTestName(t.name))
    .filter(Boolean);
  
  const uniquePatterns = [...new Set(testPatterns)].slice(0, 2);

  return (
    <Card className="border-orange-200 dark:border-orange-800 bg-orange-50/50 dark:bg-orange-900/10">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm flex items-center gap-2">
          <AlertTriangle className="h-4 w-4 text-orange-600 dark:text-orange-400" />
          Understanding the Failures
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Main Error Explanation */}
        {errorInfo && (
          <div className="space-y-2">
            <div className="flex items-start gap-2">
              <Target className="h-4 w-4 text-orange-600 dark:text-orange-400 mt-0.5 shrink-0" />
              <div>
                <p className="text-sm font-medium text-foreground">
                  {errorInfo.title}
                </p>
                <p className="text-sm text-muted-foreground">
                  {errorInfo.explanation}
                </p>
              </div>
            </div>
            <div className="bg-background/80 rounded p-3 text-sm">
              <span className="font-medium text-orange-700 dark:text-orange-400">
                Tip:
              </span>{" "}
              {errorInfo.tip}
            </div>
          </div>
        )}

        {/* Specific Patterns */}
        {uniquePatterns.length > 0 && (
          <div className="space-y-2">
            <p className="text-sm font-medium">Common Issues in Failed Tests:</p>
            <ul className="space-y-1">
              {uniquePatterns.map((pattern, index) => (
                <li
                  key={index}
                  className="text-sm text-muted-foreground flex items-start gap-2"
                >
                  <span className="text-orange-600 dark:text-orange-400">•</span>
                  {pattern}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Hint Suggestions */}
        {suggestedHints && suggestedHints.length > 0 && (
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <Lightbulb className="h-4 w-4 text-yellow-600 dark:text-yellow-400" />
              <p className="text-sm font-medium">Suggested Help</p>
            </div>
            <div className="space-y-2">
              {suggestedHints.slice(0, 2).map((hint, index) => (
                <div
                  key={index}
                  className="bg-background/80 rounded p-2 text-sm flex items-center justify-between"
                >
                  <div>
                    <span className="font-medium">Hint {hint.hint_index + 1}</span>
                    <span className="text-muted-foreground">
                      {" "}
                      — {hint.reason}
                    </span>
                    <span
                      className={cn(
                        "ml-2 text-xs px-1.5 py-0.5 rounded",
                        hint.confidence === "high"
                          ? "bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300"
                          : "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/40 dark:text-yellow-300"
                      )}
                    >
                      {hint.confidence} confidence
                    </span>
                  </div>
                </div>
              ))}
            </div>
            {onGetHelp && suggestedHints[0] && (
              <Button
                variant="secondary"
                size="sm"
                onClick={() => onGetHelp(suggestedHints[0].hint_index)}
                className="w-full gap-2"
              >
                <Lightbulb className="h-4 w-4" />
                View Suggested Hint
              </Button>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

