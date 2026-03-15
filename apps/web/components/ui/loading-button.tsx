'use client';

import * as React from 'react';
import { Loader2 } from 'lucide-react';
import { Slot } from '@radix-ui/react-slot';
import { cva, type VariantProps } from 'class-variance-authority';

import { cn } from '@/lib/utils';
import { buttonVariants } from './button';

export interface LoadingButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  /** Whether the button is in a loading state */
  loading?: boolean;
  /** Loading text to display (defaults to spinner only) */
  loadingText?: string;
  /** Icon to show when not loading */
  icon?: React.ReactNode;
  /** Position of the icon/loading spinner */
  iconPosition?: 'left' | 'right';
  /** Whether to use the asChild pattern */
  asChild?: boolean;
}

/**
 * Button component with built-in loading state support
 * Shows a spinner when loading and handles disabled state automatically
 * 
 * @example
 * ```tsx
 * <LoadingButton loading={isSubmitting} loadingText="Saving...">
 *   Save Changes
 * </LoadingButton>
 * 
 * <LoadingButton 
 *   loading={isRunning} 
 *   icon={<Play className="h-4 w-4" />}
 *   loadingText="Running..."
 * >
 *   Run Code
 * </LoadingButton>
 * ```
 */
const LoadingButton = React.forwardRef<HTMLButtonElement, LoadingButtonProps>(
  (
    {
      className,
      variant,
      size,
      loading = false,
      loadingText,
      icon,
      iconPosition = 'left',
      children,
      disabled,
      asChild = false,
      ...props
    },
    ref
  ) => {
    const Comp = asChild ? Slot : 'button';
    
    // Determine what to render for the icon/loading area
    const renderIcon = () => {
      if (loading) {
        return (
          <Loader2 
            className={cn(
              'h-4 w-4 animate-spin',
              loadingText && iconPosition === 'left' && 'mr-2',
              loadingText && iconPosition === 'right' && 'ml-2'
            )} 
          />
        );
      }
      
      if (icon) {
        return (
          <span
            className={cn(
              iconPosition === 'left' && children && 'mr-2',
              iconPosition === 'right' && children && 'ml-2'
            )}
          >
            {icon}
          </span>
        );
      }
      
      return null;
    };

    return (
      <Comp
        className={cn(
          buttonVariants({ variant, size, className }),
          loading && 'cursor-wait'
        )}
        ref={ref}
        disabled={disabled || loading}
        {...props}
      >
        {iconPosition === 'left' && renderIcon()}
        {loading && loadingText ? loadingText : children}
        {iconPosition === 'right' && renderIcon()}
      </Comp>
    );
  }
);
LoadingButton.displayName = 'LoadingButton';

export { LoadingButton };
