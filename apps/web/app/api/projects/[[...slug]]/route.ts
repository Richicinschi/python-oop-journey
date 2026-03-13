import { NextRequest, NextResponse } from 'next/server';
import { getCurriculum } from '@/lib/curriculum-loader';

// GET /api/projects/:slug - Get project data
// POST /api/projects/:slug/save - Save project files
// POST /api/projects/:slug/run - Run project
// POST /api/projects/:slug/submit - Submit project

export async function GET(
  request: NextRequest,
  { params }: { params: { slug?: string[] } }
) {
  try {
    const slugParts = params.slug || [];
    const projectSlug = slugParts[0];
    const action = slugParts[1];

    if (!projectSlug) {
      return NextResponse.json(
        { error: 'Project slug is required' },
        { status: 400 }
      );
    }

    const curriculum = getCurriculum();
    
    // Find project by slug
    let foundProject = null;
    let foundWeek = null;

    for (const week of curriculum.weeks) {
      if (week.project && week.project.slug === projectSlug) {
        foundWeek = week;
        foundProject = {
          ...week.project,
          weekSlug: week.slug,
          weekTitle: week.title,
          weekOrder: week.order,
        };
        break;
      }
    }

    if (!foundProject) {
      return NextResponse.json(
        { error: 'Project not found' },
        { status: 404 }
      );
    }

    return NextResponse.json({
      project: foundProject,
      week: foundWeek,
    });
  } catch (error) {
    console.error('Project API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function POST(
  request: NextRequest,
  { params }: { params: { slug?: string[] } }
) {
  try {
    const slugParts = params.slug || [];
    const projectSlug = slugParts[0];
    const action = slugParts[1];

    if (!projectSlug) {
      return NextResponse.json(
        { error: 'Project slug is required' },
        { status: 400 }
      );
    }

    const body = await request.json();

    switch (action) {
      case 'save':
        // In production, this would save to a database
        // For now, we just return success since client-side localStorage handles it
        return NextResponse.json({
          success: true,
          message: 'Project saved successfully',
          savedAt: new Date().toISOString(),
        });

      case 'run':
        // Execute project code
        const runResult = await executeProject(projectSlug, body.files, body.entryPoint);
        return NextResponse.json(runResult);

      case 'submit':
        // Submit project for review
        const submissionResult = await submitProject(projectSlug, body);
        return NextResponse.json(submissionResult);

      case 'test':
        // Run tests
        const testResult = await runTests(projectSlug, body.files, body.testFiles);
        return NextResponse.json(testResult);

      default:
        return NextResponse.json(
          { error: 'Invalid action' },
          { status: 400 }
        );
    }
  } catch (error) {
    console.error('Project API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

// Mock execution function
async function executeProject(
  projectSlug: string,
  files: Record<string, string>,
  entryPoint: string
): Promise<{
  success: boolean;
  stdout: string;
  stderr: string;
  exitCode: number;
  executionTime: number;
}> {
  const startTime = Date.now();

  // Simulate execution delay
  await new Promise(resolve => setTimeout(resolve, 1000));

  const entryContent = files[entryPoint] || '';

  // Check for NotImplementedError
  if (entryContent.includes('NotImplementedError') || entryContent.includes('pass')) {
    return {
      success: false,
      stdout: '',
      stderr: 'Error: NotImplementedError - Complete the implementation\n',
      exitCode: 1,
      executionTime: Date.now() - startTime,
    };
  }

  // Simulate successful execution
  return {
    success: true,
    stdout: `Executing ${entryPoint}...\nProject executed successfully.\n`,
    stderr: '',
    exitCode: 0,
    executionTime: Date.now() - startTime,
  };
}

// Mock test runner
async function runTests(
  projectSlug: string,
  files: Record<string, string>,
  testFiles?: Record<string, string>
): Promise<{
  success: boolean;
  summary: {
    total: number;
    passed: number;
    failed: number;
    errors: number;
  };
  tests: {
    name: string;
    status: 'passed' | 'failed' | 'error';
    message?: string;
  }[];
  stdout: string;
  stderr: string;
  executionTime: number;
}> {
  const startTime = Date.now();

  // Simulate test execution delay
  await new Promise(resolve => setTimeout(resolve, 1500));

  // Generate mock test results
  const mockTests = [
    { name: 'test_basic_functionality', status: 'passed' as const },
    { name: 'test_edge_cases', status: 'passed' as const },
    { name: 'test_error_handling', status: Math.random() > 0.5 ? 'passed' as const : 'failed' as const, message: 'Expected Exception, got None' },
  ];

  const passed = mockTests.filter(t => t.status === 'passed').length;
  const failed = mockTests.filter(t => t.status === 'failed').length;

  return {
    success: failed === 0,
    summary: {
      total: mockTests.length,
      passed,
      failed,
      errors: 0,
    },
    tests: mockTests,
    stdout: `\n============================= test session starts ==============================
platform linux -- Python 3.11.0, pytest-7.4.0, pluggy-1.1.0
rootdir: /workspace
plugins: anyio-3.7.1

collected ${mockTests.length} items

${mockTests.map(t => `${t.status === 'passed' ? '.' : 'F'} ${t.name}`).join('\n')}

=========================== short test summary info ============================
${failed > 0 ? `FAILED test_project.py::test_error_handling - ${mockTests.find(t => t.status === 'failed')?.message}` : ''}
================== ${passed} passed, ${failed} failed in 0.12s ==================
`,
    stderr: '',
    executionTime: Date.now() - startTime,
  };
}

// Mock submission handler
async function submitProject(
  projectSlug: string,
  data: {
    files: Record<string, string>;
    completedTasks: string[];
  }
): Promise<{
  success: boolean;
  submissionId: string;
  status: 'submitted' | 'pending_review';
  submittedAt: string;
}> {
  // Simulate submission processing
  await new Promise(resolve => setTimeout(resolve, 500));

  return {
    success: true,
    submissionId: `sub-${Date.now()}`,
    status: 'pending_review',
    submittedAt: new Date().toISOString(),
  };
}
