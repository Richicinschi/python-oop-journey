/**
 * Sidebar Component
 * Collapsible navigation sidebar
 */

'use client';

import * as React from 'react';
import { cn } from '../../lib/utils';
import { Button } from '../button';
import { ScrollArea } from '../scroll-area';
import { Separator } from '../separator';
import { ChevronLeft, ChevronRight } from 'lucide-react';

interface SidebarProps extends React.HTMLAttributes<HTMLDivElement> {
  /**
   * Whether the sidebar is collapsed
   */
  collapsed?: boolean;
  /**
   * Callback when collapse state changes
   */
  onCollapseChange?: (collapsed: boolean) => void;
  /**
   * Sidebar header content
   */
  header?: React.ReactNode;
  /**
   * Sidebar footer content
   */
  footer?: React.ReactNode;
  /**
   * Width when expanded
   */
  width?: string;
  /**
   * Width when collapsed
   */
  collapsedWidth?: string;
}

const Sidebar = React.forwardRef<HTMLDivElement, SidebarProps>(
  (
    {
      className,
      collapsed = false,
      onCollapseChange,
      header,
      footer,
      children,
      width = '16rem',
      collapsedWidth = '4rem',
      ...props
    },
    ref
  ) => {
    const [isCollapsed, setIsCollapsed] = React.useState(collapsed);

    React.useEffect(() => {
      setIsCollapsed(collapsed);
    }, [collapsed]);

    const handleToggle = () => {
      const newState = !isCollapsed;
      setIsCollapsed(newState);
      onCollapseChange?.(newState);
    };

    return (
      <div
        ref={ref}
        className={cn(
          'flex flex-col border-r bg-sidebar transition-all duration-300 ease-in-out',
          className
        )}
        style={{
          width: isCollapsed ? collapsedWidth : width,
        }}
        {...props}
      >
        {/* Header */}
        {header && (
          <div
            className={cn(
              'flex h-14 items-center border-b px-4',
              isCollapsed && 'justify-center px-2'
            )}
          >
            {header}
          </div>
        )}

        {/* Toggle Button */}
        <Button
          variant="ghost"
          size="icon"
          onClick={handleToggle}
          className="absolute -right-3 top-16 h-6 w-6 rounded-full border bg-background shadow-sm"
          aria-label={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {isCollapsed ? (
            <ChevronRight className="h-3 w-3" />
          ) : (
            <ChevronLeft className="h-3 w-3" />
          )}
        </Button>

        {/* Content */}
        <ScrollArea className="flex-1 py-2">
          <div className={cn('px-3', isCollapsed && 'px-1')}>{children}</div>
        </ScrollArea>

        {/* Footer */}
        {footer && (
          <>
            <Separator />
            <div
              className={cn(
                'p-4',
                isCollapsed && 'flex justify-center p-2'
              )}
            >
              {footer}
            </div>
          </>
        )}
      </div>
    );
  }
);
Sidebar.displayName = 'Sidebar';

/**
 * Sidebar Section for grouping navigation items
 */
const SidebarSection = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & {
    title?: string;
    collapsed?: boolean;
  }
>(({ className, title, collapsed, children, ...props }, ref) => (
  <div ref={ref} className={cn('py-2', className)} {...props}>
    {title && !collapsed && (
      <h3 className="mb-2 px-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
        {title}
      </h3>
    )}
    <div className="space-y-1">{children}</div>
  </div>
));
SidebarSection.displayName = 'SidebarSection';

/**
 * Sidebar Item for individual navigation links
 */
const SidebarItem = React.forwardRef<
  HTMLAnchorElement,
  React.AnchorHTMLAttributes<HTMLAnchorElement> & {
    active?: boolean;
    collapsed?: boolean;
    icon?: React.ReactNode;
  }
>(
  (
    { className, active, collapsed, icon, children, ...props },
    ref
  ) => (
    <a
      ref={ref}
      className={cn(
        'flex items-center gap-3 rounded-md px-2 py-2 text-sm font-medium transition-colors',
        'hover:bg-accent hover:text-accent-foreground',
        active && 'bg-accent text-accent-foreground',
        collapsed && 'justify-center',
        className
      )}
      {...props}
    >
      {icon && <span className="h-4 w-4 flex-shrink-0">{icon}</span>}
      {!collapsed && <span className="truncate">{children}</span>}
    </a>
  )
);
SidebarItem.displayName = 'SidebarItem';

export { Sidebar, SidebarSection, SidebarItem };
