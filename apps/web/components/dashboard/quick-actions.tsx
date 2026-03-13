'use client';

import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { 
  Shuffle, 
  Bookmark, 
  Award,
  ChevronDown,
  Target,
  RotateCcw,
  Sparkles,
  Trophy,
  BookOpen
} from 'lucide-react';
import Link from 'next/link';
import { WEEKS_DATA } from '@/types/dashboard';

export function QuickActions() {
  return (
    <div className="flex flex-wrap gap-3">
      {/* Jump to Week Dropdown */}
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="outline" className="gap-2">
            <BookOpen className="h-4 w-4" />
            Jump to Week
            <ChevronDown className="h-4 w-4" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="start" className="w-56">
          <DropdownMenuLabel>Curriculum Weeks</DropdownMenuLabel>
          <DropdownMenuSeparator />
          {WEEKS_DATA.map((week) => (
            <DropdownMenuItem key={week.slug} asChild>
              <Link href={`/weeks/${week.number}`} className="flex items-center justify-between">
                <span>Week {week.number}: {week.title}</span>
                <span className="text-xs text-muted-foreground">{week.problemCount}</span>
              </Link>
            </DropdownMenuItem>
          ))}
        </DropdownMenuContent>
      </DropdownMenu>

      {/* Practice Random Problem */}
      <Link href="/problems/problem-01-calculate-sum">
        <Button variant="outline" className="gap-2">
          <Shuffle className="h-4 w-4" />
          Random Problem
        </Button>
      </Link>

      {/* Review Bookmarks */}
      <Link href="/bookmarks">
        <Button variant="outline" className="gap-2">
          <Bookmark className="h-4 w-4" />
          Bookmarks
        </Button>
      </Link>

      {/* View Certificates - Coming Soon */}
      <Button variant="outline" className="gap-2 opacity-60" disabled>
        <Award className="h-4 w-4" />
        Certificates
        <span className="text-xs ml-1 px-1.5 py-0.5 rounded bg-muted">Soon</span>
      </Button>
    </div>
  );
}

export function ActionButtons() {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
      {[
        { icon: Target, label: 'Practice', href: '/problems', color: 'hover:bg-blue-500/10 hover:text-blue-500' },
        { icon: RotateCcw, label: 'Review', href: '/weeks', color: 'hover:bg-yellow-500/10 hover:text-yellow-500' },
        { icon: Sparkles, label: 'Learn', href: '/weeks/1', color: 'hover:bg-pink-500/10 hover:text-pink-500' },
        { icon: Trophy, label: 'Achievements', href: '/achievements', color: 'hover:bg-green-500/10 hover:text-green-500' },
      ].map((action, index) => (
        <div
          key={action.label}
          className="animate-fade-in"
          style={{ animationDelay: `${300 + index * 50}ms` }}
        >
          <Link href={action.href}>
            <Button 
              variant="outline" 
              className={`w-full h-auto py-4 flex flex-col items-center gap-2 transition-colors ${action.color}`}
            >
              <action.icon className="h-5 w-5" />
              <span className="text-xs font-medium">{action.label}</span>
            </Button>
          </Link>
        </div>
      ))}
    </div>
  );
}
