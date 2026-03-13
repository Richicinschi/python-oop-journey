'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { 
  BookOpen, 
  Lightbulb, 
  Code, 
  Trophy,
  ArrowRight,
  Sparkles,
  Target,
  Zap
} from 'lucide-react';
import Link from 'next/link';

const steps = [
  {
    icon: BookOpen,
    title: 'Learn Theory',
    description: 'Read comprehensive lessons on Python OOP concepts, from basics to advanced topics.',
    color: 'text-blue-500',
    bgColor: 'bg-blue-500/10',
  },
  {
    icon: Code,
    title: 'Practice Problems',
    description: 'Solve hands-on coding exercises to reinforce your understanding.',
    color: 'text-green-500',
    bgColor: 'bg-green-500/10',
  },
  {
    icon: Trophy,
    title: 'Build Projects',
    description: 'Apply your skills to real-world projects and build your portfolio.',
    color: 'text-yellow-500',
    bgColor: 'bg-yellow-500/10',
  },
];

const curriculumPreview = [
  { week: 1, title: 'Foundations', topics: ['Variables', 'Functions', 'Control Flow'] },
  { week: 2, title: 'Classes & Objects', topics: ['Creating Classes', 'Constructors', 'Methods'] },
  { week: 3, title: 'Encapsulation', topics: ['Public/Private', 'Properties', 'Validation'] },
  { week: 4, title: 'Inheritance', topics: ['Parent Classes', 'super()', 'Overriding'] },
];

export function EmptyState() {
  return (
    <div className="space-y-8">
      {/* How It Works */}
      <div className="animate-fade-in" style={{ animationDelay: '100ms' }}>
        <div className="text-center mb-6">
          <h2 className="text-2xl font-bold mb-2">How It Works</h2>
          <p className="text-muted-foreground">Your path to mastering Python OOP in three simple steps</p>
        </div>
        
        <div className="grid md:grid-cols-3 gap-6">
          {steps.map((step, index) => (
            <div
              key={step.title}
              className="animate-fade-in"
              style={{ animationDelay: `${200 + index * 100}ms` }}
            >
              <Card className="h-full text-center group hover:border-primary/50 transition-colors">
                <CardHeader>
                  <div className={`mx-auto w-14 h-14 rounded-full ${step.bgColor} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                    <step.icon className={`h-7 w-7 ${step.color}`} />
                  </div>
                  <CardTitle className="text-lg">{step.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription>{step.description}</CardDescription>
                </CardContent>
              </Card>
            </div>
          ))}
        </div>
      </div>

      {/* Curriculum Preview */}
      <div className="animate-fade-in" style={{ animationDelay: '400ms' }}>
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Curriculum Preview</CardTitle>
                <CardDescription>8 weeks of structured learning ahead</CardDescription>
              </div>
              <Sparkles className="h-5 w-5 text-muted-foreground" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid sm:grid-cols-2 gap-4">
              {curriculumPreview.map((week) => (
                <div 
                  key={week.week}
                  className="flex items-start gap-4 p-4 rounded-lg bg-muted/50 hover:bg-muted transition-colors"
                >
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10 text-primary font-bold shrink-0">
                    {week.week}
                  </div>
                  <div>
                    <h4 className="font-medium">{week.title}</h4>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {week.topics.map(topic => (
                        <span 
                          key={topic}
                          className="text-xs px-2 py-0.5 rounded-full bg-background text-muted-foreground"
                        >
                          {topic}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
            
            <div className="mt-6 text-center">
              <Link href="/weeks">
                <Button variant="outline" className="gap-2">
                  View Full Curriculum
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Features */}
      <div 
        className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 animate-fade-in"
        style={{ animationDelay: '500ms' }}
      >
        {[
          { icon: Target, label: '453+ Problems', description: 'Hands-on practice' },
          { icon: Zap, label: 'Instant Feedback', description: 'Real-time code execution' },
          { icon: Trophy, label: 'Track Progress', description: 'Visual achievement system' },
          { icon: Lightbulb, label: 'AI Hints', description: 'Smart learning assistance' },
        ].map((feature) => (
          <div
            key={feature.label}
            className="flex items-center gap-3 p-4 rounded-lg border bg-card"
          >
            <feature.icon className="h-5 w-5 text-primary" />
            <div>
              <p className="font-medium text-sm">{feature.label}</p>
              <p className="text-xs text-muted-foreground">{feature.description}</p>
            </div>
          </div>
        ))}
      </div>

      {/* CTA */}
      <div className="text-center py-8 animate-fade-in" style={{ animationDelay: '600ms' }}>
        <Link href="/weeks/1">
          <Button size="lg" className="gap-2">
            <Sparkles className="h-5 w-5" />
            Start Your Journey
            <ArrowRight className="h-4 w-4" />
          </Button>
        </Link>
      </div>
    </div>
  );
}
