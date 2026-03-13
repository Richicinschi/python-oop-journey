'use client';

import { useEffect, useState, useCallback } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  ChevronLeft, 
  FolderGit2, 
  Play, 
  Save, 
  CheckCircle2,
  Clock,
  AlertCircle,
  MoreVertical,
  Terminal,
  FileCode2,
  Bug,
  Keyboard,
  X,
  ChevronRight,
  LayoutTemplate
} from 'lucide-react';
import { getWeekBySlug, getWeeks, formatWeekNumber } from '@/lib/curriculum-loader';
import { 
  FileTree, 
  ProjectTour,
  KeyboardShortcutsDialog,
  ShortcutBadge,
  ProjectErrorBoundary,
  ExecutionLoadingState,
  ProjectPageSkeleton,
  BreadcrumbSkeleton
} from '@/components/projects';
import { WeeklyProject, UserProjectProgress, ProjectFile } from '@/types/project';
import { useProjectStore, useProjectKeyboardShortcuts } from '@/hooks/use-project-store';
import { cn } from '@/lib/utils';
import dynamic from 'next/dynamic';

// Dynamic import for Monaco Editor to avoid SSR issues
const CodeEditor = dynamic(
  () => import('@/components/editor/code-editor').then(mod => mod.CodeEditor),
  { 
    ssr: false,
    loading: () => (
      <div className="h-full flex items-center justify-center">
        <div className="h-8 w-8 rounded-full border-4 border-primary/20 border-t-primary animate-spin" />
      </div>
    )
  }
);

// Mock project data - in real app, fetch from API
const getMockProject = (weekSlug: string): WeeklyProject | null => {
  const week = getWeekBySlug(weekSlug);
  if (!week?.project) return null;

  return {
    slug: `${weekSlug}-project`,
    title: week.project.title,
    description: week.project.description,
    difficulty: 'intermediate',
    estimatedHours: 3,
    week: week.order,
    status: 'not_started',
    completedTasks: 0,
    totalTasks: 4,
  };
};

