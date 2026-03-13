'use client';

import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Copy, Trash2, CheckCircle2, XCircle, AlertCircle } from 'lucide-react';
import { useState } from 'react';
import { cn } from '@/lib/utils';

interface TestResult {
  name: string;
  passed: boolean;
  error?: string;
}

interface ExecutionResult {
  stdout: string;
  stderr: string;
  exitCode: number;
  executionTime?: number;
}

interface VerificationResult {
  passed: boolean;
  tests: TestResult[];
  summary: string;
}

interface OutputPanelProps {
  executionResult: ExecutionResult | null;
  verificationResult: VerificationResult | null;
  logs: string[];
  onClear: () => void;
}

export function OutputPanel({
  executionResult,
  verificationResult,
  logs,
  onClear,
}: OutputPanelProps) {
  const [activeTab, setActiveTab] = useState('output');
  const [copied, setCopied] = useState(false);

  const copyOutput = () => {
    let content = '';
    if (executionResult) {
      content += `STDOUT:\n${executionResult.stdout}\n\n`;
      content += `STDERR:\n${executionResult.stderr}\n`;
    }
    if (verificationResult) {
      content += `\nVerification: ${verificationResult.summary}\n`;
    }
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getOutputContent = () => {
    if (!executionResult) return '';
    let content = '';
    if (executionResult.stdout) content += executionResult.stdout + '\n';
    if (executionResult.stderr) content += executionResult.stderr + '\n';
    if (executionResult.exitCode !== 0 && !executionResult.stderr) {
      content += `Process exited with code ${executionResult.exitCode}\n`;
    }
    return content || 'No output';
  };

  return (
    <div className="border-t bg-card flex flex-col h-[250px]">
      <Tabs
        value={activeTab}
        onValueChange={setActiveTab}
        className="flex flex-col h-full"
      >
        <div className="flex items-center justify-between px-3 py-2 border-b">
          <TabsList className="h-8">
            <TabsTrigger value="output" className="text-xs">
              Output
              {executionResult && executionResult.exitCode !== 0 && (
                <AlertCircle className="ml-1 h-3 w-3 text-red-500" />
              )}
            </TabsTrigger>
            <TabsTrigger value="verification" className="text-xs">
              Verification
              {verificationResult && (
                <span className="ml-1">
                  {verificationResult.passed ? (
                    <CheckCircle2 className="h-3 w-3 text-green-500" />
                  ) : (
                    <XCircle className="h-3 w-3 text-red-500" />
                  )}
                </span>
              )}
            </TabsTrigger>
            <TabsTrigger value="console" className="text-xs">
              Console
              {logs.length > 0 && (
                <Badge variant="secondary" className="ml-1 text-[10px] h-4 px-1">
                  {logs.length}
                </Badge>
              )}
            </TabsTrigger>
          </TabsList>
          <div className="flex items-center gap-1">
            <Button
              onClick={copyOutput}
              variant="ghost"
              size="sm"
              className="h-7 px-2"
            >
              {copied ? 'Copied!' : <Copy className="h-3 w-3" />}
            </Button>
            <Button
              onClick={onClear}
              variant="ghost"
              size="sm"
              className="h-7 px-2"
            >
              <Trash2 className="h-3 w-3" />
            </Button>
          </div>
        </div>

        <div className="flex-1 overflow-hidden">
          <TabsContent value="output" className="h-full m-0">
            <ScrollArea className="h-full">
              <div className="p-3 font-mono text-sm">
                {executionResult ? (
                  <>
                    {executionResult.stdout && (
                      <pre className="whitespace-pre-wrap text-foreground">
                        {executionResult.stdout}
                      </pre>
                    )}
                    {executionResult.stderr && (
                      <pre className="whitespace-pre-wrap text-red-500 mt-2">
                        {executionResult.stderr}
                      </pre>
                    )}
                    {executionResult.exitCode !== 0 && (
                      <div className="text-red-500 mt-2">
                        Process exited with code {executionResult.exitCode}
                      </div>
                    )}
                    {executionResult.executionTime && (
                      <div className="text-muted-foreground text-xs mt-2">
                        Execution time: {executionResult.executionTime}ms
                      </div>
                    )}
                  </>
                ) : (
                  <span className="text-muted-foreground">
                    Run your code to see output here
                  </span>
                )}
              </div>
            </ScrollArea>
          </TabsContent>

          <TabsContent value="verification" className="h-full m-0">
            <ScrollArea className="h-full">
              <div className="p-3">
                {verificationResult ? (
                  <div className="space-y-3">
                    <div
                      className={cn(
                        'flex items-center gap-2 p-3 rounded-lg',
                        verificationResult.passed
                          ? 'bg-green-500/10 text-green-600'
                          : 'bg-red-500/10 text-red-600'
                      )}
                    >
                      {verificationResult.passed ? (
                        <CheckCircle2 className="h-5 w-5" />
                      ) : (
                        <XCircle className="h-5 w-5" />
                      )}
                      <span className="font-medium">
                        {verificationResult.summary}
                      </span>
                    </div>
                    <div className="space-y-2">
                      {verificationResult.tests.map((test, index) => (
                        <div
                          key={index}
                          className={cn(
                            'flex items-start gap-2 p-2 rounded text-sm',
                            test.passed
                              ? 'bg-green-500/5'
                              : 'bg-red-500/5'
                          )}
                        >
                          {test.passed ? (
                            <CheckCircle2 className="h-4 w-4 text-green-500 shrink-0 mt-0.5" />
                          ) : (
                            <XCircle className="h-4 w-4 text-red-500 shrink-0 mt-0.5" />
                          )}
                          <div className="flex-1">
                            <span className="font-medium">{test.name}</span>
                            {test.error && !test.passed && (
                              <pre className="text-xs text-red-500 mt-1 whitespace-pre-wrap">
                                {test.error}
                              </pre>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ) : (
                  <span className="text-muted-foreground">
                    Click Verify to run tests
                  </span>
                )}
              </div>
            </ScrollArea>
          </TabsContent>

          <TabsContent value="console" className="h-full m-0">
            <ScrollArea className="h-full">
              <div className="p-3 font-mono text-sm space-y-1">
                {logs.length > 0 ? (
                  logs.map((log, index) => (
                    <div
                      key={index}
                      className="text-muted-foreground border-l-2 border-muted pl-2"
                    >
                      <span className="text-xs text-muted-foreground/60">
                        {new Date().toLocaleTimeString()}
                      </span>{' '}
                      {log}
                    </div>
                  ))
                ) : (
                  <span className="text-muted-foreground">
                    No console messages
                  </span>
                )}
              </div>
            </ScrollArea>
          </TabsContent>
        </div>
      </Tabs>
    </div>
  );
}
