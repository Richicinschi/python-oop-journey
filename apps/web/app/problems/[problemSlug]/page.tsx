import { getAllTransformedProblems } from '@/lib/curriculum-loader';

// Generate static params for all problems (required for static export)
export function generateStaticParams() {
  const problems = getAllTransformedProblems();
  return problems.map((problem) => ({
    problemSlug: problem.slug,
  }));
}

// Re-export the client component
export { default } from './problem-page-client';
