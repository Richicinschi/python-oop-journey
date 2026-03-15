'use client';

import { useEffect, useState, useCallback, useRef } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { ChevronLeft, BookOpen, Eye } from 'lucide-react';
import { CodeEditor } from '@/components/editor/code-editor';
import { EditorToolbar } from '@/components/editor/editor-toolbar';
import { OutputPanel } from '@/components/editor/output-panel';
import { HintsPanel } from '@/components/editor/hints-panel';
import { InstructionsPanel } from '@/components/editor/instructions-panel';
import { SolutionModal } from '@/components/editor/solution-modal';
import { ProblemSkeleton } from '@/components/problems/problem-skeleton';
import { useLocalStorage } from '@/hooks/use-local-storage';
import { useProgress } from '@/hooks/use-progress';
import { verificationApi } from '@/lib/verification-api';
import { getTransformedProblemBySlug, getTransformedWeekBySlug, getTransformedDayBySlug } from '@/lib/curriculum-loader';
import { TransformedProblem, TransformedWeek, TransformedDay } from '@/types/curriculum';
import { cn, getDifficultyColor } from '@/lib/utils';

export default function ProblemPage() {
  const params = useParams<{ problemSlug: string }>();
  const { problemSlug } = params;

  // Load curriculum data
  const [problem, setProblem] = useState<TransformedProblem | null>(null);
  const [week, setWeek] = useState<TransformedWeek | null>(null);
  const [day, setDay] = useState<TransformedDay | null>(null);
  const [prevProblem, setPrevProblem] = useState<TransformedProblem | null>(null);
  const [nextProblem, setNextProblem] = useState<TransformedProblem | null>(null);
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
    try {
      console.log('[ProblemPage] Loading problem:', problemSlug);
      const foundProblem = getTransformedProblemBySlug(problemSlug);
      
      if (!foundProblem) {
        console.error('[ProblemPage] Problem not found:', problemSlug);
        setLoading(false);
        return;
      }

      console.log('[ProblemPage] Found problem:', foundProblem.title, 'weekSlug:', foundProblem.weekSlug, 'daySlug:', foundProblem.daySlug);
      setProblem(foundProblem);

      // Load week and day data
      const foundWeek = foundProblem.weekSlug ? getTransformedWeekBySlug(foundProblem.weekSlug) ?? null : null;
      const foundDay = foundProblem.weekSlug && foundProblem.daySlug 
        ? getTransformedDayBySlug(foundProblem.weekSlug, foundProblem.daySlug) ?? null
        : null;

      console.log('[ProblemPage] Found week:', foundWeek?.title || 'null', 'day:', foundDay?.title || 'null');
      setWeek(foundWeek);
      setDay(foundDay);

      // Find prev/next problems using the slugs from transformed data
      if (foundProblem.prevProblemSlug) {
        setPrevProblem(getTransformedProblemBySlug(foundProblem.prevProblemSlug) ?? null);
      }
      if (foundProblem.nextProblemSlug) {
        setNextProblem(getTransformedProblemBySlug(foundProblem.nextProblemSlug) ?? null);
      }

      // Load saved code or starter code
      const savedCode = localStorage.getItem(`code-${problemSlug}`);
      const starterCode = foundProblem.starterCode;
      setCode(savedCode || starterCode);
      setOriginalCode(starterCode);
    } catch (error) {
      console.error('[ProblemPage] Error loading problem data:', error);
    } finally {
      setLoading(false);
    }
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

  // Define refs for keyboard shortcuts (will be assigned after functions are defined)
  const handleRunRef = useRef<(() => void) | null>(null);
  const handleVerifyRef = useRef<(() => void) | null>(null);

  const addLog = useCallback((message: string) => {
    setLogs((prev) => [...prev.slice(-49), message]);
  }, []);

  const handleRun = useCallback(async () => {
    setIsRunning(true);
    setExecutionResult(null);
    addLog('Running code...');

    try {
      // Call the backend execution API
      const response = await fetch('/api/execute', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code,
          mode: 'run',
        }),
      });

      const result = await response.json();

      setExecutionResult({
        stdout: result.stdout || '',
        stderr: result.stderr || '',
        exitCode: result.exitCode || 0,
        executionTime: result.executionTime,
      });

      if (result.exitCode === 0) {
        addLog('Code executed successfully');
      } else {
        addLog(`Execution failed with exit code ${result.exitCode}`);
      }
    } catch (error) {
      addLog('Execution failed: Network error');
      setExecutionResult({
        stdout: '',
        stderr: error instanceof Error ? error.message : 'Failed to execute code. Please try again.',
        exitCode: 1,
      });
    } finally {
      setIsRunning(false);
    }
  }, [code, addLog, problemSlug]);

  const handleVerify = useCallback(async () => {
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
  }, [code, addLog, problemSlug, completeProblem]);

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

  // Update refs to point to current function versions
  handleRunRef.current = handleRun;
  handleVerifyRef.current = handleVerify;

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.ctrlKey || e.metaKey) {
        if (e.key === 'Enter') {
          e.preventDefault();
          if (e.shiftKey) {
            handleVerifyRef.current?.();
          } else {
            handleRunRef.current?.();
          }
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  if (loading) {
    return <ProblemSkeleton />;
  }

  // Show error state if problem not found
  if (!problem) {
    return (
      <div className="h-screen flex flex-col items-center justify-center bg-background p-4">
        <div className="text-center max-w-md">
          <h1 className="text-2xl font-bold text-destructive mb-2">Problem Not Found</h1>
          <p className="text-muted-foreground mb-4">
            Could not find problem with slug: <code className="bg-muted px-1 py-0.5 rounded">{problemSlug}</code>
          </p>
          <p className="text-sm text-muted-foreground mb-6">
            The problem you&apos;re looking for doesn&apos;t exist or has been moved.
          </p>
          <div className="flex gap-2 justify-center">
            <Link href="/weeks">
              <Button variant="default">Browse All Weeks</Button>
            </Link>
            <Link href="/">
              <Button variant="outline">Go Home</Button>
            </Link>
          </div>
        </div>
      </div>
    );
  }

  // Show error if week or day data is missing (shouldn't normally happen)
  if (!week || !day) {
    return (
      <div className="h-screen flex flex-col items-center justify-center bg-background p-4">
        <div className="text-center max-w-md">
          <h1 className="text-2xl font-bold text-destructive mb-2">Data Error</h1>
          <p className="text-muted-foreground mb-4">
            Problem found but missing parent data.
          </p>
          <p className="text-sm text-muted-foreground mb-6">
            weekSlug: <code className="bg-muted px-1 py-0.5 rounded">{problem.weekSlug || 'null'}</code>
            <br />
            daySlug: <code className="bg-muted px-1 py-0.5 rounded">{problem.daySlug || 'null'}</code>
          </p>
          <div className="flex gap-2 justify-center">
            <Link href="/weeks">
              <Button variant="default">Browse All Weeks</Button>
            </Link>
          </div>
        </div>
      </div>
    );
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
              problemSlug={problemSlug}
              code={code}
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
            isRunning={isRunning}
            isVerifying={isVerifying}
            onReset={handleReset}
            onSave={handleSave}
            onRun={handleRun}
            onVerify={handleVerify}
            onFontSizeChange={setFontSize}
            onWordWrapChange={setWordWrap}
          />

          <div className="flex-1 relative min-h-0">
            <CodeEditor
              value={code}
              onChange={(value) => value !== undefined && setCode(value)}
              height="100%"
              fontSize={fontSize}
              wordWrap={wordWrap ? 'on' : 'off'}
              minimap={true}
              onRun={handleRun}
              className="absolute inset-0"
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
        solutionCode={problem.solutionCode}
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
