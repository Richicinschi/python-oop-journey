/**
 * Curriculum data loader for static generation
 * Loads curriculum.json at build time
 */

import { Curriculum, Week, Day, Problem, Project } from '@/types/curriculum';
import type {
  TransformedCurriculum,
  TransformedWeek,
  TransformedDay,
  TransformedProblem,
  TransformedProject,
  TransformedProjectFile,
  ProjectTask,
} from '@/types/curriculum';

// Import curriculum.json at build time for static generation
import curriculumData from '@/data/curriculum.json';

let curriculumCache: Curriculum | null = null;

/**
 * Get the full curriculum data
 */
export function getCurriculum(): Curriculum {
  if (!curriculumCache) {
    curriculumCache = curriculumData as Curriculum;
  }
  return curriculumCache;
}

/**
 * Get all weeks
 */
export function getWeeks(): Week[] {
  return getCurriculum().weeks;
}

/**
 * Get a week by its slug
 */
export function getWeekBySlug(slug: string): Week | undefined {
  return getWeeks().find((week) => week.slug === slug);
}

/**
 * Get a day by week slug and day slug
 */
export function getDayBySlug(weekSlug: string, daySlug: string): Day | undefined {
  const week = getWeekBySlug(weekSlug);
  return week?.days.find((day) => day.slug === daySlug);
}

/**
 * Get a problem by week slug, day slug, and problem slug
 */
export function getProblemBySlug(
  weekSlug: string,
  daySlug: string,
  problemSlug: string
): Problem | undefined {
  const day = getDayBySlug(weekSlug, daySlug);
  return day?.problems.find((problem) => problem.slug === problemSlug);
}

/**
 * Get all problems across all weeks
 */
export function getAllProblems(): Problem[] {
  const weeks = getWeeks();
  const problems: Problem[] = [];
  
  for (const week of weeks) {
    for (const day of week.days) {
      problems.push(...day.problems);
    }
  }
  
  return problems;
}

/**
 * Get problems for a specific day
 */
export function getProblemsForDay(weekSlug: string, daySlug: string): Problem[] {
  const day = getDayBySlug(weekSlug, daySlug);
  return day?.problems || [];
}

/**
 * Find a problem by its slug across all weeks
 * Returns problem with both snake_case and camelCase properties
 */
export function findProblemBySlug(problemSlug: string): (Problem & { 
  weekNumber: number; 
  dayNumber: number;
  weekSlug: string;
  daySlug: string;
  starterCode: string;
  solutionCode: string;
  testCode: string;
}) | undefined {
  const weeks = getWeeks();
  
  for (const week of weeks) {
    for (const day of week.days) {
      const problem = day.problems.find((p) => p.slug === problemSlug);
      if (problem) {
        return { 
          ...problem, 
          weekNumber: week.order, 
          dayNumber: day.order,
          weekSlug: week.slug,
          daySlug: day.slug,
          starterCode: problem.starter_code,
          solutionCode: problem.solution_code,
          testCode: problem.test_code,
        };
      }
    }
  }
  
  return undefined;
}

/**
 * Get static params for week pages
 */
export function generateWeekParams(): { weekSlug: string }[] {
  return getWeeks().map((week) => ({
    weekSlug: week.slug,
  }));
}

/**
 * Get static params for day pages
 */
export function generateDayParams(): { weekSlug: string; daySlug: string }[] {
  const params: { weekSlug: string; daySlug: string }[] = [];
  
  for (const week of getWeeks()) {
    for (const day of week.days) {
      params.push({
        weekSlug: week.slug,
        daySlug: day.slug,
      });
    }
  }
  
  return params;
}

/**
 * Get static params for theory pages
 */
export function generateTheoryParams(): { weekSlug: string; daySlug: string }[] {
  return generateDayParams();
}

/**
 * Get difficulty color class
 */
export function getDifficultyColor(difficulty: string): string {
  switch (difficulty.toLowerCase()) {
    case 'easy':
    case 'beginner':
      return 'bg-green-500/10 text-green-600 border-green-500/20';
    case 'medium':
      return 'bg-yellow-500/10 text-yellow-600 border-yellow-500/20';
    case 'hard':
      return 'bg-red-500/10 text-red-600 border-red-500/20';
    default:
      return 'bg-gray-500/10 text-gray-600 border-gray-500/20';
  }
}

