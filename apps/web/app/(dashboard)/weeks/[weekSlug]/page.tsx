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
  getWeeks,
  getWeekProblemCount,
  formatWeekNumber,
  formatDayNumber,
  getDayProgress,
  getWeekProgress
} from '@/lib/curriculum-loader';
import { 
  BookOpen, 
  ChevronLeft, 
  ChevronRight, 
  FileText, 
  GraduationCap,
  CheckCircle2,
  Circle,
  Target,
  ListChecks,
  FolderGit2,
  Clock,
  AlertCircle,
  Play,
  ArrowRight,
  Lock,
  CheckIcon
} from 'lucide-react';
import { ProjectEmptyState } from '@/components/projects';

interface WeekPageProps {
  params: {
    weekSlug: string;
  };
}

export async function generateStaticParams() {
  const weeks = getWeeks();
  return weeks.map((week) => ({
    weekSlug: week.slug,
  }));
}

export async function generateMetadata({ params }: WeekPageProps): Promise<Metadata> {
  const week = getTransformedWeekBySlug(params.weekSlug);
  if (!week) {
    return { title: 'Week Not Found' };
  }
  return {
    title: `${week.title} | Python OOP Journey`,
    description: week.objective,
  };
}

// Mock function to get project status - in real app, fetch from API/localStorage
function getProjectStatus(weekSlug: string): 'not_started' | 'in_progress' | 'submitted' {
  // This would check localStorage or API for actual status
  return 'not_started';
}

// Mock function to get project progress - in real app, fetch from API/localStorage
function getProjectProgress(weekSlug: string): number {
  return 0;
}

