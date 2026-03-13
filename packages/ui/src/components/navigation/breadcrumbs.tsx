/**
 * Breadcrumbs Component
 * Page hierarchy navigation
 */

'use client';

import * as React from 'react';
import Link from 'next/link';
import { cn } from '../../lib/utils';
import { ChevronRight, Home } from 'lucide-react';

/**
 * Breadcrumb item data
 */
export interface BreadcrumbItem {
  /**
   * Item label
   */
  label: string;
  /**
   * Item href
   */
  href?: string;
  /**
   * Optional icon
   */
  icon?: React.ReactNode;
}

export interface BreadcrumbsProps extends React.HTMLAttributes<HTMLElement> {
  /**
   * Array of breadcrumb items
   */
  items: BreadcrumbItem[];
  /**
   * Show home icon as first item
   */
  showHome?: boolean;
  /**
   * Home link href
   */
  homeHref?: string;
  /**
   * Separator between items
   */
  separator?: React.ReactNode;
  /**
   * Maximum items to show before collapsing
   */
  maxItems?: number;
}

const Breadcrumbs = React.forwardRef<HTMLElement, BreadcrumbsProps>(
  (
    {
      className,
      items,
      showHome = true,
      homeHref = '/',
      separator = <ChevronRight className="h-4 w-4" />,
      maxItems = 4,
      ...props
    },
    ref
  ) => {
    // Handle truncation if too many items
    const displayItems = React.useMemo(() => {
      if (items.length <= maxItems) return items;
      
      const start = items.slice(0, 1);
      const end = items.slice(-2);
      return [
        ...start,
        { label: '...', href: undefined },
        ...end,
      ];
    }, [items, maxItems]);

    return (
      <nav
        ref={ref}
        aria-label="Breadcrumb"
        className={cn('flex', className)}
        {...props}
      >
        <ol className="flex flex-wrap items-center gap-1.5 break-words text-sm text-muted-foreground sm:gap-2.5">
          {showHome && (
            <li className="inline-flex items-center gap-1.5">
              <Link
                href={homeHref}
                className="flex items-center gap-1 transition-colors hover:text-foreground"
                aria-label="Home"
              >
                <Home className="h-4 w-4" />
              </Link>
              <span className="text-muted-foreground/50" aria-hidden="true">
                {separator}
              </span>
            </li>
          )}
          {displayItems.map((item, index) => {
            const isLast = index === displayItems.length - 1;
            const isEllipsis = item.label === '...';

            return (
              <li
                key={index}
                className="inline-flex items-center gap-1.5"
              >
                {isEllipsis ? (
                  <span className="px-1">...</span>
                ) : isLast || !item.href ? (
                  <span
                    className="font-medium text-foreground"
                    aria-current={isLast ? 'page' : undefined}
                  >
                    {item.icon && (
                      <span className="mr-1 inline-flex">{item.icon}</span>
                    )}
                    {item.label}
                  </span>
                ) : (
                  <Link
                    href={item.href}
                    className="flex items-center gap-1 transition-colors hover:text-foreground"
                  >
                    {item.icon && (
                      <span className="inline-flex">{item.icon}</span>
                    )}
                    {item.label}
                  </Link>
                )}
                {!isLast && (
                  <span
                    className="text-muted-foreground/50"
                    aria-hidden="true"
                  >
                    {separator}
                  </span>
                )}
              </li>
            );
          })}
        </ol>
      </nav>
    );
  }
);
Breadcrumbs.displayName = 'Breadcrumbs';

export { Breadcrumbs };
