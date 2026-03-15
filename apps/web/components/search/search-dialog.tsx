'use client';

import { CommandPalette } from './command-palette';
import type { SearchIndexItem } from '@repo/types';

interface SearchDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  searchIndex: SearchIndexItem[];
}

export function SearchDialog({ open, onOpenChange, searchIndex }: SearchDialogProps) {
  return (
    <CommandPalette 
      open={open} 
      onOpenChange={onOpenChange} 
      searchIndex={searchIndex} 
    />
  );
}
