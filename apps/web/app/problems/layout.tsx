'use client';

import { ThemeProvider } from '@/components/theme-provider';

export default function ProblemsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  // Full-screen layout for problem solving - no sidebar/header
  // ThemeProvider is already in root layout, but we ensure dark mode works
  return (
    <div className="h-screen overflow-hidden">
      {children}
    </div>
  );
}
