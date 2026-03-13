"use client";

import { useState, useCallback } from "react";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Separator } from "@/components/ui/separator";
import { 
  ChevronLeft, 
  Play,
  CheckCircle2,
  Clock,
  Lightbulb,
  BookOpen,
  RotateCcw
} from "lucide-react";
import { VerificationPanel } from "@/components/verification";
import { useVerification } from "@/hooks/use-verification";
import { findProblemBySlug, getDifficultyColor } from "@/lib/curriculum";
import { cn } from "@/lib/utils";

interface ProblemPageProps {
  params: {
    problemSlug: string;
  };
}

export default function ProblemPageWithVerification({ params }: ProblemPageProps) {
  const problem = findProblemBySlug(params.problemSlug);
  const [code, setCode] = useState(problem?.starter_code || "");
  const [activeHint, setActiveHint] = useState<number | null>(null);
  
  const { 
    data: verification, 
    isLoading: isVerifying, 
    error: verificationError, 
    verify,
    reset: resetVerification
  } = useVerification();

  if (!problem) {
    notFound();
  }

  const handleRunTests = useCallback(async () => {
    await verify({
      code,
      problem_slug: problem.slug,
    });
  }, [code, problem.slug, verify]);

  const handleResetCode = useCallback(() => {
    setCode(problem.starter_code || "");
    resetVerification();
  }, [problem.starter_code, resetVerification]);

  const handleShowHint = useCallback((hintIndex: number) => {
    setActiveHint(hintIndex);
    // Scroll to hints tab or show hint modal
    const hintsTab = document.querySelector('[data-value="hints"]');
    if (hintsTab instanceof HTMLElement) {
      hintsTab.click();
    }
  }, []);

  const allTestsPassed = verification?.success && verification?.summary.passed === verification?.summary.total;

  return (
    <div className="space-y-6">
      {/* Breadcrumb */}
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <Link href="/problems" className="hover:text-foreground">
          Problems
        </Link>
        <ChevronLeft className="h-4 w-4 rotate-180" />
        <span className="text-foreground">{problem.title}</span>
      </div>

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">{problem.title}</h1>
          <p className="text-muted-foreground mt-2">{problem.description}</p>
          <div className="flex items-center gap-2 mt-3">
            <Badge className={getDifficultyColor(problem.difficulty)}>
              {problem.difficulty}
            </Badge>
            <Badge variant="outline">Week {problem.weekNumber}</Badge>
            <Badge variant="outline">Day {problem.dayNumber}</Badge>
          </div>
        </div>
        <div className="flex gap-2">
          <Button 
            variant="outline" 
            className="gap-2"
            onClick={() => handleShowHint(0)}
          >
            <Lightbulb className="h-4 w-4" />
            Hint
          </Button>
          <Button 
            className={cn(
              "gap-2 transition-all",
              allTestsPassed && "bg-green-600 hover:bg-green-700"
            )}
            onClick={handleRunTests}
            disabled={isVerifying || !code.trim()}
          >
            {isVerifying ? (
              <>
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
                Running...
              </>
            ) : allTestsPassed ? (
              <>
                <CheckCircle2 className="h-4 w-4" />
                Completed
              </>
            ) : (
              <>
                <Play className="h-4 w-4" />
                Run Tests
              </>
            )}
          </Button>
        </div>
      </div>

      <Separator />

      {/* Main Content */}
      <div className="grid lg:grid-cols-2 gap-6">
        {/* Left Panel - Problem Description */}
        <div className="space-y-4">
          <Tabs defaultValue="description" className="w-full">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="description">Description</TabsTrigger>
              <TabsTrigger value="examples">Examples</TabsTrigger>
              <TabsTrigger value="hints" data-value="hints">Hints</TabsTrigger>
            </TabsList>

            <TabsContent value="description">
              <Card>
                <CardContent className="p-6">
                  <div className="prose prose-slate dark:prose-invert max-w-none">
                    <h3>Problem Statement</h3>
                    <p>{problem.description}</p>
                    
                    <h4>Requirements</h4>
                    <ul>
                      <li>Implement the solution using Python</li>
                      <li>Follow OOP principles where applicable</li>
                      <li>Handle edge cases appropriately</li>
                      <li>Write clean, readable code</li>
                    </ul>

                    <h4>Constraints</h4>
                    <ul>
                      <li>Time complexity should be optimal</li>
                      <li>Space complexity should be reasonable</li>
                      <li>Input will be valid Python code</li>
                    </ul>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="examples">
              <Card>
                <CardContent className="p-6 space-y-4">
                  <div>
                    <p className="font-medium mb-2">Example 1:</p>
                    <div className="bg-muted p-4 rounded-lg">
                      <p className="text-sm"><strong>Input:</strong> TBD</p>
                      <p className="text-sm"><strong>Output:</strong> TBD</p>
                      <p className="text-sm text-muted-foreground mt-2">
                        <strong>Explanation:</strong> Placeholder explanation
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="hints">
              <Card>
                <CardContent className="p-6">
                  <div className="space-y-4">
                    {problem.hints?.map((hint, index) => (
                      <div 
                        key={index} 
                        className={cn(
                          "flex gap-3 p-3 rounded-lg transition-colors",
                          activeHint === index && "bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800"
                        )}
                      >
                        <Lightbulb className={cn(
                          "h-5 w-5 shrink-0",
                          activeHint === index ? "text-yellow-600" : "text-yellow-500"
                        )} />
                        <div>
                          <p className="font-medium">Hint {index + 1}</p>
                          <p className="text-sm text-muted-foreground">{hint}</p>
                        </div>
                      </div>
                    )) || (
                      <p className="text-muted-foreground">No hints available for this problem.</p>
                    )}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>

          {/* Submission Status */}
          <Card>
            <CardHeader>
              <CardTitle className="text-sm font-medium">Submission Status</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  {verification ? (
                    allTestsPassed ? (
                      <>
                        <CheckCircle2 className="h-5 w-5 text-green-600" />
                        <span className="text-sm text-green-600 font-medium">
                          All tests passed!
                        </span>
                      </>
                    ) : (
                      <>
                        <Clock className="h-5 w-5 text-yellow-600" />
                        <span className="text-sm text-muted-foreground">
                          {verification.summary.passed}/{verification.summary.total} tests passed
                        </span>
                      </>
                    )
                  ) : (
                    <>
                      <CheckCircle2 className="h-5 w-5 text-muted-foreground" />
                      <span className="text-sm text-muted-foreground">Not submitted</span>
                    </>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Right Panel - Code Editor + Verification */}
        <div className="space-y-4">
          {/* Code Editor Card */}
          <Card className="flex flex-col">
            <CardHeader className="border-b">
              <div className="flex items-center justify-between">
                <CardTitle className="text-sm font-medium">Code Editor</CardTitle>
                <div className="flex items-center gap-2">
                  <Badge variant="outline">Python 3.11</Badge>
                  <Button 
                    variant="ghost" 
                    size="sm" 
                    onClick={handleResetCode}
                    className="h-8 gap-1"
                  >
                    <RotateCcw className="h-3.5 w-3.5" />
                    Reset
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent className="p-0">
              <textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                className="w-full h-[300px] p-4 font-mono text-sm bg-muted/30 resize-none focus:outline-none focus:ring-2 focus:ring-primary/50"
                placeholder="Write your solution here..."
                spellCheck={false}
              />
            </CardContent>
            <div className="border-t p-4">
              <div className="flex items-center justify-between">
                <Button variant="outline" className="gap-2" asChild>
                  <Link href={`/weeks/${problem.weekSlug}/days/${problem.daySlug}/theory`}>
                    <BookOpen className="h-4 w-4" />
                    Read Theory
                  </Link>
                </Button>
                <div className="flex gap-2">
                  <Button 
                    variant="outline" 
                    onClick={handleResetCode}
                  >
                    Reset
                  </Button>
                  <Button 
                    className={cn(
                      "gap-2",
                      allTestsPassed && "bg-green-600 hover:bg-green-700"
                    )}
                    onClick={handleRunTests}
                    disabled={isVerifying || !code.trim()}
                  >
                    {isVerifying ? (
                      <>
                        <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
                        Running...
                      </>
                    ) : allTestsPassed ? (
                      <>
                        <CheckCircle2 className="h-4 w-4" />
                        Submit
                      </>
                    ) : (
                      <>
                        <Play className="h-4 w-4" />
                        Run Tests
                      </>
                    )}
                  </Button>
                </div>
              </div>
            </div>
          </Card>

          {/* Verification Results */}
          <VerificationPanel
            verification={verification}
            isLoading={isVerifying}
            onRetry={handleRunTests}
            onGetHelp={handleShowHint}
          />

          {/* Error Display */}
          {verificationError && (
            <Card className="border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/10">
              <CardContent className="p-4">
                <p className="text-sm text-red-700 dark:text-red-300">
                  <span className="font-medium">Error:</span> {verificationError}
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>

      {/* Navigation */}
      <div className="flex justify-between pt-4">
        <Link href="/problems">
          <Button variant="outline">
            <ChevronLeft className="mr-2 h-4 w-4" />
            Back to Problems
          </Button>
        </Link>
        {allTestsPassed && (
          <Link href={`/problems/${problem.nextProblemSlug || ""}`}>
            <Button>
              Next Problem
              <ChevronLeft className="ml-2 h-4 w-4 rotate-180" />
            </Button>
          </Link>
        )}
      </div>
    </div>
  );
}
