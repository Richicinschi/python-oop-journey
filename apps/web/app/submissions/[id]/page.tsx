'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { useSubmission, useSubmissionFiles, useSubmissionComments } from '@/lib/hooks/use-submissions';
import { SubmissionStatus } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Separator } from '@/components/ui/separator';
import { ScrollArea } from '@/components/ui/scroll-area';
import { 
  Clock, 
  CheckCircle, 
  XCircle, 
  Star, 
  FileCode, 
  ArrowLeft,
  Award,
  AlertCircle,
  GitCommit,
  MessageSquare,
  Code2,
  BarChart3
} from 'lucide-react';
import { formatDistanceToNow, formatDate } from '@/lib/utils';

const statusConfig: Record<SubmissionStatus, { label: string; variant: 'default' | 'secondary' | 'destructive' | 'outline'; icon: React.ReactNode; color: string }> = {
  pending_review: { 
    label: 'Pending Review', 
    variant: 'secondary', 
    icon: <Clock className="w-4 h-4" />,
    color: 'text-yellow-600'
  },
  approved: { 
    label: 'Approved', 
    variant: 'default', 
    icon: <CheckCircle className="w-4 h-4" />,
    color: 'text-green-600'
  },
  needs_work: { 
    label: 'Needs Work', 
    variant: 'destructive', 
    icon: <XCircle className="w-4 h-4" />,
    color: 'text-red-600'
  },
  exemplary: { 
    label: 'Exemplary', 
    variant: 'default', 
    icon: <Star className="w-4 h-4" />,
    color: 'text-purple-600'
  },
};

function StatusBadge({ status }: { status: SubmissionStatus }) {
  const config = statusConfig[status];
  return (
    <Badge variant={config.variant} className="flex items-center gap-1.5 px-2.5 py-1">
      {config.icon}
      {config.label}
    </Badge>
  );
}

function CodeViewer({ files }: { files: Record<string, string> }) {
  const [selectedFile, setSelectedFile] = useState(Object.keys(files)[0] || '');

  if (!files || Object.keys(files).length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">
        <FileCode className="w-12 h-12 mx-auto mb-4 opacity-50" />
        <p>No files available</p>
      </div>
    );
  }

  return (
    <div className="flex h-[500px] border rounded-lg overflow-hidden">
      <div className="w-48 border-r bg-muted/50">
        <ScrollArea className="h-full">
          <div className="p-2">
            <h4 className="text-xs font-semibold text-muted-foreground mb-2 px-2">FILES</h4>
            {Object.keys(files).map((path) => (
              <button
                key={path}
                onClick={() => setSelectedFile(path)}
                className={`w-full text-left px-2 py-1.5 text-sm rounded truncate transition-colors ${
                  selectedFile === path 
                    ? 'bg-primary/10 text-primary font-medium' 
                    : 'hover:bg-muted'
                }`}
              >
                {path.split('/').pop()}
              </button>
            ))}
          </div>
        </ScrollArea>
      </div>
      <div className="flex-1 overflow-auto">
        <div className="p-4">
          <div className="flex items-center justify-between mb-4">
            <h4 className="text-sm font-medium">{selectedFile}</h4>
            <span className="text-xs text-muted-foreground">
              {files[selectedFile]?.split('\n').length} lines
            </span>
          </div>
          <pre className="text-sm font-mono bg-muted/50 p-4 rounded-lg overflow-x-auto">
            <code>{files[selectedFile]}</code>
          </pre>
        </div>
      </div>
    </div>
  );
}

