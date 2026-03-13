/**
 * MobileNav Component
 * Mobile navigation drawer
 */

'use client';

import * as React from 'react';
import { cn } from '../../lib/utils';
import { Button } from '../button';
import { ScrollArea } from '../scroll-area';
import { Separator } from '../separator';
import { Menu, X } from 'lucide-react';

interface MobileNavProps {
  /**
   * Navigation content
   */
  children: React.ReactNode;
  /**
   * Optional header content
   */
  header?: React.ReactNode;
  /**
   * Optional footer content
   */
  footer?: React.ReactNode;
  /**
   * Custom trigger element
   */
  trigger?: React.ReactNode;
  /**
   * Callback when open state changes
   */
  onOpenChange?: (open: boolean) => void;
  /**
   * Controlled open state
   */
  open?: boolean;
  /**
   * Default open state
   */
  defaultOpen?: boolean;
  /**
   * Side from which drawer appears
   */
  side?: 'left' | 'right';
}

const MobileNav = React.forwardRef<HTMLDivElement, MobileNavProps>(
  (
    {
      children,
      header,
      footer,
      trigger,
      onOpenChange,
      open: controlledOpen,
      defaultOpen = false,
      side = 'left',
    },
    ref
  ) => {
    const [internalOpen, setInternalOpen] = React.useState(defaultOpen);
    const isOpen = controlledOpen ?? internalOpen;

    const setOpen = React.useCallback(
      (value: boolean) => {
        setInternalOpen(value);
        onOpenChange?.(value);
      },
      [onOpenChange]
    );

    // Close on escape key
    React.useEffect(() => {
      const handleEscape = (e: KeyboardEvent) => {
        if (e.key === 'Escape') setOpen(false);
      };

      if (isOpen) {
        document.addEventListener('keydown', handleEscape);
        document.body.style.overflow = 'hidden';
      }

      return () => {
        document.removeEventListener('keydown', handleEscape);
        document.body.style.overflow = '';
      };
    }, [isOpen, setOpen]);

    return (
      <>
        {/* Trigger */}
        {trigger ? (
          <div onClick={() => setOpen(true)}>{trigger}</div>
        ) : (
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden"
            onClick={() => setOpen(true)}
            aria-label="Open menu"
          >
            <Menu className="h-5 w-5" />
          </Button>
        )}

        {/* Overlay */}
        {isOpen && (
          <div
            className="fixed inset-0 z-40 bg-black/50 backdrop-blur-sm md:hidden"
            onClick={() => setOpen(false)}
            aria-hidden="true"
          />
        )}

        {/* Drawer */}
        <div
          ref={ref}
          className={cn(
            'fixed top-0 z-50 h-full w-[280px] bg-background shadow-xl transition-transform duration-300 ease-in-out md:hidden',
            side === 'left' ? 'left-0' : 'right-0',
            isOpen
              ? 'translate-x-0'
              : side === 'left'
              ? '-translate-x-full'
              : 'translate-x-full'
          )}
        >
          {/* Header */}
          <div className="flex h-14 items-center justify-between border-b px-4">
            {header ? (
              <div className="flex-1">{header}</div>
            ) : (
              <span className="font-semibold">Menu</span>
            )}
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setOpen(false)}
              aria-label="Close menu"
            >
              <X className="h-5 w-5" />
            </Button>
          </div>

          {/* Content */}
          <ScrollArea className="h-[calc(100vh-3.5rem)]">
            <div className="p-4">{children}</div>

            {/* Footer */}
            {footer && (
              <>
                <Separator className="my-4" />
                <div className="p-4">{footer}</div>
              </>
            )}
          </ScrollArea>
        </div>
      </>
    );
  }
);
MobileNav.displayName = 'MobileNav';

/**
 * MobileNavSection for grouping navigation items
 */
const MobileNavSection = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & {
    title?: string;
  }
>(({ className, title, children, ...props }, ref) => (
  <div ref={ref} className={cn('py-2', className)} {...props}>
    {title && (
      <h3 className="mb-2 px-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
        {title}
      </h3>
    )}
    <div className="space-y-1">{children}</div>
  </div>
));
MobileNavSection.displayName = 'MobileNavSection';

/**
 * MobileNavItem for individual navigation links
 */
const MobileNavItem = React.forwardRef<
  HTMLAnchorElement,
  React.AnchorHTMLAttributes<HTMLAnchorElement> & {
    active?: boolean;
    icon?: React.ReactNode;
  }
>(({ className, active, icon, children, ...props }, ref) => (
  <a
    ref={ref}
    className={cn(
      'flex items-center gap-3 rounded-md px-2 py-2.5 text-sm font-medium transition-colors',
      'hover:bg-accent hover:text-accent-foreground',
      active && 'bg-accent text-accent-foreground',
      className
    )}
    aria-current={active ? 'page' : undefined}
    {...props}
  >
    {icon && <span className="h-4 w-4 flex-shrink-0">{icon}</span>}
    <span className="truncate">{children}</span>
  </a>
));
MobileNavItem.displayName = 'MobileNavItem';

export { MobileNav, MobileNavSection, MobileNavItem };
