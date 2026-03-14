'use client';

import { useState, useCallback, useEffect, useRef } from 'react';
import { 
  WeeklyProject, 
  UserProjectProgress, 
  ProjectStatus,
  EditorTab,
  AnalyticsEvent
} from '@/types/project';
import { ProjectFile } from '@/types/project-files';

const STORAGE_KEY = 'oop-journey-projects-v1';
const ANALYTICS_KEY = 'oop-journey-project-analytics-v1';

interface ProjectStore {
  projects: Record<string, UserProjectProgress>;
  currentProject: WeeklyProject | null;
  activeTabs: EditorTab[];
  activeFileId: string | null;
}

const createDefaultProjectProgress = (projectSlug: string): UserProjectProgress => ({
  projectSlug,
  status: 'not_started',
  completedTasks: [],
  lastAccessed: new Date().toISOString(),
  files: [],
  totalTimeSpent: 0,
});

export function useProjectStore() {
  const [store, setStore] = useState<ProjectStore>({
    projects: {},
    currentProject: null,
    activeTabs: [],
    activeFileId: null,
  });
  const [isLoading, setIsLoading] = useState(true);
  const sessionStartTime = useRef<number | null>(null);
  const analyticsBuffer = useRef<AnalyticsEvent[]>([]);

  // Load from localStorage on mount
  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        setStore(prev => ({ ...prev, projects: parsed.projects || {} }));
      } catch {
        console.warn('Failed to load project data');
      }
    }
    setIsLoading(false);
  }, []);

  // Save to localStorage when projects change
  useEffect(() => {
    if (!isLoading) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({ projects: store.projects }));
    }
  }, [store.projects, isLoading]);

  // Track session time
  useEffect(() => {
    if (store.currentProject && store.projects[store.currentProject.slug]?.status === 'in_progress') {
      sessionStartTime.current = Date.now();
      
      const interval = setInterval(() => {
        if (sessionStartTime.current) {
          const elapsed = Math.floor((Date.now() - sessionStartTime.current) / 1000);
          updateTimeSpent(store.currentProject!.slug, elapsed);
          sessionStartTime.current = Date.now();
        }
      }, 60000); // Update every minute

      return () => {
        clearInterval(interval);
        sessionStartTime.current = null;
      };
    }
  }, [store.currentProject?.slug]);

  const startProject = useCallback((project: WeeklyProject) => {
    setStore(prev => {
      const existing = prev.projects[project.slug];
      const updated: UserProjectProgress = existing 
        ? { ...existing, status: 'in_progress', startTime: existing.startTime || Date.now(), lastActiveTime: Date.now() }
        : { 
            projectSlug: project.slug, 
            status: 'in_progress', 
            completedTasks: [],
            lastAccessed: new Date().toISOString(),
            files: [...(project.starterFiles ?? [])],
            startTime: Date.now(),
            lastActiveTime: Date.now(),
            totalTimeSpent: 0,
          };

      // Initialize tabs with first file
      const initialTabs: EditorTab[] = (updated.files ?? [])
        .filter((file): file is typeof file & { id: string; name: string } => !!file.id && !!file.name)
        .slice(0, 3)
        .map((file, index) => ({
          id: `tab-${file.id}`,
          fileId: file.id,
          fileName: file.name,
          filePath: file.path,
          isModified: false,
          isActive: index === 0,
        }));

      return {
        ...prev,
        currentProject: project,
        projects: { ...prev.projects, [project.slug]: updated },
        activeTabs: initialTabs,
        activeFileId: initialTabs[0]?.fileId || null,
      };
    });

    trackEvent(project.slug, 'project_started');
  }, []);

  const updateTimeSpent = useCallback((projectSlug: string, additionalSeconds: number) => {
    setStore(prev => {
      const project = prev.projects[projectSlug];
      if (!project) return prev;

      return {
        ...prev,
        projects: {
          ...prev.projects,
          [projectSlug]: {
            ...project,
            totalTimeSpent: (project.totalTimeSpent ?? 0) + additionalSeconds,
            lastActiveTime: Date.now(),
          },
        },
      };
    });
  }, []);

  const updateFileContent = useCallback((fileId: string, content: string) => {
    setStore(prev => {
      if (!prev.currentProject) return prev;

      const projectSlug = prev.currentProject.slug;
      const project = prev.projects[projectSlug];
      if (!project) return prev;

      const updatedFiles = (project.files ?? []).map(f => 
        f.id === fileId 
          ? { ...f, content, isModified: true, lastModified: Date.now() }
          : f
      );

      const wasModified = (project.files ?? []).find(f => f.id === fileId)?.content !== content;

      // Update tabs to reflect modified state
      const updatedTabs = prev.activeTabs.map(tab => 
        tab.fileId === fileId ? { ...tab, isModified: true } : tab
      );

      return {
        ...prev,
        projects: {
          ...prev.projects,
          [projectSlug]: { ...project, files: updatedFiles },
        },
        activeTabs: updatedTabs,
      };
    });

    if (store.currentProject) {
      trackEvent(store.currentProject.slug, 'file_edited', { fileId });
    }
  }, [store.currentProject]);

  const saveFile = useCallback((fileId: string) => {
    setStore(prev => {
      if (!prev.currentProject) return prev;

      const projectSlug = prev.currentProject.slug;
      const project = prev.projects[projectSlug];
      if (!project) return prev;

      const updatedFiles = (project.files ?? []).map(f => 
        f.id === fileId 
          ? { ...f, isModified: false }
          : f
      );

      const updatedTabs = prev.activeTabs.map(tab => 
        tab.fileId === fileId ? { ...tab, isModified: false } : tab
      );

      return {
        ...prev,
        projects: {
          ...prev.projects,
          [projectSlug]: { ...project, files: updatedFiles },
        },
        activeTabs: updatedTabs,
      };
    });

    if (store.currentProject) {
      trackEvent(store.currentProject.slug, 'file_saved', { fileId });
    }
  }, [store.currentProject]);

  const createFile = useCallback((name: string, path: string = '/') => {
    setStore(prev => {
      if (!prev.currentProject) return prev;

      const projectSlug = prev.currentProject.slug;
      const project = prev.projects[projectSlug];
      if (!project) return prev;

      const newFile: ProjectFile = {
        id: `file-${Date.now()}`,
        name,
        path: `${path}${name}`,
        content: '',
        language: name.split('.').pop() || 'python',
        isModified: false,
        lastModified: Date.now(),
      };

      const newTab: EditorTab = {
        id: `tab-${newFile.id}`,
        fileId: newFile.id!,
        fileName: newFile.name!,
        filePath: newFile.path,
        isModified: false,
        isActive: true,
      };

      return {
        ...prev,
        projects: {
          ...prev.projects,
          [projectSlug]: { 
            ...project, 
            files: [...(project.files ?? []), newFile],
            lastActiveTime: Date.now(),
          },
        },
        activeTabs: prev.activeTabs.map(t => ({ ...t, isActive: false })).concat(newTab),
        activeFileId: (newFile.id ?? null) as string | null,
      };
    });

    if (store.currentProject) {
      trackEvent(store.currentProject.slug, 'file_created', { fileName: name });
    }
  }, [store.currentProject]);

  const deleteFile = useCallback((fileId: string) => {
    setStore(prev => {
      if (!prev.currentProject) return prev;

      const projectSlug = prev.currentProject.slug;
      const project = prev.projects[projectSlug];
      if (!project) return prev;

      const updatedFiles = (project.files ?? []).filter(f => f.id !== fileId);
      const updatedTabs = prev.activeTabs.filter(t => t.fileId !== fileId);
      
      // Activate another tab if we closed the active one
      let newActiveFileId = prev.activeFileId;
      if (prev.activeFileId === fileId && updatedTabs.length > 0) {
        newActiveFileId = updatedTabs[updatedTabs.length - 1].fileId;
        updatedTabs[updatedTabs.length - 1].isActive = true;
      }

      return {
        ...prev,
        projects: {
          ...prev.projects,
          [projectSlug]: { ...project, files: updatedFiles },
        },
        activeTabs: updatedTabs,
        activeFileId: newActiveFileId,
      };
    });
  }, []);

  const openTab = useCallback((fileId: string) => {
    setStore(prev => {
      if (!prev.currentProject) return prev;

      const file = (prev.projects[prev.currentProject.slug]?.files ?? []).find(f => f.id === fileId);
      if (!file) return prev;

      const existingTab = prev.activeTabs.find(t => t.fileId === fileId);
      if (existingTab) {
        return {
          ...prev,
          activeTabs: prev.activeTabs.map(t => ({ ...t, isActive: t.fileId === fileId })),
          activeFileId: fileId,
        };
      }

      const newTab: EditorTab = {
        id: `tab-${fileId}`,
        fileId: file.id!,
        fileName: file.name!,
        filePath: file.path,
        isModified: file.isModified ?? false,
        isActive: true,
      };

      // Limit to 5 tabs
      const newTabs = prev.activeTabs
        .map(t => ({ ...t, isActive: false }))
        .concat(newTab)
        .slice(-5);

      return {
        ...prev,
        activeTabs: newTabs,
        activeFileId: fileId,
      };
    });
  }, []);

  const closeTab = useCallback((tabId: string) => {
    setStore(prev => {
      const tabToClose = prev.activeTabs.find(t => t.id === tabId);
      const updatedTabs = prev.activeTabs.filter(t => t.id !== tabId);
      
      let newActiveFileId = prev.activeFileId;
      if (tabToClose?.fileId === prev.activeFileId && updatedTabs.length > 0) {
        newActiveFileId = updatedTabs[updatedTabs.length - 1].fileId;
        updatedTabs[updatedTabs.length - 1].isActive = true;
      } else if (updatedTabs.length === 0) {
        newActiveFileId = null;
      }

      return {
        ...prev,
        activeTabs: updatedTabs,
        activeFileId: newActiveFileId,
      };
    });
  }, []);

  const submitProject = useCallback(() => {
    setStore(prev => {
      if (!prev.currentProject) return prev;

      const projectSlug = prev.currentProject.slug;
      const project = prev.projects[projectSlug];
      if (!project) return prev;

      // Save all modified files first
      const updatedFiles = (project.files ?? []).map(f => ({ ...f, isModified: false }));

      return {
        ...prev,
        projects: {
          ...prev.projects,
          [projectSlug]: {
            ...project,
            status: 'submitted',
            files: updatedFiles,
            submissionTime: Date.now(),
          },
        },
        activeTabs: prev.activeTabs.map(t => ({ ...t, isModified: false })),
      };
    });

    if (store.currentProject) {
      trackEvent(store.currentProject.slug, 'project_submitted');
      flushAnalytics();
    }
  }, [store.currentProject]);

  const getProjectProgress = useCallback((projectSlug: string): UserProjectProgress | undefined => {
    return store.projects[projectSlug];
  }, [store.projects]);

  const getActiveFile = useCallback((): ProjectFile | undefined => {
    if (!store.currentProject || !store.activeFileId) return undefined;
    return (store.projects[store.currentProject.slug]?.files ?? []).find(f => f.id === store.activeFileId);
  }, [store.currentProject, store.activeFileId, store.projects]);

  // Analytics tracking
  const trackEvent = (projectSlug: string, type: AnalyticsEvent['type'], metadata?: Record<string, unknown>) => {
    const event: AnalyticsEvent = {
      id: `evt-${Date.now()}`,
      type,
      timestamp: Date.now(),
      metadata,
    };
    analyticsBuffer.current.push(event);

    // Flush every 10 events or when project is submitted
    if (analyticsBuffer.current.length >= 10) {
      flushAnalytics();
    }
  };

  const flushAnalytics = () => {
    if (analyticsBuffer.current.length === 0) return;
    
    const stored = localStorage.getItem(ANALYTICS_KEY);
    const analytics = stored ? JSON.parse(stored) : {};
    
    analyticsBuffer.current.forEach(event => {
      const projectSlug = store.currentProject?.slug;
      if (projectSlug) {
        if (!analytics[projectSlug]) analytics[projectSlug] = [];
        analytics[projectSlug].push(event);
      }
    });

    localStorage.setItem(ANALYTICS_KEY, JSON.stringify(analytics));
    analyticsBuffer.current = [];
  };

  return {
    currentProject: store.currentProject,
    activeTabs: store.activeTabs,
    activeFileId: store.activeFileId,
    isLoading,
    startProject,
    updateFileContent,
    saveFile,
    createFile,
    deleteFile,
    openTab,
    closeTab,
    submitProject,
    getProjectProgress,
    getActiveFile,
    trackEvent: (type: AnalyticsEvent['type'], metadata?: Record<string, unknown>) => {
      if (store.currentProject) {
        trackEvent(store.currentProject.slug, type, metadata);
      }
    },
  };
}