/**
 * Format week number for display
 */
export function formatWeekNumber(order: number): string {
  if (order === 0) return 'Week 0';
  return `Week ${order}`;
}

/**
 * Format day number for display
 */
export function formatDayNumber(order: number): string {
  return `Day ${order}`;
}

/**
 * Get total problem count for a week
 */
export function getWeekProblemCount(week: Week): number {
  return week.days.reduce((total, day) => total + day.problems.length, 0);
}

/**
 * Get completion percentage for a week (placeholder)
 */
export function getWeekProgress(week: Week): number {
  // TODO: Connect to user progress store
  return 0;
}

/**
 * Get completion percentage for a day (placeholder)
 */
export function getDayProgress(day: Day): number {
  // TODO: Connect to user progress store
  return 0;
}

// ============================================================================
// Convenience aliases for cleaner API
// ============================================================================

export const loadCurriculum = getCurriculum;
export const getWeek = getWeekBySlug;
export const getDay = getDayBySlug;
export const getProblem = findProblemBySlug;

/**
 * Search problems by query string (matches title or topic)
 */
export function searchProblems(query: string): Problem[] {
  const all = getAllProblems();
  const q = query.toLowerCase();
  return all.filter(p => 
    p.title.toLowerCase().includes(q) || 
    p.topic.toLowerCase().includes(q)
  );
}

// ============================================================================
// TRANSFORMATION FUNCTIONS
// ============================================================================

/**
 * Transform a raw ProjectFile to component-ready format
 */
function transformProjectFile(rawFile: any, index: number): TransformedProjectFile {
  return {
    id: rawFile.id || `file-${index}`,
    name: rawFile.name || rawFile.path?.split('/').pop() || 'unnamed',
    path: rawFile.path || '/',
    content: rawFile.content || rawFile.template || '',
    language: rawFile.language || getLanguageFromExtension(rawFile.path || ''),
    isModified: rawFile.isModified || false,
    lastModified: rawFile.lastModified || Date.now(),
    isEntryPoint: rawFile.isEntryPoint || false,
    template: rawFile.template,
  };
}

/**
 * Get language from file extension
 */
function getLanguageFromExtension(filename: string): string {
  const ext = filename.split('.').pop()?.toLowerCase() || '';
  const map: Record<string, string> = {
    py: 'python',
    md: 'markdown',
    txt: 'plaintext',
    json: 'json',
    yaml: 'yaml',
    yml: 'yaml',
  };
  return map[ext] || 'plaintext';
}

/**
 * Generate default project files
 */
function generateDefaultProjectFiles(title: string): TransformedProjectFile[] {
  return [
    {
      id: 'main-py',
      name: 'main.py',
      path: '/main.py',
      content: `# ${title}\n\ndef main():\n    pass\n\nif __name__ == "__main__":\n    main()`,
      language: 'python',
      isModified: false,
      lastModified: Date.now(),
      isEntryPoint: true,
    },
    {
      id: 'readme-md',
      name: 'README.md',
      path: '/README.md',
      content: `# ${title}\n\nSee project requirements.`,
      language: 'markdown',
      isModified: false,
      lastModified: Date.now(),
    },
  ];
}

/**
 * Generate default tasks from requirements
 */
function generateDefaultTasks(requirements: string[]): ProjectTask[] {
  return requirements.map((req, index) => ({
    id: `task-${index}`,
    description: req,
    completed: false,
    autoCheck: false,
  }));
}

/**
 * Transform a raw Project to component-ready format
 */
function transformProject(rawProject: any, weekOrder: number): TransformedProject {
  const requirements = rawProject.requirements || ['Complete the project'];
  const files = rawProject.files?.map((f: any, i: number) => transformProjectFile(f, i)) 
    || generateDefaultProjectFiles(rawProject.title);
  
  return {
    slug: rawProject.slug,
    title: rawProject.title,
    description: rawProject.description,
    overview: rawProject.overview || rawProject.description,
    entryPoint: rawProject.entryPoint || 'main.py',
    starterPath: rawProject.starter_path || null,
    solutionPath: rawProject.solution_path || null,
    testPath: rawProject.test_path || null,
    requirements,
    hints: rawProject.hints || [],
    files,
    tasks: rawProject.tasks || generateDefaultTasks(requirements),
  };
}

