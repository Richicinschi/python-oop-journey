'use client';

import { useState } from 'react';
import { useReviewQueue, useReviewSubmission } from '@/lib/hooks/use-submissions';
import { SubmissionStatus } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import { Textarea } from '@/components/ui/textarea';
import { 
  Clock, 
  CheckCircle, 
  XCircle, 
  Star, 
  FileCode, 
  User,
  BarChart3,
  CheckSquare,
  AlertCircle,
  Award,
  RefreshCw,
  ChevronRight,
  Eye
} from 'lucide-react';
import { formatDistanceToNow } from '@/lib/utils';
import { toast } from 'sonner';

const statusOptions: { value: SubmissionStatus; label: string; icon: React.ReactNode; color: string }[] = [
  { value: 'approved', label: 'Approve', icon: <CheckCircle className="w-4 h-4" />, color: 'bg-green-500 hover:bg-green-600' },
  { value: 'needs_work', label: 'Needs Work', icon: <XCircle className="w-4 h-4" />, color: 'bg-red-500 hover:bg-red-600' },
  { value: 'exemplary', label: 'Exemplary', icon: <Award className="w-4 h-4" />, color: 'bg-purple-500 hover:bg-purple-600' },
];

interface ReviewQueueItemProps {
  item: import('@/lib/api').ReviewQueueItem;
  isSelected: boolean;
  onSelect: () => void;
}

function ReviewQueueItem({ item, isSelected, onSelect }: ReviewQueueItemProps) {
  return (
    <button
      onClick={onSelect}
      className={`w-full text-left p-3 rounded-lg border transition-colors ${
        isSelected 
          ? 'border-primary bg-primary/5' 
          : 'border-border hover:border-primary/50 hover:bg-muted/50'
      }`}
    >
      <div className="flex items-start justify-between gap-2">
        <div className="flex-1 min-w-0">
          <p className="font-medium truncate">{item.projectName || item.projectSlug}</p>
          <p className="text-sm text-muted-foreground flex items-center gap-1">
            <User className="w-3 h-3" />
            {item.userName || 'Unknown User'}
          </p>
        </div>
        <ChevronRight className={`w-4 h-4 flex-shrink-0 transition-transform ${isSelected ? 'rotate-90' : ''}`} />
      </div>
      <div className="flex items-center gap-3 mt-2 text-xs text-muted-foreground">
        <span className="flex items-center gap-1">
          <Clock className="w-3 h-3" />
          Waiting {item.waitingHours.toFixed(1)}h
        </span>
        <span className="flex items-center gap-1">
          <CheckCircle className="w-3 h-3" />
          {item.testSummary.passed}/{item.testSummary.total}
        </span>
        <span className="flex items-center gap-1">
          <FileCode className="w-3 h-3" />
          {item.metricsSummary.linesOfCode} lines
        </span>
      </div>
    </button>
  );
}

