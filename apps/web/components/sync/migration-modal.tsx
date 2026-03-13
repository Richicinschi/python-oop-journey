'use client';

/**
 * Data Migration Modal
 * 
 * Shown when legacy localStorage data is detected on login.
 * Allows users to migrate their data to the new IndexedDB system.
 */

import { useEffect, useState } from 'react';
import { 
  Database, 
  ArrowRight, 
  CheckCircle2, 
  AlertCircle,
  Loader2,
  X,
} from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { cn } from '@/lib/utils';
import {
  hasLegacyData,
  migrateLegacyData,
  clearLegacyData,
  estimateMigrationSize,
  type MigrationResult,
  type MigrationProgress,
} from '@/lib/migrate-local-data';

interface MigrationModalProps {
  isOpen: boolean;
  onClose: () => void;
  onComplete?: (result: MigrationResult) => void;
}

export function MigrationModal({ isOpen, onClose, onComplete }: MigrationModalProps) {
  const [step, setStep] = useState<'detected' | 'migrating' | 'complete' | 'error'>('detected');
  const [progress, setProgress] = useState<MigrationProgress | null>(null);
  const [result, setResult] = useState<MigrationResult | null>(null);
  const [estimatedSize, setEstimatedSize] = useState({ progressItems: 0, draftItems: 0, bookmarkItems: 0, totalSize: 0 });

  useEffect(() => {
    if (isOpen) {
      setStep('detected');
      setProgress(null);
      setResult(null);
      setEstimatedSize(estimateMigrationSize());
    }
  }, [isOpen]);

  const handleMigrate = async () => {
    setStep('migrating');

    const migrationResult = await migrateLegacyData({
      onProgress: (p) => setProgress(p),
      onComplete: (r) => {
        setResult(r);
        setStep(r.success ? 'complete' : 'error');
        if (r.success) {
          clearLegacyData();
        }
        onComplete?.(r);
      },
    });

    if (!migrationResult.success && migrationResult.errors.length > 0) {
      setResult(migrationResult);
      setStep('error');
    }
  };

  const handleSkip = () => {
    onClose();
  };

  const handleDismiss = () => {
    if (step === 'complete' || step === 'error') {
      onClose();
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={handleDismiss}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Database className="h-5 w-5 text-primary" />
            {step === 'detected' && 'Legacy Data Detected'}
            {step === 'migrating' && 'Migrating Your Data...'}
            {step === 'complete' && 'Migration Complete!'}
            {step === 'error' && 'Migration Failed'}
          </DialogTitle>
          <DialogDescription>
            {step === 'detected' && 'We found progress data from your previous sessions.'}
            {step === 'migrating' && 'Please wait while we transfer your data to the new system.'}
            {step === 'complete' && 'Your data has been successfully migrated.'}
            {step === 'error' && 'Some items could not be migrated.'}
          </DialogDescription>
        </DialogHeader>

        {/* Detection Step */}
        {step === 'detected' && (
          <>
            <div className="py-4">
              <div className="space-y-3">
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Completed Problems</span>
                  <span className="font-medium">{estimatedSize.progressItems}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Code Drafts</span>
                  <span className="font-medium">{estimatedSize.draftItems}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Bookmarks</span>
                  <span className="font-medium">{estimatedSize.bookmarkItems}</span>
                </div>
              </div>

              <Alert className="mt-4">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>
                  Your data will be transferred to the new sync system and uploaded to your account.
                </AlertDescription>
              </Alert>
            </div>

            <DialogFooter className="gap-2">
              <Button variant="outline" onClick={handleSkip}>
                Skip for Now
              </Button>
              <Button onClick={handleMigrate} className="gap-2">
                Migrate Data
                <ArrowRight className="h-4 w-4" />
              </Button>
            </DialogFooter>
          </>
        )}

        {/* Migrating Step */}
        {step === 'migrating' && progress && (
          <div className="py-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium">
                {progress.currentItem ? `Processing: ${progress.currentItem}` : 'Finalizing...'}
              </span>
              <span className="text-sm text-muted-foreground">
                {progress.processed} / {progress.total}
              </span>
            </div>
            <Progress 
              value={(progress.processed / progress.total) * 100} 
              className="h-2"
            />
            {progress.errors.length > 0 && (
              <p className="text-xs text-amber-600 mt-2">
                {progress.errors.length} errors encountered (will retry)
              </p>
            )}
          </div>
        )}

        {/* Complete Step */}
        {step === 'complete' && result && (
          <>
            <div className="py-4">
              <div className="flex flex-col items-center gap-4">
                <CheckCircle2 className="h-12 w-12 text-green-500" />
                <div className="text-center">
                  <p className="font-medium">Successfully Migrated</p>
                  <p className="text-sm text-muted-foreground">
                    {result.migrated} items transferred
                  </p>
                </div>
              </div>
            </div>
            <DialogFooter>
              <Button onClick={handleDismiss} className="w-full">
                Continue
              </Button>
            </DialogFooter>
          </>
        )}

        {/* Error Step */}
        {step === 'error' && result && (
          <>
            <div className="py-4">
              <div className="flex flex-col items-center gap-4">
                <AlertCircle className="h-12 w-12 text-red-500" />
                <div className="text-center">
                  <p className="font-medium">Migration Incomplete</p>
                  <p className="text-sm text-muted-foreground">
                    {result.migrated} items migrated, {result.errors.length} errors
                  </p>
                </div>
              </div>
              {result.errors.length > 0 && (
                <div className="mt-4 max-h-32 overflow-y-auto text-xs bg-red-50 p-3 rounded">
                  {result.errors.map((error, i) => (
                    <p key={i} className="text-red-700">{error}</p>
                  ))}
                </div>
              )}
            </div>
            <DialogFooter className="gap-2">
              <Button variant="outline" onClick={handleDismiss}>
                Skip Remaining
              </Button>
              <Button onClick={handleMigrate}>
                Try Again
              </Button>
            </DialogFooter>
          </>
        )}
      </DialogContent>
    </Dialog>
  );
}

export default MigrationModal;