export default function WeekPage({ params }: WeekPageProps) {
  const week = getTransformedWeekBySlug(params.weekSlug);

  if (!week) {
    notFound();
  }

  const progress = getWeekProgress(week);
  const problemCount = getWeekProblemCount(week);
  const weeks = getWeeks();
  const currentWeekIndex = weeks.findIndex(w => w.slug === week.slug);
  const prevWeek = currentWeekIndex > 0 ? weeks[currentWeekIndex - 1] : null;
  const nextWeek = currentWeekIndex < weeks.length - 1 ? weeks[currentWeekIndex + 1] : null;
  
  // Project data
  const projectStatus = getProjectStatus(week.slug);
  const projectProgress = getProjectProgress(week.slug);
  const hasProject = !!week.project;

  return (
    <div className="space-y-8">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-2 text-sm text-muted-foreground" aria-label="Breadcrumb">
        <Link href="/weeks" className="hover:text-foreground transition-colors">
          Curriculum
        </Link>
        <ChevronRight className="h-4 w-4" />
        <span className="text-foreground font-medium">{formatWeekNumber(week.order)}</span>
      </nav>

      {/* Header */}
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
          <div className="flex items-start gap-4">
            <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-xl bg-primary/10 text-primary">
              <GraduationCap className="h-7 w-7" />
            </div>
            <div>
              <Badge variant="secondary" className="mb-2 font-mono">
                {formatWeekNumber(week.order)}
              </Badge>
              <h1 className="text-3xl font-bold tracking-tight">
                {week.title.replace(`Week ${week.order}: `, '').replace('Week 0: ', '')}
              </h1>
            </div>
          </div>
          
          <div className="flex gap-2">
            {prevWeek && (
              <Link href={`/weeks/${prevWeek.slug}`}>
                <Button variant="outline" size="sm">
                  <ChevronLeft className="mr-1 h-4 w-4" />
                  Previous
                </Button>
              </Link>
            )}
            {nextWeek && (
              <Link href={`/weeks/${nextWeek.slug}`}>
                <Button variant="outline" size="sm">
                  Next
                  <ChevronRight className="ml-1 h-4 w-4" />
                </Button>
              </Link>
            )}
          </div>
        </div>

        {/* Objective */}
        {week.objective && (
          <Card className="bg-muted/50 border-dashed">
            <CardContent className="pt-6">
              <div className="flex items-start gap-3">
                <Target className="h-5 w-5 text-primary mt-0.5" />
                <div>
                  <p className="font-medium mb-1">Week Objective</p>
                  <p className="text-muted-foreground">{week.objective}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Progress Card */}
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <ListChecks className="h-5 w-5 text-muted-foreground" />
                <span className="font-medium">Week Progress</span>
              </div>
              <span className="text-sm text-muted-foreground">
                0/{week.days.length} days • 0/{problemCount} problems
              </span>
            </div>
            <Progress value={progress} className="h-3" aria-label="Week progress" />
          </CardContent>
        </Card>
      </div>

      <Separator />

      {/* Days Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold">Daily Lessons</h2>
          <span className="text-sm text-muted-foreground">{week.days.length} days</span>
        </div>
        
        <div className="grid gap-4">
          {week.days.map((day, index) => {
            const isLocked = index > 0;
            const dayProgress = getDayProgress(day);
            const hasTheory = day.theory_content && day.theory_content.length > 0;

            return (
              <Card 
                key={day.slug} 
                className={`transition-all hover:shadow-sm ${isLocked ? 'opacity-60' : ''}`}
              >
                <CardContent className="p-6">
                  <div className="flex flex-col sm:flex-row sm:items-center gap-4">
                    {/* Status & Day Number */}
                    <div className="flex items-center gap-3">
                      <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-muted">
                        {dayProgress === 100 ? (
                          <CheckCircle2 className="h-5 w-5 text-green-500" />
                        ) : (
                          <span className="text-sm font-medium">{day.order}</span>
                        )}
                      </div>
                      <div>
                        <Badge variant="outline" className="font-mono text-xs">
                          {formatDayNumber(day.order)}
                        </Badge>
                      </div>
                    </div>

                    {/* Content */}
                    <div className="flex-1 min-w-0">
                      <h3 className="font-semibold text-lg truncate">
                        {day.title.replace(`Day ${day.order}: `, '')}
                      </h3>
                      <div className="flex flex-wrap items-center gap-3 mt-1 text-sm text-muted-foreground">
                        <span className="flex items-center gap-1">
                          <BookOpen className="h-3.5 w-3.5" />
                          {day.problems.length} problems
                        </span>
                        {hasTheory && (
                          <span className="flex items-center gap-1">
                            <FileText className="h-3.5 w-3.5" />
                            Theory included
                          </span>
                        )}
                      </div>
                      
                      {/* Learning Objectives */}
                      {day.learning_objectives && day.learning_objectives.length > 0 && (
                        <ul className="mt-2 space-y-1">
                          {day.learning_objectives.slice(0, 2).map((obj, i) => (
                            <li key={i} className="text-xs text-muted-foreground flex items-start gap-2">
                              <span className="text-primary mt-0.5">•</span>
                              <span className="line-clamp-1">{obj}</span>
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>

                    {/* Actions */}
                    <div className="flex items-center gap-2">
                      {hasTheory && (
                        <Link href={`/weeks/${week.slug}/days/${day.slug}/theory`}>
                          <Button variant="outline" size="sm" disabled={isLocked}>
                            <FileText className="mr-2 h-4 w-4" />
                            Theory
                          </Button>
                        </Link>
                      )}
                      <Link href={`/weeks/${week.slug}/days/${day.slug}`}>
                        <Button size="sm" disabled={isLocked}>
                          <BookOpen className="mr-2 h-4 w-4" />
                          {dayProgress > 0 ? 'Continue' : 'Start'}
                        </Button>
                      </Link>
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>

      {/* Weekly Project Section */}
      <section aria-labelledby="weekly-project-heading">
        <div className="flex items-center justify-between mb-4">
          <h2 id="weekly-project-heading" className="text-xl font-semibold flex items-center gap-2">
            <FolderGit2 className="h-5 w-5 text-primary" />
            Weekly Project
          </h2>
        </div>

        {hasProject && week.project ? (
          <Card className={`
            border-2 transition-all
            ${projectStatus === 'submitted' 
              ? 'border-green-500/30 bg-green-500/5' 
              : projectStatus === 'in_progress'
                ? 'border-blue-500/30 bg-blue-500/5'
                : 'border-primary/20 bg-gradient-to-br from-primary/5 to-primary/10'
            }
          `}>
            <CardHeader>
              <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
                <div className="flex items-start gap-4">
                  <div className={`
                    flex h-14 w-14 shrink-0 items-center justify-center rounded-xl
                    ${projectStatus === 'submitted' 
                      ? 'bg-green-500/10' 
                      : projectStatus === 'in_progress'
                        ? 'bg-blue-500/10'
                        : 'bg-primary/10'
                    }
                  `}>
                    {projectStatus === 'submitted' ? (
                      <CheckCircle2 className="h-7 w-7 text-green-600" />
                    ) : projectStatus === 'in_progress' ? (
                      <Play className="h-7 w-7 text-blue-600" />
                    ) : (
                      <FolderGit2 className="h-7 w-7 text-primary" />
                    )}
                  </div>
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <CardTitle>{week.project.title}</CardTitle>
                      {projectStatus === 'submitted' && (
                        <Badge variant="default" className="bg-green-500">
                          Submitted
                        </Badge>
                      )}
                      {projectStatus === 'in_progress' && (
                        <Badge variant="secondary" className="bg-blue-500/20 text-blue-700">
                          In Progress
                        </Badge>
                      )}
                    </div>
                    <CardDescription className="flex items-center gap-3 mt-1">
                      <span className="flex items-center gap-1">
                        <Clock className="h-3.5 w-3.5" />
                        2-3 hours estimated
                      </span>
                      <span className="flex items-center gap-1">
                        <AlertCircle className="h-3.5 w-3.5" />
                        Applied learning
                      </span>
                    </CardDescription>
                  </div>
                </div>
                
                <div className="flex gap-2">
                  {projectStatus === 'not_started' ? (
                    <Button asChild>
                      <Link href={`/weeks/${week.slug}/project`}>
                        <Play className="mr-2 h-4 w-4" />
                        Start Project
                      </Link>
                    </Button>
                  ) : projectStatus === 'in_progress' ? (
                    <Button asChild>
                      <Link href={`/weeks/${week.slug}/project`}>
                        Continue Project
                        <ArrowRight className="ml-2 h-4 w-4" />
                      </Link>
                    </Button>
                  ) : (
                    <Button variant="outline" asChild>
                      <Link href={`/weeks/${week.slug}/project`}>
                        <CheckCircle2 className="mr-2 h-4 w-4" />
                        Review
                      </Link>
                    </Button>
                  )}
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-muted-foreground">
                {week.project.description}
              </p>
              
              {/* Progress bar for in-progress projects */}
              {projectStatus === 'in_progress' && (
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">Your Progress</span>
                    <span className="font-medium">{projectProgress}%</span>
                  </div>
                  <Progress value={projectProgress} className="h-2" />
                </div>
              )}

              {/* Requirements preview */}
              {week.project.requirements && week.project.requirements.length > 0 && (
                <div className="bg-muted/50 rounded-lg p-4">
                  <p className="font-medium text-sm mb-2">What you&apos;ll build:</p>
                  <ul className="space-y-1.5">
                    {week.project.requirements.slice(0, 3).map((req, i) => (
                      <li key={i} className="text-sm text-muted-foreground flex items-start gap-2">
                        <CheckIcon className="h-4 w-4 text-primary shrink-0 mt-0.5" />
                        <span>{req}</span>
                      </li>
                    ))}
                    {week.project.requirements.length > 3 && (
                      <li className="text-sm text-muted-foreground">
                        +{week.project.requirements.length - 3} more requirements
                      </li>
                    )}
                  </ul>
                </div>
              )}
            </CardContent>
          </Card>
        ) : (
          <ProjectEmptyState variant="week" />
        )}
      </section>

      {/* Navigation Footer */}
      <div className="flex items-center justify-between pt-4 border-t">
        <Link href="/weeks">
          <Button variant="outline">
            <ChevronLeft className="mr-2 h-4 w-4" />
            All Weeks
          </Button>
        </Link>
        {week.days.length > 0 && (
          <Link href={`/weeks/${week.slug}/days/${week.days[0].slug}`}>
            <Button>
              Start {formatWeekNumber(week.order)}
              <ChevronRight className="ml-2 h-4 w-4" />
            </Button>
          </Link>
        )}
      </div>
    </div>
  );
}
