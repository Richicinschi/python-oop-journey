'use client';

import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { 
  BookOpen, 
  Play, 
  RotateCcw, 
  Sparkles,
  ArrowRight,
  Target
} from 'lucide-react';
import Link from 'next/link';
import { DashboardData } from '@/types/dashboard';

interface HeroSectionProps {
  data: DashboardData;
  overallProgress: number;
}

export function HeroSection({ data, overallProgress }: HeroSectionProps) {
  const isNewUser = !data.currentPosition;
  
  if (isNewUser) {
    return (
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-primary/10 via-primary/5 to-background border p-8 animate-fade-in">
        {/* Decorative elements */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-primary/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />
        <div className="absolute bottom-0 left-0 w-48 h-48 bg-primary/5 rounded-full blur-3xl translate-y-1/2 -translate-x-1/2" />
        
        <div className="relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-sm font-medium mb-4 animate-scale-in">
            <Sparkles className="h-4 w-4" />
            Welcome to Python OOP Journey
          </div>
          
          <h1 className="text-4xl font-bold tracking-tight mb-4">
            Master Object-Oriented Programming
          </h1>
          
          <p className="text-lg text-muted-foreground max-w-2xl mb-8">
            Start your journey from Python basics to advanced OOP concepts. 
            Build real projects, solve hands-on problems, and become a confident Python developer.
          </p>
          
          <div className="flex flex-wrap gap-4">
            <Link href="/weeks/1">
              <Button size="lg" className="gap-2">
                <BookOpen className="h-5 w-5" />
                Start Your Journey
                <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
            <Link href="/problems">
              <Button variant="outline" size="lg" className="gap-2">
                <Target className="h-5 w-5" />
                Browse Problems
              </Button>
            </Link>
          </div>
          
          {/* Stats preview */}
          <div className="grid grid-cols-3 gap-8 mt-10 pt-8 border-t border-border/50">
            {[
              { value: '8', label: 'Weeks' },
              { value: '453', label: 'Problems' },
              { value: '∞', label: 'Possibilities' },
            ].map((stat, index) => (
              <div
                key={stat.label}
                className="animate-fade-in"
                style={{ animationDelay: `${400 + index * 100}ms` }}
              >
                <div className="text-3xl font-bold text-primary">{stat.value}</div>
                <div className="text-sm text-muted-foreground">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  // Returning user hero
  return (
    <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-background via-background to-muted border p-8 animate-fade-in">
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
        <div className="flex-1">
          <div className="flex items-center gap-2 text-muted-foreground mb-2 animate-fade-in" style={{ animationDelay: '100ms' }}>
            <span className="text-sm">Welcome back{data.userName ? `, ${data.userName}` : ''}</span>
            {data.stats.currentStreak > 0 && (
              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-orange-500/10 text-orange-500 text-xs font-medium">
                🔥 {data.stats.currentStreak} day streak
              </span>
            )}
          </div>
          
          <h1 className="text-3xl font-bold tracking-tight mb-2">
            Continue Your Learning Journey
          </h1>
          
          <p className="text-muted-foreground mb-6">
            You&apos;ve completed <span className="font-medium text-foreground">{data.stats.solvedProblems}</span> problems. 
            Keep up the great work!
          </p>
          
          <div className="space-y-3 max-w-md">
            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground">Overall Progress</span>
              <span className="font-medium">{overallProgress}%</span>
            </div>
            <Progress value={overallProgress} className="h-2" />
          </div>
        </div>

        <div className="flex flex-col sm:flex-row gap-3 animate-slide-in-right" style={{ animationDelay: '200ms' }}>
          <Link href={`/weeks/${data.currentPosition?.weekNumber}`}>
            <Button size="lg" className="gap-2 w-full sm:w-auto">
              <Play className="h-4 w-4" />
              Continue Learning
            </Button>
          </Link>
          <Link href="/weeks">
            <Button variant="outline" size="lg" className="gap-2 w-full sm:w-auto">
              <RotateCcw className="h-4 w-4" />
              Review
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
