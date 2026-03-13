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
    difficulty: 'beginner',
    estimatedHours: 2,
    week: 1,
    status: 'not_started',
    completedTasks: 0,
    totalTasks: 3,
  },
  {
    slug: 'week-02-project',
    title: 'Contact Book',
    description: 'Create a contact management system with add, search, and delete functionality. Practice working with dictionaries and file I/O.',
    difficulty: 'beginner',
    estimatedHours: 2,
    week: 2,
    status: 'not_started',
    completedTasks: 0,
    totalTasks: 4,
  },
  {
    slug: 'week-03-project',
    title: 'Bank Account Manager',
    description: 'Build a banking system with deposits, withdrawals, and balance tracking. Master encapsulation and private attributes.',
    difficulty: 'intermediate',
    estimatedHours: 3,
    week: 3,
    status: 'not_started',
    completedTasks: 0,
    totalTasks: 4,
  },
  {
    slug: 'week-04-project',
    title: 'Library Management System',
    description: 'Design a library system with books, patrons, and checkout tracking. Apply inheritance and composition principles.',
    difficulty: 'intermediate',
    estimatedHours: 3,
    week: 4,
    status: 'not_started',
    completedTasks: 0,
    totalTasks: 4,
  },
  {
    slug: 'week-05-project',
    title: 'Shape Drawing App',
    description: 'Create a polymorphic shape system with area calculations and drawing. Explore abstract classes and method overriding.',
    difficulty: 'intermediate',
    estimatedHours: 3,
    week: 5,
    status: 'not_started',
    completedTasks: 0,
    totalTasks: 4,
  },
  {
    slug: 'week-06-project',
    title: 'Custom Collection',
    description: 'Build your own list-like container with full iterator support. Master special methods and Python data model.',
    difficulty: 'advanced',
    estimatedHours: 3,
    week: 6,
    status: 'not_started',
    completedTasks: 0,
    totalTasks: 4,
  },
  {
    slug: 'week-07-project',
    title: 'Plugin System',
    description: 'Design an extensible plugin architecture using design patterns. Apply Factory, Observer, and Strategy patterns.',
    difficulty: 'advanced',
    estimatedHours: 4,
    week: 7,
    status: 'not_started',
    completedTasks: 0,
    totalTasks: 4,
  },
  {
    slug: 'week-08-project',
    title: 'E-Commerce System',
    description: 'Build a complete e-commerce backend with inventory, cart, and checkout. Apply all OOP principles in a capstone project.',
    difficulty: 'advanced',
    estimatedHours: 6,
    week: 8,
    status: 'not_started',
    completedTasks: 0,
    totalTasks: 5,
  },
];

// Mock progress data - in real app, fetch from store
const mockProgress: Record<string, UserProjectProgress> = {
  'week-01-project': {
    projectSlug: 'week-01-project',
    status: 'in_progress',
    completedTasks: ['task-1'],
    lastAccessed: new Date(Date.now() - 86400000).toISOString(),
  },
  'week-02-project': {
    projectSlug: 'week-02-project',
    status: 'submitted',
    completedTasks: ['task-1', 'task-2', 'task-3', 'task-4'],
    lastAccessed: new Date(Date.now() - 86400000).toISOString(),
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
