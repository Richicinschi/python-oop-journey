'use client';

import { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Keyboard, Command, FileCode, Play, Eye, Navigation } from 'lucide-react';
import { cn } from '@/lib/utils';

interface Shortcut {
  keys: string[];
  description: string;
  category: 'file' | 'run' | 'view' | 'navigation';
}

const shortcuts: Shortcut[] = [
  // File operations
  { keys: ['Ctrl', 'S'], description: 'Save current file', category: 'file' },
  { keys: ['Ctrl', 'Shift', 'S'], description: 'Save all files', category: 'file' },
  { keys: ['Ctrl', 'N'], description: 'Create new file', category: 'file' },
  
  // Run operations
  { keys: ['Ctrl', 'R'], description: 'Run project', category: 'run' },
  { keys: ['Ctrl', 'T'], description: 'Run tests', category: 'run' },
  { keys: ['Ctrl', 'Enter'], description: 'Run current file', category: 'run' },
  
  // View operations
  { keys: ['Ctrl', 'B'], description: 'Toggle file tree', category: 'view' },
  { keys: ['Ctrl', '\\'], description: 'Split editor', category: 'view' },
  { keys: ['Ctrl', '0'], description: 'Reset zoom', category: 'view' },
  { keys: ['Ctrl', '+'], description: 'Zoom in', category: 'view' },
  { keys: ['Ctrl', '-'], description: 'Zoom out', category: 'view' },
  
  // Navigation
  { keys: ['Ctrl', 'Tab'], description: 'Next tab', category: 'navigation' },
  { keys: ['Ctrl', 'Shift', 'Tab'], description: 'Previous tab', category: 'navigation' },
  { keys: ['Ctrl', 'W'], description: 'Close current tab', category: 'navigation' },
];

const categoryConfig = {
  file: { label: 'File Operations', icon: FileCode, color: 'text-blue-500' },
  run: { label: 'Run & Test', icon: Play, color: 'text-green-500' },
  view: { label: 'View', icon: Eye, color: 'text-purple-500' },
  navigation: { label: 'Navigation', icon: Navigation, color: 'text-orange-500' },
};

export function KeyboardShortcutsDialog({ children }: { children?: React.ReactNode }) {
  const [open, setOpen] = useState(false);

  // Listen for ? key to open shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === '?' && !e.ctrlKey && !e.metaKey && !e.altKey) {
        // Don't trigger when typing in inputs
        const target = e.target as HTMLElement;
        if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.isContentEditable) {
          return;
        }
        setOpen(true);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const groupedShortcuts = shortcuts.reduce((acc, shortcut) => {
    if (!acc[shortcut.category]) acc[shortcut.category] = [];
    acc[shortcut.category].push(shortcut);
    return acc;
  }, {} as Record<string, Shortcut[]>);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        {children || (
          <Button variant="outline" size="sm" className="gap-2">
            <Keyboard className="h-4 w-4" />
            Shortcuts
          </Button>
        )}
      </DialogTrigger>
      <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Keyboard className="h-5 w-5" />
            Keyboard Shortcuts
          </DialogTitle>
          <DialogDescription>
            Speed up your workflow with these keyboard shortcuts
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6 py-4">
          {Object.entries(groupedShortcuts).map(([category, categoryShortcuts]) => {
            const config = categoryConfig[category as keyof typeof categoryConfig];
            const Icon = config.icon;

            return (
              <div key={category}>
                <div className="flex items-center gap-2 mb-3">
                  <Icon className={cn('h-4 w-4', config.color)} />
                  <h3 className="font-semibold text-sm">{config.label}</h3>
                </div>
                <div className="grid gap-2">
                  {categoryShortcuts.map((shortcut, index) => (
                    <div 
                      key={index}
                      className="flex items-center justify-between py-2 px-3 rounded-lg bg-muted/50 hover:bg-muted transition-colors"
                    >
                      <span className="text-sm">{shortcut.description}</span>
                      <div className="flex items-center gap-1">
                        {shortcut.keys.map((key, keyIndex) => (
                          <span key={keyIndex} className="flex items-center">
                            <kbd className="inline-flex items-center justify-center px-2 py-0.5 text-xs font-medium rounded border bg-background shadow-sm min-w-[24px]">
                              {key}
                            </kbd>
                            {keyIndex < shortcut.keys.length - 1 && (
                              <span className="mx-1 text-muted-foreground">+</span>
                            )}
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>

        <div className="text-xs text-muted-foreground text-center pt-4 border-t">
          Press <kbd className="px-1.5 py-0.5 rounded border bg-muted">?</kbd> anytime to show this dialog
        </div>
      </DialogContent>
    </Dialog>
  );
}

// Shortcut display component for individual shortcuts
export function ShortcutDisplay({ keys, className }: { keys: string[]; className?: string }) {
  return (
    <span className={cn('inline-flex items-center gap-0.5', className)}>
      {keys.map((key, index) => (
        <span key={index} className="flex items-center">
          <kbd className="inline-flex items-center justify-center px-1.5 py-0.5 text-[10px] font-medium rounded border bg-muted">
            {key}
          </kbd>
          {index < keys.length - 1 && (
            <span className="mx-0.5 text-muted-foreground">+</span>
          )}
        </span>
      ))}
    </span>
  );
}

// Quick shortcut tooltip
export function ShortcutHint({ shortcut, children }: { shortcut: string; children: React.ReactNode }) {
  return (
    <div className="group relative inline-flex">
      {children}
      <span className="absolute -top-8 left-1/2 -translate-x-1/2 px-2 py-1 text-xs bg-popover text-popover-foreground rounded shadow-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none">
        {shortcut}
      </span>
    </div>
  );
}

// Shortcut badge for buttons
export function ShortcutBadge({ keys }: { keys: string[] }) {
  return (
    <span className="hidden sm:inline-flex items-center gap-0.5 ml-2 opacity-60">
      {keys.map((key, index) => (
        <span key={index} className="flex items-center">
          <kbd className="text-[10px] font-normal">{key}</kbd>
          {index < keys.length - 1 && (
            <span className="mx-0.5">+</span>
          )}
        </span>
      ))}
    </span>
  );
}