function TestResults({ testResults }: { testResults: import('@/lib/api').TestResults }) {
  const passRate = testResults.total > 0 
    ? Math.round((testResults.passed / testResults.total) * 100) 
    : 0;

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-4">
        <div className={`text-4xl font-bold ${passRate === 100 ? 'text-green-600' : passRate >= 50 ? 'text-yellow-600' : 'text-red-600'}`}>
          {passRate}%
        </div>
        <div className="text-sm text-muted-foreground">
          <p>{testResults.passed} of {testResults.total} tests passed</p>
          <p>Execution time: {testResults.executionTimeMs}ms</p>
        </div>
      </div>

      {testResults.tests.length > 0 && (
        <div className="space-y-2">
          <h4 className="text-sm font-medium">Test Details</h4>
          <div className="space-y-1">
            {testResults.tests.map((test, i) => (
              <div 
                key={i} 
                className={`flex items-center gap-2 p-2 rounded text-sm ${
                  test.passed ? 'bg-green-500/10' : 'bg-red-500/10'
                }`}
              >
                {test.passed ? (
                  <CheckCircle className="w-4 h-4 text-green-600" />
                ) : (
                  <XCircle className="w-4 h-4 text-red-600" />
                )}
                <span className="flex-1">{test.name}</span>
                <span className="text-xs text-muted-foreground">{test.durationMs}ms</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {testResults.stdout && (
        <div>
          <h4 className="text-sm font-medium mb-2">Output</h4>
          <pre className="text-xs bg-muted p-3 rounded overflow-x-auto max-h-48">
            {testResults.stdout}
          </pre>
        </div>
      )}

      {testResults.stderr && (
        <div>
          <h4 className="text-sm font-medium mb-2 text-red-600">Errors</h4>
          <pre className="text-xs bg-red-500/10 p-3 rounded overflow-x-auto max-h-48 text-red-700">
            {testResults.stderr}
          </pre>
        </div>
      )}
    </div>
  );
}

function CodeMetrics({ metrics }: { metrics: import('@/lib/api').CodeMetrics }) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      <MetricCard 
        label="Lines of Code" 
        value={metrics.linesOfCode} 
        subtitle={`${metrics.totalLines} total`}
      />
      <MetricCard 
        label="Functions" 
        value={metrics.functionCount} 
        subtitle={`${metrics.classCount} classes`}
      />
      <MetricCard 
        label="Docstrings" 
        value={`${Math.round(metrics.docstringCoverage)}%`}
        subtitle="coverage"
      />
      <MetricCard 
        label="Lint Issues" 
        value={metrics.lintErrors + metrics.lintWarnings}
        subtitle={`${metrics.lintErrors} errors, ${metrics.lintWarnings} warnings`}
        variant={metrics.lintErrors > 0 ? 'warning' : 'success'}
      />
    </div>
  );
}

function MetricCard({ 
  label, 
  value, 
  subtitle,
  variant = 'default'
}: { 
  label: string; 
  value: string | number; 
  subtitle?: string;
  variant?: 'default' | 'success' | 'warning' | 'error';
}) {
  const variantClasses = {
    default: '',
    success: 'text-green-600',
    warning: 'text-yellow-600',
    error: 'text-red-600',
  };

  return (
    <div className="p-4 bg-muted rounded-lg">
      <p className="text-xs text-muted-foreground mb-1">{label}</p>
      <p className={`text-2xl font-bold ${variantClasses[variant]}`}>{value}</p>
      {subtitle && <p className="text-xs text-muted-foreground mt-1">{subtitle}</p>}
    </div>
  );
}

export default function SubmissionDetailPage() {
  const params = useParams();
  const submissionId = params.id as string;
  
  const { data: submission, isLoading: isLoadingSubmission } = useSubmission(submissionId);
  const { data: files, isLoading: isLoadingFiles } = useSubmissionFiles(submissionId);

  if (isLoadingSubmission) {
    return (
      <div className="container mx-auto py-8 px-4">
        <Skeleton className="h-8 w-64 mb-4" />
        <Skeleton className="h-96 w-full" />
      </div>
    );
  }

  if (!submission) {
    return (
      <div className="container mx-auto py-8 px-4">
        <Card>
          <CardContent className="p-8 text-center">
            <AlertCircle className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
            <h2 className="text-xl font-semibold mb-2">Submission Not Found</h2>
            <p className="text-muted-foreground mb-4">
              The submission you&apos;re looking for doesn&apos;t exist or you don&apos;t have access.
            </p>
            <Button asChild>
              <Link href="/submissions">Back to Submissions</Link>
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="mb-6">
        <Button variant="ghost" asChild className="mb-4">
          <Link href="/submissions">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Submissions
          </Link>
        </Button>

        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <h1 className="text-3xl font-bold">{submission.projectName || submission.projectSlug}</h1>
              <StatusBadge status={submission.status} />
              {submission.isExemplary && (
                <Badge className="bg-yellow-500/10 text-yellow-600 border-yellow-500/20">
                  <Award className="w-3 h-3 mr-1" />
                  Exemplary
                </Badge>
              )}
            </div>
            <div className="flex items-center gap-4 text-sm text-muted-foreground">
              <span className="flex items-center gap-1">
                <GitCommit className="w-4 h-4" />
                ID: {submission.id.slice(0, 8)}
              </span>
              <span className="flex items-center gap-1">
                <Clock className="w-4 h-4" />
                Submitted {formatDistanceToNow(new Date(submission.submittedAt))}
              </span>
              {submission.weekSlug && (
                <span className="flex items-center gap-1">
                  <FileCode className="w-4 h-4" />
                  {submission.weekSlug}
                </span>
              )}
            </div>
          </div>
        </div>
      </div>

      <Tabs defaultValue="code" className="space-y-6">
        <TabsList>
          <TabsTrigger value="code">
            <Code2 className="w-4 h-4 mr-2" />
            Code
          </TabsTrigger>
          <TabsTrigger value="tests">
            <CheckCircle className="w-4 h-4 mr-2" />
            Test Results
          </TabsTrigger>
          <TabsTrigger value="metrics">
            <BarChart3 className="w-4 h-4 mr-2" />
            Metrics
          </TabsTrigger>
          {submission.reviewerNotes && (
            <TabsTrigger value="review">
              <MessageSquare className="w-4 h-4 mr-2" />
              Review Notes
            </TabsTrigger>
          )}
        </TabsList>

        <TabsContent value="code">
          <Card>
            <CardHeader>
              <CardTitle>Code Snapshot</CardTitle>
              <CardDescription>
                This is the exact code that was submitted for review
              </CardDescription>
            </CardHeader>
            <CardContent>
              {isLoadingFiles ? (
                <Skeleton className="h-[500px] w-full" />
              ) : (
                <CodeViewer files={files || {}} />
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="tests">
          <Card>
            <CardHeader>
              <CardTitle>Test Results</CardTitle>
              <CardDescription>
                Automated test execution results
              </CardDescription>
            </CardHeader>
            <CardContent>
              <TestResults testResults={submission.testResults} />
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="metrics">
          <Card>
            <CardHeader>
              <CardTitle>Code Metrics</CardTitle>
              <CardDescription>
                Code quality and complexity analysis
              </CardDescription>
            </CardHeader>
            <CardContent>
              <CodeMetrics metrics={submission.metrics} />
              <Separator className="my-6" />
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <MetricCard label="Blank Lines" value={submission.metrics.blankLines} />
                <MetricCard label="Comment Lines" value={submission.metrics.commentLines} />
                <MetricCard 
                  label="Avg Function Length" 
                  value={`${submission.metrics.averageFunctionLength.toFixed(1)} lines`} 
                />
                {submission.metrics.complexityScore !== undefined && (
                  <MetricCard 
                    label="Complexity Score" 
                    value={submission.metrics.complexityScore}
                    variant={submission.metrics.complexityScore > 10 ? 'warning' : 'default'}
                  />
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {submission.reviewerNotes && (
          <TabsContent value="review">
            <Card>
              <CardHeader>
                <CardTitle>Review Notes</CardTitle>
                <CardDescription>
                  Feedback from the reviewer
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="bg-muted p-4 rounded-lg">
                  <p className="whitespace-pre-wrap">{submission.reviewerNotes}</p>
                </div>
                {submission.reviewedBy && (
                  <div className="mt-4 text-sm text-muted-foreground">
                    <p>Reviewed by: {submission.reviewerName || 'Unknown'}</p>
                    {submission.reviewedAt && (
                      <p>Reviewed: {formatDate(new Date(submission.reviewedAt))}</p>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        )}
      </Tabs>
    </div>
  );
}
