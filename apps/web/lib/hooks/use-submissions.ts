/** React hooks for submissions. */

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api, SubmissionStatus, Submission, SubmissionList, SubmissionResponse, SubmissionChecklist, GamificationStats } from '@/lib/api';
import { toast } from 'sonner';

// Query keys
const submissionKeys = {
  all: ['submissions'] as const,
  lists: () => [...submissionKeys.all, 'list'] as const,
  list: (filters: { status?: SubmissionStatus }) => [...submissionKeys.lists(), filters] as const,
  details: () => [...submissionKeys.all, 'detail'] as const,
  detail: (id: string) => [...submissionKeys.details(), id] as const,
  files: (id: string) => [...submissionKeys.detail(id), 'files'] as const,
  comments: (id: string) => [...submissionKeys.detail(id), 'comments'] as const,
  gamification: () => [...submissionKeys.all, 'gamification'] as const,
  checklist: (projectSlug: string) => [...submissionKeys.all, 'checklist', projectSlug] as const,
};

/**
 * Hook to fetch user's submissions
 */
export function useSubmissions(status?: SubmissionStatus) {
  return useQuery({
    queryKey: submissionKeys.list({ status }),
    queryFn: () => api.submissions.list(status),
  });
}

/**
 * Hook to fetch a specific submission
 */
export function useSubmission(id: string) {
  return useQuery({
    queryKey: submissionKeys.detail(id),
    queryFn: () => api.submissions.get(id),
    enabled: !!id,
  });
}

/**
 * Hook to fetch submission files
 */
export function useSubmissionFiles(id: string) {
  return useQuery({
    queryKey: submissionKeys.files(id),
    queryFn: () => api.submissions.getFiles(id),
    enabled: !!id,
  });
}

/**
 * Hook to fetch gamification stats
 */
export function useGamificationStats() {
  return useQuery({
    queryKey: submissionKeys.gamification(),
    queryFn: () => api.submissions.getGamificationStats(),
  });
}

/**
 * Hook to submit a project
 */
export function useSubmitProject() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      projectSlug,
      files,
      options,
    }: {
      projectSlug: string;
      files: Record<string, string>;
      options?: { weekSlug?: string; daySlug?: string; showcaseOptIn?: boolean };
    }) => api.submissions.submit(projectSlug, files, options),
    onSuccess: (data) => {
      // Invalidate submissions list
      queryClient.invalidateQueries({ queryKey: submissionKeys.lists() });
      queryClient.invalidateQueries({ queryKey: submissionKeys.gamification() });
      
      if (data.checklist.canSubmit) {
        toast.success('Project submitted successfully!', {
          description: `Submission ID: ${data.submissionId}`,
        });
      } else {
        toast.warning('Project submitted with warnings', {
          description: data.checklist.warnings.join(', '),
        });
      }
    },
    onError: (error: Error) => {
      toast.error('Failed to submit project', {
        description: error.message,
      });
    },
  });
}

/**
 * Hook to fetch submission checklist
 */
export function useSubmissionChecklist(projectSlug: string, files: Record<string, string>) {
  return useQuery({
    queryKey: submissionKeys.checklist(projectSlug),
    queryFn: () => api.submissions.getChecklist(projectSlug, files),
    enabled: !!projectSlug && Object.keys(files).length > 0,
  });
}

/**
 * Hook to fetch submission comments
 */
export function useSubmissionComments(submissionId: string, filePath?: string) {
  return useQuery({
    queryKey: [...submissionKeys.comments(submissionId), filePath],
    queryFn: () => api.submissions.getComments(submissionId, filePath),
    enabled: !!submissionId,
  });
}

/**
 * Hook to add a comment to a submission
 */
export function useAddComment() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      submissionId,
      filePath,
      lineNumber,
      content,
    }: {
      submissionId: string;
      filePath: string;
      lineNumber: number;
      content: string;
    }) => api.submissions.addComment(submissionId, { filePath, lineNumber, content }),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: submissionKeys.comments(variables.submissionId),
      });
      toast.success('Comment added');
    },
    onError: (error: Error) => {
      toast.error('Failed to add comment', {
        description: error.message,
      });
    },
  });
}

// Admin hooks

/**
 * Hook to fetch the review queue (admin only)
 */
export function useReviewQueue(limit?: number) {
  return useQuery({
    queryKey: ['admin', 'review-queue', limit],
    queryFn: () => api.admin.getReviewQueue(limit),
  });
}

/**
 * Hook to review a submission (admin only)
 */
export function useReviewSubmission() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      submissionId,
      status,
      reviewerNotes,
      isExemplary,
    }: {
      submissionId: string;
      status: SubmissionStatus;
      reviewerNotes?: string;
      isExemplary?: boolean;
    }) => api.admin.reviewSubmission(submissionId, { status, reviewerNotes, isExemplary }),
    onSuccess: (_, variables) => {
      // Invalidate submission detail
      queryClient.invalidateQueries({
        queryKey: submissionKeys.detail(variables.submissionId),
      });
      // Invalidate review queue
      queryClient.invalidateQueries({ queryKey: ['admin', 'review-queue'] });
      // Invalidate submissions list
      queryClient.invalidateQueries({ queryKey: submissionKeys.lists() });
      
      toast.success('Review submitted');
    },
    onError: (error: Error) => {
      toast.error('Failed to submit review', {
        description: error.message,
      });
    },
  });
}
