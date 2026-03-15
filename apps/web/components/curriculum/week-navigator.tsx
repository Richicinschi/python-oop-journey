'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { Progress } from '@/components/ui/progress';
import { ScrollArea } from '@/components/ui/scroll-area';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion';
import { Week, Day } from '@/types/curriculum';
import { BookOpen, FileText, CheckCircle2, Circle, Lock } from 'lucide-react';
import { useLocalStorage } from '@/hooks/use-local-storage';
import { useEffect, useCallback } from 'react';

interface WeekNavigatorProps {
  weeks: Week[];
  className?: string;
  /**
   * Callback when a link is clicked (used to close mobile sidebar)
   */
  onLinkClick?: () => void;
}

export function WeekNavigator({ weeks, className, onLinkClick }: WeekNavigatorProps) {
  const pathname = usePathname();
  
  // Persist expanded weeks in localStorage
  const [expandedWeeks, setExpandedWeeks] = useLocalStorage<string[]>('oop-journey-expanded-weeks', []);

  // Determine which week is currently active based on pathname
  const getActiveWeek = useCallback(() => {
    for (const week of weeks) {
      if (pathname.includes(week.slug)) {
        return week.slug;
      }
    }
    return null;
  }, [pathname, weeks]);

  const activeWeek = getActiveWeek();

  // Auto-expand the active week when pathname changes
  useEffect(() => {
    if (activeWeek && !expandedWeeks.includes(activeWeek)) {
      setExpandedWeeks((prev) => [...prev, activeWeek]);
    }
  }, [activeWeek, expandedWeeks, setExpandedWeeks]);

  // Handle accordion value changes
  const handleValueChange = (value: string[]) => {
    setExpandedWeeks(value);
  };

  return (
    <ScrollArea className={cn('h-full', className)}>
      <div className="p-4 space-y-4">
        <div className="flex items-center justify-between px-2">
          <h3 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            Curriculum
          </h3>
          <span className="text-xs text-muted-foreground">
            {weeks.length} weeks
          </span>
        </div>

        <Accordion 
          type="multiple" 
          value={expandedWeeks}
          onValueChange={handleValueChange}
          className="space-y-1"
        >
          {weeks.map((week, weekIndex) => (
            <WeekItem 
              key={week.slug} 
              week={week} 
              weekIndex={weekIndex}
              isActive={pathname.includes(week.slug)}
              pathname={pathname}
              onLinkClick={onLinkClick}
            />
          ))}
        </Accordion>
      </div>
    </ScrollArea>
  );
}

interface WeekItemProps {
  week: Week;
  weekIndex: number;
  isActive: boolean;
  pathname: string;
  onLinkClick?: () => void;
}

function WeekItem({ week, weekIndex, isActive, pathname, onLinkClick }: WeekItemProps) {
  const isLocked = weekIndex > 0; // First week unlocked
  const completedDays = 0; // TODO: Get from progress store
  const progress = week.days.length > 0 
    ? Math.round((completedDays / week.days.length) * 100) 
    : 0;

  return (
    <AccordionItem value={week.slug} className="border-none">
      <AccordionTrigger 
        className={cn(
          'py-2 px-2 hover:no-underline hover:bg-accent rounded-md text-sm',
          isActive && 'bg-accent'
        )}
      >
        <div className="flex items-center gap-3 w-full pr-2">
          <span className={cn(
            'flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-xs font-medium',
            isActive 
              ? 'bg-primary text-primary-foreground' 
              : 'bg-muted text-muted-foreground'
          )}>
            {week.order}
          </span>
          <div className="flex-1 text-left">
            <span className={cn('block truncate', isActive && 'font-medium')}>
              {week.title.replace(`Week ${week.order}: `, '').replace('Week 0: ', '')}
            </span>
            {progress > 0 && (
              <Progress value={progress} className="h-1 mt-1" />
            )}
          </div>
          {isLocked && <Lock className="h-3 w-3 text-muted-foreground" />}
        </div>
      </AccordionTrigger>
      
      <AccordionContent>
        <div className="pl-2 space-y-0.5">
          {/* Week Overview Link */}
          <Link
            href={`/weeks/${week.slug}`}
            onClick={onLinkClick}
            className={cn(
              'flex items-center gap-2 py-1.5 px-2 text-sm rounded-md transition-colors',
              pathname === `/weeks/${week.slug}`
                ? 'bg-accent font-medium text-foreground'
                : 'text-muted-foreground hover:bg-accent hover:text-foreground'
            )}
          >
            <BookOpen className="h-3.5 w-3.5" />
            <span>Overview</span>
          </Link>

          {/* Day Links */}
          {week.days.map((day, dayIndex) => (
            <DayItem 
              key={day.slug} 
              week={week} 
              day={day} 
              dayIndex={dayIndex}
              isActive={pathname.includes(day.slug)}
              onLinkClick={onLinkClick}
            />
          ))}
        </div>
      </AccordionContent>
    </AccordionItem>
  );
}

interface DayItemProps {
  week: Week;
  day: Day;
  dayIndex: number;
  isActive: boolean;
  onLinkClick?: () => void;
}

function DayItem({ week, day, dayIndex, isActive, onLinkClick }: DayItemProps) {
  const isLocked = dayIndex > 0;
  const isCompleted = false; // TODO: Get from progress store
  const hasTheory = day.theory_content && day.theory_content.length > 0;
  const pathname = usePathname();
  const isTheoryPage = pathname.includes('theory');

  return (
    <div className="space-y-0.5">
      <Link
        href={`/weeks/${week.slug}/days/${day.slug}`}
        onClick={onLinkClick}
        className={cn(
          'flex items-center gap-2 py-1.5 px-2 text-sm rounded-md transition-colors',
          isActive && !isTheoryPage
            ? 'bg-accent font-medium text-foreground'
            : 'text-muted-foreground hover:bg-accent hover:text-foreground'
        )}
      >
        {isCompleted ? (
          <CheckCircle2 className="h-3.5 w-3.5 text-green-500" />
        ) : (
          <Circle className="h-3.5 w-3.5" />
        )}
        <span className="truncate">
          {day.order}. {day.title.replace(`Day ${day.order}: `, '')}
        </span>
        {isLocked && <Lock className="h-3 w-3 ml-auto text-muted-foreground" />}
      </Link>

      {/* Theory Sub-link */}
      {hasTheory && isActive && (
        <Link
          href={`/weeks/${week.slug}/days/${day.slug}/theory`}
          onClick={onLinkClick}
          className={cn(
            'flex items-center gap-2 py-1 px-2 text-xs rounded-md transition-colors ml-4',
            isTheoryPage
              ? 'bg-accent font-medium text-foreground'
              : 'text-muted-foreground hover:bg-accent hover:text-foreground'
          )}
        >
          <FileText className="h-3 w-3" />
          <span>Theory</span>
        </Link>
      )}
    </div>
  );
}
