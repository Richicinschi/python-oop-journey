import { NextRequest, NextResponse } from 'next/server';

interface ExecutionRequest {
  code: string;
  testCode?: string;
  mode: 'run' | 'verify';
}

interface ExecutionResponse {
  success: boolean;
  stdout: string;
  stderr: string;
  exitCode: number;
  executionTime?: number;
  testResults?: {
    name: string;
    passed: boolean;
    error?: string;
  }[];
}

/**
 * POST /api/execute
 * Execute Python code or run tests
 * 
 * For now, this is a mock implementation that returns simulated results.
 * In production, this would connect to a sandboxed execution environment.
 */
export async function POST(
  request: NextRequest
): Promise<NextResponse<ExecutionResponse>> {
  try {
    const body: ExecutionRequest = await request.json();
    const { code, testCode, mode } = body;

    // TODO: Connect to real execution environment (Agent 10)
    // For now, return mock responses based on the code

    const startTime = Date.now();

    // Simulate execution delay
    await new Promise((resolve) => setTimeout(resolve, 500));

    if (mode === 'run') {
      // Simple code execution mode
      const result = simulateCodeExecution(code);
      return NextResponse.json({
        ...result,
        executionTime: Date.now() - startTime,
      });
    } else {
      // Verification mode with tests
      const result = simulateTestExecution(code, testCode || '');
      return NextResponse.json({
        ...result,
        executionTime: Date.now() - startTime,
      });
    }
  } catch (error) {
    console.error('Execution error:', error);
    return NextResponse.json(
      {
        success: false,
        stdout: '',
        stderr: 'Internal server error',
        exitCode: 1,
      },
      { status: 500 }
    );
  }
}

function simulateCodeExecution(code: string): Omit<ExecutionResponse, 'executionTime'> {
  // Check for NotImplementedError
  if (code.includes('NotImplementedError') || code.includes('pass')) {
    return {
      success: false,
      stdout: '',
      stderr: 'Error: Function not implemented yet. Remove "raise NotImplementedError" and write your solution.',
      exitCode: 1,
    };
  }

  // Check for syntax errors (basic)
  if (!code.includes('def ') && code.includes('return')) {
    return {
      success: false,
      stdout: '',
      stderr: 'SyntaxError: return outside function',
      exitCode: 1,
    };
  }

  // Return success with placeholder output
  return {
    success: true,
    stdout: 'Code executed successfully.\nNo output to display.',
    stderr: '',
    exitCode: 0,
  };
}

function simulateTestExecution(
  code: string,
  testCode: string
): Omit<ExecutionResponse, 'executionTime'> {
  // Check for NotImplementedError
  if (code.includes('NotImplementedError') || code.includes('pass')) {
    return {
      success: false,
      stdout: '',
      stderr: '',
      exitCode: 1,
      testResults: [
        {
          name: 'test_basic',
          passed: false,
          error: 'NotImplementedError: Function not implemented yet',
        },
      ],
    };
  }

  // Parse the function name from code
  const funcMatch = code.match(/def\s+(\w+)\s*\(/);
  const funcName = funcMatch ? funcMatch[1] : 'unknown';

  // Generate mock test results based on the function
  const testResults = generateMockTestResults(funcName, code);
  const allPassed = testResults.every((t) => t.passed);

  return {
    success: allPassed,
    stdout: allPassed ? 'All tests passed!' : 'Some tests failed.',
    stderr: '',
    exitCode: allPassed ? 0 : 1,
    testResults,
  };
}

function generateMockTestResults(
  funcName: string,
  code: string
): { name: string; passed: boolean; error?: string }[] {
  const tests: { name: string; passed: boolean; error?: string }[] = [];

  // Add some mock tests based on function patterns
  if (code.includes('return') && !code.includes('raise')) {
    // Function has a return statement - assume it might be correct
    tests.push({
      name: 'test_basic_case',
      passed: true,
    });
    tests.push({
      name: 'test_edge_case',
      passed: Math.random() > 0.3, // Simulate some edge cases failing
      error: Math.random() > 0.3 ? undefined : 'Expected 42, got 0',
    });
  } else {
    tests.push({
      name: 'test_basic_case',
      passed: false,
      error: 'Function returned None',
    });
  }

  return tests;
}
