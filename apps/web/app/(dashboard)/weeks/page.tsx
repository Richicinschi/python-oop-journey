import type { Metadata } from 'next';
import Link from 'next/link';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Input } from '@/components/ui/input';
import { 
  getWeeks, 
  getWeekProblemCount, 
  formatWeekNumber,
  getWeekProgress 
} from '@/lib/curriculum-loader';
import { BookOpen, ChevronRight, Lock, Search, GraduationCap, Code } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Curriculum | Python OOP Journey',
  description: 'Master Python OOP through our structured learning path',
};

export default function WeeksPage() {
  const weeks = getWeeks();

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="space-y-4">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-primary/10">
            <GraduationCap className="h-6 w-6 text-primary" />
          </div>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Curriculum</h1>
            <p className="text-muted-foreground">
              Master Python OOP through our structured {weeks.length}-week learning path
            </p>
          </div>
        </div>

        {/* Stats Bar */}
        <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground">
          <div className="flex items-center gap-2">
            <BookOpen className="h-4 w-4" />
            <span>{weeks.length} Weeks</span>
          </div>
          <div className="flex items-center gap-2">
            <Code className="h-4 w-4" />
            <span>{weeks.reduce((acc, w) => acc + getWeekProblemCount(w), 0)} Problems</span>
          </div>
        </div>
      </div>

      {/* Search */}
      <Link href="/search">
        <div className="relative max-w-md cursor-pointer">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input 
            placeholder="Search problems..." 
            className="pl-10 cursor-pointer"
            readOnly
          />
        </div>
      </Link>

      {/* Weeks Grid */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {weeks.map((week, index) => {
          const isLocked = index > 0; // First week unlocked by default
          const progress = getWeekProgress(week);
          const problemCount = getWeekProblemCount(week);

          return (
            <Card 
              key={week.slug} 
              className={`group transition-all hover:shadow-md ${isLocked ? 'opacity-75' : ''}`}
            >
              <CardHeader>
                <div className="flex items-center justify-between">
                  <Badge variant="secondary" className="font-mono">
                    {formatWeekNumber(week.order)}
                  </Badge>
                  {isLocked && (
                    <div className="flex items-center gap-1 text-muted-foreground text-xs">
                      <Lock className="h-3 w-3" />
                      <span>Locked</span>
                    </div>
                  )}
                </div>
                <CardTitle className="mt-3 text-xl group-hover:text-primary transition-colors">
                  {week.title.replace(`Week ${week.order}: `, '').replace('Week 0: ', '')}
                </CardTitle>
                <CardDescription className="line-clamp-2">
                  {week.objective || `Master ${week.days.length} days of content with hands-on exercises`}
                </CardDescription>
              </CardHeader>
              
              <CardContent className="space-y-4">
                {/* Progress */}
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Progress</span>
                    <span className="font-medium">{progress}%</span>
                  </div>
                  <Progress value={progress} className="h-2" />
                </div>

                {/* Stats */}
                <div className="flex items-center gap-4 text-sm text-muted-foreground">
                  <div className="flex items-center gap-1.5">
                    <BookOpen className="h-4 w-4" />
                    <span>{week.days.length} days</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <Code className="h-4 w-4" />
                    <span>{problemCount} problems</span>
                  </div>
                </div>

                {/* CTA */}
                <Link href={`/weeks/${week.slug}`}>
                  <Button 
                    className="w-full mt-2" 
                    variant={isLocked ? 'outline' : 'default'}
                    disabled={isLocked}
                  >
                    {isLocked ? 'Complete Previous Week' : progress > 0 ? 'Continue Week' : 'Start Week'}
                    <ChevronRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Learning Path */}
      <Card className="mt-8">
        <CardHeader>
          <CardTitle>Learning Path</CardTitle>
          <CardDescription>
            Your journey from Python basics to OOP mastery
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {weeks.map((week, index) => (
              <div key={week.slug} className="flex items-start gap-4">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary/10 text-primary text-sm font-medium">
                  {week.order}
                </div>
                <div className="flex-1 pb-4 border-b last:border-0 last:pb-0">
                  <p className="font-medium">{week.title}</p>
                  <p className="text-sm text-muted-foreground">
                    {week.objective || `${week.days.length} days, ${getWeekProblemCount(week)} problems`}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
