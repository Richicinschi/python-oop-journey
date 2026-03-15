'use client';

import { createContext, useContext, useEffect, useState, ReactNode, useCallback } from 'react';

type Theme = 'dark' | 'light' | 'system';

interface ThemeProviderProps {
  children: ReactNode;
  defaultTheme?: Theme;
  // Ignored props (for next-themes compatibility)
  attribute?: string;
  enableSystem?: boolean;
  disableTransitionOnChange?: boolean;
}

interface ThemeContextType {
  theme: Theme;
  setTheme: (theme: Theme) => void;
  systemTheme: 'dark' | 'light';
  resolvedTheme: 'dark' | 'light';
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

const STORAGE_KEY = 'python-oop-journey-theme';

export function ThemeProvider({ 
  children, 
  defaultTheme = 'system',
  enableSystem = true 
}: ThemeProviderProps) {
  const [theme, setThemeState] = useState<Theme>(defaultTheme);
  const [systemTheme, setSystemTheme] = useState<'dark' | 'light'>('light');
  const [mounted, setMounted] = useState(false);

  // Initialize theme from localStorage on mount
  useEffect(() => {
    setMounted(true);
    
    // Check localStorage first
    const stored = localStorage.getItem(STORAGE_KEY) as Theme | null;
    if (stored && ['light', 'dark', 'system'].includes(stored)) {
      setThemeState(stored);
    } else if (enableSystem) {
      setThemeState('system');
    }

    // Detect system theme
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    setSystemTheme(mediaQuery.matches ? 'dark' : 'light');

    const handler = (e: MediaQueryListEvent) => {
      setSystemTheme(e.matches ? 'dark' : 'light');
    };

    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, [enableSystem]);

  // Apply theme to document
  useEffect(() => {
    if (!mounted) return;

    const root = document.documentElement;
    const effectiveTheme = theme === 'system' ? systemTheme : theme;

    root.classList.remove('light', 'dark');
    root.classList.add(effectiveTheme);
  }, [theme, systemTheme, mounted]);

  // Persist theme to localStorage
  const setTheme = useCallback((newTheme: Theme) => {
    setThemeState(newTheme);
    localStorage.setItem(STORAGE_KEY, newTheme);
  }, []);

  const resolvedTheme = theme === 'system' ? systemTheme : theme;

  return (
    <ThemeContext.Provider value={{ theme, setTheme, systemTheme, resolvedTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}
