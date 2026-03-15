import { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Progress } from '@/components/ui/progress';
import { 
  getWeekBySlug, 
  getDayBySlug,
  getWeeks,
  formatWeekNumber,
  formatDayNumber,
  getDifficultyColor,
  getDayProgress
} from '@/lib/curriculum-loader';
import { 
  BookOpen, 
  ChevronLeft, 
  ChevronRight, 
  FileText,
  Play,
  CheckCircle2,
  Circle,
  Target,
  Code2,
  Clock,
  Lightbulb,
  ArrowRight
} from 'lucide-react';

interface DayPageProps {
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

export async function generateMetadata({ params }: DayPageProps): Promise<Metadata> {
  const day = getDayBySlug(params.weekSlug, params.daySlug);
  if (!day) {
    return { title: 'Day Not Found' };
  }
  return {
    title: `${day.title} | Python OOP Journey`,
  };
}

export default function DayPage({ params }: DayPageProps) {
  const week = getWeekBySlug(params.weekSlug);
  const day = getDayBySlug(params.weekSlug, params.daySlug);

  if (!week || !day) {
    notFound();
  }

  const progress = getDayProgress(day);
  const hasTheory = day.theory_content && day.theory_content.length > 0;
  const hasObjectives = day.learning_objectives && day.learning_objectives.length > 0;
  
  // Navigation
  const currentDayIndex = week.days.findIndex(d => d.slug === day.slug);
  const prevDay = currentDayIndex > 0 ? week.days[currentDayIndex - 1] : null;
  const nextDay = currentDayIndex < week.days.length - 1 ? week.days[currentDayIndex + 1] : null;

  // Calculate total estimated time (5 min per problem as rough estimate)
  const estimatedMinutes = day.problems.length * 5;

  return (
    <div className="space-y-8">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-2 text-sm text-muted-foreground" aria-label="Breadcrumb">
        <Link href="/weeks" className="hover:text-foreground transition-colors">
          Curriculum
        </Link>
        <ChevronRight className="h-4 w-4" />
        <Link href={`/weeks/${week.slug}`} className="hover:text-foreground transition-colors">
          {formatWeekNumber(week.order)}
        </Link>
        <ChevronRight className="h-4 w-4" />
        <span className="text-foreground font-medium">{formatDayNumber(day.order)}</span>
      </nav>

      {/* Header */}
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
          <div className="flex items-start gap-4">
            <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-xl bg-primary/10 text-primary">
              <BookOpen className="h-7 w-7" />
            </div>
            <div>
              <div className="flex items-center gap-2 mb-1 flex-wrap">
                <Badge variant="secondary" className="font-mono">
                  {formatWeekNumber(week.order)}
                </Badge>
                <Badge variant="outline" className="font-mono">
                  {formatDayNumber(day.order)}
                </Badge>
              </div>
              <h1 className="text-3xl font-bold tracking-tight">
                {day.title.replace(`Day ${day.order}: `, '')}
              </h1>
            </div>
          </div>

          <div className="flex gap-2">
            {prevDay && (
              <Link href={`/weeks/${week.slug}/days/${prevDay.slug}`}>
                <Button variant="outline" size="sm">
                  <ChevronLeft className="mr-1 h-4 w-4" />
                  Previous
                </Button>
              </Link>
            )}
            {nextDay && (
              <Link href={`/weeks/${week.slug}/days/${nextDay.slug}`}>
                <Button variant="outline" size="sm">
                  Next
                  <ChevronRight className="ml-1 h-4 w-4" />
                </Button>
              </Link>
            )}
          </div>
        </div>

        {/* Progress Card */}
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="h-5 w-5 text-muted-foreground" />
                <span className="font-medium">Day Progress</span>
              </div>
              <span className="text-sm text-muted-foreground">
                {day.problems.length} problems • ~{estimatedMinutes} min
              </span>
            </div>
            <Progress value={progress} className="h-3" aria-label="Day progress" />
          </CardContent>
        </Card>

        {/* Theory & Learning Objectives */}
        <div className="grid gap-4 md:grid-cols-2">
          {/* Theory Card */}
          {hasTheory && (
            <Card className="border-primary/20 bg-gradient-to-br from-primary/5 to-primary/10">
              <CardContent className="p-6">
                <div className="flex items-start gap-4">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary">
                    <FileText className="h-5 w-5" />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold mb-1">Theory Content</h3>
                    <p className="text-sm text-muted-foreground mb-4">
                      Learn the concepts before practicing
                    </p>
                    <Link href={`/weeks/${week.slug}/days/${day.slug}/theory`}>
                      <Button variant="secondary" size="sm">
                        <FileText className="mr-2 h-4 w-4" />
                        Read Theory
                      </Button>
                    </Link>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Quick Start Card */}
          {day.problems.length > 0 && (
            <Card className="border-green-500/20 bg-gradient-to-br from-green-500/5 to-green-500/10">
              <CardContent className="p-6">
                <div className="flex items-start gap-4">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-green-500/10 text-green-600">
                    <Play className="h-5 w-5" />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold mb-1">Start Practicing</h3>
                    <p className="text-sm text-muted-foreground mb-4">
                      Jump into the coding exercises
                    </p>
                    <Link href={`/problems/${day.problems[0].slug}`}>
                      <Button size="sm" className="bg-green-600 hover:bg-green-700">
                        <Play className="mr-2 h-4 w-4" />
                        Start First Problem
                      </Button>
                    </Link>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>

      <Separator />

      {/* Learning Objectives */}
      {hasObjectives && (
        <section aria-labelledby="objectives-heading">
          <div className="flex items-center gap-2 mb-4">
            <Target className="h-5 w-5 text-primary" />
            <h2 id="objectives-heading" className="text-xl font-semibold">
              Learning Objectives
            </h2>
          </div>
          <Card>
            <CardContent className="p-6">
              <ul className="space-y-3">
                {day.learning_objectives.map((objective, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary/10 text-primary text-xs font-medium">
                      {index + 1}
                    </div>
                    <span className="text-muted-foreground">{objective}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </section>
      )}

      {/* Problems Section */}
      <section aria-labelledby="problems-heading">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Code2 className="h-5 w-5 text-primary" />
            <h2 id="problems-heading" className="text-xl font-semibold">
              Practice Problems
            </h2>
          </div>
          <span className="text-sm text-muted-foreground">
            {day.problems.length} exercises
          </span>
        </div>

        {day.problems.length > 0 ? (
          <div className="space-y-3">
            {day.problems.map((problem, index) => {
              const difficultyClass = getDifficultyColor(problem.difficulty);
              
              return (
                <Card 
                  key={problem.slug}
                  className="transition-all hover:shadow-sm hover:border-primary/20"
                >
                  <CardContent className="p-5">
                    <div className="flex flex-col sm:flex-row sm:items-center gap-4">
                      {/* Problem Number & Status */}
                      <div className="flex items-center gap-3">
                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-muted font-medium text-sm">
                          {index + 1}
                        </div>
                      </div>

                      {/* Content */}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 flex-wrap mb-1">
                          <h3 className="font-semibold truncate">
                            {problem.title}
                          </h3>
                          <Badge variant="outline" className={`text-xs ${difficultyClass}`}>
                            {problem.difficulty}
                          </Badge>
                        </div>
                        <div className="flex items-center gap-3 text-sm text-muted-foreground">
                          <span className="flex items-center gap-1">
                            <Lightbulb className="h-3.5 w-3.5" />
                            {problem.topic}
                          </span>
                          {problem.hints.length > 0 && (
                            <span className="flex items-center gap-1">
                              <Target className="h-3.5 w-3.5" />
                              {problem.hints.length} hint{problem.hints.length !== 1 ? 's' : ''}
                            </span>
                          )}
                        </div>
                      </div>

                      {/* Action */}
                      <Link href={`/problems/${problem.slug}`}>
                        <Button size="sm">
                          <Play className="mr-2 h-4 w-4" />
                          Solve
                        </Button>
                      </Link>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        ) : (
          <Card className="border-dashed">
            <CardContent className="py-12 text-center">
              <Circle className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-medium mb-2">No Problems Yet</h3>
              <p className="text-muted-foreground">
                This day doesn&apos;t have any practice problems.
              </p>
            </CardContent>
          </Card>
        )}
      </section>

      {/* Navigation Footer */}
      <div className="flex items-center justify-between pt-6 border-t">
        <Link href={`/weeks/${week.slug}`}>
          <Button variant="outline">
            <ChevronLeft className="mr-2 h-4 w-4" />
            Back to {formatWeekNumber(week.order)}
          </Button>
        </Link>
        
        {nextDay ? (
          <Link href={`/weeks/${week.slug}/days/${nextDay.slug}`}>
            <Button>
              Next: {formatDayNumber(nextDay.order)}
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </Link>
        ) : week.days.length > 0 && week.days[week.days.length - 1].slug === day.slug ? (
          // Last day of week - link to project or back to weeks
          <Link href={`/weeks/${week.slug}`}>
            <Button variant="outline">
              Week Complete
              <CheckCircle2 className="ml-2 h-4 w-4 text-green-500" />
            </Button>
          </Link>
        ) : null}
      </div>
    </div>
  );
}
