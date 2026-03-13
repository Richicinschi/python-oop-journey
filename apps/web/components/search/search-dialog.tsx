'use client';

import { CommandPalette } from './command-palette';

interface SearchDialogProps {
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
}

export function SearchDialog({ open, onOpenChange }: SearchDialogProps) {
  return (
    <CommandPalette 
      open={open} 
      onOpenChange={onOpenChange} 
      searchIndex={[]} 
    />
  );
}
