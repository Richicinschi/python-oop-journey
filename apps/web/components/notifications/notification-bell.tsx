'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Bell, CheckCircle, Clock } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { ScrollArea } from '@/components/ui/scroll-area';
import { useSubmissions } from '@/lib/hooks/use-submissions';
import { SubmissionStatus } from '@/lib/api';
import { formatDistanceToNow } from '@/lib/utils';
import { toast } from 'sonner';

interface Notification {
  id: string;
  type: 'review_complete' | 'comment' | 'system';
  title: string;
  message: string;
  submissionId?: string;
  submissionStatus?: SubmissionStatus;
  createdAt: Date;
  read: boolean;
}

export function NotificationBell() {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [open, setOpen] = useState(false);
  
  // Fetch submissions to check for status changes
  const { data: submissions } = useSubmissions();

  // Generate notifications from submission data
  useEffect(() => {
    if (!submissions?.items) return;

    const newNotifications: Notification[] = [];
    
    submissions.items.forEach((submission) => {
      // Only create notifications for reviewed submissions
      if (submission.status !== 'pending_review') {
        const statusLabels: Record<SubmissionStatus, string> = {
          approved: 'Project Approved!',
          needs_work: 'Project Needs Work',
          exemplary: 'Exemplary Project!',
          pending_review: 'Pending Review',
        };

        const statusMessages: Record<SubmissionStatus, string> = {
          approved: 'Your project has been approved. Great job!',
          needs_work: 'Your project needs some improvements. Check the review notes.',
          exemplary: 'Outstanding work! Your project has been marked as exemplary.',
          pending_review: 'Your project is pending review.',
        };

        newNotifications.push({
          id: `submission-${submission.id}`,
          type: 'review_complete',
          title: statusLabels[submission.status],
          message: statusMessages[submission.status],
          submissionId: submission.id,
          submissionStatus: submission.status,
          createdAt: new Date(submission.submittedAt),
          read: false,
        });
      }
    });

    // Sort by date, newest first
    newNotifications.sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime());
    
    setNotifications(newNotifications);
    setUnreadCount(newNotifications.filter(n => !n.read).length);
  }, [submissions]);

  // Show toast for new notifications
  useEffect(() => {
    const handle = setTimeout(() => {
      const unreadApproved = notifications.find(
        n => n.type === 'review_complete' && n.submissionStatus === 'approved' && !n.read
      );
      
      if (unreadApproved) {
        toast.success('Project Approved!', {
          description: unreadApproved.message,
          action: {
            label: 'View',
            onClick: () => {
              window.location.href = `/submissions/${unreadApproved.submissionId}`;
            },
          },
        });
      }
    }, 1000);

    return () => clearTimeout(handle);
  }, [notifications]);

  const markAsRead = (notificationId: string) => {
    setNotifications(prev =>
      prev.map(n => (n.id === notificationId ? { ...n, read: true } : n))
    );
    setUnreadCount(prev => Math.max(0, prev - 1));
  };

  const markAllAsRead = () => {
    setNotifications(prev => prev.map(n => ({ ...n, read: true })));
    setUnreadCount(0);
  };

  const clearAll = () => {
    setNotifications([]);
    setUnreadCount(0);
  };

  const getStatusIcon = (status?: SubmissionStatus) => {
    switch (status) {
      case 'approved':
      case 'exemplary':
        return <CheckCircle className="w-4 h-4 text-green-600" />;
      case 'needs_work':
        return <Clock className="w-4 h-4 text-red-600" />;
      default:
        return <Bell className="w-4 h-4" />;
    }
  };

  return (
    <DropdownMenu open={open} onOpenChange={setOpen}>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon" className="relative">
          <Bell className="h-5 w-5" />
          {unreadCount > 0 && (
            <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
              {unreadCount > 9 ? '9+' : unreadCount}
            </span>
          )}
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-80">
        <div className="flex items-center justify-between px-3 py-2 border-b">
          <span className="font-semibold">Notifications</span>
          <div className="flex items-center gap-1">
            {unreadCount > 0 && (
              <Button variant="ghost" size="sm" onClick={markAllAsRead}>
                Mark all read
              </Button>
            )}
            {notifications.length > 0 && (
              <Button variant="ghost" size="sm" onClick={clearAll}>
                Clear
              </Button>
            )}
          </div>
        </div>
        
        <ScrollArea className="h-[300px]">
          {notifications.length === 0 ? (
            <div className="py-8 text-center text-muted-foreground">
              <Bell className="w-8 h-8 mx-auto mb-2 opacity-50" />
              <p className="text-sm">No notifications yet</p>
              <p className="text-xs">Submit projects to get updates</p>
            </div>
          ) : (
            <div className="divide-y">
              {notifications.map((notification) => (
                <DropdownMenuItem
                  key={notification.id}
                  className={`p-3 cursor-pointer ${!notification.read ? 'bg-primary/5' : ''}`}
                  onClick={() => {
                    markAsRead(notification.id);
                    if (notification.submissionId) {
                      window.location.href = `/submissions/${notification.submissionId}`;
                    }
                    setOpen(false);
                  }}
                >
                  <div className="flex items-start gap-3 w-full">
                    <div className="mt-0.5">
                      {getStatusIcon(notification.submissionStatus)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="font-medium text-sm">{notification.title}</p>
                      <p className="text-xs text-muted-foreground line-clamp-2">
                        {notification.message}
                      </p>
                      <p className="text-xs text-muted-foreground mt-1">
                        {formatDistanceToNow(notification.createdAt)}
                      </p>
                    </div>
                    {!notification.read && (
                      <span className="w-2 h-2 bg-primary rounded-full flex-shrink-0 mt-1" />
                    )}
                  </div>
                </DropdownMenuItem>
              ))}
            </div>
          )}
        </ScrollArea>
        
        <DropdownMenuSeparator />
        <DropdownMenuItem asChild>
          <Link href="/submissions" className="w-full text-center cursor-pointer">
            View all submissions
          </Link>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
