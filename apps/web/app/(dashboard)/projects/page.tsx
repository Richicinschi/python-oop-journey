'use client';

import { useState, useMemo } from 'react';
import Link from 'next/link';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  FolderGit2, 
  Plus,
  Clock,
  CheckCircle2,
  Play,
  AlertCircle,
  Trophy,
  Calendar
} from 'lucide-react';
import { ProjectCard, ProjectEmptyState } from '@/components/projects';
import { WeeklyProject, UserProjectProgress } from '@/types/project';

// Mock projects data - in real app, fetch from API
const allProjects: WeeklyProject[] = [
  {
    slug: 'week-01-project',
    title: 'CLI Calculator',
    description: 'Build a command-line calculator with basic arithmetic operations. Learn to handle user input and create a reusable utility.',
    difficulty: 'Beginner',
    estimatedTime: '2 hours',
    weekSlug: 'week-01-foundations',
    weekNumber: 1,
    starterFiles: [],
    requirements: ['Implement add, subtract, multiply, divide', 'Handle invalid input gracefully', 'Add help command'],
    hints: ['Use input() for user input', 'Consider using a loop for continuous operation'],
  },
  {
    slug: 'week-02-project',
    title: 'Contact Book',
    description: 'Create a contact management system with add, search, and delete functionality. Practice working with dictionaries and file I/O.',
    difficulty: 'Beginner',
    estimatedTime: '2.5 hours',
    weekSlug: 'week-02-classes-objects',
    weekNumber: 2,
    starterFiles: [],
    requirements: ['Add new contacts', 'Search contacts by name', 'Save to file', 'Load from file'],
    hints: ['Use dictionaries to store contacts', 'JSON is good for serialization'],
  },
  {
    slug: 'week-03-project',
    title: 'Bank Account Manager',
    description: 'Build a banking system with deposits, withdrawals, and balance tracking. Master encapsulation and private attributes.',
    difficulty: 'Intermediate',
    estimatedTime: '3 hours',
    weekSlug: 'week-03-encapsulation',
    weekNumber: 3,
    starterFiles: [],
    requirements: ['Create Account class', 'Implement deposit/withdraw', 'Track transaction history', 'Validate operations'],
    hints: ['Use private attributes for balance', 'Properties can control access'],
  },
  {
    slug: 'week-04-project',
    title: 'Library Management System',
    description: 'Design a library system with books, patrons, and checkout tracking. Apply inheritance and composition principles.',
    difficulty: 'Intermediate',
    estimatedTime: '3 hours',
    weekSlug: 'week-04-inheritance',
    weekNumber: 4,
    starterFiles: [],
    requirements: ['Create Book and Patron classes', 'Implement checkout system', 'Track due dates', 'Handle returns'],
    hints: ['Use inheritance for different book types', 'Composition helps organize library'],
  },
  {
    slug: 'week-05-project',
    title: 'Shape Drawing App',
    description: 'Create a polymorphic shape system with area calculations and drawing. Explore abstract classes and method overriding.',
    difficulty: 'Intermediate',
    estimatedTime: '3 hours',
    weekSlug: 'week-05-polymorphism',
    weekNumber: 5,
    starterFiles: [],
    requirements: ['Abstract Shape base class', 'Concrete shape implementations', 'Area calculation', 'Drawing representation'],
    hints: ['@abstractmethod enforces implementation', 'Polymorphism enables generic handling'],
  },
  {
    slug: 'week-06-project',
    title: 'Custom Collection',
    description: 'Build your own list-like container with full iterator support. Master special methods and Python data model.',
    difficulty: 'Advanced',
    estimatedTime: '3.5 hours',
    weekSlug: 'week-06-special-methods',
    weekNumber: 6,
    starterFiles: [],
    requirements: ['Implement __len__, __getitem__', 'Add iteration support', 'Enable slicing', 'Support membership testing'],
    hints: ['__iter__ and __next__ for iteration', 'Consider edge cases'],
  },
  {
    slug: 'week-07-project',
    title: 'Plugin System',
    description: 'Design an extensible plugin architecture using design patterns. Apply Factory, Observer, and Strategy patterns.',
    difficulty: 'Advanced',
    estimatedTime: '4 hours',
    weekSlug: 'week-07-design-patterns',
    weekNumber: 7,
    starterFiles: [],
    requirements: ['Plugin discovery mechanism', 'Plugin loading system', 'Event handling', 'Configuration management'],
    hints: ['Factory pattern for plugin creation', 'Observer for event handling'],
  },
  {
    slug: 'week-08-project',
    title: 'E-Commerce System',
    description: 'Build a complete e-commerce backend with inventory, cart, and checkout. Apply all OOP principles in a capstone project.',
    difficulty: 'Expert',
    estimatedTime: '6 hours',
    weekSlug: 'week-08-capstone',
    weekNumber: 8,
    starterFiles: [],
    requirements: ['Product catalog', 'Shopping cart', 'Order processing', 'Inventory management', 'User accounts'],
    hints: ['Plan your class hierarchy', 'Test-driven development helps'],
  },
];

