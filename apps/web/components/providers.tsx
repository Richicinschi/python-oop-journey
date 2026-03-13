"use client";

import { ReactNode } from "react";
import { AuthProvider } from "@/contexts/auth-context";
import { ThemeProvider } from "@/components/theme-provider";

interface ProvidersProps {
  children: ReactNode;
}

export function Providers({ children }: ProvidersProps) {
  return (
    <ThemeProvider defaultTheme="system">
      <AuthProvider>
        <div className="min-h-screen bg-background">{children}</div>
      </AuthProvider>
    </ThemeProvider>
  );
}
