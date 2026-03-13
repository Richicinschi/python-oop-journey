"use client";

import * as React from "react";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

const weeks = [
  { number: 0, title: "Getting Started", description: "Python basics and setup", difficulty: "Beginner", problems: 80 },
  { number: 1, title: "Fundamentals", description: "Core programming concepts", difficulty: "Beginner", problems: 63 },
  { number: 2, title: "Advanced Fundamentals", description: "File I/O and functional programming", difficulty: "Intermediate", problems: 54 },
  { number: 3, title: "OOP Basics", description: "Classes and objects", difficulty: "Intermediate", problems: 52 },
  { number: 4, title: "OOP Intermediate", description: "Inheritance and polymorphism", difficulty: "Intermediate", problems: 38 },
  { number: 5, title: "OOP Advanced", description: "Abstract classes and metaclasses", difficulty: "Advanced", problems: 51 },
  { number: 6, title: "Design Patterns", description: "Common design patterns", difficulty: "Advanced", problems: 30 },
  { number: 7, title: "Real-World OOP", description: "Testing and best practices", difficulty: "Advanced", problems: 30 },
  { number: 8, title: "Capstone Project", description: "Build a complete system", difficulty: "Expert", problems: 5 },
];

export default function WeeksPage() {
  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">All Weeks</h1>
        <p className="text-muted-foreground">
          Browse through all 9 weeks of the curriculum
        </p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        {weeks.map((week) => (
          <Link key={week.number} href={`/weeks/${week.number}`}>
            <Card className="h-full hover:shadow-md transition-shadow">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <CardTitle className="text-lg">Week {week.number}</CardTitle>
                  <Badge variant="secondary">{week.difficulty}</Badge>
                </div>
                <p className="font-medium">{week.title}</p>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground mb-4">
                  {week.description}
                </p>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-muted-foreground">
                    {week.problems} problems
                  </span>
                  <Button variant="ghost" size="sm">
                    View
                    <ArrowRight className="ml-1 h-4 w-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
