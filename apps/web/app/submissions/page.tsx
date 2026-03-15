'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useSubmissions, useGamificationStats } from '@/lib/hooks/use-submissions';
import { SubmissionStatus } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Clock, 
  CheckCircle, 
  XCircle, 
  Star, 
  FileCode, 
  ChevronRight,
  Trophy,
  Flame,
  Award
} from 'lucide-react';
import { formatDistanceToNow } from '@/lib/utils';

const statusConfig: Record<SubmissionStatus, { label: string; variant: 'default' | 'secondary' | 'destructive' | 'outline'; icon: React.ReactNode }> = {
  pending_review: { label: 'Pending Review', variant: 'secondary', icon: <Clock className="w-3 h-3" /> },
  approved: { label: 'Approved', variant: 'default', icon: <CheckCircle className="w-3 h-3" /> },
  needs_work: { label: 'Needs Work', variant: 'destructive', icon: <XCircle className="w-3 h-3" /> },
  exemplary: { label: 'Exemplary', variant: 'default', icon: <Star className="w-3 h-3" /> },
};

function StatusBadge({ status }: { status: SubmissionStatus }) {
  const config = statusConfig[status];
  return (
    <Badge variant={config.variant} className="flex items-center gap-1">
      {config.icon}
      {config.label}
    </Badge>
  );
}

function GamificationCard() {
  const { data: stats, isLoading } = useGamificationStats();

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Your Progress</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <Skeleton className="h-8 w-full" />
            <Skeleton className="h-8 w-full" />
            <Skeleton className="h-8 w-full" />
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!stats) return null;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Trophy className="w-5 h-5 text-yellow-500" />
          Your Progress
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="text-center p-3 bg-muted rounded-lg">
            <div className="text-2xl font-bold">{stats.totalSubmissions}</div>
            <div className="text-xs text-muted-foreground">Total Submissions</div>
          </div>
          <div className="text-center p-3 bg-muted rounded-lg">
            <div className="text-2xl font-bold">{stats.approvedCount}</div>
            <div className="text-xs text-muted-foreground">Approved</div>
          </div>
          <div className="text-center p-3 bg-muted rounded-lg">
            <div className="text-2xl font-bold">{stats.exemplaryCount}</div>
            <div className="text-xs text-muted-foreground">Exemplary</div>
          </div>
          <div className="text-center p-3 bg-muted rounded-lg">
            <div className="text-2xl font-bold flex items-center justify-center gap-1">
              <Flame className="w-5 h-5 text-orange-500" />
              {stats.currentStreak}
            </div>
            <div className="text-xs text-muted-foreground">Day Streak</div>
          </div>
        </div>

        {stats.badges.length > 0 && (
          <div>
            <h4 className="text-sm font-medium mb-3">Badges</h4>
            <div className="flex flex-wrap gap-2">
              {stats.badges.map((badge) => (
                <div
                  key={badge.id}
                  className="flex items-center gap-1.5 px-2 py-1 bg-primary/10 rounded-full text-xs"
                  title={badge.description}
                >
                  <span>{badge.icon}</span>
                  <span className="font-medium">{badge.name}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

function SubmissionListItem({ submission }: { submission: import('@/lib/api').SubmissionListItem }) {
  return (
    <Link href={`/submissions/${submission.id}`}>
      <Card className="hover:border-primary/50 transition-colors cursor-pointer">
        <CardContent className="p-4">
          <div className="flex items-start justify-between gap-4">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <h3 className="font-semibold truncate">
                  {submission.projectName || submission.projectSlug}
                </h3>
                <StatusBadge status={submission.status} />
                {submission.isExemplary && (
                  <Badge variant="outline" className="bg-yellow-500/10 text-yellow-600 border-yellow-500/20">
                    <Award className="w-3 h-3 mr-1" />
                    Exemplary
                  </Badge>
                )}
              </div>
              <div className="flex items-center gap-4 text-sm text-muted-foreground">
                <span className="flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  {formatDistanceToNow(new Date(submission.submittedAt))}
                </span>
                <span className="flex items-center gap-1">
                  <FileCode className="w-3 h-3" />
                  {submission.metricsSummary.linesOfCode} lines
                </span>
                <span className="flex items-center gap-1">
                  <CheckCircle className="w-3 h-3" />
                  {submission.testSummary.passed}/{submission.testSummary.total} tests
                </span>
              </div>
            </div>
            <ChevronRight className="w-5 h-5 text-muted-foreground flex-shrink-0" />
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}

export default function SubmissionsPage() {
  const [statusFilter, setStatusFilter] = useState<SubmissionStatus | undefined>();
  const { data: submissions, isLoading } = useSubmissions(statusFilter);

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold">Your Submissions</h1>
          <p className="text-muted-foreground mt-1">
            Track your project submissions and review status
          </p>
        </div>
        <Button asChild>
          <Link href="/weeks">Start New Project</Link>
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <Tabs value={statusFilter || 'all'} onValueChange={(v) => setStatusFilter(v === 'all' ? undefined : v as SubmissionStatus)}>
              <TabsList>
                <TabsTrigger value="all">All</TabsTrigger>
                <TabsTrigger value="pending_review">Pending</TabsTrigger>
                <TabsTrigger value="approved">Approved</TabsTrigger>
                <TabsTrigger value="exemplary">Exemplary</TabsTrigger>
              </TabsList>
            </Tabs>
          </div>

          {isLoading ? (
            <div className="space-y-4">
              {[...Array(3)].map((_, i) => (
                <Card key={i}>
                  <CardContent className="p-4">
                    <Skeleton className="h-16 w-full" />
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : submissions?.items.length === 0 ? (
            <Card>
              <CardContent className="p-8 text-center">
                <FileCode className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
                <h3 className="text-lg font-semibold mb-2">No submissions yet</h3>
                <p className="text-muted-foreground mb-4">
                  Complete projects and submit them for review to see them here.
                </p>
                <Button asChild>
                  <Link href="/weeks">Browse Projects</Link>
                </Button>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-3">
              {submissions?.items.map((submission) => (
                <SubmissionListItem key={submission.id} submission={submission} />
              ))}
            </div>
          )}
        </div>

        <div className="space-y-6">
          <GamificationCard />
          
          <Card>
            <CardHeader>
              <CardTitle>Review Process</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4 text-sm">
                <div className="flex items-start gap-3">
                  <div className="w-6 h-6 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                    <span className="text-xs font-medium">1</span>
                  </div>
                  <div>
                    <p className="font-medium">Submit Project</p>
                    <p className="text-muted-foreground">Complete all requirements and submit</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-6 h-6 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                    <span className="text-xs font-medium">2</span>
                  </div>
                  <div>
                    <p className="font-medium">Automated Checks</p>
                    <p className="text-muted-foreground">Tests and code quality analysis</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-6 h-6 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                    <span className="text-xs font-medium">3</span>
                  </div>
                  <div>
                    <p className="font-medium">Mentor Review</p>
                    <p className="text-muted-foreground">Typically 24-48 hours</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
