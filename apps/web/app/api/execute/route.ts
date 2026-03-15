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

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * POST /api/execute
 * Execute Python code by forwarding to the backend API
 */
export async function POST(
  request: NextRequest
): Promise<NextResponse<ExecutionResponse>> {
  try {
    const body: ExecutionRequest = await request.json();
    const { code, mode } = body;

    if (!code || typeof code !== 'string') {
      return NextResponse.json(
        {
          success: false,
          stdout: '',
          stderr: 'No code provided',
          exitCode: 1,
        },
        { status: 400 }
      );
    }

    if (mode === 'run') {
      // Call backend execution API
      const response = await fetch(`${API_BASE_URL}/api/v1/execute/run`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code,
          language: 'python',
          timeout: 10,
        }),
      });

      // Handle HTTP errors gracefully
      if (!response.ok) {
        let errorMessage = 'Execution failed';
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorData.error || `HTTP ${response.status}`;
        } catch {
          errorMessage = `HTTP ${response.status}: ${response.statusText}`;
        }
        
        return NextResponse.json(
          {
            success: false,
            stdout: '',
            stderr: errorMessage,
            exitCode: 1,
          },
          { status: 200 } // Return 200 so frontend can display error
        );
      }

      const result = await response.json();
      
      return NextResponse.json({
        success: result.success ?? (result.exit_code === 0),
        stdout: result.output || result.stdout || '',
        stderr: result.error || result.stderr || '',
        exitCode: result.exit_code ?? 0,
        executionTime: result.execution_time_ms,
      });
    } else {
      // Verification mode - call verification API
      // This would need problem_slug which isn't in the request
      // For now return mock response
      return NextResponse.json({
        success: false,
        stdout: '',
        stderr: 'Verification mode requires problem context. Use verify endpoint directly.',
        exitCode: 1,
      });
    }
  } catch (error) {
    console.error('Execution error:', error);
    return NextResponse.json(
      {
        success: false,
        stdout: '',
        stderr: error instanceof Error ? error.message : 'Network error',
        exitCode: 1,
      },
      { status: 200 } // Return 200 so frontend can display error
    );
  }
}
