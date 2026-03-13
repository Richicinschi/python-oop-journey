'use client';

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { CodeEditor } from './code-editor';
import { AlertTriangle, Eye, BookOpen } from 'lucide-react';
import { useState } from 'react';
import { useTheme } from '@/components/theme-provider';

interface SolutionModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  solutionCode: string;
  userCode: string;
}

export function SolutionModal({
  isOpen,
  onClose,
  onConfirm,
  solutionCode,
  userCode,
}: SolutionModalProps) {
  const [showingSolution, setShowingSolution] = useState(false);
  const { systemTheme } = useTheme();
  const isDark = systemTheme === 'dark';

  const handleConfirm = () => {
    setShowingSolution(true);
    onConfirm();
  };

  const handleClose = () => {
    setShowingSolution(false);
    onClose();
  };

  return (
    <Dialog open={isOpen} onOpenChange={handleClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] flex flex-col">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            {showingSolution ? (
              <>
                <BookOpen className="h-5 w-5" />
                Solution
              </>
            ) : (
              <>
                <AlertTriangle className="h-5 w-5 text-yellow-500" />
                Are you sure?
              </>
            )}
          </DialogTitle>
          <DialogDescription>
            {showingSolution
              ? "Here's the reference solution. Compare it with your approach."
              : "Viewing the solution will mark this problem. We recommend trying your best first!"}
          </DialogDescription>
        </DialogHeader>

        {showingSolution ? (
          <div className="grid md:grid-cols-2 gap-4 flex-1 min-h-[400px]">
            <div className="flex flex-col">
              <h4 className="text-sm font-medium mb-2">Your Code</h4>
              <div className="flex-1 border rounded-lg overflow-hidden">
                <CodeEditor
                  value={userCode}
                  onChange={() => {}}
                  height="100%"
                  readOnly
                />
              </div>
            </div>
            <div className="flex flex-col">
              <h4 className="text-sm font-medium mb-2">Solution</h4>
              <div className="flex-1 border rounded-lg overflow-hidden">
                <CodeEditor
                  value={solutionCode}
                  onChange={() => {}}
                  height="100%"
                  readOnly
                />
              </div>
            </div>
          </div>
        ) : (
          <div className="py-6 text-center space-y-4">
            <div className="w-16 h-16 bg-yellow-500/10 rounded-full flex items-center justify-center mx-auto">
              <Eye className="h-8 w-8 text-yellow-500" />
            </div>
            <div className="space-y-2">
              <p className="text-muted-foreground">
                Looking at the solution before attempting the problem yourself
                can limit your learning.
              </p>
              <p className="text-sm text-muted-foreground">
                Consider using hints first, or taking a break if you're stuck.
              </p>
            </div>
          </div>
        )}

        <DialogFooter className="gap-2">
          {showingSolution ? (
            <Button onClick={handleClose}>Close</Button>
          ) : (
            <>
              <Button variant="outline" onClick={handleClose}>
                Cancel
              </Button>
              <Button onClick={handleConfirm} variant="secondary">
                <Eye className="mr-2 h-4 w-4" />
                Show Solution
              </Button>
            </>
          )}
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