// Mock progress data - in real app, fetch from store
const mockProgress: Record<string, UserProjectProgress> = {
  'week-01-project': {
    projectSlug: 'week-01-project',
    status: 'in_progress',
    files: [
      { id: '1', name: 'calculator.py', path: '/calculator.py', content: '', language: 'python', isModified: false, lastModified: Date.now() },
    ],
    startTime: Date.now() - 86400000,
    lastActiveTime: Date.now(),
    totalTimeSpent: 3600,
  },
  'week-02-project': {
    projectSlug: 'week-02-project',
    status: 'submitted',
    files: [],
    startTime: Date.now() - 172800000,
    submissionTime: Date.now() - 86400000,
    totalTimeSpent: 7200,
    score: 95,
  },
};

export default function ProjectsPage() {
  const [activeTab, setActiveTab] = useState('all');

  const { activeProjects, completedProjects, notStartedProjects } = useMemo(() => {
    const active: WeeklyProject[] = [];
    const completed: WeeklyProject[] = [];
    const notStarted: WeeklyProject[] = [];

    allProjects.forEach(project => {
      const progress = mockProgress[project.slug];
      if (!progress || progress.status === 'not_started') {
        notStarted.push(project);
      } else if (progress.status === 'in_progress') {
        active.push(project);
      } else if (progress.status === 'submitted') {
        completed.push(project);
      }
    });

    return { activeProjects: active, completedProjects: completed, notStartedProjects: notStarted };
  }, []);

  const stats = {
    total: allProjects.length,
    completed: completedProjects.length,
    inProgress: activeProjects.length,
    notStarted: notStartedProjects.length,
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3">
            <FolderGit2 className="h-8 w-8 text-primary" />
            Projects
          </h1>
          <p className="text-muted-foreground mt-1">
            Apply what you learn through hands-on coding projects
          </p>
        </div>
        <Button asChild>
          <Link href="/weeks">
            <Plus className="h-4 w-4 mr-2" />
            Start New Project
          </Link>
        </Button>
      </div>

      {/* Stats Overview */}
      <div className="grid gap-4 sm:grid-cols-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
              <FolderGit2 className="h-5 w-5 text-primary" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.total}</p>
              <p className="text-sm text-muted-foreground">Total Projects</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-500/10">
              <Play className="h-5 w-5 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.inProgress}</p>
              <p className="text-sm text-muted-foreground">In Progress</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-green-500/10">
              <CheckCircle2 className="h-5 w-5 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.completed}</p>
              <p className="text-sm text-muted-foreground">Completed</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-yellow-500/10">
              <Trophy className="h-5 w-5 text-yellow-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{Math.round((stats.completed / stats.total) * 100)}%</p>
              <p className="text-sm text-muted-foreground">Completion</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Projects Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-4 sm:w-auto sm:inline-grid">
          <TabsTrigger value="all">
            All
            <Badge variant="secondary" className="ml-2 hidden sm:inline-flex">
              {stats.total}
            </Badge>
          </TabsTrigger>
          <TabsTrigger value="active">
            Active
            <Badge variant="secondary" className="ml-2 hidden sm:inline-flex">
              {stats.inProgress}
            </Badge>
          </TabsTrigger>
          <TabsTrigger value="completed">
            Completed
            <Badge variant="secondary" className="ml-2 hidden sm:inline-flex">
              {stats.completed}
            </Badge>
          </TabsTrigger>
          <TabsTrigger value="available">
            Available
            <Badge variant="secondary" className="ml-2 hidden sm:inline-flex">
              {stats.notStarted}
            </Badge>
          </TabsTrigger>
        </TabsList>

        <TabsContent value="all" className="mt-6">
          {allProjects.length > 0 ? (
            <div className="grid gap-4 lg:grid-cols-2">
              {allProjects.map(project => (
                <ProjectCard
                  key={project.slug}
                  project={project}
                  progress={mockProgress[project.slug]}
                  variant="detailed"
                />
              ))}
            </div>
          ) : (
            <ProjectEmptyState />
          )}
        </TabsContent>

        <TabsContent value="active" className="mt-6">
          {activeProjects.length > 0 ? (
            <div className="grid gap-4 lg:grid-cols-2">
              {activeProjects.map(project => (
                <ProjectCard
                  key={project.slug}
                  project={project}
                  progress={mockProgress[project.slug]}
                  variant="detailed"
                />
              ))}
            </div>
          ) : (
            <Card className="border-dashed">
              <CardContent className="p-12 text-center">
                <Play className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                <h3 className="font-medium mb-2">No Active Projects</h3>
                <p className="text-sm text-muted-foreground mb-4">
                  Start a project to see it here
                </p>
                <Button asChild>
                  <Link href="/weeks">Browse Projects</Link>
                </Button>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="completed" className="mt-6">
          {completedProjects.length > 0 ? (
            <div className="grid gap-4 lg:grid-cols-2">
              {completedProjects.map(project => (
                <ProjectCard
                  key={project.slug}
                  project={project}
                  progress={mockProgress[project.slug]}
                  variant="detailed"
                />
              ))}
            </div>
          ) : (
            <Card className="border-dashed">
              <CardContent className="p-12 text-center">
                <CheckCircle2 className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                <h3 className="font-medium mb-2">No Completed Projects</h3>
                <p className="text-sm text-muted-foreground mb-4">
                  Complete a project to see it here
                </p>
                <Button asChild>
                  <Link href="/weeks">Start a Project</Link>
                </Button>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="available" className="mt-6">
          {notStartedProjects.length > 0 ? (
            <div className="grid gap-4 lg:grid-cols-2">
              {notStartedProjects.map(project => (
                <ProjectCard
                  key={project.slug}
                  project={project}
                  variant="detailed"
                />
              ))}
            </div>
          ) : (
            <Card className="border-dashed">
              <CardContent className="p-12 text-center">
                <AlertCircle className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                <h3 className="font-medium mb-2">All Projects Started!</h3>
                <p className="text-sm text-muted-foreground mb-4">
                  Great job! You&apos;ve started all available projects.
                </p>
                <Button asChild variant="outline">
                  <Link href="/projects?tab=active">View Active</Link>
                </Button>
              </CardContent>
            </Card>
          )}
        </TabsContent>
      </Tabs>

      {/* Tips Section */}
      <Card className="bg-muted/50 border-dashed">
        <CardHeader>
          <CardTitle className="text-base flex items-center gap-2">
            <Calendar className="h-4 w-4" />
            Project Tips
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li className="flex items-start gap-2">
              <span className="text-primary">•</span>
              <span>Projects are designed to reinforce concepts from each week&apos;s lessons</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary">•</span>
              <span>Start with the README file to understand requirements</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary">•</span>
              <span>Use Ctrl+S to save files and Ctrl+R to run your code</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary">•</span>
              <span>Submit when ready - you can always come back to improve your solution</span>
            </li>
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}
