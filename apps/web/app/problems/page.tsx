import { redirect } from 'next/navigation';

/**
 * Problems index page
 * Redirects to search page for now
 */
export default function ProblemsPage() {
  redirect('/search');
}
