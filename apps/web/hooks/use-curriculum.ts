'use client';

import { useState, useEffect } from 'react';
import { Week, Day, Problem } from '@/types/curriculum';
import { getWeeks, getWeekBySlug, getDayBySlug, getAllProblems, getProblemBySlugOnly } from '@/lib/curriculum-loader';

export function useWeeks() {
  const [weeks, setWeeks] = useState<Week[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // In the future, this will fetch from the API
    const data = getWeeks();
    setWeeks(data);
    setIsLoading(false);
  }, []);

  return { weeks, isLoading };
}

export function useWeek(slug: string) {
  const [week, setWeek] = useState<Week | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const data = getWeekBySlug(slug);
    setWeek(data || null);
    setIsLoading(false);
  }, [slug]);

  return { week, isLoading };
}

export function useDay(weekSlug: string, daySlug: string) {
  const [day, setDay] = useState<Day | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const data = getDayBySlug(weekSlug, daySlug);
    setDay(data || null);
    setIsLoading(false);
  }, [weekSlug, daySlug]);

  return { day, isLoading };
}

export function useProblems() {
  const [problems, setProblems] = useState<Problem[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const data = getAllProblems();
    setProblems(data);
    setIsLoading(false);
  }, []);

  return { problems, isLoading };
}

export function useProblem(slug: string) {
  const [problem, setProblem] = useState<Problem | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const data = getProblemBySlugOnly(slug);
    setProblem(data || null);
    setIsLoading(false);
  }, [slug]);

  return { problem, isLoading };
}
