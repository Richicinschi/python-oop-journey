"use client";

import { useState } from 'react';
import { Sidebar } from '@/components/layout/sidebar';
import { Header } from '@/components/layout/header';
import { AuthProvider } from '@/contexts/auth-context';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  // Create QueryClient instance for this layout
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 60 * 1000, // 1 minute
        retry: 1,
      },
    },
  }));

  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <div className="flex h-screen overflow-hidden">
          {/* Sidebar */}
          <Sidebar className="w-64 hidden md:flex" />
          
          {/* Main Content */}
          <div className="flex flex-col flex-1 overflow-hidden">
            <Header />
            <main className="flex-1 overflow-y-auto p-6">
              {children}
            </main>
          </div>
        </div>
      </AuthProvider>
    </QueryClientProvider>
  );
}
