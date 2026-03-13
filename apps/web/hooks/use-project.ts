'use client';

import { useCallback, useEffect, useState } from 'react';
import { ProjectTask, ProjectStatus } from '@/types/project';
import { ProjectFile } from '@/types/project-files';

interface UseProjectOptions {
  projectSlug: string;
  initialFiles: ProjectFile[];
  initialTasks: ProjectTask[];
  entryPoint: string;
}

interface UseProjectReturn {
  // Files
  files: ProjectFile[];
  activeFile: ProjectFile | null;
  setActiveFile: (file: ProjectFile | null) => void;
  updateFileContent: (path: string, content: string) => void;
  addFile: (path: string, content?: string) => void;
  deleteFile: (path: string) => void;
  
  // Tasks
  tasks: ProjectTask[];
  completedTasks: Set<string>;
  toggleTask: (taskId: string) => void;
  taskProgress: number;
  
  // Status
  status: ProjectStatus;
  setStatus: (status: ProjectStatus) => void;
  
  // Actions
  save: () => Promise<void>;
  submit: () => Promise<void>;
  reset: () => void;
  
  // Loading states
  isSaving: boolean;
  isSubmitting: boolean;
}

export function useProject({
  projectSlug,
  initialFiles,
  initialTasks,
  entryPoint,
}: UseProjectOptions): UseProjectReturn {
  // Files state
  const [files, setFiles] = useState<ProjectFile[]>(() => {
    if (typeof window === 'undefined') return initialFiles;
    
    const saved = localStorage.getItem(`project-files-${projectSlug}`);
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        // Merge saved content with initial files
        return initialFiles.map(f => ({
          ...f,
          content: parsed[f.path] ?? f.content,
        }));
      } catch {
        return initialFiles;
      }
    }
    return initialFiles;
  });

  const [activeFile, setActiveFile] = useState<ProjectFile | null>(null);

  // Tasks state
  const [tasks, setTasks] = useState<ProjectTask[]>(initialTasks);
  const [completedTasks, setCompletedTasks] = useState<Set<string>>(() => {
    if (typeof window === 'undefined') return new Set();
    
    const saved = localStorage.getItem(`project-tasks-${projectSlug}`);
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        return new Set(parsed.completed || []);
      } catch {
        return new Set();
      }
    }
    return new Set();
  });

  // Status
  const [status, setStatus] = useState<ProjectStatus>(() => {
    if (typeof window === 'undefined') return 'not_started';
    
    const saved = localStorage.getItem(`project-status-${projectSlug}`);
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        return parsed.status || 'not_started';
      } catch {
        return 'not_started';
      }
    }
    return completedTasks.size > 0 ? 'in_progress' : 'not_started';
  });

  // Loading states
  const [isSaving, setIsSaving] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Set initial active file
  useEffect(() => {
    if (!activeFile && files.length > 0) {
      const entryFile = files.find(f => f.path === entryPoint);
      setActiveFile(entryFile || files[0]);
    }
  }, [files, entryPoint, activeFile]);

  // Calculate progress
  const taskProgress = tasks.length > 0 
    ? (completedTasks.size / tasks.length) * 100 
    : 0;

  // Update file content
  const updateFileContent = useCallback((path: string, content: string) => {
    setFiles(prev => prev.map(f => 
      f.path === path ? { ...f, content } : f
    ));
  }, []);

  // Add new file
  const addFile = useCallback((path: string, content: string = '') => {
    const name = path.split('/').pop() || path;
    const newFile: ProjectFile = { id: path, name, path, content };
    setFiles(prev => [...prev, newFile]);
    setActiveFile(newFile);
  }, []);

  // Delete file
  const deleteFile = useCallback((path: string) => {
    setFiles(prev => prev.filter(f => f.path !== path));
    if (activeFile?.path === path) {
      setActiveFile(null);
    }
  }, [activeFile]);

  // Toggle task completion
  const toggleTask = useCallback((taskId: string) => {
    setCompletedTasks(prev => {
      const newSet = new Set(prev);
      if (newSet.has(taskId)) {
        newSet.delete(taskId);
      } else {
        newSet.add(taskId);
      }
      return newSet;
    });
  }, []);

  // Save project
  const save = useCallback(async () => {
    setIsSaving(true);
    
    try {
      // Save to localStorage
      const fileData: Record<string, string> = {};
      files.forEach(f => {
        fileData[f.path] = f.content || '';
      });
      
      localStorage.setItem(`project-files-${projectSlug}`, JSON.stringify(fileData));
      localStorage.setItem(`project-tasks-${projectSlug}`, JSON.stringify({
        completed: Array.from(completedTasks),
        progress: taskProgress,
      }));
      localStorage.setItem(`project-status-${projectSlug}`, JSON.stringify({
        status: status === 'not_started' && completedTasks.size > 0 ? 'in_progress' : status,
      }));

      // In production, also save to server
      await fetch(`/api/projects/${projectSlug}/save`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ files, completedTasks }),
      });
    } finally {
      setIsSaving(false);
    }
  }, [files, completedTasks, taskProgress, status, projectSlug]);

  // Submit project
  const submit = useCallback(async () => {
    setIsSubmitting(true);
    
    try {
      const fileData: Record<string, string> = {};
      files.forEach(f => {
        fileData[f.path] = f.content || '';
      });

      const response = await fetch(`/api/projects/${projectSlug}/submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          files: fileData,
          completedTasks: Array.from(completedTasks),
        }),
      });

      if (response.ok) {
        setStatus('submitted');
      }
    } finally {
      setIsSubmitting(false);
    }
  }, [files, completedTasks, projectSlug]);

  // Reset project to initial state
  const reset = useCallback(() => {
    if (confirm('Reset all files to starter code? Your changes will be lost.')) {
      setFiles(initialFiles);
      setCompletedTasks(new Set());
      setStatus('not_started');
      
      localStorage.removeItem(`project-files-${projectSlug}`);
      localStorage.removeItem(`project-tasks-${projectSlug}`);
      localStorage.removeItem(`project-status-${projectSlug}`);
      
      const entryFile = initialFiles.find(f => f.path === entryPoint);
      setActiveFile(entryFile || initialFiles[0]);
    }
  }, [initialFiles, entryPoint, projectSlug]);

  // Auto-save when files or tasks change
  useEffect(() => {
    const timeout = setTimeout(() => {
      const fileData: Record<string, string> = {};
      files.forEach(f => {
        fileData[f.path] = f.content || '';
      });
      localStorage.setItem(`project-files-${projectSlug}`, JSON.stringify(fileData));
    }, 1000);

    return () => clearTimeout(timeout);
  }, [files, projectSlug]);

  useEffect(() => {
    localStorage.setItem(`project-tasks-${projectSlug}`, JSON.stringify({
      completed: Array.from(completedTasks),
      progress: taskProgress,
    }));
  }, [completedTasks, taskProgress, projectSlug]);

  return {
    files,
    activeFile,
    setActiveFile,
    updateFileContent,
    addFile,
    deleteFile,
    tasks,
    completedTasks,
    toggleTask,
    taskProgress,
    status,
    setStatus,
    save,
    submit,
    reset,
    isSaving,
    isSubmitting,
  };
}