export default function ProjectPage() {
  const params = useParams();
  const router = useRouter();
  const weekSlug = params.weekSlug as string;
  
  const [project, setProject] = useState<WeeklyProject | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showTour, setShowTour] = useState(false);
  const [output, setOutput] = useState<string>('');
  const [isRunning, setIsRunning] = useState(false);
  const [activeTab, setActiveTab] = useState('output');

  const {
    currentProject,
    activeTabs,
    activeFileId,
    startProject,
    updateFileContent,
    saveFile,
    createFile,
    deleteFile,
    openTab,
    closeTab,
    submitProject,
    getActiveFile,
    trackEvent,
  } = useProjectStore();

  // Load project data
  useEffect(() => {
    const mockProject = getMockProject(weekSlug);
    if (mockProject) {
      setProject(mockProject);
      // Check if project is already started
      const existingProgress = localStorage.getItem(`oop-journey-projects-v1`);
      if (existingProgress) {
        try {
          const parsed = JSON.parse(existingProgress);
          if (parsed.projects?.[mockProject.slug]) {
            // Project exists, don't auto-start
          } else {
            // Auto-start for demo
            startProject(mockProject);
            setShowTour(true);
          }
        } catch {
          startProject(mockProject);
          setShowTour(true);
        }
      } else {
        startProject(mockProject);
        setShowTour(true);
      }
    }
    setIsLoading(false);
  }, [weekSlug, startProject]);

  // Keyboard shortcuts
  useProjectKeyboardShortcuts({
    onSave: () => {
      if (activeFileId) {
        saveFile(activeFileId);
      }
    },
    onSaveAll: () => {
      activeTabs.forEach(tab => {
        if (tab.isModified) {
          saveFile(tab.fileId);
        }
      });
    },
    onRun: () => handleRun(),
    onTest: () => handleTest(),
    onToggleFileTree: () => {
      // Toggle file tree visibility - would connect to layout state
      console.log('Toggle file tree');
    },
    onSplitEditor: () => {
      // Toggle split editor - would connect to layout state
      console.log('Split editor');
    },
  });

  const handleRun = useCallback(async () => {
    setIsRunning(true);
    setActiveTab('output');
    setOutput('Running...\n');
    
    trackEvent('run_executed');

    // Simulate execution
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    const activeFile = getActiveFile();
    if (activeFile) {
      setOutput(`> python ${activeFile.name}\n\nHello, World!\n\nProcess completed successfully.\n`);
    } else {
      setOutput('> python main.py\n\nHello, World!\n\nProcess completed successfully.\n');
    }
    
    setIsRunning(false);
  }, [getActiveFile, trackEvent]);

  const handleTest = useCallback(async () => {
    setIsRunning(true);
    setActiveTab('tests');
    setOutput('Running tests...\n');
    
    trackEvent('tests_run');

    // Simulate test execution
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    setOutput(`Running pytest...\n\n============================= test session starts =============================\nplatform linux -- Python 3.11.0\ncollected 3 items\n\ntest_main.py ...                                                        [100%]\n\n============================== 3 passed in 0.05s ==============================\n`);
    
    setIsRunning(false);
  }, [trackEvent]);

  const handleSubmit = useCallback(() => {
    submitProject();
    // Show success message or redirect
  }, [submitProject]);

  const activeFile = getActiveFile();
  const week = getWeekBySlug(weekSlug);

  if (isLoading) {
    return <ProjectPageSkeleton />;
  }

  if (!project || !week) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px]">
        <AlertCircle className="h-12 w-12 text-muted-foreground mb-4" />
        <h2 className="text-xl font-semibold mb-2">Project Not Found</h2>
        <p className="text-muted-foreground mb-4">
          This week doesn&apos;t have a project yet.
        </p>
        <Button asChild>
          <Link href={`/weeks/${weekSlug}`}>
            <ChevronLeft className="mr-2 h-4 w-4" />
            Back to Week
          </Link>
        </Button>
      </div>
    );
  }

  return (
    <ProjectErrorBoundary>
      <div className="space-y-4 h-full flex flex-col">
        {/* Tour */}
        {showTour && (
          <ProjectTour 
            onComplete={() => setShowTour(false)}
            onSkip={() => setShowTour(false)}
          />
        )}

        {/* Breadcrumb & Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <nav className="flex items-center gap-2 text-sm text-muted-foreground mb-1" aria-label="Breadcrumb">
              <Link href="/weeks" className="hover:text-foreground transition-colors">
                Curriculum
              </Link>
              <ChevronRight className="h-4 w-4" />
              <Link href={`/weeks/${weekSlug}`} className="hover:text-foreground transition-colors">
                {formatWeekNumber(week.order)}
              </Link>
              <ChevronRight className="h-4 w-4" />
              <span className="text-foreground">Project</span>
            </nav>
            <h1 className="text-2xl font-bold flex items-center gap-2">
              <FolderGit2 className="h-6 w-6 text-primary" />
              {project.title}
            </h1>
          </div>
          
          <div className="flex items-center gap-2">
            <KeyboardShortcutsDialog>
              <Button variant="ghost" size="icon" title="Keyboard Shortcuts">
                <Keyboard className="h-4 w-4" />
              </Button>
            </KeyboardShortcutsDialog>
            
            <Button 
              variant="outline" 
              onClick={handleRun}
              disabled={isRunning}
              data-tour="run-button"
            >
              <Play className="h-4 w-4 mr-2" />
              Run
              <ShortcutBadge keys={['Ctrl', 'R']} />
            </Button>
            
            <Button 
              onClick={handleSubmit}
              data-tour="submit-button"
            >
              <CheckCircle2 className="h-4 w-4 mr-2" />
              Submit
            </Button>
          </div>
        </div>

        {/* Main Editor Area */}
        <div className="flex-1 grid lg:grid-cols-[280px_1fr] gap-4 min-h-[600px]">
          {/* File Tree */}
          <Card className="lg:h-full">
            <FileTree
              files={currentProject?.slug === project.slug 
                ? (currentProject.files || project.starterFiles)
                : project.starterFiles
              }
              activeFileId={activeFileId}
              onFileSelect={openTab}
              onFileCreate={createFile}
              onFileDelete={deleteFile}
              onFileSave={saveFile}
              className="h-full"
            />
          </Card>

          {/* Editor & Output */}
          <div className="space-y-4 flex flex-col">
            {/* Editor Tabs */}
            <Card className="flex-1 flex flex-col">
              <div 
                className="flex items-center border-b bg-muted/30"
                data-tour="editor-tabs"
              >
                {activeTabs.map(tab => (
                  <button
                    key={tab.id}
                    onClick={() => openTab(tab.fileId)}
                    className={cn(
                      'flex items-center gap-2 px-3 py-2 text-sm border-r transition-colors',
                      tab.isActive 
                        ? 'bg-background text-foreground' 
                        : 'text-muted-foreground hover:bg-muted'
                    )}
                  >
                    <FileCode2 className="h-3.5 w-3.5" />
                    <span className={cn(tab.isModified && 'italic')}>
                      {tab.fileName}
                      {tab.isModified && ' •'}
                    </span>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        closeTab(tab.id);
                      }}
                      className="ml-1 hover:bg-muted rounded p-0.5"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  </button>
                ))}
              </div>
              
              <div className="flex-1 min-h-[300px]" data-tour="editor">
                {activeFile ? (
                  <CodeEditor
                    value={activeFile.content}
                    onChange={(value) => updateFileContent(activeFile.id, value || '')}
                    language={activeFile.language === 'python' ? 'python' : 'markdown'}
                    height="100%"
                  />
                ) : (
                  <div className="h-full flex items-center justify-center text-muted-foreground">
                    <div className="text-center">
                      <FileCode2 className="h-12 w-12 mx-auto mb-3 opacity-50" />
                      <p>Select a file to start editing</p>
                    </div>
                  </div>
                )}
              </div>
            </Card>

            {/* Output Panel */}
            <Card className="h-48">
              <Tabs value={activeTab} onValueChange={setActiveTab}>
                <TabsList className="w-full justify-start rounded-none border-b bg-muted/30 px-2">
                  <TabsTrigger value="output" className="gap-2">
                    <Terminal className="h-4 w-4" />
                    Output
                  </TabsTrigger>
                  <TabsTrigger value="tests" className="gap-2">
                    <Bug className="h-4 w-4" />
                    Tests
                  </TabsTrigger>
                  <TabsTrigger value="problems" className="gap-2">
                    <AlertCircle className="h-4 w-4" />
                    Problems
                  </TabsTrigger>
                </TabsList>
                
                <TabsContent value="output" className="m-0">
                  <div className="p-4 font-mono text-sm bg-black text-green-400 h-40 overflow-auto">
                    {isRunning ? (
                      <ExecutionLoadingState type="run" />
                    ) : (
                      <pre className="whitespace-pre-wrap">{output || 'Click Run to execute your code'}</pre>
                    )}
                  </div>
                </TabsContent>
                
                <TabsContent value="tests" className="m-0">
                  <div className="p-4 font-mono text-sm bg-black text-green-400 h-40 overflow-auto">
                    {isRunning ? (
                      <ExecutionLoadingState type="test" />
                    ) : (
                      <pre className="whitespace-pre-wrap">
                        {output || 'Click Run Tests to check your solution'}
                      </pre>
                    )}
                  </div>
                </TabsContent>
                
                <TabsContent value="problems" className="m-0">
                  <div className="p-4 h-40 overflow-auto">
                    <p className="text-muted-foreground text-sm">No problems detected</p>
                  </div>
                </TabsContent>
              </Tabs>
            </Card>
          </div>
        </div>
      </div>
    </ProjectErrorBoundary>
  );
}
