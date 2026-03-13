'use client';

/**
 * Data Export/Import Page
 * 
 * Features:
 * - Export all data as JSON
 * - Import from JSON file
 * - Merge or replace option
 * - Validate imported data
 */

import { useState, useRef, useCallback } from 'react';
import { 
  Download, 
  Upload, 
  FileJson, 
  AlertCircle, 
  CheckCircle2,
  RefreshCw,
  Trash2,
  Database,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import { 
  Dialog, 
  DialogContent, 
  DialogDescription, 
  DialogFooter, 
  DialogHeader, 
  DialogTitle 
} from '@/components/ui/dialog';
import { cn } from '@/lib/utils';
import { 
  exportAllData, 
  importData, 
  deleteDatabase,
  SyncOperation, 
  LocalDraft, 
  LocalProgress, 
  LocalBookmark, 
  CachedCurriculum 
} from '@/lib/offline-db';
import { syncPendingOperations } from '@/lib/sync-engine';

interface ValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
  data?: {
    operations: unknown[];
    drafts: unknown[];
    progress: unknown[];
    bookmarks: unknown[];
    curriculum: unknown[];
    exportedAt: string;
    version: string;
  };
}

export default function DataPage() {
  const [isExporting, setIsExporting] = useState(false);
  const [isImporting, setIsImporting] = useState(false);
  const [importMode, setImportMode] = useState<'merge' | 'replace'>('merge');
  const [validationResult, setValidationResult] = useState<ValidationResult | null>(null);
  const [showImportDialog, setShowImportDialog] = useState(false);
  const [showClearDialog, setShowClearDialog] = useState(false);
  const [lastAction, setLastAction] = useState<{ type: 'success' | 'error'; message: string } | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // ==================== Export ====================

  const handleExport = async () => {
    setIsExporting(true);
    try {
      const data = await exportAllData();
      const exportPayload = {
        ...data,
        version: '1.0',
      };

      // Create download
      const blob = new Blob([JSON.stringify(exportPayload, null, 2)], {
        type: 'application/json',
      });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `oop-journey-backup-${new Date().toISOString().split('T')[0]}.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);

      setLastAction({
        type: 'success',
        message: `Exported ${data.operations.length + data.drafts.length + data.progress.length + data.bookmarks.length} items successfully.`,
      });
    } catch (error) {
      setLastAction({
        type: 'error',
        message: error instanceof Error ? error.message : 'Export failed',
      });
    } finally {
      setIsExporting(false);
    }
  };

  // ==================== Import ====================

  const handleFileSelect = useCallback(async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setIsImporting(true);
    try {
      const text = await file.text();
      const data = JSON.parse(text);
      
      const validation = validateImportData(data);
      setValidationResult(validation);
      
      if (validation.valid) {
        setShowImportDialog(true);
      }
    } catch (error) {
      setValidationResult({
        valid: false,
        errors: ['Failed to parse JSON file'],
        warnings: [],
      });
    } finally {
      setIsImporting(false);
      // Reset file input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  }, []);

  const validateImportData = (data: unknown): ValidationResult => {
    const errors: string[] = [];
    const warnings: string[] = [];

    if (!data || typeof data !== 'object') {
      errors.push('Invalid data format');
      return { valid: false, errors, warnings };
    }

    const exportData = data as Record<string, unknown>;

    // Check required fields
    if (!exportData.version) {
      warnings.push('Missing version field - import may be from an older version');
    }

    if (!exportData.exportedAt) {
      warnings.push('Missing exportedAt timestamp');
    }

    // Validate arrays
    const arrays = ['operations', 'drafts', 'progress', 'bookmarks', 'curriculum'];
    for (const key of arrays) {
      const arr = exportData[key];
      if (arr !== undefined && !Array.isArray(arr)) {
        errors.push(`${key} must be an array`);
      }
    }

    if (errors.length > 0) {
      return { valid: false, errors, warnings };
    }

    return { 
      valid: true, 
      errors, 
      warnings, 
      data: {
        operations: (exportData.operations || []) as unknown[],
        drafts: (exportData.drafts || []) as unknown[],
        progress: (exportData.progress || []) as unknown[],
        bookmarks: (exportData.bookmarks || []) as unknown[],
        curriculum: (exportData.curriculum || []) as unknown[],
        exportedAt: String(exportData.exportedAt || ''),
        version: String(exportData.version || ''),
      },
    };
  };

  const handleImport = async () => {
    if (!validationResult?.data) return;

    setIsImporting(true);
    try {
      const data = validationResult.data;

      // In replace mode, clear existing data first
      if (importMode === 'replace') {
        await deleteDatabase();
      }

      // Import the data
      await importData({
        operations: (data.operations || []) as SyncOperation[],
        drafts: (data.drafts || []) as LocalDraft[],
        progress: (data.progress || []) as LocalProgress[],
        bookmarks: (data.bookmarks || []) as LocalBookmark[],
        curriculum: (data.curriculum || []) as CachedCurriculum[],
      });

      // Trigger sync
      if (navigator.onLine) {
        await syncPendingOperations();
      }

      setLastAction({
        type: 'success',
        message: `Imported ${data.operations.length + data.drafts.length + data.progress.length + data.bookmarks.length} items successfully (${importMode} mode).`,
      });

      setShowImportDialog(false);
      setValidationResult(null);
    } catch (error) {
      setLastAction({
        type: 'error',
        message: error instanceof Error ? error.message : 'Import failed',
      });
    } finally {
      setIsImporting(false);
    }
  };

  // ==================== Clear Data ====================

  const handleClearData = async () => {
    setIsImporting(true);
    try {
      await deleteDatabase();
      setLastAction({
        type: 'success',
        message: 'All local data has been cleared.',
      });
      setShowClearDialog(false);
    } catch (error) {
      setLastAction({
        type: 'error',
        message: error instanceof Error ? error.message : 'Failed to clear data',
      });
    } finally {
      setIsImporting(false);
    }
  };

  return (
    <div className="container max-w-4xl py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight">Data Management</h1>
        <p className="text-muted-foreground mt-2">
          Export, import, and manage your learning data.
        </p>
      </div>

      {lastAction && (
        <Alert 
          className={cn(
            "mb-6",
            lastAction.type === 'success' ? 'border-green-500/50 bg-green-50/50' : 'border-red-500/50 bg-red-50/50'
          )}
        >
          {lastAction.type === 'success' ? (
            <CheckCircle2 className="h-4 w-4 text-green-600" />
          ) : (
            <AlertCircle className="h-4 w-4 text-red-600" />
          )}
          <AlertTitle>{lastAction.type === 'success' ? 'Success' : 'Error'}</AlertTitle>
          <AlertDescription>{lastAction.message}</AlertDescription>
        </Alert>
      )}

      <div className="space-y-6">
        {/* Export Section */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Download className="h-5 w-5" />
              Export Data
            </CardTitle>
            <CardDescription>
              Download all your progress, drafts, bookmarks, and settings as a JSON file.
              This file can be used as a backup or to transfer your data to another device.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button 
              onClick={handleExport} 
              disabled={isExporting}
              className="gap-2"
            >
              {isExporting ? (
                <RefreshCw className="h-4 w-4 animate-spin" />
              ) : (
                <Download className="h-4 w-4" />
              )}
              {isExporting ? 'Exporting...' : 'Export to JSON'}
            </Button>
          </CardContent>
        </Card>

        {/* Import Section */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Upload className="h-5 w-5" />
              Import Data
            </CardTitle>
            <CardDescription>
              Restore your data from a previously exported JSON file.
              Choose whether to merge with existing data or replace it entirely.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Import Mode Selection */}
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Switch
                  id="import-mode"
                  checked={importMode === 'replace'}
                  onCheckedChange={(checked) => 
                    setImportMode(checked ? 'replace' : 'merge')
                  }
                />
                <Label htmlFor="import-mode">
                  {importMode === 'merge' ? 'Merge with existing data' : 'Replace all data'}
                </Label>
              </div>
              <Badge variant={importMode === 'merge' ? 'default' : 'destructive'}>
                {importMode === 'merge' ? 'Safe' : 'Destructive'}
              </Badge>
            </div>

            {importMode === 'replace' && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Warning</AlertTitle>
                <AlertDescription>
                  Replace mode will delete all existing data before importing.
                  This action cannot be undone.
                </AlertDescription>
              </Alert>
            )}

            {/* File Upload */}
            <div className="flex items-center gap-4">
              <input
                ref={fileInputRef}
                type="file"
                accept=".json,application/json"
                onChange={handleFileSelect}
                className="hidden"
                id="import-file"
              />
              <Label htmlFor="import-file" className="cursor-pointer">
                <div className="flex items-center gap-2 px-4 py-2 border-2 border-dashed border-muted-foreground/25 rounded-lg hover:border-muted-foreground/50 transition-colors">
                  <FileJson className="h-5 w-5 text-muted-foreground" />
                  <span className="text-muted-foreground">
                    {isImporting ? 'Reading file...' : 'Click to select JSON file'}
                  </span>
                </div>
              </Label>
            </div>

            {/* Validation Results */}
            {validationResult && !validationResult.valid && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Validation Failed</AlertTitle>
                <AlertDescription>
                  <ul className="list-disc list-inside mt-2 space-y-1">
                    {validationResult.errors.map((error, i) => (
                      <li key={i}>{error}</li>
                    ))}
                  </ul>
                </AlertDescription>
              </Alert>
            )}

            {validationResult?.warnings.length ? (
              <Alert>
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Warnings</AlertTitle>
                <AlertDescription>
                  <ul className="list-disc list-inside mt-2 space-y-1">
                    {validationResult.warnings.map((warning, i) => (
                      <li key={i}>{warning}</li>
                    ))}
                  </ul>
                </AlertDescription>
              </Alert>
            ) : null}
          </CardContent>
        </Card>

        {/* Clear Data Section */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-destructive">
              <Trash2 className="h-5 w-5" />
              Clear Local Data
            </CardTitle>
            <CardDescription>
              Delete all locally stored data including drafts, progress, and cached content.
              This does not affect data already synced to the server.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button 
              variant="destructive" 
              onClick={() => setShowClearDialog(true)}
              className="gap-2"
            >
              <Trash2 className="h-4 w-4" />
              Clear All Local Data
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Import Confirmation Dialog */}
      <Dialog open={showImportDialog} onOpenChange={setShowImportDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Confirm Import</DialogTitle>
            <DialogDescription>
              You are about to import data using <strong>{importMode}</strong> mode.
              {importMode === 'replace' && (
                <span className="text-destructive block mt-2">
                  This will delete all existing data first.
                </span>
              )}
            </DialogDescription>
          </DialogHeader>

          {validationResult?.data && (
            <div className="py-4">
              <h4 className="text-sm font-medium mb-2">Data to import:</h4>
              <div className="grid grid-cols-2 gap-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Operations:</span>
                  <span>{validationResult.data.operations.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Drafts:</span>
                  <span>{validationResult.data.drafts.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Progress:</span>
                  <span>{validationResult.data.progress.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Bookmarks:</span>
                  <span>{validationResult.data.bookmarks.length}</span>
                </div>
              </div>
            </div>
          )}

          <DialogFooter>
            <Button variant="outline" onClick={() => setShowImportDialog(false)}>
              Cancel
            </Button>
            <Button 
              onClick={handleImport} 
              disabled={isImporting}
              variant={importMode === 'replace' ? 'destructive' : 'default'}
            >
              {isImporting ? (
                <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
              ) : null}
              {isImporting ? 'Importing...' : `Import (${importMode})`}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Clear Data Confirmation Dialog */}
      <Dialog open={showClearDialog} onOpenChange={setShowClearDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="text-destructive flex items-center gap-2">
              <AlertCircle className="h-5 w-5" />
              Clear All Local Data?
            </DialogTitle>
            <DialogDescription>
              This action will permanently delete all locally stored data including:
            </DialogDescription>
          </DialogHeader>

          <div className="py-4">
            <ul className="list-disc list-inside space-y-1 text-sm">
              <li>Code drafts</li>
              <li>Progress tracking</li>
              <li>Bookmarks</li>
              <li>Pending sync operations</li>
              <li>Cached curriculum data</li>
            </ul>
            <p className="mt-4 text-sm text-muted-foreground">
              Data already synced to the server will not be affected.
            </p>
          </div>

          <DialogFooter>
            <Button variant="outline" onClick={() => setShowClearDialog(false)}>
              Cancel
            </Button>
            <Button 
              variant="destructive" 
              onClick={handleClearData}
              disabled={isImporting}
            >
              {isImporting ? (
                <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
              ) : (
                <Trash2 className="h-4 w-4 mr-2" />
              )}
              {isImporting ? 'Clearing...' : 'Yes, Clear All Data'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
