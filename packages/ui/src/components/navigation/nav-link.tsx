/**
 * NavLink Component
 * Active state navigation link
 */

'use client';

import * as React from 'react';
import Link from 'next/link';
import { cn } from '../../lib/utils';
import { cva, type VariantProps } from 'class-variance-authority';

const navLinkVariants = cva(
  'inline-flex items-center gap-2 text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
  {
    variants: {
      variant: {
        default: 'text-foreground hover:text-foreground/80',
        muted: 'text-muted-foreground hover:text-foreground',
        ghost: 'hover:bg-accent hover:text-accent-foreground rounded-md px-3 py-2',
        underline:
          'border-b-2 border-transparent hover:border-foreground/20 data-[active=true]:border-primary',
      },
      size: {
        default: 'text-sm',
        sm: 'text-xs',
        lg: 'text-base',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);

export interface NavLinkProps
  extends React.ComponentPropsWithoutRef<typeof Link>,
    VariantProps<typeof navLinkVariants> {
  /**
   * Whether this link is currently active
   */
  active?: boolean;
  /**
   * Icon to display before the text
   */
  icon?: React.ReactNode;
  /**
   * External link indicator
   */
  external?: boolean;
}

const NavLink = React.forwardRef<HTMLAnchorElement, NavLinkProps>(
  (
    {
      className,
      variant,
      size,
      active = false,
      icon,
      external = false,
      children,
      ...props
    },
    ref
  ) => {
    const externalProps = external
      ? { target: '_blank', rel: 'noopener noreferrer' }
      : {};

    return (
      <Link
        ref={ref}
        className={cn(navLinkVariants({ variant, size }), className)}
        data-active={active}
        aria-current={active ? 'page' : undefined}
        {...externalProps}
        {...props}
      >
        {icon && <span className="h-4 w-4 flex-shrink-0">{icon}</span>}
        {children}
        {external && (
          <svg
            className="h-3 w-3 opacity-50"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
            />
          </svg>
        )}
      </Link>
    );
  }
);
NavLink.displayName = 'NavLink';

/**
 * NavGroup - Group of navigation links with optional label
 */
const NavGroup = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & {
    label?: string;
  }
>(({ className, label, children, ...props }, ref) => (
  <nav ref={ref} className={cn('flex flex-col gap-1', className)} {...props}>
    {label && (
      <span className="mb-1 px-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
        {label}
      </span>
    )}
    {children}
  </nav>
));
NavGroup.displayName = 'NavGroup';

export { NavLink, navLinkVariants, NavGroup };
