'use client';

import { useState } from 'react';
import { useSubmitProject } from '@/lib/hooks/use-submissions';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Separator } from '@/components/ui/separator';
import {
  CheckCircle,
  AlertCircle,
  FileCode,
  Eye,
  Loader2,
  Send,
  Trophy
} from 'lucide-react';
import Link from 'next/link';

interface SubmitModalProps {
  isOpen: boolean;
  onClose: () => void;
  projectSlug: string;
  weekSlug?: string;
  daySlug?: string;
  files: Record<string, string>;
  testResults?: {
    total: number;
    passed: number;
    failed: number;
  } | null;
}

interface ChecklistItemProps {
  checked: boolean;
  label: string;
  description?: string;
}

function ChecklistItem({ checked, label, description }: ChecklistItemProps) {
  return (
    <div className="flex items-start gap-3">
      <div className={`mt-0.5 ${checked ? 'text-green-600' : 'text-muted-foreground'}`}>
        {checked ? (
          <CheckCircle className="w-5 h-5" />
        ) : (
          <AlertCircle className="w-5 h-5" />
        )}
      </div>
      <div className="flex-1">
        <p className={`text-sm font-medium ${checked ? 'text-green-700' : ''}`}>{label}</p>
        {description && (
          <p className="text-xs text-muted-foreground">{description}</p>
        )}
      </div>
    </div>
  );
}

