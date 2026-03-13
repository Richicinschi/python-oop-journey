'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { cn } from '@/lib/utils';
import {
  Check,
  Copy,
  Lightbulb,
  ThumbsDown,
  ThumbsUp,
  X,
} from 'lucide-react';

interface AIHintProps {
  hint: string;
  relevantLines: number[];
  explanation: string;
  hintLevel: number;
  onClose?: () => void;
  onFeedback?: (wasHelpful: boolean) => void;
  onRequestAnother?: () => void;
  onHighlightLines?: (lines: number[]) => void;
  isLoading?: boolean;
}

export function AIHintCard({
  hint,
  relevantLines,
  explanation,
  hintLevel,
  onClose,
  onFeedback,
  onRequestAnother,
  onHighlightLines,
  isLoading = false,
}: AIHintProps) {
  const [copied, setCopied] = useState(false);
  const [feedbackGiven, setFeedbackGiven] = useState<boolean | null>(null);

  const getLevelLabel = (level: number) => {
    switch (level) {
      case 1:
        return 'Conceptual Nudge';
      case 2:
        return 'Structural Guidance';
      case 3:
        return 'Specific Suggestion';
      default:
        return 'AI Hint';
    }
  };

  const getLevelColor = (level: number) => {
    switch (level) {
      case 1:
        return 'text-blue-500 border-blue-200 bg-blue-50';
      case 2:
        return 'text-amber-500 border-amber-200 bg-amber-50';
      case 3:
        return 'text-orange-500 border-orange-200 bg-orange-50';
      default:
        return 'text-muted-foreground';
    }
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(hint);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Ignore copy errors
    }
  };

  const handleFeedback = (wasHelpful: boolean) => {
    setFeedbackGiven(wasHelpful);
    onFeedback?.(wasHelpful);
  };

  const handleLineClick = (line: number) => {
    onHighlightLines?.([line]);
  };

  // Parse hint text to highlight code references
  const renderHintWithLineReferences = (text: string) => {
    // Match patterns like "line 15", "line #15", "on line 15"
    const lineRegex = /(line\s+#?(\d+))/gi;
    const parts = text.split(lineRegex);

    return parts.map((part, index) => {
      // Check if this part matches the line number pattern
      const match = part.match(/line\s+#?(\d+)/i);
      if (match) {
        const lineNum = parseInt(match[1], 10);
        return (
          <button
            key={index}
            onClick={() => handleLineClick(lineNum)}
            className="inline-flex items-center gap-1 px-1.5 py-0.5 text-xs font-medium bg-primary/10 text-primary rounded hover:bg-primary/20 transition-colors cursor-pointer"
            title={`Click to highlight line ${lineNum}`}
          >
            {part}
          </button>
        );
      }
      return <span key={index}>{part}</span>;
    });
  };

  if (isLoading) {
    return (
      <Card className="border-primary/20">
        <CardHeader className="pb-3">
          <CardTitle className="flex items-center gap-2 text-sm font-medium">
            <div className="h-4 w-4 rounded-full border-2 border-primary border-t-transparent animate-spin" />
            Generating AI Hint...
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <div className="h-4 bg-muted rounded animate-pulse w-3/4" />
            <div className="h-4 bg-muted rounded animate-pulse w-full" />
            <div className="h-4 bg-muted rounded animate-pulse w-5/6" />
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={cn('border-2', getLevelColor(hintLevel))}>
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-2">
          <CardTitle className="flex items-center gap-2 text-sm font-medium">
            <Lightbulb className="h-4 w-4" />
            <span>AI Hint: {getLevelLabel(hintLevel)}</span>
          </CardTitle>
          {onClose && (
            <Button
              variant="ghost"
              size="icon"
              className="h-6 w-6 -mr-2 -mt-2"
              onClick={onClose}
            >
              <X className="h-4 w-4" />
            </Button>
          )}
        </div>
        {explanation && (
          <p className="text-xs text-muted-foreground">{explanation}</p>
        )}
      </CardHeader>

      <CardContent className="space-y-4">
        <div className="text-sm leading-relaxed">
          {renderHintWithLineReferences(hint)}
        </div>

        {relevantLines.length > 0 && (
          <div className="flex flex-wrap gap-2">
            <span className="text-xs text-muted-foreground">Relevant lines:</span>
            {relevantLines.map((line) => (
              <button
                key={line}
                onClick={() => handleLineClick(line)}
                className="text-xs px-2 py-0.5 bg-background border rounded hover:bg-primary/10 transition-colors"
              >
                Line {line}
              </button>
            ))}
          </div>
        )}
      </CardContent>

      <CardFooter className="flex flex-col gap-3 pt-0">
        <div className="flex items-center justify-between w-full">
          <div className="flex items-center gap-2">
            <span className="text-xs text-muted-foreground">Was this helpful?</span>
            <div className="flex gap-1">
              <Button
                variant="ghost"
                size="sm"
                className={cn(
                  'h-7 w-7 p-0',
                  feedbackGiven === true && 'text-green-600 bg-green-50'
                )}
                onClick={() => handleFeedback(true)}
                disabled={feedbackGiven !== null}
              >
                <ThumbsUp className="h-3.5 w-3.5" />
              </Button>
              <Button
                variant="ghost"
                size="sm"
                className={cn(
                  'h-7 w-7 p-0',
                  feedbackGiven === false && 'text-red-600 bg-red-50'
                )}
                onClick={() => handleFeedback(false)}
                disabled={feedbackGiven !== null}
              >
                <ThumbsDown className="h-3.5 w-3.5" />
              </Button>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="sm"
              className="h-7 gap-1 text-xs"
              onClick={handleCopy}
            >
              {copied ? (
                <>
                  <Check className="h-3.5 w-3.5" />
                  Copied
                </>
              ) : (
                <>
                  <Copy className="h-3.5 w-3.5" />
                  Copy
                </>
              )}
            </Button>
          </div>
        </div>

        {onRequestAnother && hintLevel < 3 && (
          <Button
            variant="outline"
            size="sm"
            className="w-full text-xs"
            onClick={onRequestAnother}
          >
            Get More Specific Hint
          </Button>
        )}
      </CardFooter>
    </Card>
  );
}

// Compact version for inline use
export function AIHintBadge({
  onClick,
  isLoading,
}: {
  onClick?: () => void;
  isLoading?: boolean;
}) {
  return (
    <Button
      variant="outline"
      size="sm"
      className="gap-2 text-xs border-primary/30 hover:bg-primary/10"
      onClick={onClick}
      disabled={isLoading}
    >
      {isLoading ? (
        <>
          <div className="h-3 w-3 rounded-full border-2 border-primary border-t-transparent animate-spin" />
          Thinking...
        </>
      ) : (
        <>
          <Lightbulb className="h-3.5 w-3.5 text-yellow-500" />
          Get AI Hint
        </>
      )}
    </Button>
  );
}
