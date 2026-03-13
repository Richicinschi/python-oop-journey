'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { ChevronRight, Home } from 'lucide-react';
import { cn } from '@/lib/utils';
import { getWeekBySlug, getDayBySlug, formatWeekNumber, formatDayNumber } from '@/lib/curriculum-loader';

interface BreadcrumbItem {
  label: string;
  href: string;
  isCurrent: boolean;
}

export function Breadcrumb() {
  const pathname = usePathname();
  
  const items = generateBreadcrumbItems(pathname);
  
  if (items.length <= 1) {
    return null;
  }

  return (
    <nav aria-label="Breadcrumb" className="flex items-center text-sm text-muted-foreground">
      <ol className="flex items-center gap-2">
        {items.map((item, index) => (
          <li key={item.href} className="flex items-center gap-2">
            {index > 0 && <ChevronRight className="h-4 w-4" />}
            {item.isCurrent ? (
              <span className="font-medium text-foreground">{item.label}</span>
            ) : (
              <Link 
                href={item.href}
                className="hover:text-foreground transition-colors"
              >
                {index === 0 ? (
                  <Home className="h-4 w-4" />
                ) : (
                  item.label
                )}
              </Link>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
}

function generateBreadcrumbItems(pathname: string): BreadcrumbItem[] {
  const items: BreadcrumbItem[] = [
    { label: 'Home', href: '/', isCurrent: pathname === '/' }
  ];

  const segments = pathname.split('/').filter(Boolean);
  
  if (segments.length === 0) {
    return items;
  }

  let currentPath = '';
  
  for (let i = 0; i < segments.length; i++) {
    const segment = segments[i];
    currentPath += `/${segment}`;
    
    // Skip parameter segments (they start with [)
    if (segment.startsWith('[')) {
      continue;
    }

    const isCurrent = i === segments.length - 1;
    let label = formatSegmentLabel(segment);

    // Try to get better labels for dynamic segments
    if (segment.startsWith('week')) {
      const week = getWeekBySlug(segment);
      if (week) {
        label = formatWeekNumber(week.order);
      }
    } else if (segment.startsWith('day')) {
      const weekSlug = segments[i - 1];
      if (weekSlug && !weekSlug.startsWith('[')) {
        const day = getDayBySlug(weekSlug, segment);
        if (day) {
          label = formatDayNumber(day.order);
        }
      }
    }

    items.push({
      label,
      href: currentPath,
      isCurrent,
    });
  }

  return items;
}

function formatSegmentLabel(segment: string): string {
  // Special cases
  if (segment === 'weeks') return 'Curriculum';
  if (segment === 'days') return 'Days';
  if (segment === 'theory') return 'Theory';
  if (segment === 'problems') return 'Problems';
  if (segment === 'achievements') return 'Achievements';
  if (segment === 'settings') return 'Settings';
  if (segment === 'profile') return 'Profile';
  
  // Default: replace dashes with spaces and capitalize
  return segment
    .replace(/-/g, ' ')
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase());
}
