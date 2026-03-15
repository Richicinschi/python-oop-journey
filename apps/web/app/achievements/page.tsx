'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Trophy, Lock, Star, Zap, Target, BookOpen, Code, Award } from 'lucide-react';
import Link from 'next/link';

interface Achievement {
  id: string;
  name: string;
  description: string;
  icon: React.ReactNode;
  unlocked: boolean;
  unlockedAt?: string;
  category: 'progress' | 'learning' | 'mastery';
}

const achievements: Achievement[] = [
  {
    id: 'first-steps',
    name: 'First Steps',
    description: 'Complete your first problem',
    icon: <Star className="h-6 w-6" />,
    unlocked: false,
    category: 'progress',
  },
  {
    id: 'week-warrior',
    name: 'Week Warrior',
    description: 'Complete all problems in a week',
    icon: <Trophy className="h-6 w-6" />,
    unlocked: false,
    category: 'progress',
  },
  {
    id: 'streak-starter',
    name: 'Streak Starter',
    description: 'Solve problems for 3 days in a row',
    icon: <Zap className="h-6 w-6" />,
    unlocked: false,
    category: 'progress',
  },
  {
    id: 'theory-master',
    name: 'Theory Master',
    description: 'Read all theory sections in a week',
    icon: <BookOpen className="h-6 w-6" />,
    unlocked: false,
    category: 'learning',
  },
  {
    id: 'code-ninja',
    name: 'Code Ninja',
    description: 'Solve 10 problems without hints',
    icon: <Code className="h-6 w-6" />,
    unlocked: false,
    category: 'mastery',
  },
  {
    id: 'perfectionist',
    name: 'Perfectionist',
    description: 'Get all tests passing on first attempt',
    icon: <Target className="h-6 w-6" />,
    unlocked: false,
    category: 'mastery',
  },
];

const categoryColors = {
  progress: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
  learning: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
  mastery: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
};

export default function AchievementsPage() {
  const unlockedCount = achievements.filter(a => a.unlocked).length;
  const progress = Math.round((unlockedCount / achievements.length) * 100);

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Achievements</h1>
        <p className="text-muted-foreground">
          Track your progress and earn badges as you learn
        </p>
      </div>

      {/* Progress Card */}
      <Card className="mb-8">
        <CardContent className="pt-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-primary/10 rounded-full">
                <Award className="h-8 w-8 text-primary" />
              </div>
              <div>
                <h2 className="text-xl font-semibold">Your Progress</h2>
                <p className="text-muted-foreground">
                  {unlockedCount} of {achievements.length} achievements unlocked
                </p>
              </div>
            </div>
            <div className="text-right">
              <span className="text-3xl font-bold">{progress}%</span>
            </div>
          </div>
          <div className="w-full bg-secondary h-3 rounded-full overflow-hidden">
            <div 
              className="bg-primary h-full transition-all duration-500"
              style={{ width: `${progress}%` }}
            />
          </div>
        </CardContent>
      </Card>

      {/* Achievement Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {achievements.map((achievement) => (
          <Card 
            key={achievement.id}
            className={achievement.unlocked ? '' : 'opacity-60'}
          >
            <CardHeader className="pb-3">
              <div className="flex items-start justify-between">
                <div className={`p-2 rounded-lg ${
                  achievement.unlocked 
                    ? 'bg-primary/10 text-primary' 
                    : 'bg-muted text-muted-foreground'
                }`}>
                  {achievement.unlocked ? achievement.icon : <Lock className="h-6 w-6" />}
                </div>
                <Badge className={categoryColors[achievement.category]}>
                  {achievement.category}
                </Badge>
              </div>
              <CardTitle className="text-lg mt-3">{achievement.name}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-3">
                {achievement.description}
              </p>
              {achievement.unlocked && achievement.unlockedAt && (
                <p className="text-xs text-muted-foreground">
                  Unlocked {new Date(achievement.unlockedAt).toLocaleDateString()}
                </p>
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      {/* CTA */}
      <div className="mt-8 text-center">
        <p className="text-muted-foreground mb-4">
          Start solving problems to unlock achievements!
        </p>
        <Button asChild>
          <Link href="/weeks">Start Learning</Link>
        </Button>
      </div>
    </div>
  );
}
