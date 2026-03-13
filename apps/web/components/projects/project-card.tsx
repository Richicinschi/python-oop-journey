'use client';

import { WeeklyProject, UserProjectProgress, ProjectStatus } from '@/types/project';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { 
  Clock, 
  FolderGit2, 
  Play, 
  CheckCircle2, 
  Circle, 
  ArrowRight,
  FileCode2,
  AlertCircle
} from 'lucide-react';
import Link from 'next/link';
import { cn } from '@/lib/utils';

interface ProjectCardProps {
  project: WeeklyProject;
  progress?: UserProjectProgress;
  variant?: 'default' | 'compact' | 'detailed';
  showActions?: boolean;
  onStart?: () => void;
  onContinue?: () => void;
  className?: string;
}

const difficultyColors: Record<string, string> = {
  'Beginner': 'bg-green-500/10 text-green-600 border-green-500/20',
  'Intermediate': 'bg-yellow-500/10 text-yellow-600 border-yellow-500/20',
  'Advanced': 'bg-orange-500/10 text-orange-600 border-orange-500/20',
  'Expert': 'bg-red-500/10 text-red-600 border-red-500/20',
};

const statusConfig: Record<ProjectStatus, { label: string; icon: typeof Circle; color: string }> = {
  'not_started': { 
    label: 'Not Started', 
    icon: Circle, 
    color: 'text-muted-foreground' 
  },
  'in_progress': { 
    label: 'In Progress', 
    icon: Play, 
    color: 'text-blue-500' 
  },
  'submitted': { 
    label: 'Submitted', 
    icon: CheckCircle2, 
    color: 'text-green-500' 
  },
  'completed': { 
    label: 'Completed', 
    icon: CheckCircle2, 
    color: 'text-green-500' 
  },
};

