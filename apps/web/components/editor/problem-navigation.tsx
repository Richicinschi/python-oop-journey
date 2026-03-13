'use client';

import { Button } from '@/components/ui/button';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import Link from 'next/link';
import { Problem } from '@/types/curriculum';

interface ProblemNavigationProps {
  currentProblem: Problem;
  prevProblem: Problem | null;
  nextProblem: Problem | null;
  weekSlug: string;
  daySlug: string;
}

export function ProblemNavigation({
  currentProblem,
  prevProblem,
  nextProblem,
  weekSlug,
  daySlug,
}: ProblemNavigationProps) {
  return (
    <div className="flex items-center justify-between p-4 border-t bg-card">
      <div className="flex items-center gap-2">
        {prevProblem ? (
          <Link
            href={`/problems/${weekSlug}/${daySlug}/${prevProblem.slug}`}
          >
            <Button variant="outline" className="gap-2">
              <ChevronLeft className="h-4 w-4" />
              Previous
            </Button>
          </Link>
        ) : (
          <Button variant="outline" disabled className="gap-2">
            <ChevronLeft className="h-4 w-4" />
            Previous
          </Button>
        )}

        <Link href={`/weeks/${weekSlug}/days/${daySlug}`}>
          <Button variant="ghost" className="text-muted-foreground">
            Back to Day
          </Button>
        </Link>
      </div>

      <div className="text-sm text-muted-foreground">
        Problem {currentProblem.order}
      </div>

      <div className="flex items-center gap-2">
        {nextProblem ? (
          <Link
            href={`/problems/${weekSlug}/${daySlug}/${nextProblem.slug}`}
          >
            <Button variant="outline" className="gap-2">
              Next
              <ChevronRight className="h-4 w-4" />
            </Button>
          </Link>
        ) : (
          <Button variant="outline" disabled className="gap-2">
            Next
            <ChevronRight className="h-4 w-4" />
          </Button>
        )}
      </div>
    </div>
  );
}