export function SubmitModal({
  isOpen,
  onClose,
  projectSlug,
  weekSlug,
  daySlug,
  files,
  testResults,
}: SubmitModalProps) {
  const [step, setStep] = useState<'checklist' | 'confirm' | 'success'>('checklist');
  const [confirmed, setConfirmed] = useState({
    testsPass: false,
    codeReviewed: false,
    requirementsMet: false,
  });
  const [showcaseOptIn, setShowcaseOptIn] = useState(false);
  const [submissionId, setSubmissionId] = useState<string>('');

  const submitMutation = useSubmitProject();

  const allConfirmed = confirmed.testsPass && confirmed.codeReviewed && confirmed.requirementsMet;
  const testsPass = testResults ? testResults.failed === 0 && testResults.total > 0 : false;
  const hasFiles = Object.keys(files).length > 0;

  const handleSubmit = async () => {
    try {
      const result = await submitMutation.mutateAsync({
        projectSlug,
        files,
        options: {
          weekSlug,
          daySlug,
          showcaseOptIn,
        },
      });
      setSubmissionId(result.submissionId);
      setStep('success');
    } catch (error) {
      // Error is handled by the mutation
    }
  };

  const handleClose = () => {
    setStep('checklist');
    setConfirmed({
      testsPass: false,
      codeReviewed: false,
      requirementsMet: false,
    });
    setShowcaseOptIn(false);
    onClose();
  };

  return (
    <Dialog open={isOpen} onOpenChange={handleClose}>
      <DialogContent className="max-w-lg">
        {step === 'checklist' && (
          <>
            <DialogHeader>
              <DialogTitle className="flex items-center gap-2">
                <Send className="w-5 h-5" />
                Submit Project
              </DialogTitle>
              <DialogDescription>
                Before submitting, please review the checklist below.
              </DialogDescription>
            </DialogHeader>

            <div className="space-y-4 py-4">
              <div className="space-y-4">
                <ChecklistItem
                  checked={testsPass}
                  label="All tests passing"
                  description={
                    testsPass
                      ? `${testResults?.passed} of ${testResults?.total} tests passed`
                      : `${testResults?.failed || 0} tests failed - fix them before submitting`
                  }
                />

                <ChecklistItem
                  checked={hasFiles}
                  label="Code files present"
                  description={
                    hasFiles
                      ? `${Object.keys(files).length} file(s) ready`
                      : 'No code files to submit'
                  }
                />

                <div className="pt-2">
                  <p className="text-sm font-medium mb-3">Confirm the following:</p>
                  
                  <div className="space-y-3">
                    <div className="flex items-start gap-3">
                      <Checkbox
                        id="testsPass"
                        checked={confirmed.testsPass}
                        onCheckedChange={(checked) =>
                          setConfirmed((prev) => ({ ...prev, testsPass: checked as boolean }))
                        }
                      />
                      <Label htmlFor="testsPass" className="text-sm cursor-pointer">
                        I have verified all tests pass
                      </Label>
                    </div>

                    <div className="flex items-start gap-3">
                      <Checkbox
                        id="codeReviewed"
                        checked={confirmed.codeReviewed}
                        onCheckedChange={(checked) =>
                          setConfirmed((prev) => ({ ...prev, codeReviewed: checked as boolean }))
                        }
                      />
                      <Label htmlFor="codeReviewed" className="text-sm cursor-pointer">
                        I have reviewed my code for quality and best practices
                      </Label>
                    </div>

                    <div className="flex items-start gap-3">
                      <Checkbox
                        id="requirementsMet"
                        checked={confirmed.requirementsMet}
                        onCheckedChange={(checked) =>
                          setConfirmed((prev) => ({ ...prev, requirementsMet: checked as boolean }))
                        }
                      />
                      <Label htmlFor="requirementsMet" className="text-sm cursor-pointer">
                        I have met all project requirements
                      </Label>
                    </div>
                  </div>
                </div>
              </div>

              {!testsPass && (
                <Alert variant="destructive">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>
                    Some tests are failing. It&apos;s recommended to fix them before submitting.
                  </AlertDescription>
                </Alert>
              )}
            </div>

            <DialogFooter>
              <Button variant="outline" onClick={handleClose}>
                Cancel
              </Button>
              <Button
                onClick={() => setStep('confirm')}
                disabled={!allConfirmed}
              >
                Continue
                <Send className="w-4 h-4 ml-2" />
              </Button>
            </DialogFooter>
          </>
        )}

        {step === 'confirm' && (
          <>
            <DialogHeader>
              <DialogTitle>Confirm Submission</DialogTitle>
              <DialogDescription>
                Review your submission details before confirming.
              </DialogDescription>
            </DialogHeader>

            <div className="space-y-4 py-4">
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Project</span>
                  <span className="font-medium">{projectSlug}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Files</span>
                  <span className="font-medium">{Object.keys(files).length}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Tests</span>
                  <span className="font-medium">
                    {testResults?.passed}/{testResults?.total} passed
                  </span>
                </div>
              </div>

              <Separator />

              <div className="flex items-start gap-3">
                <Checkbox
                  id="showcaseOptIn"
                  checked={showcaseOptIn}
                  onCheckedChange={(checked) => setShowcaseOptIn(checked as boolean)}
                />
                <div>
                  <Label htmlFor="showcaseOptIn" className="text-sm cursor-pointer">
                    Allow my solution to be showcased
                  </Label>
                  <p className="text-xs text-muted-foreground">
                    Opt-in to have your exemplary solution featured for other students to learn from
                  </p>
                </div>
              </div>

              <Alert>
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>
                  Your submission will be reviewed within 24-48 hours. You&apos;ll receive a notification when the review is complete.
                </AlertDescription>
              </Alert>
            </div>

            <DialogFooter>
              <Button variant="outline" onClick={() => setStep('checklist')}>
                Back
              </Button>
              <Button
                onClick={handleSubmit}
                disabled={submitMutation.isPending}
              >
                {submitMutation.isPending ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Submitting...
                  </>
                ) : (
                  <>
                    Submit for Review
                    <Send className="w-4 h-4 ml-2" />
                  </>
                )}
              </Button>
            </DialogFooter>
          </>
        )}

        {step === 'success' && (
          <>
            <DialogHeader>
              <DialogTitle className="flex items-center gap-2 text-green-600">
                <Trophy className="w-6 h-6" />
                Submission Successful!
              </DialogTitle>
              <DialogDescription>
                Your project has been submitted for review.
              </DialogDescription>
            </DialogHeader>

            <div className="py-6 text-center">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <CheckCircle className="w-8 h-8 text-green-600" />
              </div>
              <p className="text-sm text-muted-foreground mb-2">Submission ID</p>
              <p className="text-lg font-mono font-medium">{submissionId}</p>
            </div>

            <div className="space-y-3">
              <Button className="w-full" asChild>
                <Link href={`/submissions/${submissionId}`}>
                  <Eye className="w-4 h-4 mr-2" />
                  View Submission
                </Link>
              </Button>
              <Button variant="outline" className="w-full" asChild>
                <Link href="/submissions">
                  <FileCode className="w-4 h-4 mr-2" />
                  View All Submissions
                </Link>
              </Button>
            </div>
          </>
        )}
      </DialogContent>
    </Dialog>
  );
}