export function ProjectCard({ 
  project, 
  progress, 
  variant = 'default',
  showActions = true,
  onStart,
  onContinue,
  className,
}: ProjectCardProps) {
  const status = progress?.status || 'not_started';
  const statusConfigItem = statusConfig[status];
  const StatusIcon = statusConfigItem.icon;
  
  // Calculate completion percentage
  const completionPercentage = progress?.files.length 
    ? Math.round((progress.files.filter(f => !f.isModified).length / progress.files.length) * 100)
    : 0;

  if (variant === 'compact') {
    return (
      <Card className={cn('hover:shadow-md transition-shadow', className)}>
        <CardContent className="p-4">
          <div className="flex items-center gap-4">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
              <FolderGit2 className="h-5 w-5 text-primary" />
            </div>
            <div className="flex-1 min-w-0">
              <h4 className="font-medium truncate">{project.title}</h4>
              <p className="text-sm text-muted-foreground">Week {project.week}</p>
            </div>
            <StatusIcon className={cn('h-5 w-5', statusConfigItem.color)} />
          </div>
        </CardContent>
      </Card>
    );
  }

  if (variant === 'detailed') {
    return (
      <Card className={cn('hover:shadow-md transition-shadow', className)}>
        <CardHeader>
          <div className="flex items-start justify-between gap-4">
            <div className="flex items-start gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-primary/20 to-primary/10">
                <FolderGit2 className="h-6 w-6 text-primary" />
              </div>
              <div>
                <CardTitle className="text-xl">{project.title}</CardTitle>
                <CardDescription className="mt-1">
                  Week {project.week} • {project.estimatedHours}
                </CardDescription>
              </div>
            </div>
            <Badge variant="outline" className={cn(difficultyColors[project.difficulty])}>
              {project.difficulty}
            </Badge>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-muted-foreground">{project.description}</p>
          
          {progress && status !== 'not_started' && (
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Progress</span>
                <span className="font-medium">{completionPercentage}%</span>
              </div>
              <Progress value={completionPercentage} className="h-2" />
            </div>
          )}

          <div className="flex items-center gap-4 text-sm text-muted-foreground">
            <span className="flex items-center gap-1.5">
              <Clock className="h-4 w-4" />
              {project.estimatedHours}
            </span>
            <span className="flex items-center gap-1.5">
              <FileCode2 className="h-4 w-4" />
              {project.starterFiles.length} starter files
            </span>
            <span className={cn('flex items-center gap-1.5', statusConfigItem.color)}>
              <StatusIcon className="h-4 w-4" />
              {statusConfigItem.label}
            </span>
          </div>

          {showActions && (
            <div className="pt-2">
              {status === 'not_started' ? (
                <Button onClick={onStart} className="w-full gap-2">
                  <Play className="h-4 w-4" />
                  Start Project
                </Button>
              ) : status === 'in_progress' ? (
                <Button onClick={onContinue} className="w-full gap-2">
                  Continue Project
                  <ArrowRight className="h-4 w-4" />
                </Button>
              ) : (
                <div className="flex gap-2">
                  <Button variant="outline" className="flex-1 gap-2">
                    <CheckCircle2 className="h-4 w-4" />
                    Review
                  </Button>
                  <Button variant="outline" className="flex-1 gap-2">
                    <AlertCircle className="h-4 w-4" />
                    Feedback
                  </Button>
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>
    );
  }

  // Default variant
  return (
    <Card className={cn('hover:shadow-md transition-shadow', className)}>
      <CardContent className="p-6">
        <div className="flex items-start gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-primary/20 to-primary/10">
            <FolderGit2 className="h-6 w-6 text-primary" />
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1">
              <h3 className="font-semibold truncate">{project.title}</h3>
              <Badge variant="outline" className={cn('text-xs', difficultyColors[project.difficulty])}>
                {project.difficulty}
              </Badge>
            </div>
            <p className="text-sm text-muted-foreground line-clamp-2 mb-3">
              {project.description}
            </p>
            
            <div className="flex items-center gap-4 text-sm text-muted-foreground mb-4">
              <span className="flex items-center gap-1.5">
                <Clock className="h-4 w-4" />
                {project.estimatedHours}
              </span>
              <span className={cn('flex items-center gap-1.5', statusConfigItem.color)}>
                <StatusIcon className="h-4 w-4" />
                {statusConfigItem.label}
              </span>
            </div>

            {progress && status === 'in_progress' && (
              <div className="space-y-1.5 mb-4">
                <div className="flex items-center justify-between text-xs">
                  <span className="text-muted-foreground">Progress</span>
                  <span className="font-medium">{completionPercentage}%</span>
                </div>
                <Progress value={completionPercentage} className="h-1.5" />
              </div>
            )}

            {showActions && (
              <div className="flex gap-2">
                {status === 'not_started' ? (
                  <Button size="sm" onClick={onStart} className="gap-1.5">
                    <Play className="h-3.5 w-3.5" />
                    Start
                  </Button>
                ) : status === 'in_progress' ? (
                  <Button size="sm" onClick={onContinue} className="gap-1.5">
                    Continue
                    <ArrowRight className="h-3.5 w-3.5" />
                  </Button>
                ) : (
                  <Button size="sm" variant="outline" className="gap-1.5">
                    <CheckCircle2 className="h-3.5 w-3.5" />
                    Submitted
                  </Button>
                )}
              </div>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

// Mini project card for sidebar/lists
export function ProjectMiniCard({ 
  project, 
  progress,
  onClick 
}: { 
  project: WeeklyProject; 
  progress?: UserProjectProgress;
  onClick?: () => void;
}) {
  const status = progress?.status || 'not_started';
  const statusConfigItem = statusConfig[status];
  const StatusIcon = statusConfigItem.icon;

  return (
    <button
      onClick={onClick}
      className="w-full flex items-center gap-3 p-3 rounded-lg hover:bg-accent transition-colors text-left"
    >
      <div className="flex h-8 w-8 items-center justify-center rounded-md bg-primary/10">
        <FolderGit2 className="h-4 w-4 text-primary" />
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium truncate">{project.title}</p>
        <p className="text-xs text-muted-foreground">Week {project.week}</p>
      </div>
      <StatusIcon className={cn('h-4 w-4 shrink-0', statusConfigItem.color)} />
    </button>
  );
}
