'use client';

import { useMemo } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { ProjectCard, ProjectMiniCard } from './project-card';
import { ProjectEmptyState, ActiveProjectsEmptyState } from './empty-state';
import { ActiveProjectsSkeleton } from './skeletons';
import { WeeklyProject, UserProjectProgress, ActiveProject } from '@/types/project';
import { FolderGit2, ArrowRight, Clock, CheckCircle2, Play } from 'lucide-react';
import Link from 'next/link';
import { cn } from '@/lib/utils';

interface ActiveProjectsSectionProps {
  projects: WeeklyProject[];
  progressMap: Record<string, UserProjectProgress>;
  currentWeekNumber?: number;
  isLoading?: boolean;
  variant?: 'full' | 'compact' | 'minimal';
  onContinueProject?: (project: WeeklyProject) => void;
  className?: string;
}

export function ActiveProjectsSection({
  projects,
  progressMap,
  currentWeekNumber,
  isLoading,
  variant = 'full',
  onContinueProject,
  className,
}: ActiveProjectsSectionProps) {
  // Get active and completed projects
  const { activeProjects, completedProjects, currentWeekProject } = useMemo<{
    activeProjects: ActiveProject[];
    completedProjects: ActiveProject[];
    currentWeekProject: ActiveProject | null;
  }>(() => {
    const active: ActiveProject[] = [];
    const completed: ActiveProject[] = [];
    let current: ActiveProject | null = null;

    projects.forEach(project => {
      const progress = progressMap[project.slug];
      if (!progress) return;

      const activeProject: ActiveProject = {
        project,
        progress,
        completionPercentage: calculateCompletion(progress),
      };

      if (progress.status === 'in_progress') {
        active.push(activeProject);
        if (project.week === currentWeekNumber) {
          current = activeProject;
        }
      } else if (progress.status === 'submitted') {
        completed.push(activeProject);
      }
    });

    return {
      activeProjects: active,
      completedProjects: completed,
      currentWeekProject: current,
    };
  }, [projects, progressMap, currentWeekNumber]);

  // Find the next unstarted project for the current or next week
  const nextProject = useMemo(() => {
    if (currentWeekProject) return null;
    
    const weekOrder = currentWeekNumber || 1;
    return projects
      .filter(p => p.week >= weekOrder && !progressMap[p.slug])
      .sort((a, b) => a.week - b.week)[0];
  }, [projects, progressMap, currentWeekNumber, currentWeekProject]);

  if (isLoading) {
    return <ActiveProjectsSkeleton />;
  }

  // Minimal variant - just a link
  if (variant === 'minimal') {
    const hasProjects = activeProjects.length > 0;
    
    return (
      <Card className={className}>
        <CardContent className="p-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
              <FolderGit2 className="h-5 w-5 text-primary" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="font-medium truncate">
                {hasProjects ? 'Projects in Progress' : 'Weekly Projects'}
              </p>
              <p className="text-sm text-muted-foreground">
                {hasProjects 
                  ? `${activeProjects.length} active project${activeProjects.length !== 1 ? 's' : ''}`
                  : 'Apply what you learn'
                }
              </p>
            </div>
            <Button variant="ghost" size="sm" asChild>
              <Link href="/projects">
                <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  // Compact variant - list of projects
  if (variant === 'compact') {
    if (activeProjects.length === 0) {
      return (
        <Card className={className}>
          <CardHeader className="pb-3">
            <CardTitle className="text-base flex items-center gap-2">
              <FolderGit2 className="h-4 w-4" />
              Active Projects
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ProjectEmptyState variant="compact" />
          </CardContent>
        </Card>
      );
    }

    return (
      <Card className={className}>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <CardTitle className="text-base flex items-center gap-2">
              <FolderGit2 className="h-4 w-4" />
              Active Projects
            </CardTitle>
            <Badge variant="secondary">{activeProjects.length}</Badge>
          </div>
        </CardHeader>
        <CardContent className="space-y-2">
          {activeProjects.slice(0, 3).map(({ project, progress, completionPercentage }) => (
            <button
              key={project.slug}
              onClick={() => onContinueProject?.(project)}
              className="w-full text-left p-3 rounded-lg hover:bg-accent transition-colors"
            >
              <div className="flex items-center justify-between mb-1.5">
                <span className="font-medium text-sm truncate">{project.title}</span>
                <Badge variant="outline" className="text-xs">
                  Week {project.week}
                </Badge>
              </div>
              <div className="flex items-center gap-2">
                <Progress value={completionPercentage} className="h-1.5 flex-1" />
                <span className="text-xs text-muted-foreground w-10 text-right">
                  {completionPercentage}%
                </span>
              </div>
            </button>
          ))}
          
          {activeProjects.length > 3 && (
            <Button variant="ghost" size="sm" className="w-full" asChild>
              <Link href="/projects">
                View all {activeProjects.length} projects
              </Link>
            </Button>
          )}
        </CardContent>
      </Card>
    );
  }

  // Full variant - detailed cards
  return (
    <div className={cn('space-y-6', className)}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <FolderGit2 className="h-5 w-5 text-primary" />
            Active Projects
          </h2>
          <p className="text-sm text-muted-foreground mt-1">
            Your in-progress and completed projects
          </p>
        </div>
        <Button variant="outline" size="sm" asChild>
          <Link href="/projects">View All</Link>
        </Button>
      </div>

      {/* Current week project (if active) */}
      {currentWeekProject && (
        <Card className="border-primary/20 bg-primary/5">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <Badge className="mb-2">Current Week</Badge>
                <CardTitle>{currentWeekProject.project.title}</CardTitle>
                <CardDescription>
                  Week {currentWeekProject.project.week} • {currentWeekProject.project.estimatedHours}
                </CardDescription>
              </div>
              <Button onClick={() => onContinueProject?.(currentWeekProject!.project)}>
                <Play className="h-4 w-4 mr-2" />
                Continue
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Progress</span>
                <span className="font-medium">{currentWeekProject.completionPercentage}%</span>
              </div>
              <Progress value={currentWeekProject.completionPercentage} className="h-2" />
              {(currentWeekProject.progress as unknown as { totalTimeSpent?: number }).totalTimeSpent && (
                <p className="text-sm text-muted-foreground">
                  {formatTime((currentWeekProject.progress as unknown as { totalTimeSpent: number }).totalTimeSpent)} spent so far
                </p>
              )}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Next project suggestion */}
      {!currentWeekProject && nextProject && (
        <Card className="border-dashed">
          <CardHeader>
            <div className="flex items-start justify-between">
              <div>
                <CardTitle>Ready for a Project?</CardTitle>
                <CardDescription>
                  Apply what you&apos;ve learned with hands-on practice
                </CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-4 p-4 rounded-lg bg-muted/50">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10">
                <FolderGit2 className="h-6 w-6 text-primary" />
              </div>
              <div className="flex-1">
                <p className="font-medium">{nextProject.title}</p>
                <p className="text-sm text-muted-foreground">
                  Week {nextProject.week} • {nextProject.estimatedHours}
                </p>
              </div>
              <Button asChild>
                <Link href={`/projects/${nextProject.slug}`}>
                  Start Project
                  <ArrowRight className="h-4 w-4 ml-2" />
                </Link>
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Other active projects */}
      {activeProjects.filter(p => p !== currentWeekProject).length > 0 && (
        <div className="space-y-3">
          <h3 className="text-sm font-medium text-muted-foreground">Other Active Projects</h3>
          <div className="grid gap-4 sm:grid-cols-2">
            {activeProjects
              .filter(p => p !== currentWeekProject)
              .map(({ project, progress, completionPercentage }) => (
                <ProjectCard
                  key={project.slug}
                  project={project}
                  progress={progress}
                  variant="default"
                  onContinue={() => onContinueProject?.(project)}
                />
              ))}
          </div>
        </div>
      )}

      {/* Completed projects */}
      {completedProjects.length > 0 && (
        <div className="space-y-3">
          <h3 className="text-sm font-medium text-muted-foreground">
            Completed Projects
          </h3>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {completedProjects.slice(0, 3).map(({ project }) => (
              <Card key={project.slug} className="opacity-75">
                <CardContent className="p-4">
                  <div className="flex items-center gap-3">
                    <CheckCircle2 className="h-5 w-5 text-green-500" />
                    <div className="flex-1 min-w-0">
                      <p className="font-medium text-sm truncate">{project.title}</p>
                      <p className="text-xs text-muted-foreground">
                        Week {project.week}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Empty state */}
      {activeProjects.length === 0 && completedProjects.length === 0 && !nextProject && (
        <ProjectEmptyState variant="dashboard" />
      )}
    </div>
  );
}

// Helper functions
function calculateCompletion(progress: UserProjectProgress): number {
  if (!progress.files.length) return 0;
  const savedFiles = progress.files.filter(f => !f.isModified).length;
  return Math.round((savedFiles / progress.files.length) * 100);
}

function formatTime(seconds: number): string {
  if (seconds < 60) return `${seconds}s`;
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m`;
  const hours = Math.floor(seconds / 3600);
  const mins = Math.floor((seconds % 3600) / 60);
  return mins > 0 ? `${hours}h ${mins}m` : `${hours}h`;
}