// Hook for keyboard shortcuts
export function useProjectKeyboardShortcuts({
  onSave,
  onSaveAll,
  onRun,
  onTest,
  onToggleFileTree,
  onSplitEditor,
}: {
  onSave?: () => void;
  onSaveAll?: () => void;
  onRun?: () => void;
  onTest?: () => void;
  onToggleFileTree?: () => void;
  onSplitEditor?: () => void;
}) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Ctrl+S - Save current file
      if (e.ctrlKey && e.key === 's' && !e.shiftKey) {
        e.preventDefault();
        onSave?.();
      }

      // Ctrl+Shift+S - Save all files
      if (e.ctrlKey && e.shiftKey && e.key === 'S') {
        e.preventDefault();
        onSaveAll?.();
      }

      // Ctrl+R - Run project
      if (e.ctrlKey && e.key === 'r' && !e.shiftKey) {
        e.preventDefault();
        onRun?.();
      }

      // Ctrl+T - Run tests
      if (e.ctrlKey && e.key === 't' && !e.shiftKey) {
        e.preventDefault();
        onTest?.();
      }

      // Ctrl+B - Toggle file tree
      if (e.ctrlKey && e.key === 'b' && !e.shiftKey) {
        e.preventDefault();
        onToggleFileTree?.();
      }

      // Ctrl+\ - Split editor
      if (e.ctrlKey && e.key === '\\') {
        e.preventDefault();
        onSplitEditor?.();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onSave, onSaveAll, onRun, onTest, onToggleFileTree, onSplitEditor]);
}
