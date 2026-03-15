"use client";

import * as React from "react";
import Link from "next/link";
import {
  Home,
  BookOpen,
  Search,
  Code2,
  FileQuestion,
  ArrowLeft,
  Terminal,
  Bug,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

// Animated 404 illustration component using CSS animations
function NotFoundIllustration() {
  return (
    <div className="relative w-48 h-48 mx-auto">
      {/* Background glow effect */}
      <div className="absolute inset-0 bg-primary/10 rounded-full blur-3xl animate-pulse" />
      
      {/* Floating code blocks with CSS animations */}
      <div
        className="absolute top-4 left-4 w-16 h-16 bg-muted rounded-lg border-2 border-dashed border-muted-foreground/30 flex items-center justify-center animate-bounce"
        style={{ animationDuration: '4s', animationTimingFunction: 'ease-in-out' }}
      >
        <Code2 className="h-8 w-8 text-muted-foreground/50" />
      </div>

      <div
        className="absolute top-8 right-4 w-14 h-14 bg-muted rounded-lg border-2 border-dashed border-muted-foreground/30 flex items-center justify-center animate-bounce"
        style={{ animationDuration: '3.5s', animationTimingFunction: 'ease-in-out', animationDelay: '0.5s' }}
      >
        <Terminal className="h-7 w-7 text-muted-foreground/50" />
      </div>

      <div
        className="absolute bottom-8 left-8 w-12 h-12 bg-muted rounded-lg border-2 border-dashed border-muted-foreground/30 flex items-center justify-center animate-bounce"
        style={{ animationDuration: '3s', animationTimingFunction: 'ease-in-out', animationDelay: '1s' }}
      >
        <Bug className="h-6 w-6 text-muted-foreground/50" />
      </div>

      {/* Main 404 circle with scale animation */}
      <div className="absolute inset-0 flex items-center justify-center animate-in zoom-in duration-500">
        <div className="w-32 h-32 rounded-full bg-gradient-to-br from-primary/20 to-primary/5 border-2 border-primary/30 flex items-center justify-center backdrop-blur-sm">
          <div className="text-center">
            <FileQuestion className="h-12 w-12 mx-auto text-primary mb-1" />
            <span className="text-2xl font-bold text-primary">404</span>
          </div>
        </div>
      </div>

      {/* Decorative dots with pulse animation */}
      <div
        className="absolute bottom-4 right-6 w-3 h-3 rounded-full bg-primary/40 animate-pulse"
        style={{ animationDuration: '2s' }}
      />
      <div
        className="absolute top-2 left-1/2 w-2 h-2 rounded-full bg-primary/30 animate-pulse"
        style={{ animationDuration: '2.5s', animationDelay: '0.3s' }}
      />
    </div>
  );
}

// Suggested links data
const suggestedLinks = [
  {
    href: "/",
    label: "Home",
    description: "Return to the main page",
    icon: Home,
  },
  {
    href: "/weeks",
    label: "Curriculum",
    description: "Browse all learning weeks",
    icon: BookOpen,
  },
  {
    href: "/problems",
    label: "Problems",
    description: "Explore coding exercises",
    icon: Code2,
  },
];

export default function NotFoundPage() {
  return (
    <div className="min-h-[calc(100vh-3.5rem)] flex items-center justify-center p-4">
      <div className="w-full max-w-2xl">
        <Card className="border-dashed">
          <CardHeader className="text-center pb-2">
            {/* Animated Illustration */}
            <NotFoundIllustration />

            <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 delay-150">
              <Badge variant="secondary" className="mb-4">
                Page Not Found
              </Badge>
              <CardTitle className="text-3xl md:text-4xl font-bold tracking-tight mb-2">
                Lost in the Code?
              </CardTitle>
              <CardDescription className="text-base max-w-md mx-auto">
                The page you&apos;re looking for seems to have wandered off into the 
                digital void. Let&apos;s get you back on track.
              </CardDescription>
            </div>
          </CardHeader>

          <CardContent className="space-y-6">
            {/* Suggested Links */}
            <div className="grid gap-3 animate-in fade-in slide-in-from-bottom-4 duration-500 delay-200">
              {suggestedLinks.map((link, index) => (
                <div
                  key={link.href}
                  className="animate-in slide-in-from-left-4 fade-in"
                  style={{ animationDelay: `${0.3 + index * 0.1}s` }}
                >
                  <Link href={link.href}>
                    <Button
                      variant="ghost"
                      className="w-full justify-start h-auto py-3 px-4 group"
                    >
                      <div className="flex items-start gap-4 w-full">
                        <div className="flex-shrink-0 w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center group-hover:bg-primary/20 transition-colors">
                          <link.icon className="h-5 w-5 text-primary" />
                        </div>
                        <div className="flex-1 text-left">
                          <div className="font-medium text-foreground group-hover:text-primary transition-colors">
                            {link.label}
                          </div>
                          <div className="text-sm text-muted-foreground">
                            {link.description}
                          </div>
                        </div>
                        <ArrowLeft className="h-4 w-4 text-muted-foreground rotate-180 opacity-0 group-hover:opacity-100 transition-opacity" />
                      </div>
                    </Button>
                  </Link>
                </div>
              ))}
            </div>

            {/* Search Suggestion */}
            <div 
              className="pt-4 border-t animate-in fade-in slide-in-from-bottom-4 duration-500"
              style={{ animationDelay: '0.5s' }}
            >
              <p className="text-sm text-muted-foreground text-center mb-3">
                Looking for something specific?
              </p>
              <div className="flex flex-col sm:flex-row gap-3 justify-center">
                <Button asChild variant="outline" className="gap-2">
                  <Link href="/search">
                    <Search className="h-4 w-4" />
                    Search Problems
                  </Link>
                </Button>
                <Button asChild className="gap-2">
                  <Link href="/weeks">
                    <BookOpen className="h-4 w-4" />
                    Browse Curriculum
                  </Link>
                </Button>
              </div>
            </div>

            {/* Error Code */}
            <div 
              className="text-center pt-2 animate-in fade-in duration-500"
              style={{ animationDelay: '0.6s' }}
            >
              <code className="text-xs text-muted-foreground bg-muted px-2 py-1 rounded">
                Error Code: 404 | Page Not Found
              </code>
            </div>
          </CardContent>
        </Card>

        {/* Brand Footer */}
        <div 
          className="text-center mt-8 animate-in fade-in duration-500"
          style={{ animationDelay: '0.7s' }}
        >
          <Link href="/" className="inline-flex items-center gap-2 text-muted-foreground hover:text-primary transition-colors">
            <BookOpen className="h-5 w-5" />
            <span className="font-semibold">Python OOP Journey</span>
          </Link>
          <p className="text-xs text-muted-foreground mt-2">
            Master Object-Oriented Programming, one step at a time.
          </p>
        </div>
      </div>
    </div>
  );
}
