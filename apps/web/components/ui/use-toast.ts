'use client';

import { toast as sonnerToast } from 'sonner';
import { ReactNode } from 'react';

interface ToastOptions {
  title?: string | ReactNode;
  description?: string;
  variant?: 'default' | 'destructive';
  duration?: number;
}

export function useToast() {
  const toast = (options: ToastOptions) => {
    const toastOptions: { description?: string; duration?: number } = {};
    
    if (options.description) {
      toastOptions.description = options.description;
    }
    
    if (options.duration) {
      toastOptions.duration = options.duration;
    }

    if (options.variant === 'destructive') {
      sonnerToast.error(options.title as string, toastOptions);
    } else {
      sonnerToast.success(options.title as string, toastOptions);
    }
  };

  return { toast };
}
