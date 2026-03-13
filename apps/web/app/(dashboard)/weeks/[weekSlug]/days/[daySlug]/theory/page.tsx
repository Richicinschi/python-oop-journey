import { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { TheoryContent } from '@/components/curriculum/theory-content';
import { TableOfContents } from '@/components/curriculum/table-of-contents';
import { 
  getWeekBySlug, 
  getDayBySlug,
  getWeeks,
  formatWeekNumber,
  formatDayNumber,
  getDayProgress
} from '@/lib/curriculum-loader';
import { 
  BookOpen, 
  ChevronLeft, 
  ChevronRight, 
  FileText,
  Play,
  Clock,
  Target,
  CheckCircle2
} from 'lucide-react';

interface TheoryPageProps {
  params: {
    weekSlug: string;
    daySlug: string;
  };
}

export async function generateStaticParams() {
  const weeks = getWeeks();
  const params: { weekSlug: string; daySlug: string }[] = [];
  
  for (const week of weeks) {
    for (const day of week.days) {
      params.push({
        weekSlug: week.slug,
        daySlug: day.slug,
      });
    }
  }
  
  return params;
}

export async function generateMetadata({ params }: TheoryPageProps): Promise<Metadata> {
  const day = getDayBySlug(params.weekSlug, params.daySlug);
  if (!day) {
    return { title: 'Theory Not Found' };
  }
  return {
    title: `Theory: ${day.title} | Python OOP Journey`,
  };
}

export default function TheoryPage({ params }: TheoryPageProps) {
  const week = getWeekBySlug(params.weekSlug);
  const day = getDayBySlug(params.weekSlug, params.daySlug);

  if (!week || !day) {
    notFound();
  }

  const hasTheory = day.theory_content && day.theory_content.length > 0;
  const progress = getDayProgress(day);
  
  // Navigation
  const currentDayIndex = week.days.findIndex(d => d.slug === day.slug);
  const prevDay = currentDayIndex > 0 ? week.days[currentDayIndex - 1] : null;
  const nextDay = currentDayIndex < week.days.length - 1 ? week.days[currentDayIndex + 1] : null;

  // Find theory navigation (previous/next day with theory)
  const findTheoryNav = () => {
    let prev = prevDay;
    while (prev && !prev.theory_content) {
      const idx = week.days.findIndex(d => d.slug === prev!.slug);
      prev = idx > 0 ? week.days[idx - 1] : null;
    }
    
    let next = nextDay;
    while (next && !next.theory_content) {
      const idx = week.days.findIndex(d => d.slug === next!.slug);
      next = idx < week.days.length - 1 ? week.days[idx + 1] : null;
    }
    
    return { prev, next };
  };
  
  const { prev: prevTheory, next: nextTheory } = findTheoryNav();

  if (!hasTheory) {
    return (
      <div className="space-y-6">
        <nav className="flex items-center gap-2 text-sm text-muted-foreground">
          <Link href="/weeks" className="hover:text-foreground">Curriculum</Link>
          <ChevronRight className="h-4 w-4" />
          <Link href={`/weeks/${week.slug}`} className="hover:text-foreground">
            {formatWeekNumber(week.order)}
          </Link>
          <ChevronRight className="h-4 w-4" />
          <Link href={`/weeks/${week.slug}/days/${day.slug}`} className="hover:text-foreground">
            {formatDayNumber(day.order)}
          </Link>
          <ChevronRight className="h-4 w-4" />
          <span className="text-foreground">Theory</span>
        </nav>

        <Card className="border-dashed">
          <CardContent className="py-16 text-center">
            <FileText className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <h1 className="text-xl font-semibold mb-2">No Theory Content</h1>
            <p className="text-muted-foreground mb-6">
              This day doesn&apos;t have theory content yet.
            </p>
            <Link href={`/weeks/${week.slug}/days/${day.slug}`}>
              <Button>
                <ChevronLeft className="mr-2 h-4 w-4" />
                Back to Day
              </Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    );
  }

  // Estimate reading time (rough estimate: 200 words per minute)
  const wordCount = day.theory_content.split(/\s+/).length;
  const readingTime = Math.ceil(wordCount / 200);

  return (
    <div className="space-y-6">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-2 text-sm text-muted-foreground">
        <Link href="/weeks" className="hover:text-foreground transition-colors">
          Curriculum
        </Link>
        <ChevronRight className="h-4 w-4" />
        <Link href={`/weeks/${week.slug}`} className="hover:text-foreground transition-colors">
          {formatWeekNumber(week.order)}
        </Link>
        <ChevronRight className="h-4 w-4" />
        <Link href={`/weeks/${week.slug}/days/${day.slug}`} className="hover:text-foreground transition-colors">
          {formatDayNumber(day.order)}
        </Link>
        <ChevronRight className="h-4 w-4" />
        <span className="text-foreground font-medium">Theory</span>
      </nav>

      {/* Header */}
      <div className="space-y-4">
        <div className="flex items-start gap-4">
          <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-xl bg-primary/10 text-primary">
            <FileText className="h-7 w-7" />
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1 flex-wrap">
              <Badge variant="secondary" className="font-mono">
                {formatWeekNumber(week.order)}
              </Badge>
              <Badge variant="outline" className="font-mono">
                {formatDayNumber(day.order)}
              </Badge>
              <Badge variant="outline" className="bg-blue-500/10 text-blue-600 border-blue-500/20">
                <Clock className="mr-1 h-3 w-3" />
                {readingTime} min read
              </Badge>
            </div>
            <h1 className="text-3xl font-bold tracking-tight">
              {day.title.replace(`Day ${day.order}: `, '')}
            </h1>
            <p className="text-muted-foreground mt-1">
              Theory and concepts for this day
            </p>
          </div>
        </div>
      </div>

      <Separator />

      {/* Content Layout */}
      <div className="flex gap-8">
        {/* Main Content */}
        <div className="flex-1 min-w-0">
          <TheoryContent content={day.theory_content} />

          {/* Learning Objectives Section */}
          {day.learning_objectives && day.learning_objectives.length > 0 && (
            <>
              <Separator className="my-8" />
              <div className="bg-muted/50 rounded-lg p-6">
                <div className="flex items-center gap-2 mb-4">
                  <Target className="h-5 w-5 text-primary" />
                  <h2 className="font-semibold text-lg">Learning Objectives</h2>
                </div>
                <ul className="space-y-2">
                  {day.learning_objectives.map((objective, index) => (
                    <li key={index} className="flex items-start gap-3">
                      <CheckCircle2 className="h-5 w-5 text-green-500 shrink-0 mt-0.5" />
                      <span>{objective}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </>
          )}

          {/* CTA Section */}
          <Separator className="my-8" />
          <Card className="bg-gradient-to-br from-primary/5 to-primary/10 border-primary/20">
            <CardContent className="py-8 px-6">
              <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
                <div className="text-center sm:text-left">
                  <h3 className="font-semibold text-lg">Ready to practice?</h3>
                  <p className="text-muted-foreground text-sm">
                    Apply what you&apos;ve learned with {day.problems.length} coding exercises
                  </p>
                </div>
                <div className="flex gap-2">
                  <Link href={`/weeks/${week.slug}/days/${day.slug}`}>
                    <Button variant="outline">
                      <ChevronLeft className="mr-2 h-4 w-4" />
                      Back to Day
                    </Button>
                  </Link>
                  {day.problems.length > 0 && (
                    <Link href={`/problems/${day.problems[0].slug}`}>
                      <Button>
                        <Play className="mr-2 h-4 w-4" />
                        Start Exercises
                      </Button>
                    </Link>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Navigation Footer */}
          <div className="flex items-center justify-between mt-8 pt-4 border-t">
            {prevTheory ? (
              <Link href={`/weeks/${week.slug}/days/${prevTheory.slug}/theory`}>
                <Button variant="outline">
                  <ChevronLeft className="mr-2 h-4 w-4" />
                  Previous: {prevTheory.title.replace(`Day ${prevTheory.order}: `, '')}
                </Button>
              </Link>
            ) : (
              <div />
            )}
            {nextTheory ? (
              <Link href={`/weeks/${week.slug}/days/${nextTheory.slug}/theory`}>
                <Button variant="outline">
                  Next: {nextTheory.title.replace(`Day ${nextTheory.order}: `, '')}
                  <ChevronRight className="ml-2 h-4 w-4" />
                </Button>
              </Link>
            ) : (
              <div />
            )}
          </div>
        </div>

        {/* Table of Contents Sidebar */}
        <TableOfContents content={day.theory_content} />
      </div>
    </div>
  );
}
