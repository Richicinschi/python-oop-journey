"use client";

import Link from "next/link";
import {
  BookOpen,
  Code2,
  Target,
  Trophy,
  ArrowRight,
  Sparkles,
  GraduationCap,
  Zap,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { ContinueLearningWidget } from "@/components/continue-learning";
import { Badge } from "@/components/ui/badge";
import { Footer } from "@/components/layout/footer";

const stats = [
  { label: "Weeks", value: "9", icon: BookOpen },
  { label: "Problems", value: "450+", icon: Code2 },
  { label: "Topics", value: "50+", icon: Target },
  { label: "Projects", value: "9", icon: Trophy },
];

const weeks = [
  {
    number: 0,
    slug: "week00_getting_started",
    title: "Getting Started",
    description: "Python basics, variables, types, and control flow",
    problems: 80,
    difficulty: "Beginner",
    color: "bg-green-500",
  },
  {
    number: 1,
    slug: "week01_fundamentals",
    title: "Fundamentals",
    description: "Math, strings, arrays, and basic algorithms",
    problems: 63,
    difficulty: "Beginner",
    color: "bg-blue-500",
  },
  {
    number: 2,
    slug: "week02_fundamentals_advanced",
    title: "Advanced Fundamentals",
    description: "File I/O, exceptions, modules, and functional programming",
    problems: 54,
    difficulty: "Intermediate",
    color: "bg-indigo-500",
  },
  {
    number: 3,
    slug: "week03_oop_basics",
    title: "OOP Basics",
    description: "Classes, objects, methods, and encapsulation",
    problems: 52,
    difficulty: "Intermediate",
    color: "bg-purple-500",
  },
  {
    number: 4,
    slug: "week04_oop_intermediate",
    title: "OOP Intermediate",
    description: "Inheritance, polymorphism, and special methods",
    problems: 38,
    difficulty: "Intermediate",
    color: "bg-pink-500",
  },
  {
    number: 5,
    slug: "week05_oop_advanced",
    title: "OOP Advanced",
    description: "Abstract classes, descriptors, and metaclasses",
    problems: 51,
    difficulty: "Advanced",
    color: "bg-orange-500",
  },
  {
    number: 6,
    slug: "week06_patterns",
    title: "Design Patterns",
    description: "Singleton, Factory, Observer, and more patterns",
    problems: 30,
    difficulty: "Advanced",
    color: "bg-red-500",
  },
  {
    number: 7,
    slug: "week07_real_world",
    title: "Real-World OOP",
    description: "Testing, documentation, and best practices",
    problems: 30,
    difficulty: "Advanced",
    color: "bg-yellow-500",
  },
  {
    number: 8,
    slug: "week08_capstone",
    title: "Capstone Project",
    description: "Build a complete library management system",
    problems: 5,
    difficulty: "Expert",
    color: "bg-emerald-500",
  },
];

export default function HomePage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden border-b bg-gradient-to-b from-background to-muted/30">
        <div className="container mx-auto px-4 py-16 md:py-24">
          <div className="max-w-3xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-sm font-medium mb-6">
              <Sparkles className="h-4 w-4" />
              Master Python OOP
            </div>
            <h1 className="text-4xl md:text-6xl font-bold tracking-tight mb-6">
              Your Journey to{" "}
              <span className="text-primary">Object-Oriented</span> Mastery
            </h1>
            <p className="text-lg md:text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
              Master Python OOP through hands-on exercises, real-world projects,
              and comprehensive curriculum designed to take you from beginner to
              expert.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button asChild size="lg" className="gap-2">
                <Link href="/weeks">
                  <Zap className="h-4 w-4" />
                  Start Learning
                </Link>
              </Button>
              <Button asChild size="lg" variant="outline" className="gap-2">
                <Link href="/weeks">
                  <GraduationCap className="h-4 w-4" />
                  Browse Curriculum
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {stats.map((stat) => (
            <Card key={stat.label} className="text-center">
              <CardContent className="pt-6">
                <stat.icon className="h-6 w-6 mx-auto text-primary mb-2" />
                <div className="text-3xl font-bold">{stat.value}</div>
                <div className="text-sm text-muted-foreground">{stat.label}</div>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* Main Content */}
      <section className="container mx-auto px-4 py-12">
        <div className="grid lg:grid-cols-[1fr,320px] gap-8">
          {/* Weeks Grid */}
          <div>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold">Curriculum Overview</h2>
              <Button variant="ghost" size="sm" asChild>
                <Link href="/weeks">
                  View All
                  <ArrowRight className="ml-1 h-4 w-4" />
                </Link>
              </Button>
            </div>
            <div className="grid sm:grid-cols-2 gap-4">
              {weeks.map((week) => (
                <WeekCard key={week.number} week={week} />
              ))}
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            <ContinueLearningWidget />

            <Card>
              <CardHeader>
                <CardTitle className="text-base">Quick Links</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <Button asChild variant="ghost" className="w-full justify-start">
                  <Link href="/search">
                    <Code2 className="mr-2 h-4 w-4" />
                    All Problems
                  </Link>
                </Button>
                <Button asChild variant="ghost" className="w-full justify-start">
                  <Link href="/recent">
                    <BookOpen className="mr-2 h-4 w-4" />
                    Recently Viewed
                  </Link>
                </Button>
                <Button asChild variant="ghost" className="w-full justify-start">
                  <Link href="/bookmarks">
                    <Target className="mr-2 h-4 w-4" />
                    My Bookmarks
                  </Link>
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-base">Keyboard Shortcuts</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 text-sm">
                  <div className="flex items-center justify-between">
                    <span className="text-muted-foreground">Search</span>
                    <kbd className="px-2 py-1 rounded bg-muted text-xs font-mono">
                      ⌘K
                    </kbd>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-muted-foreground">Quick Nav</span>
                    <kbd className="px-2 py-1 rounded bg-muted text-xs font-mono">
                      /
                    </kbd>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>
      <Footer />
    </div>
  );
}

function WeekCard({
  week,
}: {
  week: {
    number: number;
    slug: string;
    title: string;
    description: string;
    problems: number;
    difficulty: string;
    color: string;
  };
}) {
  return (
    <Link href={`/weeks/${week.slug}`}>
      <Card className="h-full hover:shadow-md transition-shadow group">
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between">
            <div className={`w-1 h-8 rounded-full ${week.color}`} />
            <Badge variant="secondary" className="text-[10px]">
              {week.difficulty}
            </Badge>
          </div>
          <CardTitle className="text-lg mt-2 group-hover:text-primary transition-colors">
            Week {week.number}: {week.title}
          </CardTitle>
          <CardDescription className="line-clamp-2">
            {week.description}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-sm text-muted-foreground">
            {week.problems} problems
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}
