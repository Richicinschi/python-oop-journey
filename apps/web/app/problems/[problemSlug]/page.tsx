'use client';

import { useEffect, useState, useCallback } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ChevronLeft, BookOpen, Eye } from 'lucide-react';
import { CodeEditor } from '@/components/editor/code-editor';
import { EditorToolbar } from '@/components/editor/editor-toolbar';
import { OutputPanel } from '@/components/editor/output-panel';
import { HintsPanel } from '@/components/editor/hints-panel';
import { InstructionsPanel } from '@/components/editor/instructions-panel';
import { SolutionModal } from '@/components/editor/solution-modal';
import { useLocalStorage } from '@/hooks/use-local-storage';
import { useProgress } from '@/hooks/use-progress';
import { verificationApi } from '@/lib/verification-api';
import { getCurriculum } from '@/lib/curriculum-loader';
import { Problem, Week, Day } from '@/types/curriculum';
import { cn, getDifficultyColor } from '@/lib/utils';

export default function ProblemPage() {
  const params = useParams<{ problemSlug: string }>();
  const { problemSlug } = params;

  // Load curriculum data
  const [problem, setProblem] = useState<Problem | null>(null);
  const [week, setWeek] = useState<Week | null>(null);
  const [day, setDay] = useState<Day | null>(null);
  const [prevProblem, setPrevProblem] = useState<Problem | null>(null);
  const [nextProblem, setNextProblem] = useState<Problem | null>(null);
  const [loading, setLoading] = useState(true);

  // Editor state
  const [code, setCode] = useState('');
  const [originalCode, setOriginalCode] = useState('');
  const [fontSize, setFontSize] = useLocalStorage('problem-editor-font-size', 14);
  const [wordWrap, setWordWrap] = useLocalStorage('problem-editor-word-wrap', true);

  // Execution state
  const [isRunning, setIsRunning] = useState(false);
  const [isVerifying, setIsVerifying] = useState(false);
  const [executionResult, setExecutionResult] = useState<{
    stdout: string;
    stderr: string;
    exitCode: number;
    executionTime?: number;
  } | null>(null);
  const [verificationResult, setVerificationResult] = useState<{
    passed: boolean;
    tests: { name: string; passed: boolean; error?: string }[];
    summary: string;
  } | null>(null);
  const [logs, setLogs] = useState<string[]>([]);

  // Hints and solution state
  const [revealedHints, setRevealedHints] = useLocalStorage<number[]>(`hints-${problemSlug}`, []);
  const [solutionShown, setSolutionShown] = useLocalStorage(`solution-shown-${problemSlug}`, false);
  const [isSolutionModalOpen, setIsSolutionModalOpen] = useState(false);

  // Progress tracking
  const { completeProblem, isCompleted, updateStreak } = useProgress();
  const [hasStarted, setHasStarted] = useLocalStorage(`started-${problemSlug}`, false);

  // Load problem data
  useEffect(() => {
    const curriculum = getCurriculum();
    
    // Find problem by slug across all weeks and days
    let foundProblem: Problem | null = null;
    let foundWeek: Week | null = null;
    let foundDay: Day | null = null;
    
    for (const w of curriculum.weeks) {
      for (const d of w.days) {
        const p = d.problems.find((prob) => prob.slug === problemSlug);
        if (p) {
          foundProblem = p;
          foundWeek = w;
          foundDay = d;
          break;
        }
      }
      if (foundProblem) break;
    }

    if (!foundProblem || !foundWeek || !foundDay) {
      setLoading(false);
      return;
    }

    setProblem(foundProblem);
    setWeek(foundWeek);
    setDay(foundDay);

    // Find prev/next problems within the same day
    const problemIndex = foundDay.problems.findIndex((p) => p.slug === problemSlug);
    setPrevProblem(problemIndex > 0 ? foundDay.problems[problemIndex - 1] : null);
    setNextProblem(
      problemIndex < foundDay.problems.length - 1
        ? foundDay.problems[problemIndex + 1]
        : null
    );

    // Load saved code or starter code
    const savedCode = localStorage.getItem(`code-${problemSlug}`);
    const starterCode = foundProblem.starter_code;
    setCode(savedCode || starterCode);
    setOriginalCode(starterCode);

    setLoading(false);
  }, [problemSlug]);

  // Auto-save code
  useEffect(() => {
    if (problem && code !== originalCode) {
      localStorage.setItem(`code-${problemSlug}`, code);
      if (!hasStarted) {
        setHasStarted(true);
        updateStreak();
      }
    }
  }, [code, problem, problemSlug, originalCode, hasStarted, setHasStarted, updateStreak]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.ctrlKey || e.metaKey) {
        if (e.key === 'Enter') {
          e.preventDefault();
          if (e.shiftKey) {
            handleVerify();
          } else {
            handleRun();
          }
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [code]);

  const addLog = useCallback((message: string) => {
    setLogs((prev) => [...prev.slice(-49), message]);
  }, []);

  const handleRun = async () => {
    setIsRunning(true);
    setExecutionResult(null);
    addLog('Running code...');

    try {
      // Try to validate syntax first using the verification API
      const validation = await verificationApi.validateSyntax(code);
      
      if (!validation.valid) {
        setExecutionResult({
          stdout: '',
          stderr: validation.message || 'Syntax error',
          exitCode: 1,
        });
        addLog('Syntax validation failed');
        setIsRunning(false);
        return;
      }

      // For now, simulate execution since we don't have a direct run endpoint
      await new Promise(resolve => setTimeout(resolve, 500));
      
      setExecutionResult({
        stdout: 'Code syntax is valid.\nNote: Full execution requires the Python runner service.',
        stderr: '',
        exitCode: 0,
        executionTime: 500,
      });
      addLog('Code validation completed');
    } catch (error) {
      addLog('Execution failed: Network error');
      setExecutionResult({
        stdout: '',
        stderr: 'Failed to execute code. Please try again.',
        exitCode: 1,
      });
    } finally {
      setIsRunning(false);
    }
  };

  const handleVerify = async () => {
    setIsVerifying(true);
    setVerificationResult(null);
    addLog('Running tests...');

    try {
      const response = await verificationApi.verifyForProblem(problemSlug, code);
      
      const passed = response.success && response.summary.failed === 0;
      
      setVerificationResult({
        passed,
        tests: response.tests.map(t => ({
          name: t.name,
          passed: t.status === 'passed',
          error: t.status !== 'passed' ? t.message : undefined,
        })),
        summary: `${response.summary.passed} of ${response.summary.total} tests passed`,
      });

      setExecutionResult({
        stdout: response.stdout || '',
        stderr: response.stderr || '',
        exitCode: passed ? 0 : 1,
        executionTime: response.execution_time_ms,
      });

      if (passed) {
        completeProblem(problemSlug);
        addLog('All tests passed! Problem marked as complete.');
      } else {
        addLog('Some tests failed. Check the verification tab for details.');
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Verification failed';
      addLog(`Verification failed: ${errorMessage}`);
      setVerificationResult({
        passed: false,
        tests: [],
        summary: errorMessage,
      });
    } finally {
      setIsVerifying(false);
    }
  };

  const handleReset = () => {
    if (confirm('Reset code to starter template? All changes will be lost.')) {
      setCode(originalCode);
      localStorage.removeItem(`code-${problemSlug}`);
      addLog('Code reset to starter template');
    }
  };

  const handleSave = () => {
    localStorage.setItem(`code-${problemSlug}`, code);
    addLog('Code saved');
  };

  const handleRevealHint = (hintIndex: number) => {
    if (!revealedHints.includes(hintIndex)) {
      setRevealedHints([...revealedHints, hintIndex]);
    }
  };

  const handleShowSolution = () => {
    setIsSolutionModalOpen(true);
  };

  const handleConfirmSolution = () => {
    setSolutionShown(true);
    addLog('Solution viewed');
  };

  const handleClearOutput = () => {
    setExecutionResult(null);
    setVerificationResult(null);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
      </div>
    );
  }

  if (!problem || !week || !day) {
    notFound();
  }

  const hasUnsavedChanges = code !== originalCode && code !== localStorage.getItem(`code-${problemSlug}`);
  const completed = isCompleted(problemSlug);

  // Parse examples from instructions
  const examples = parseExamples(problem.instructions);

  return (
    <div className="h-screen flex flex-col bg-background">
      {/* Breadcrumb Header */}
      <header className="border-b bg-card px-4 py-3 shrink-0">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-sm">
            <Link href="/weeks" className="text-muted-foreground hover:text-foreground">
              Weeks
            </Link>
            <ChevronLeft className="h-4 w-4 text-muted-foreground rotate-180" />
            <Link
              href={`/weeks/${week.slug}`}
              className="text-muted-foreground hover:text-foreground"
            >
              {week.title}
            </Link>
            <ChevronLeft className="h-4 w-4 text-muted-foreground rotate-180" />
            <Link
              href={`/weeks/${week.slug}/days/${day.slug}`}
              className="text-muted-foreground hover:text-foreground"
            >
              {day.title}
            </Link>
            <ChevronLeft className="h-4 w-4 text-muted-foreground rotate-180" />
            <span className="font-medium truncate max-w-[200px]">{problem.title}</span>
          </div>

          <div className="flex items-center gap-2">
            <Link href={`/weeks/${week.slug}/days/${day.slug}/theory`}>
              <Button variant="ghost" size="sm" className="gap-2">
                <BookOpen className="h-4 w-4" />
                Theory
              </Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Panel - Instructions */}
        <div className="w-[45%] min-w-[400px] max-w-[600px] border-r flex flex-col overflow-hidden">
          <InstructionsPanel
            title={problem.title}
            difficulty={problem.difficulty}
            topic={problem.topic}
            instructions={problem.instructions}
            examples={examples}
            theoryLink={`/weeks/${week.slug}/days/${day.slug}/theory`}
            isCompleted={completed}
            isStarted={hasStarted}
          />

          {/* Hints Section */}
          <div className="border-t p-4 bg-card shrink-0">
            <HintsPanel
              hints={problem.hints.length > 0 ? problem.hints : getDefaultHints()}
              revealedHints={revealedHints}
              onRevealHint={handleRevealHint}
            />
          </div>

          {/* Navigation */}
          <div className="border-t p-4 bg-card shrink-0">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                {prevProblem ? (
                  <Link href={`/problems/${prevProblem.slug}`}>
                    <Button variant="outline" size="sm">
                      ← Previous
                    </Button>
                  </Link>
                ) : (
                  <Button variant="outline" size="sm" disabled>
                    ← Previous
                  </Button>
                )}

                <Link href={`/weeks/${week.slug}/days/${day.slug}`}>
                  <Button variant="ghost" size="sm">
                    Back to Day
                  </Button>
                </Link>
              </div>

              <div className="flex items-center gap-2">
                <Button
                  onClick={handleShowSolution}
                  variant="outline"
                  size="sm"
                  className={cn(solutionShown && 'text-yellow-600')}
                >
                  <Eye className="mr-2 h-4 w-4" />
                  {solutionShown ? 'Solution' : 'Show Solution'}
                </Button>

                {nextProblem ? (
                  <Link href={`/problems/${nextProblem.slug}`}>
                    <Button variant="outline" size="sm">
                      Next →
                    </Button>
                  </Link>
                ) : (
                  <Button variant="outline" size="sm" disabled>
                    Next →
                  </Button>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Right Panel - Editor */}
        <div className="flex-1 flex flex-col min-w-[400px] overflow-hidden">
          <EditorToolbar
            hasUnsavedChanges={hasUnsavedChanges}
            fontSize={fontSize}
            wordWrap={wordWrap}
            onReset={handleReset}
            onSave={handleSave}
            onRun={handleRun}
            onFontSizeChange={setFontSize}
            onWordWrapChange={setWordWrap}
          />

          <div className="flex-1 overflow-hidden">
            <CodeEditor
              value={code}
              onChange={setCode}
              height="100%"
              fontSize={fontSize}
              wordWrap={wordWrap ? 'on' : 'off'}
              minimap={true}
              onRun={handleRun}
            />
          </div>

          <OutputPanel
            executionResult={executionResult}
            verificationResult={verificationResult}
            logs={logs}
            onClear={handleClearOutput}
          />
        </div>
      </div>

      {/* Solution Modal */}
      <SolutionModal
        isOpen={isSolutionModalOpen}
        onClose={() => setIsSolutionModalOpen(false)}
        onConfirm={handleConfirmSolution}
        solutionCode={problem.solution_code}
        userCode={code}
      />
    </div>
  );
}

function parseExamples(instructions: string): { input: string; output: string; explanation?: string }[] {
  const examples: { input: string; output: string; explanation?: string }[] = [];
  
  // Match example patterns like:
  // >>> function_name(input)
  // output
  const exampleRegex = />>>\s*(.+?)\n\s*(.+?)(?:\n\s*#\s*(.+?))?(?=\n\s*>>>|$)/gs;
  let match;
  
  while ((match = exampleRegex.exec(instructions)) !== null) {
    examples.push({
      input: match[1].trim(),
      output: match[2].trim(),
      explanation: match[3]?.trim(),
    });
  }

  return examples;
}

function getDefaultHints(): string[] {
  return [
    'Read the problem carefully and identify what needs to be returned.',
    'Break down the problem into smaller steps before coding.',
    'Consider edge cases like empty inputs or boundary values.',
  ];
}