function SubmissionDetail({ 
  submissionId, 
  onReviewed 
}: { 
  submissionId: string; 
  onReviewed: () => void;
}) {
  const [reviewerNotes, setReviewerNotes] = useState('');
  const [selectedStatus, setSelectedStatus] = useState<SubmissionStatus | null>(null);
  const reviewMutation = useReviewSubmission();

  // In a real app, you'd fetch the full submission details here
  // For now, we'll use the review queue data

  const handleReview = async (status: SubmissionStatus) => {
    try {
      await reviewMutation.mutateAsync({
        submissionId,
        status,
        reviewerNotes,
        isExemplary: status === 'exemplary',
      });
      toast.success(`Submission ${status === 'approved' ? 'approved' : status === 'exemplary' ? 'marked as exemplary' : 'marked as needs work'}`);
      setReviewerNotes('');
      setSelectedStatus(null);
      onReviewed();
    } catch (error) {
      toast.error('Failed to submit review');
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Review Submission</CardTitle>
          <CardDescription>
            Review the code and provide feedback to the student
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium mb-2 block">Review Notes</label>
            <Textarea
              value={reviewerNotes}
              onChange={(e) => setReviewerNotes(e.target.value)}
              placeholder="Provide constructive feedback..."
              className="min-h-[120px]"
            />
          </div>

          <div>
            <label className="text-sm font-medium mb-2 block">Decision</label>
            <div className="grid grid-cols-3 gap-2">
              {statusOptions.map((option) => (
                <Button
                  key={option.value}
                  variant={selectedStatus === option.value ? 'default' : 'outline'}
                  className={selectedStatus === option.value ? option.color : ''}
                  onClick={() => setSelectedStatus(option.value)}
                  disabled={reviewMutation.isPending}
                >
                  {option.icon}
                  <span className="ml-2">{option.label}</span>
                </Button>
              ))}
            </div>
          </div>

          {selectedStatus && (
            <Button 
              className="w-full"
              onClick={() => handleReview(selectedStatus)}
              disabled={reviewMutation.isPending}
            >
              {reviewMutation.isPending ? (
                <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
              ) : (
                <CheckSquare className="w-4 h-4 mr-2" />
              )}
              Submit Review
            </Button>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          <Button variant="outline" className="w-full justify-start">
            <Eye className="w-4 h-4 mr-2" />
            View Full Details
          </Button>
          <Button variant="outline" className="w-full justify-start">
            <FileCode className="w-4 h-4 mr-2" />
            Open in Editor
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}

function StatsCard({ 
  title, 
  value, 
  subtitle,
  icon: Icon 
}: { 
  title: string; 
  value: string | number; 
  subtitle?: string;
  icon: React.ElementType;
}) {
  return (
    <Card>
      <CardContent className="p-4">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-primary/10 rounded-lg">
            <Icon className="w-5 h-5 text-primary" />
          </div>
          <div>
            <p className="text-sm text-muted-foreground">{title}</p>
            <p className="text-2xl font-bold">{value}</p>
            {subtitle && <p className="text-xs text-muted-foreground">{subtitle}</p>}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export default function ReviewDashboardPage() {
  const [selectedSubmissionId, setSelectedSubmissionId] = useState<string | null>(null);
  const { data: queue, isLoading, refetch } = useReviewQueue(50);

  const selectedItem = queue?.items.find(item => item.id === selectedSubmissionId);

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold">Review Dashboard</h1>
          <p className="text-muted-foreground mt-1">
            Review and provide feedback on student submissions
          </p>
        </div>
        <Button variant="outline" onClick={() => refetch()}>
          <RefreshCw className="w-4 h-4 mr-2" />
          Refresh
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <StatsCard
          title="Pending Reviews"
          value={queue?.pendingCount || 0}
          subtitle="in queue"
          icon={Clock}
        />
        <StatsCard
          title="My Reviews Today"
          value={queue?.myReviewsToday || 0}
          subtitle="submissions reviewed"
          icon={CheckCircle}
        />
        <StatsCard
          title="Avg Review Time"
          value={queue?.avgReviewTimeHours ? `${queue.avgReviewTimeHours.toFixed(1)}h` : 'N/A'}
          subtitle="per submission"
          icon={BarChart3}
        />
        <StatsCard
          title="Priority Score"
          value={selectedItem?.priorityScore.toFixed(1) || '-'}
          subtitle="selected submission"
          icon={Star}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <Card className="h-[600px] flex flex-col">
            <CardHeader>
              <CardTitle>Review Queue</CardTitle>
              <CardDescription>
                {queue?.pendingCount || 0} submissions waiting
              </CardDescription>
            </CardHeader>
            <CardContent className="flex-1 overflow-hidden">
              {isLoading ? (
                <div className="space-y-3">
                  {[...Array(5)].map((_, i) => (
                    <Skeleton key={i} className="h-20 w-full" />
                  ))}
                </div>
              ) : queue?.items.length === 0 ? (
                <div className="text-center py-8 text-muted-foreground">
                  <CheckCircle className="w-12 h-12 mx-auto mb-4 opacity-50" />
                  <p>No pending reviews</p>
                  <p className="text-sm">All caught up!</p>
                </div>
              ) : (
                <ScrollArea className="h-full pr-4">
                  <div className="space-y-2">
                    {queue?.items.map((item) => (
                      <ReviewQueueItem
                        key={item.id}
                        item={item}
                        isSelected={selectedSubmissionId === item.id}
                        onSelect={() => setSelectedSubmissionId(item.id)}
                      />
                    ))}
                  </div>
                </ScrollArea>
              )}
            </CardContent>
          </Card>
        </div>

        <div className="lg:col-span-2">
          {selectedSubmissionId && selectedItem ? (
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div>
                      <CardTitle>{selectedItem.projectName || selectedItem.projectSlug}</CardTitle>
                      <CardDescription className="flex items-center gap-4 mt-1">
                        <span className="flex items-center gap-1">
                          <User className="w-3 h-3" />
                          {selectedItem.userName || 'Unknown User'}
                        </span>
                        <span className="flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          Waiting {selectedItem.waitingHours.toFixed(1)} hours
                        </span>
                      </CardDescription>
                    </div>
                    <Badge variant="secondary" className="text-lg px-3 py-1">
                      #{selectedItem.id.slice(0, 8)}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-3 gap-4 mb-6">
                    <div className="p-3 bg-muted rounded-lg text-center">
                      <p className="text-2xl font-bold">{selectedItem.testSummary.total}</p>
                      <p className="text-xs text-muted-foreground">Total Tests</p>
                    </div>
                    <div className="p-3 bg-green-500/10 rounded-lg text-center">
                      <p className="text-2xl font-bold text-green-600">{selectedItem.testSummary.passed}</p>
                      <p className="text-xs text-muted-foreground">Passed</p>
                    </div>
                    <div className="p-3 bg-muted rounded-lg text-center">
                      <p className="text-2xl font-bold">{selectedItem.metricsSummary.linesOfCode}</p>
                      <p className="text-xs text-muted-foreground">Lines of Code</p>
                    </div>
                  </div>

                  <Separator className="my-4" />

                  <div className="flex gap-4">
                    <Button className="flex-1" variant="outline">
                      <Eye className="w-4 h-4 mr-2" />
                      View Code
                    </Button>
                    <Button className="flex-1" variant="outline">
                      <FileCode className="w-4 h-4 mr-2" />
                      Open in Editor
                    </Button>
                  </div>
                </CardContent>
              </Card>

              <SubmissionDetail
                submissionId={selectedSubmissionId}
                onReviewed={() => {
                  setSelectedSubmissionId(null);
                  refetch();
                }}
              />
            </div>
          ) : (
            <Card className="h-[600px] flex items-center justify-center">
              <div className="text-center p-8">
                <AlertCircle className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
                <h3 className="text-lg font-semibold mb-2">Select a Submission</h3>
                <p className="text-muted-foreground max-w-sm">
                  Choose a submission from the queue to review it and provide feedback to the student.
                </p>
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