/**
 * Transform a raw Problem to component-ready format
 */
function transformProblem(
  rawProblem: any, 
  weekOrder: number, 
  dayOrder: number,
  allProblemsInDay: any[],
  problemIndex: number
): TransformedProblem {
  const nextProblem = allProblemsInDay[problemIndex + 1];
  const prevProblem = allProblemsInDay[problemIndex - 1];
  
  return {
    slug: rawProblem.slug,
    title: rawProblem.title,
    topic: rawProblem.topic,
    difficulty: rawProblem.difficulty,
    order: rawProblem.order,
    instructions: rawProblem.instructions,
    hints: rawProblem.hints || [],
    weekSlug: rawProblem.week_slug,
    daySlug: rawProblem.day_slug,
    weekNumber: weekOrder,
    dayNumber: dayOrder,
    starterCode: rawProblem.starter_code || '',
    solutionCode: rawProblem.solution_code || '',
    testCode: rawProblem.test_code || '',
    nextProblemSlug: nextProblem?.slug || null,
    prevProblemSlug: prevProblem?.slug || null,
  };
}

/**
 * Transform a raw Day to component-ready format
 */
function transformDay(rawDay: any, weekOrder: number): TransformedDay {
  const transformedProblems = rawDay.problems?.map((p: any, index: number) => 
    transformProblem(p, weekOrder, rawDay.order, rawDay.problems, index)
  ) || [];
  
  return {
    slug: rawDay.slug,
    title: rawDay.title,
    order: rawDay.order,
    problems: transformedProblems,
    weekSlug: rawDay.week_slug,
    theoryPath: rawDay.theory_path || null,
    theoryContent: rawDay.theory_content || '',
    learningObjectives: rawDay.learning_objectives || [],
  };
}

/**
 * Transform a raw Week to component-ready format
 */
function transformWeek(rawWeek: any): TransformedWeek {
  return {
    slug: rawWeek.slug,
    title: rawWeek.title,
    order: rawWeek.order,
    objective: rawWeek.objective || '',
    prerequisites: rawWeek.prerequisites || [],
    days: rawWeek.days?.map((d: any) => transformDay(d, rawWeek.order)) || [],
    project: rawWeek.project ? transformProject(rawWeek.project, rawWeek.order) : null,
  };
}

/**
 * Transform the full curriculum
 */
function transformCurriculum(rawCurriculum: any): TransformedCurriculum {
  return {
    version: rawCurriculum.version,
    weeks: rawCurriculum.weeks?.map((w: any) => transformWeek(w)) || [],
  };
}

// ============================================================================
// TRANSFORMED DATA GETTERS (use these in pages)
// ============================================================================

let transformedCache: TransformedCurriculum | null = null;

export function getTransformedCurriculum(): TransformedCurriculum {
  if (!transformedCache) {
    transformedCache = transformCurriculum(curriculumData);
  }
  return transformedCache;
}

export function getTransformedWeeks(): TransformedWeek[] {
  return getTransformedCurriculum().weeks;
}

export function getTransformedWeekBySlug(slug: string): TransformedWeek | undefined {
  return getTransformedWeeks().find((week) => week.slug === slug);
}

export function getTransformedDayBySlug(
  weekSlug: string, 
  daySlug: string
): TransformedDay | undefined {
  const week = getTransformedWeekBySlug(weekSlug);
  return week?.days.find((day) => day.slug === daySlug);
}

export function getTransformedProblemBySlug(problemSlug: string): TransformedProblem | undefined {
  for (const week of getTransformedWeeks()) {
    for (const day of week.days) {
      const problem = day.problems.find((p) => p.slug === problemSlug);
      if (problem) return problem;
    }
  }
  return undefined;
}

export function getAllTransformedProblems(): TransformedProblem[] {
  const problems: TransformedProblem[] = [];
  for (const week of getTransformedWeeks()) {
    for (const day of week.days) {
      problems.push(...day.problems);
    }
  }
  return problems;
}

export function getTransformedProjectForWeek(weekSlug: string): TransformedProject | null {
  const week = getTransformedWeekBySlug(weekSlug);
  return week?.project || null;
}
