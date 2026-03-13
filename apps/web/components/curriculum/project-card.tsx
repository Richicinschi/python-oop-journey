'use client';

import Link from 'next/link';
import { FolderGit2, CheckCircle2, Clock, Play, ArrowRight } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { cn } from '@/lib/utils';
import { Project } from '@/types/curriculum';

interface ProjectCardProps {
  project: Project;
  weekSlug: string;
  weekOrder: number;
  status?: 'not_started' | 'in_progress' | 'completed';
  progress?: number;
}

export function ProjectCard({ 
  project, 
  weekSlug, 
  weekOrder,
  status = 'not_started',
  progress = 0,
}: ProjectCardProps) {
  const statusConfig = {
    not_started: {
      icon: Play,
      label: 'Not Started',
      variant: 'outline' as const,
      color: 'text-muted-foreground',
    },
    in_progress: {
      icon: Clock,
      label: 'In Progress',
      variant: 'secondary' as const,
      color: 'text-yellow-600',
    },
    completed: {
      icon: CheckCircle2,
      label: 'Completed',
      variant: 'default' as const,
      color: 'text-green-600',
    },
  };

  const config = statusConfig[status];
  const StatusIcon = config.icon;

  return (
    <Card className="relative overflow-hidden">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-lg bg-primary/10">
              <FolderGit2 className="h-5 w-5 text-primary" />
            </div>
            <div>
              <Badge variant="outline" className="mb-1">Week {weekOrder} Project</Badge>
              <CardTitle className="text-lg">{project.title}</CardTitle>
            </div>
          </div>
          <Badge variant={config.variant} className={cn(config.color)}>
            <StatusIcon className="h-3 w-3 mr-1" />
            {config.label}
          </Badge>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-4">
        <CardDescription className="line-clamp-2">
          {project.description}
        </CardDescription>

        {status === 'in_progress' && (
          <div className="space-y-1">
            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground">Progress</span>
              <span className="font-medium">{Math.round(progress)}%</span>
            </div>
            <Progress value={progress} className="h-2" />
          </div>
        )}

        <div className="flex items-center justify-between pt-2">
          <div className="text-sm text-muted-foreground">
            {status === 'completed' 
              ? 'Project completed! Great job!' 
              : status === 'in_progress' 
                ? 'Continue working on your project'
                : 'Start your week project'}
          </div>
          <Link href={`/projects/${project.slug}`}>
            <Button size="sm">
              {status === 'not_started' ? 'Start Project' : 'Open Project'}
              <ArrowRight className="h-4 w-4 ml-2" />
            </Button>
          </Link>
        </div>
      </CardContent>
    </Card>
  );
}
