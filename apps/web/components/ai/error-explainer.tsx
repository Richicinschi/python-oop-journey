'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible';
import { cn } from '@/lib/utils';
import { AlertCircle, ChevronDown, ChevronUp, Sparkles, Wand2, XCircle } from 'lucide-react';

interface ErrorExplainerProps {
  errorMessage: string;
  code: string;
  problemSlug?: string;
  onExplain?: () => Promise<ErrorExplanation>;
  onHighlightLines?: (lines: number[]) => void;
}

interface ErrorExplanation {
  explanation: string;
  suggestion: string;
  relevantLines: number[];
}

export function ErrorExplainer({
  errorMessage,
  code,
  problemSlug,
  onExplain,
  onHighlightLines,
}: ErrorExplainerProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [explanation, setExplanation] = useState<ErrorExplanation | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleExplain = async () => {
    if (!onExplain) return;

    setIsLoading(true);
    setError(null);

    try {
      const result = await onExplain();
      setExplanation(result);
      setIsOpen(true);
    } catch (err) {
      setError('Failed to explain error. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleLineClick = (line: number) => {
    onHighlightLines?.([line]);
  };

  // Extract line number from error message
  const extractErrorLine = (message: string): number | null => {
    // Common patterns: "line 15", "line 15,", "(line 15)"
    const patterns = [
      /line\s+(\d+)/i,
      /,\s+(\d+)[,:]/,
      /\((\d+),\s*\d+\)/,
    ];

    for (const pattern of patterns) {
      const match = message.match(pattern);
      if (match) {
        return parseInt(match[1], 10);
      }
    }

    return null;
  };

  const errorLine = extractErrorLine(errorMessage);
  const errorType = errorMessage.split(':')[0] || 'Error';
  const errorDetails = errorMessage.split(':').slice(1).join(':').trim();

  // Categorize error type
  const getErrorCategory = (type: string): { label: string; color: string } => {
    const lower = type.toLowerCase();
    if (lower.includes('syntax')) {
      return { label: 'Syntax Error', color: 'text-red-500 bg-red-50 border-red-200' };
    }
    if (lower.includes('name') || lower.includes('import')) {
      return { label: 'Name/Import Error', color: 'text-orange-500 bg-orange-50 border-orange-200' };
    }
    if (lower.includes('type') || lower.includes('attribute')) {
      return { label: 'Type Error', color: 'text-amber-500 bg-amber-50 border-amber-200' };
    }
    if (lower.includes('value') || lower.includes('key')) {
      return { label: 'Value Error', color: 'text-yellow-500 bg-yellow-50 border-yellow-200' };
    }
    if (lower.includes('index') || lower.includes('range')) {
      return { label: 'Index Error', color: 'text-purple-500 bg-purple-50 border-purple-200' };
    }
    if (lower.includes('assert') || lower.includes('test')) {
      return { label: 'Test Failure', color: 'text-blue-500 bg-blue-50 border-blue-200' };
    }
    return { label: 'Runtime Error', color: 'text-red-500 bg-red-50 border-red-200' };
  };

  const category = getErrorCategory(errorType);

  return (
    <div className="space-y-3">
      {/* Error Display */}
      <Card className={cn('border-l-4', category.color)}>
        <CardHeader className="pb-2">
          <CardTitle className="flex items-center gap-2 text-sm">
            <XCircle className="h-4 w-4" />
            <span>{category.label}</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="font-mono text-xs bg-black/5 p-3 rounded overflow-x-auto">
            {errorDetails || errorMessage}
          </div>

          {errorLine && (
            <button
              onClick={() => handleLineClick(errorLine)}
              className="text-xs text-muted-foreground hover:text-primary flex items-center gap-1"
            >
              <AlertCircle className="h-3 w-3" />
              Jump to line {errorLine}
            </button>
          )}

          {/* Explain Button */}
          {!explanation && !isLoading && (
            <Button
              variant="outline"
              size="sm"
              className="w-full gap-2 text-xs border-primary/30 hover:bg-primary/10"
              onClick={handleExplain}
            >
              <Wand2 className="h-3.5 w-3.5" />
              Explain this error
            </Button>
          )}

          {isLoading && (
            <Button
              variant="outline"
              size="sm"
              className="w-full gap-2 text-xs"
              disabled
            >
              <div className="h-3 w-3 rounded-full border-2 border-primary border-t-transparent animate-spin" />
              Analyzing error...
            </Button>
          )}

          {error && (
            <p className="text-xs text-red-500">{error}</p>
          )}
        </CardContent>
      </Card>

      {/* AI Explanation */}
      {explanation && (
        <Collapsible open={isOpen} onOpenChange={setIsOpen}>
          <Card className="border-primary/20 bg-primary/5">
            <CollapsibleTrigger asChild>
              <CardHeader className="pb-3 cursor-pointer">
                <CardTitle className="flex items-center justify-between text-sm">
                  <div className="flex items-center gap-2">
                    <Sparkles className="h-4 w-4 text-primary" />
                    <span>AI Explanation</span>
                  </div>
                  {isOpen ? (
                    <ChevronUp className="h-4 w-4 text-muted-foreground" />
                  ) : (
                    <ChevronDown className="h-4 w-4 text-muted-foreground" />
                  )}
                </CardTitle>
              </CardHeader>
            </CollapsibleTrigger>

            <CollapsibleContent>
              <CardContent className="space-y-4 pt-0">
                {/* What's happening */}
                <div className="space-y-1">
                  <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
                    What&apos;s happening
                  </h4>
                  <p className="text-sm leading-relaxed">{explanation.explanation}</p>
                </div>

                {/* How to fix it */}
                {explanation.suggestion && (
                  <div className="space-y-1">
                    <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
                      How to fix it
                    </h4>
                    <p className="text-sm leading-relaxed">{explanation.suggestion}</p>
                  </div>
                )}

                {/* Relevant lines */}
                {explanation.relevantLines.length > 0 && (
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="text-xs text-muted-foreground">Check lines:</span>
                    {explanation.relevantLines.map((line) => (
                      <button
                        key={line}
                        onClick={() => handleLineClick(line)}
                        className="text-xs px-2 py-0.5 bg-background border rounded hover:bg-primary/10 transition-colors"
                      >
                        {line}
                      </button>
                    ))}
                  </div>
                )}

                {/* Regenerate button */}
                <Button
                  variant="ghost"
                  size="sm"
                  className="w-full text-xs text-muted-foreground hover:text-primary"
                  onClick={handleExplain}
                >
                  Get another explanation
                </Button>
              </CardContent>
            </CollapsibleContent>
          </Card>
        </Collapsible>
      )}
    </div>
  );
}

// Compact inline version for test results
export function InlineErrorExplainer({
  errorMessage,
  onExplain,
}: {
  errorMessage: string;
  onExplain?: () => Promise<ErrorExplanation>;
}) {
  const [isLoading, setIsLoading] = useState(false);
  const [explanation, setExplanation] = useState<ErrorExplanation | null>(null);
  const [showExplanation, setShowExplanation] = useState(false);

  const handleExplain = async () => {
    if (!onExplain || explanation) {
      setShowExplanation(!showExplanation);
      return;
    }

    setIsLoading(true);
    try {
      const result = await onExplain();
      setExplanation(result);
      setShowExplanation(true);
    } catch {
      // Silently fail for inline version
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-2">
      <Button
        variant="ghost"
        size="sm"
        className="h-6 gap-1 text-xs text-muted-foreground hover:text-primary"
        onClick={handleExplain}
        disabled={isLoading}
      >
        {isLoading ? (
          <div className="h-3 w-3 rounded-full border-2 border-primary border-t-transparent animate-spin" />
        ) : (
          <Sparkles className="h-3 w-3" />
        )}
        {explanation ? (showExplanation ? 'Hide' : 'Show') : 'Explain'} error
      </Button>

      {showExplanation && explanation && (
        <div className="text-xs text-muted-foreground bg-muted p-2 rounded">
          <p className="font-medium text-foreground mb-1">{explanation.explanation}</p>
          {explanation.suggestion && (
            <p className="text-muted-foreground">{explanation.suggestion}</p>
          )}
        </div>
      )}
    </div>
  );
}
