'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { 
  FolderGit2, 
  ArrowRight, 
  Sparkles,
  Lightbulb,
  Rocket
} from 'lucide-react';
import Link from 'next/link';
import { cn } from '@/lib/utils';

interface ProjectEmptyStateProps {
  variant?: 'default' | 'dashboard' | 'week' | 'compact';
  className?: string;
  onBrowseWeeks?: () => void;
}

export function ProjectEmptyState({ 
  variant = 'default',
  className,
  onBrowseWeeks 
}: ProjectEmptyStateProps) {
  if (variant === 'compact') {
    return (
      <div className={cn('text-center py-8', className)}>
        <div className="inline-flex h-10 w-10 items-center justify-center rounded-lg bg-muted mb-3">
          <FolderGit2 className="h-5 w-5 text-muted-foreground" />
        </div>
        <p className="text-sm text-muted-foreground mb-3">No projects started yet</p>
        <Button size="sm" variant="outline" asChild>
          <Link href="/weeks">Browse Weeks</Link>
        </Button>
      </div>
    );
  }

  if (variant === 'dashboard') {
    return (
      <Card className={cn('border-dashed', className)}>
        <CardContent className="p-6">
          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-primary/10 to-primary/5">
              <FolderGit2 className="h-6 w-6 text-primary" />
            </div>
            <div className="flex-1">
              <h3 className="font-semibold mb-1">Ready to build something?</h3>
              <p className="text-sm text-muted-foreground">
                Start a weekly project to apply what you&apos;ve learned in a hands-on environment.
              </p>
            </div>
            <Button asChild>
              <Link href="/weeks">
                Find a Project
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (variant === 'week') {
    return (
      <Card className={cn('border-dashed bg-muted/30', className)}>
        <CardContent className="p-8 text-center">
          <div className="inline-flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-primary/20 to-primary/10 mb-4">
            <FolderGit2 className="h-8 w-8 text-primary" />
          </div>
          <h3 className="text-lg font-semibold mb-2">Weekly Project Coming Soon</h3>
          <p className="text-muted-foreground max-w-sm mx-auto mb-6">
            This week doesn&apos;t have a project yet. Check back later or explore other weeks to find projects.
          </p>
          <Button variant="outline" asChild>
            <Link href="/weeks">Browse All Weeks</Link>
          </Button>
        </CardContent>
      </Card>
    );
  }

  // Default variant
  return (
    <Card className={cn('border-dashed', className)}>
      <CardHeader className="text-center pb-4">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-primary/20 to-primary/10 mb-4">
          <FolderGit2 className="h-8 w-8 text-primary" />
        </div>
        <CardTitle className="text-xl">No Projects Yet</CardTitle>
        <CardDescription className="max-w-sm mx-auto">
          Projects help you apply what you&apos;ve learned by building real applications. 
          Start your first project today!
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Benefits */}
        <div className="grid gap-3 sm:grid-cols-3">
          <div className="text-center p-4 rounded-lg bg-muted/50">
            <Lightbulb className="h-5 w-5 mx-auto mb-2 text-yellow-500" />
            <p className="text-sm font-medium">Learn by Doing</p>
            <p className="text-xs text-muted-foreground mt-1">Apply concepts hands-on</p>
          </div>
          <div className="text-center p-4 rounded-lg bg-muted/50">
            <Sparkles className="h-5 w-5 mx-auto mb-2 text-purple-500" />
            <p className="text-sm font-medium">Build Portfolio</p>
            <p className="text-xs text-muted-foreground mt-1">Create showcase projects</p>
          </div>
          <div className="text-center p-4 rounded-lg bg-muted/50">
            <Rocket className="h-5 w-5 mx-auto mb-2 text-blue-500" />
            <p className="text-sm font-medium">Track Progress</p>
            <p className="text-xs text-muted-foreground mt-1">See your growth</p>
          </div>
        </div>

        {/* CTA */}
        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <Button asChild size="lg">
            <Link href="/weeks">
              Browse Weeks
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </Button>
          <Button variant="outline" size="lg" asChild>
            <Link href="/projects/active">
              View Active Projects
            </Link>
          </Button>
        </div>

        {/* Tip */}
        <p className="text-xs text-center text-muted-foreground">
          💡 Tip: Each week has a unique project that reinforces the concepts you&apos;ve learned.
        </p>
      </CardContent>
    </Card>
  );
}

// Empty state for active projects list
export function ActiveProjectsEmptyState({ className }: { className?: string }) {
  return (
    <div className={cn('text-center py-12', className)}>
      <div className="inline-flex h-12 w-12 items-center justify-center rounded-xl bg-muted mb-4">
        <FolderGit2 className="h-6 w-6 text-muted-foreground" />
      </div>
      <h3 className="font-medium mb-2">No Active Projects</h3>
      <p className="text-sm text-muted-foreground mb-4 max-w-sm mx-auto">
        You don&apos;t have any projects in progress. Start a project from any week to see it here.
      </p>
      <Button asChild>
        <Link href="/weeks">
          Find a Project
          <ArrowRight className="ml-2 h-4 w-4" />
        </Link>
      </Button>
    </div>
  );
}

// Empty state for file tree
export function FileTreeEmptyState({ onCreateFile }: { onCreateFile?: () => void }) {
  return (
    <div className="p-4 text-center">
      <div className="inline-flex h-10 w-10 items-center justify-center rounded-lg bg-muted mb-3">
        <FolderGit2 className="h-5 w-5 text-muted-foreground" />
      </div>
      <p className="text-sm text-muted-foreground mb-3">No files yet</p>
      {onCreateFile && (
        <Button size="sm" variant="outline" onClick={onCreateFile}>
          Create First File
        </Button>
      )}
    </div>
  );
}
