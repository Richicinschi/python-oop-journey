'use client';

import { useState, useEffect, useCallback } from 'react';
import { User } from '@/types/curriculum';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

const STORAGE_KEY = 'oop-journey-auth';

export function useAuth() {
  const [state, setState] = useState<AuthState>({
    user: null,
    isAuthenticated: false,
    isLoading: true,
  });

  useEffect(() => {
    // Check for stored auth (will be replaced with API validation)
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        setState({
          user: parsed.user,
          isAuthenticated: true,
          isLoading: false,
        });
      } catch {
        setState({
          user: null,
          isAuthenticated: false,
          isLoading: false,
        });
      }
    } else {
      setState((prev) => ({ ...prev, isLoading: false }));
    }
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    // Placeholder - will be replaced with actual API call
    const mockUser: User = {
      id: '1',
      name: 'John Doe',
      email,
    };

    const authData = {
      user: mockUser,
      token: 'mock-token',
    };

    localStorage.setItem(STORAGE_KEY, JSON.stringify(authData));
    setState({
      user: mockUser,
      isAuthenticated: true,
      isLoading: false,
    });

    return mockUser;
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem(STORAGE_KEY);
    setState({
      user: null,
      isAuthenticated: false,
      isLoading: false,
    });
  }, []);

  const updateUser = useCallback((updates: Partial<User>) => {
    setState((prev) => {
      if (!prev.user) return prev;
      
      const updatedUser = { ...prev.user, ...updates };
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        localStorage.setItem(STORAGE_KEY, JSON.stringify({
          ...parsed,
          user: updatedUser,
        }));
      }
      
      return {
        ...prev,
        user: updatedUser,
      };
    });
  }, []);

  return {
    user: state.user,
    isAuthenticated: state.isAuthenticated,
    isLoading: state.isLoading,
    login,
    logout,
    updateUser,
  };
}
