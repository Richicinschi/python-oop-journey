'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
  CardFooter,
} from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { cn } from '@/lib/utils';
import {
  CheckCircle,
  AlertCircle,
  Lightbulb,
  RefreshCw,
  Sparkles,
  ThumbsUp,
  ThumbsDown,
  X,
  FileCode,
  Check,
} from 'lucide-react';
import { api, CodeReviewResult } from '@/lib/api';

interface CodeReviewPanelProps {
  files: Record<string, string>;
  projectSlug: string;
  rubric?: Array<Record<string, unknown>>;
  onClose?: () => void;
}

export function CodeReviewPanel({
  files,
  projectSlug,
  rubric,
  onClose,
}: CodeReviewPanelProps) {
  const [review, setReview] = useState<CodeReviewResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [feedbackGiven, setFeedbackGiven] = useState<boolean | null>(null);

  const runReview = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await api.ai.reviewCode({
        files,
        projectSlug,
        rubric,
      });
      setReview(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to get code review');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFeedback = (wasHelpful: boolean) => {
    setFeedbackGiven(wasHelpful);
    // Could send feedback to analytics
  };

  // Calculate quality score based on strengths vs improvements
  const calculateScore = () => {
    if (!review) return 0;
    const total = review.strengths.length + review.improvements.length;
    if (total === 0) return 0;
    return Math.round((review.strengths.length / total) * 100);
  };

  if (isLoading) {
    return (
      <Card className="border-primary/20">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-base">
            <div className="h-4 w-4 rounded-full border-2 border-primary border-t-transparent animate-spin" />
            Analyzing your code...
          </CardTitle>
          <CardDescription>
            Our AI is reviewing your code for quality, best practices, and rubric alignment
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <div className="h-4 bg-muted rounded animate-pulse w-3/4" />
            <div className="h-4 bg-muted rounded animate-pulse w-full" />
            <div className="h-4 bg-muted rounded animate-pulse w-5/6" />
            <div className="h-4 bg-muted rounded animate-pulse w-full" />
          </div>
          <div className="flex gap-2">
            <div className="h-20 bg-muted rounded animate-pulse flex-1" />
            <div className="h-20 bg-muted rounded animate-pulse flex-1" />
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="border-red-200 bg-red-50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-base text-red-700">
            <AlertCircle className="h-5 w-5" />
            Review Failed
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-red-600">{error}</p>
          <Button
            variant="outline"
            size="sm"
            className="mt-4"
            onClick={runReview}
          >
            <RefreshCw className="h-4 w-4 mr-2" />
            Try Again
          </Button>
        </CardContent>
      </Card>
    );
  }

  if (!review) {
    return (
      <Card className="border-dashed">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-base">
            <Sparkles className="h-5 w-5 text-primary" />
            AI Code Review
          </CardTitle>
          <CardDescription>
            Get an AI-powered review of your code before submitting for human review
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex flex-wrap gap-2 text-xs text-muted-foreground">
            <span className="flex items-center gap-1">
              <Check className="h-3 w-3" /> Best practices
            </span>
            <span className="flex items-center gap-1">
              <Check className="h-3 w-3" /> Code structure
            </span>
            <span className="flex items-center gap-1">
              <Check className="h-3 w-3" /> Rubric alignment
            </span>
            <span className="flex items-center gap-1">
              <Check className="h-3 w-3" /> Improvement suggestions
            </span>
          </div>
        </CardContent>
        <CardFooter className="flex gap-2">
          <Button onClick={runReview} className="flex-1 gap-2">
            <Sparkles className="h-4 w-4" />
            Start Code Review
          </Button>
          {onClose && (
            <Button variant="ghost" size="icon" onClick={onClose}>
              <X className="h-4 w-4" />
            </Button>
          )}
        </CardFooter>
      </Card>
    );
  }

  const score = calculateScore();

  return (
    <Card className="border-primary/20">
      <CardHeader>
        <div className="flex items-start justify-between gap-2">
          <div>
            <CardTitle className="flex items-center gap-2 text-base">
              <Sparkles className="h-5 w-5 text-primary" />
              AI Code Review Results
            </CardTitle>
            <CardDescription>{review.overall_feedback}</CardDescription>
          </div>
          {onClose && (
            <Button variant="ghost" size="icon" className="h-8 w-8" onClick={onClose}>
              <X className="h-4 w-4" />
            </Button>
          )}
        </div>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Quality Score */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="font-medium">Code Quality Score</span>
            <span className={cn(
              "font-bold",
              score >= 80 ? "text-green-600" : score >= 60 ? "text-amber-600" : "text-red-600"
            )}>
              {score}%
            </span>
          </div>
          <Progress 
            value={score} 
            className={cn(
              "h-2",
              score >= 80 ? "bg-green-100" : score >= 60 ? "bg-amber-100" : "bg-red-100"
            )}
          />
        </div>

        {/* Strengths */}
        {review.strengths.length > 0 && (
          <div className="space-y-2">
            <h4 className="text-sm font-medium flex items-center gap-2 text-green-700">
              <ThumbsUp className="h-4 w-4" />
              Strengths
            </h4>
            <ul className="space-y-2">
              {review.strengths.map((strength, index) => (
                <li
                  key={index}
                  className="flex items-start gap-2 text-sm text-muted-foreground"
                >
                  <CheckCircle className="h-4 w-4 text-green-500 shrink-0 mt-0.5" />
                  <span>{strength}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Improvements */}
        {review.improvements.length > 0 && (
          <div className="space-y-2">
            <h4 className="text-sm font-medium flex items-center gap-2 text-amber-700">
              <Lightbulb className="h-4 w-4" />
              Suggested Improvements
            </h4>
            <ul className="space-y-2">
              {review.improvements.map((improvement, index) => (
                <li
                  key={index}
                  className="flex items-start gap-2 text-sm text-muted-foreground"
                >
                  <AlertCircle className="h-4 w-4 text-amber-500 shrink-0 mt-0.5" />
                  <span>{improvement}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Rubric Assessment */}
        {Object.keys(review.rubric_assessment).length > 0 && (
          <div className="space-y-2">
            <h4 className="text-sm font-medium flex items-center gap-2">
              <FileCode className="h-4 w-4" />
              Rubric Assessment
            </h4>
            <div className="space-y-2">
              {Object.entries(review.rubric_assessment).map(([criterion, assessment]) => (
                <div key={criterion} className="bg-muted/50 rounded p-2">
                  <p className="text-xs font-medium">{criterion}</p>
                  <p className="text-xs text-muted-foreground">{assessment}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Encouragement */}
        {review.encouragement && (
          <div className="bg-primary/5 border border-primary/20 rounded-lg p-3">
            <p className="text-sm text-primary">{review.encouragement}</p>
          </div>
        )}
      </CardContent>

      <CardFooter className="flex flex-col gap-3">
        {/* Feedback */}
        <div className="flex items-center justify-between w-full">
          <span className="text-xs text-muted-foreground">Was this review helpful?</span>
          <div className="flex gap-1">
            <Button
              variant="ghost"
              size="sm"
              className={cn(
                'h-8 w-8 p-0',
                feedbackGiven === true && 'text-green-600 bg-green-50'
              )}
              onClick={() => handleFeedback(true)}
              disabled={feedbackGiven !== null}
            >
              <ThumbsUp className="h-4 w-4" />
            </Button>
            <Button
              variant="ghost"
              size="sm"
              className={cn(
                'h-8 w-8 p-0',
                feedbackGiven === false && 'text-red-600 bg-red-50'
              )}
              onClick={() => handleFeedback(false)}
              disabled={feedbackGiven !== null}
            >
              <ThumbsDown className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {/* Actions */}
        <div className="flex gap-2 w-full">
          <Button variant="outline" size="sm" className="flex-1" onClick={runReview}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Review Again
          </Button>
        </div>
      </CardFooter>
    </Card>
  );
}
