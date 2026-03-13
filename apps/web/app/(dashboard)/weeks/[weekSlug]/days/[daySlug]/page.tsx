import { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Separator } from '@/components/ui/separator';
import { 
  getTransformedWeekBySlug, 
  getTransformedDayBySlug,
  getWeeks,
  getDifficultyColor,
  formatWeekNumber,
  formatDayNumber,
  getDayProgress
} from '@/lib/curriculum-loader';
import { 
  BookOpen, 
  ChevronLeft, 
  ChevronRight, 
  FileText, 
  Target,
  ListChecks,
  Clock,
  Code,
  CheckCircle2,
  Circle,
  AlertCircle,
  Play
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
  const day = getTransformedDayBySlug(params.weekSlug, params.daySlug);
  if (!day) {
    return { title: 'Day Not Found' };
  }
  return {
    title: `${day.title} | Python OOP Journey`,
  };
}

export default function DayPage({ params }: DayPageProps) {
  const week = getTransformedWeekBySlug(params.weekSlug);
  const day = getDayBySlug(params.weekSlug, params.daySlug);

  if (!week || !day) {
    notFound();
  }

  const progress = getDayProgress(day);
  const hasTheory = day.theory_content && day.theory_content.length > 0;
  
  // Navigation
  const currentDayIndex = week.days.findIndex(d => d.slug === day.slug);
  const prevDay = currentDayIndex > 0 ? week.days[currentDayIndex - 1] : null;
  const nextDay = currentDayIndex < week.days.length - 1 ? week.days[currentDayIndex + 1] : null;

  // Calculate difficulty distribution
  const difficultyCount = day.problems.reduce((acc, p) => {
    const diff = p.difficulty.toLowerCase();
    acc[diff] = (acc[diff] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  return (
    <div className="space-y-8">
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
              <div className="flex items-center gap-2 mb-1">
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
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-3">
              <div className="flex items-center gap-2">
                <ListChecks className="h-5 w-5 text-muted-foreground" />
                <span className="font-medium">Day Progress</span>
              </div>
              <div className="flex items-center gap-4 text-sm text-muted-foreground">
                <span className="flex items-center gap-1">
                  <Code className="h-4 w-4" />
                  {day.problems.length} problems
                </span>
                <span className="flex items-center gap-1">
                  <Clock className="h-4 w-4" />
                  ~{day.problems.length * 10} min
                </span>
              </div>
            </div>
            <Progress value={progress} className="h-3" />
          </CardContent>
        </Card>
      </div>

      <Separator />

      {/* Learning Objectives */}
      {day.learning_objectives && day.learning_objectives.length > 0 && (
        <Card className="bg-muted/50 border-dashed">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Target className="h-5 w-5 text-primary" />
              <CardTitle className="text-base">Learning Objectives</CardTitle>
            </div>
            <CardDescription>
              By the end of this day, you will be able to:
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {day.learning_objectives.map((objective, index) => (
                <li key={index} className="flex items-start gap-3">
                  <div className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-primary/10 text-primary text-xs mt-0.5">
                    {index + 1}
                  </div>
                  <span className="text-sm">{objective}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}

      {/* Theory Section */}
      {hasTheory && (
        <Card className="bg-gradient-to-br from-blue-500/5 to-blue-500/10 border-blue-500/20">
          <CardHeader>
            <div className="flex items-center gap-2">
              <FileText className="h-5 w-5 text-blue-500" />
              <CardTitle>Theory & Concepts</CardTitle>
            </div>
            <CardDescription>
              Read the theory before attempting the exercises
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground mb-4">
              Learn the fundamental concepts covered in this day with detailed explanations,
              code examples, and best practices.
            </p>
            <Link href={`/weeks/${week.slug}/days/${day.slug}/theory`}>
              <Button>
                <FileText className="mr-2 h-4 w-4" />
                Read Theory
                <ChevronRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </CardContent>
        </Card>
      )}

      {/* Problems Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold">Problems</h2>
            <p className="text-sm text-muted-foreground">
              Practice with {day.problems.length} coding exercises
            </p>
          </div>
          
          {/* Difficulty Legend */}
          {Object.keys(difficultyCount).length > 0 && (
            <div className="flex items-center gap-2 text-xs">
              {difficultyCount.easy > 0 && (
                <Badge variant="outline" className="bg-green-500/10 text-green-600 border-green-500/20">
                  {difficultyCount.easy} Easy
                </Badge>
              )}
              {difficultyCount.medium > 0 && (
                <Badge variant="outline" className="bg-yellow-500/10 text-yellow-600 border-yellow-500/20">
                  {difficultyCount.medium} Medium
                </Badge>
              )}
              {difficultyCount.hard > 0 && (
                <Badge variant="outline" className="bg-red-500/10 text-red-600 border-red-500/20">
                  {difficultyCount.hard} Hard
                </Badge>
              )}
            </div>
          )}
        </div>

        {day.problems.length === 0 ? (
          <Card className="border-dashed">
            <CardContent className="py-12 text-center">
              <AlertCircle className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">No problems available for this day yet.</p>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-4">
            {day.problems.map((problem, index) => (
              <Card 
                key={problem.slug}
                className="group transition-all hover:shadow-sm"
              >
                <CardContent className="p-5">
                  <div className="flex flex-col sm:flex-row sm:items-center gap-4">
                    {/* Problem Number & Status */}
                    <div className="flex items-center gap-3">
                      <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-muted">
                        {false ? ( // TODO: Check if completed
                          <CheckCircle2 className="h-5 w-5 text-green-500" />
                        ) : (
                          <span className="text-sm font-medium">{problem.order}</span>
                        )}
                      </div>
                    </div>

                    {/* Content */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 flex-wrap">
                        <h3 className="font-semibold group-hover:text-primary transition-colors">
                          {problem.title.replace(`Problem ${problem.order.toString().padStart(2, '0')}: `, '')}
                        </h3>
                        <Badge 
                          variant="outline" 
                          className={`text-xs ${getDifficultyColor(problem.difficulty)}`}
                        >
                          {problem.difficulty}
                        </Badge>
                      </div>
                      <p className="text-sm text-muted-foreground mt-1 line-clamp-2">
                        {problem.topic}
                      </p>
                    </div>

                    {/* Action */}
                    <Link href={`/problems/${problem.slug}`}>
                      <Button size="sm" variant={index === 0 ? 'default' : 'outline'}>
                        <Play className="mr-2 h-4 w-4" />
                        Solve
                      </Button>
                    </Link>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>

      {/* Navigation Footer */}
      <div className="flex items-center justify-between pt-4 border-t">
        <Link href={`/weeks/${week.slug}`}>
          <Button variant="outline">
            <ChevronLeft className="mr-2 h-4 w-4" />
            Back to Week
          </Button>
        </Link>
        
        {hasTheory ? (
          <Link href={`/weeks/${week.slug}/days/${day.slug}/theory`}>
            <Button>
              <FileText className="mr-2 h-4 w-4" />
              Start with Theory
              <ChevronRight className="ml-2 h-4 w-4" />
            </Button>
          </Link>
        ) : day.problems.length > 0 ? (
          <Link href={`/problems/${day.problems[0].slug}`}>
            <Button>
              <Play className="mr-2 h-4 w-4" />
              Start Problems
              <ChevronRight className="ml-2 h-4 w-4" />
            </Button>
          </Link>
        ) : null}
      </div>
    </div>
  );
}
