'use client';

import { useEffect, useState, useCallback } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { 
  ChevronLeft, 
  ChevronRight, 
  FolderGit2, 
  CheckCircle2, 
  Clock,
  Play,
  Save,
  Plus,
  Folder,
  FileCode,
  MoreVertical,
  Trash2,
  Download,
  Share2,
  Settings,
  Terminal,
  Layout,
  X
} from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Separator } from '@/components/ui/separator';
import { Progress } from '@/components/ui/progress';
import { Checkbox } from '@/components/ui/checkbox';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuSeparator, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import { cn } from '@/lib/utils';
import { CodeEditor } from '@/components/editor/code-editor';
import { getCurriculum, getWeekBySlug } from '@/lib/curriculum-loader';
import { useLocalStorage } from '@/hooks/use-local-storage';
import { useProgress } from '@/hooks/use-progress';
import { Project, Week, ProjectFile, ProjectTask, ProjectStatus } from '@/types/project';

interface FileNode {
  id: string;
  name: string;
  path: string;
  type: 'file' | 'directory';
  content?: string;
  isEntryPoint?: boolean;
  readOnly?: boolean;
  children?: FileNode[];
}

interface ProjectData extends Project {
  weekSlug: string;
  weekTitle: string;
  weekOrder: number;
  files: ProjectFile[];
  tasks: ProjectTask[];
  entryPoint: string;
  overview: string;
  requirements: string[];
  hints: string[];
  submissionGuidelines: string;
}

export default function ProjectPage() {
  const params = useParams<{ projectSlug: string }>();
  const { projectSlug } = params;

  // Project data state
  const [project, setProject] = useState<ProjectData | null>(null);
  const [week, setWeek] = useState<Week | null>(null);
  const [loading, setLoading] = useState(true);

  // File tree state
  const [files, setFiles] = useState<FileNode[]>([]);
  const [activeFile, setActiveFile] = useState<FileNode | null>(null);
  const [expandedDirs, setExpandedDirs] = useState<Set<string>>(new Set(['src', 'tests']));

  // Editor state
  const [code, setCode] = useState('');
  const [originalCode, setOriginalCode] = useState('');
  const [fontSize, setFontSize] = useLocalStorage('project-editor-font-size', 14);
  const [wordWrap, setWordWrap] = useLocalStorage('project-editor-word-wrap', true);

  // Execution state
  const [isRunning, setIsRunning] = useState(false);
  const [isTesting, setIsTesting] = useState(false);
  const [terminalOutput, setTerminalOutput] = useState<string>('');
  const [testResults, setTestResults] = useState<{
    passed: number;
    failed: number;
    total: number;
    details: { name: string; passed: boolean; error?: string }[];
  } | null>(null);

  // Task checklist state
  const [completedTasks, setCompletedTasks] = useState<Set<string>>(new Set());
  const [taskProgress, setTaskProgress] = useState(0);

  // Project status
  const [projectStatus, setProjectStatus] = useState<ProjectStatus>('not_started');

  // UI state
  const [showSubmitDialog, setShowSubmitDialog] = useState(false);
  const [activeMobilePanel, setActiveMobilePanel] = useState<'files' | 'editor' | 'instructions'>('editor');
  const [outputHeight, setOutputHeight] = useState(200);
  const [isResizing, setIsResizing] = useState(false);

  // Load project data
  useEffect(() => {
    const curriculum = getCurriculum();
    
    let foundProject: ProjectData | null = null;
    let foundWeek: Week | null = null;

    for (const w of curriculum.weeks) {
      if (w.project && w.project.slug === projectSlug) {
        foundWeek = w;
        foundProject = {
          ...w.project,
          weekSlug: w.slug,
          weekTitle: w.title,
          weekOrder: w.order,
          files: w.project.files || generateDefaultFiles(w.project),
          tasks: w.project.tasks || generateDefaultTasks(w.project),
          entryPoint: w.project.entryPoint || 'src/main.py',
          overview: w.project.overview || w.project.description,
          requirements: w.project.requirements || [],
          hints: w.project.hints || [],
          submissionGuidelines: w.project.submissionGuidelines || 'Submit your completed project for review.',
        };
        break;
      }
    }

    if (!foundProject || !foundWeek) {
      setLoading(false);
      return;
    }

    setProject(foundProject);
    setWeek(foundWeek);

    // Build file tree
    const fileTree = buildFileTree(foundProject.files);
    setFiles(fileTree);

    // Load saved files or set default
    const savedFiles = localStorage.getItem(`project-files-${projectSlug}`);
    if (savedFiles) {
      const parsed = JSON.parse(savedFiles);
      restoreFileTree(fileTree, parsed);
    }

    // Find and open entry point
    const entryFile = findFileByPath(fileTree, foundProject.entryPoint);
    if (entryFile) {
      setActiveFile(entryFile);
      setCode(entryFile.content || '');
      setOriginalCode(entryFile.content || '');
    }

    // Load saved task progress
    const savedTasks = localStorage.getItem(`project-tasks-${projectSlug}`);
    if (savedTasks) {
      const parsed = JSON.parse(savedTasks);
      setCompletedTasks(new Set(parsed.completed || []));
      setTaskProgress(parsed.progress || 0);
      setProjectStatus(parsed.status || 'not_started');
    }

    setLoading(false);
  }, [projectSlug]);

  // Save files to localStorage
  useEffect(() => {
    if (project && files.length > 0) {
      const fileData = extractFileData(files);
      localStorage.setItem(`project-files-${projectSlug}`, JSON.stringify(fileData));
    }
  }, [files, project, projectSlug]);

  // Save task progress
  useEffect(() => {
    if (project) {
      localStorage.setItem(`project-tasks-${projectSlug}`, JSON.stringify({
        completed: Array.from(completedTasks),
        progress: taskProgress,
        status: projectStatus,
      }));
    }
  }, [completedTasks, taskProgress, projectStatus, project, projectSlug]);

  // Calculate task progress
  useEffect(() => {
    if (project && project.tasks.length > 0) {
      const progress = (completedTasks.size / project.tasks.length) * 100;
      setTaskProgress(progress);
      
      if (completedTasks.size === 0) {
        setProjectStatus('not_started');
      } else if (completedTasks.size === project.tasks.length) {
        setProjectStatus(projectStatus === 'submitted' ? 'completed' : 'in_progress');
      } else {
        setProjectStatus('in_progress');
      }
    }
  }, [completedTasks, project, projectStatus]);

  const handleRun = async () => {
    if (!activeFile) return;
    
    setIsRunning(true);
    setTerminalOutput('Running project...\n');

    try {
      // Simulate execution
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setTerminalOutput(prev => prev + `> python ${project?.entryPoint}\n\n`);
      
      // Simulate output based on code content
      if (code.includes('print')) {
        const printMatch = code.match(/print\s*\(\s*["'](.+?)["']\s*\)/);
        if (printMatch) {
          setTerminalOutput(prev => prev + `${printMatch[1]}\n`);
        } else {
          setTerminalOutput(prev => prev + 'Hello, World!\n');
        }
      }
      
      if (code.includes('NotImplementedError')) {
        setTerminalOutput(prev => prev + '\nError: NotImplementedError - Complete the implementation\n');
      }

      setTerminalOutput(prev => prev + '\nProcess completed successfully.\n');
    } catch (error) {
      setTerminalOutput(prev => prev + `\nError: ${error}\n`);
    } finally {
      setIsRunning(false);
    }
  };

  const handleTest = async () => {
    setIsTesting(true);
    setTerminalOutput('Running tests...\n\n');
    setTestResults(null);

    try {
      // Simulate test execution
      await new Promise(resolve => setTimeout(resolve, 1500));

      const mockResults = {
        passed: 3,
        failed: 1,
        total: 4,
        details: [
          { name: 'test_deposit', passed: true },
          { name: 'test_withdraw', passed: true },
          { name: 'test_balance', passed: true },
          { name: 'test_overdraft', passed: false, error: 'Expected InsufficientFundsError, got None' },
        ],
      };

      setTestResults(mockResults);
      setTerminalOutput(prev => 
        prev + `Ran ${mockResults.total} tests\n` +
        `${mockResults.passed} passed, ${mockResults.failed} failed\n`
      );

      // Auto-check tasks based on test results
      if (mockResults.passed === mockResults.total) {
        project?.tasks.forEach(task => {
          if (!completedTasks.has(task.id)) {
            toggleTask(task.id);
          }
        });
      }
    } catch (error) {
      setTerminalOutput(prev => prev + `\nTest execution failed: ${error}\n`);
    } finally {
      setIsTesting(false);
    }
  };

  const handleSave = () => {
    if (activeFile) {
      updateFileContent(activeFile.path, code);
      localStorage.setItem(`project-files-${projectSlug}`, JSON.stringify(extractFileData(files)));
    }
  };

  const handleReset = () => {
    if (confirm('Reset all files to starter code? Your changes will be lost.')) {
      if (project) {
        const fileTree = buildFileTree(project.files);
        setFiles(fileTree);
        const entryFile = findFileByPath(fileTree, project.entryPoint);
        if (entryFile) {
          setActiveFile(entryFile);
          setCode(entryFile.content || '');
          setOriginalCode(entryFile.content || '');
        }
      }
    }
  };

  const toggleTask = (taskId: string) => {
    setCompletedTasks(prev => {
      const newSet = new Set(prev);
      if (newSet.has(taskId)) {
        newSet.delete(taskId);
      } else {
        newSet.add(taskId);
      }
      return newSet;
    });
  };

  const handleSubmit = () => {
    setProjectStatus('submitted');
    setShowSubmitDialog(false);
    setTerminalOutput(prev => prev + '\n[SYSTEM] Project submitted for review!\n');
  };

  const handleCreateFile = () => {
    const fileName = prompt('Enter file name (e.g., src/utils.py):');
    if (fileName) {
      const newFile: FileNode = {
        id: `file-${Date.now()}`,
        name: fileName.split('/').pop() || fileName,
        path: fileName,
        type: 'file',
        content: '# New file\n',
      };
      setFiles(prev => addFileToTree(prev, newFile));
      setActiveFile(newFile);
      setCode(newFile.content);
      setOriginalCode(newFile.content);
    }
  };

  const handleDeleteFile = (file: FileNode) => {
    if (confirm(`Delete ${file.path}?`)) {
      setFiles(prev => removeFileFromTree(prev, file.path));
      if (activeFile?.path === file.path) {
        setActiveFile(null);
        setCode('');
      }
    }
  };

  const toggleDir = (dirPath: string) => {
    setExpandedDirs(prev => {
      const newSet = new Set(prev);
      if (newSet.has(dirPath)) {
        newSet.delete(dirPath);
      } else {
        newSet.add(dirPath);
      }
      return newSet;
    });
  };

  const onFileSelect = (file: FileNode) => {
    if (file.type === 'file') {
      // Save current file before switching
      if (activeFile && activeFile.path !== file.path) {
        updateFileContent(activeFile.path, code);
      }
      setActiveFile(file);
      setCode(file.content || '');
      setOriginalCode(file.content || '');
      setActiveMobilePanel('editor');
    }
  };

  const updateFileContent = (path: string, newContent: string) => {
    setFiles(prev => updateFileInTree(prev, path, newContent));
  };

  // Resize handlers
  const handleResizeStart = () => setIsResizing(true);
  const handleResizeEnd = () => setIsResizing(false);
  const handleResizeMove = useCallback((e: React.MouseEvent) => {
    if (isResizing) {
      const newHeight = Math.max(100, Math.min(400, window.innerHeight - e.clientY));
      setOutputHeight(newHeight);
    }
  }, [isResizing]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
      </div>
    );
  }

  if (!project || !week) {
    notFound();
  }

  const hasUnsavedChanges = code !== originalCode;
  const allTasksComplete = completedTasks.size === project.tasks.length;

  return (
    <div 
      className="h-screen flex flex-col bg-background"
      onMouseMove={handleResizeMove}
      onMouseUp={handleResizeEnd}
    >
      {/* Header */}
      <header className="border-b bg-card px-4 py-2 shrink-0">
        <div className="flex items-center justify-between">
          {/* Breadcrumb */}
          <div className="flex items-center gap-2 text-sm">
            <Link href="/weeks" className="text-muted-foreground hover:text-foreground">
              Weeks
            </Link>
            <ChevronRight className="h-4 w-4 text-muted-foreground" />
            <Link 
              href={`/weeks/${week.slug}`}
              className="text-muted-foreground hover:text-foreground"
            >
              {week.title}
            </Link>
            <ChevronRight className="h-4 w-4 text-muted-foreground" />
            <span className="font-medium truncate max-w-[200px]">{project.title}</span>
          </div>

          {/* Actions */}
          <div className="flex items-center gap-2">
            <Badge variant={getStatusVariant(projectStatus)}>
              {getStatusLabel(projectStatus)}
            </Badge>
            <div className="hidden md:flex items-center gap-2">
              <Button variant="outline" size="sm" onClick={handleReset}>
                Reset
              </Button>
              <Button 
                size="sm" 
                onClick={() => setShowSubmitDialog(true)}
                disabled={!allTasksComplete}
              >
                <CheckCircle2 className="h-4 w-4 mr-2" />
                Submit
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content - Three Pane Layout */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Pane - File Tree */}
        <div className="hidden lg:flex w-[240px] flex-col border-r bg-card">
          <div className="p-3 border-b flex items-center justify-between">
            <span className="font-semibold text-sm flex items-center gap-2">
              <FolderGit2 className="h-4 w-4" />
              Files
            </span>
            <Button variant="ghost" size="sm" className="h-7 w-7 p-0" onClick={handleCreateFile}>
              <Plus className="h-4 w-4" />
            </Button>
          </div>
          <ScrollArea className="flex-1">
            <FileTree 
              files={files} 
              activePath={activeFile?.path}
              expandedDirs={expandedDirs}
              onToggleDir={toggleDir}
              onSelect={onFileSelect}
              onDelete={handleDeleteFile}
            />
          </ScrollArea>
        </div>

        {/* Center Pane - Editor */}
        <div className="flex-1 flex flex-col min-w-0">
          {/* Toolbar */}
          <div className="border-b px-4 py-2 flex items-center justify-between bg-card shrink-0">
            <div className="flex items-center gap-2">
              {activeFile ? (
                <div className="flex items-center gap-2">
                  <FileCode className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm font-medium">{activeFile.path}</span>
                  {activeFile.isEntryPoint && (
                    <Badge variant="secondary" className="text-xs">Entry</Badge>
                  )}
                  {hasUnsavedChanges && (
                    <span className="text-xs text-muted-foreground">• unsaved</span>
                  )}
                </div>
              ) : (
                <span className="text-sm text-muted-foreground">Select a file to edit</span>
              )}
            </div>
            <div className="flex items-center gap-2">
              <Button 
                variant="outline" 
                size="sm" 
                onClick={handleSave}
                disabled={!hasUnsavedChanges}
              >
                <Save className="h-4 w-4 mr-2" />
                Save
              </Button>
              <Button 
                size="sm" 
                onClick={handleRun}
                disabled={!activeFile || isRunning}
              >
                <Play className="h-4 w-4 mr-2" />
                Run
              </Button>
              <Button 
                variant="secondary" 
                size="sm" 
                onClick={handleTest}
                disabled={isTesting}
              >
                <CheckCircle2 className="h-4 w-4 mr-2" />
                Test
              </Button>
            </div>
          </div>

          {/* Editor */}
          <div className="flex-1 overflow-hidden">
            {activeFile ? (
              <CodeEditor
                value={code}
                onChange={setCode}
                height="100%"
                fontSize={fontSize}
                wordWrap={wordWrap ? 'on' : 'off'}
                minimap={true}
                readOnly={activeFile.readOnly}
                onRun={handleRun}
              />
            ) : (
              <div className="h-full flex items-center justify-center text-muted-foreground">
                <div className="text-center">
                  <FileCode className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p>Select a file from the file tree to start editing</p>
                </div>
              </div>
            )}
          </div>

          {/* Bottom Panel - Terminal/Output */}
          <div 
            className="border-t bg-card flex flex-col shrink-0"
            style={{ height: outputHeight }}
          >
            <div 
              className="h-1 cursor-ns-resize hover:bg-primary/50"
              onMouseDown={handleResizeStart}
            />
            <Tabs defaultValue="terminal" className="flex flex-col h-full">
              <div className="flex items-center justify-between px-4 py-2 border-b">
                <TabsList className="h-8">
                  <TabsTrigger value="terminal" className="text-xs">
                    <Terminal className="h-3 w-3 mr-2" />
                    Terminal
                  </TabsTrigger>
                  <TabsTrigger value="tests" className="text-xs">
                    <CheckCircle2 className="h-3 w-3 mr-2" />
                    Tests
                    {testResults && (
                      <Badge 
                        variant={testResults.failed === 0 ? "default" : "destructive"}
                        className="ml-2 text-[10px] h-4"
                      >
                        {testResults.passed}/{testResults.total}
                      </Badge>
                    )}
                  </TabsTrigger>
                </TabsList>
                <div className="flex items-center gap-2">
                  <Button 
                    variant="ghost" 
                    size="sm" 
                    className="h-7"
                    onClick={() => setTerminalOutput('')}
                  >
                    Clear
                  </Button>
                </div>
              </div>
              <div className="flex-1 overflow-hidden">
                <TabsContent value="terminal" className="h-full m-0">
                  <ScrollArea className="h-full">
                    <pre className="p-4 font-mono text-sm whitespace-pre-wrap">
                      {terminalOutput || '> Ready\n'}
                    </pre>
                  </ScrollArea>
                </TabsContent>
                <TabsContent value="tests" className="h-full m-0">
                  <ScrollArea className="h-full">
                    <div className="p-4 space-y-2">
                      {testResults ? (
                        <>
                          <div className={cn(
                            "flex items-center gap-2 p-3 rounded-lg",
                            testResults.failed === 0 
                              ? "bg-green-500/10 text-green-600" 
                              : "bg-red-500/10 text-red-600"
                          )}>
                            <CheckCircle2 className="h-5 w-5" />
                            <span className="font-medium">
                              {testResults.passed} of {testResults.total} tests passed
                            </span>
                          </div>
                          <div className="space-y-1">
                            {testResults.details.map((test, idx) => (
                              <div 
                                key={idx}
                                className={cn(
                                  "flex items-start gap-2 p-2 rounded text-sm",
                                  test.passed ? "bg-green-500/5" : "bg-red-500/5"
                                )}
                              >
                                {test.passed ? (
                                  <CheckCircle2 className="h-4 w-4 text-green-500 shrink-0 mt-0.5" />
                                ) : (
                                  <X className="h-4 w-4 text-red-500 shrink-0 mt-0.5" />
                                )}
                                <div className="flex-1">
                                  <span className="font-medium">{test.name}</span>
                                  {test.error && (
                                    <p className="text-xs text-red-500 mt-1">{test.error}</p>
                                  )}
                                </div>
                              </div>
                            ))}
                          </div>
                        </>
                      ) : (
                        <span className="text-muted-foreground">Run tests to see results</span>
                      )}
                    </div>
                  </ScrollArea>
                </TabsContent>
              </div>
            </Tabs>
          </div>
        </div>

        {/* Right Pane - Instructions */}
        <div className="hidden lg:flex w-[380px] flex-col border-l bg-card">
          <ScrollArea className="flex-1">
            <div className="p-6 space-y-6">
              {/* Title */}
              <div className="space-y-2">
                <Badge variant="outline">Week {project.weekOrder}</Badge>
                <h1 className="text-xl font-bold">{project.title}</h1>
                <p className="text-sm text-muted-foreground">{project.overview}</p>
              </div>

              {/* Progress */}
              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span>Task Progress</span>
                  <span className="font-medium">{Math.round(taskProgress)}%</span>
                </div>
                <Progress value={taskProgress} className="h-2" />
              </div>

              <Separator />

              {/* Tasks */}
              <div className="space-y-3">
                <h3 className="font-semibold flex items-center gap-2">
                  <CheckCircle2 className="h-4 w-4" />
                  Tasks
                </h3>
                <div className="space-y-2">
                  {project.tasks.map((task) => (
                    <div 
                      key={task.id}
                      className="flex items-start gap-3 p-3 rounded-lg border bg-background hover:bg-accent/50 transition-colors cursor-pointer"
                      onClick={() => toggleTask(task.id)}
                    >
                      <Checkbox 
                        checked={completedTasks.has(task.id)}
                        onCheckedChange={() => toggleTask(task.id)}
                        className="mt-0.5"
                      />
                      <div className="flex-1">
                        <p className={cn(
                          "text-sm",
                          completedTasks.has(task.id) && "line-through text-muted-foreground"
                        )}>
                          {task.description}
                        </p>
                        {task.hint && (
                          <p className="text-xs text-muted-foreground mt-1">{task.hint}</p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <Separator />

              {/* Requirements */}
              {project.requirements.length > 0 && (
                <div className="space-y-3">
                  <h3 className="font-semibold">Requirements</h3>
                  <ul className="space-y-2">
                    {project.requirements.map((req, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-sm">
                        <span className="text-primary mt-1">•</span>
                        <span className="text-muted-foreground">{req}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Hints */}
              {project.hints.length > 0 && (
                <div className="space-y-3">
                  <h3 className="font-semibold flex items-center gap-2">
                    <Layout className="h-4 w-4" />
                    Hints
                  </h3>
                  <div className="space-y-2">
                    {project.hints.map((hint, idx) => (
                      <Alert key={idx} className="py-2">
                        <AlertDescription className="text-xs">{hint}</AlertDescription>
                      </Alert>
                    ))}
                  </div>
                </div>
              )}

              {/* Submission Guidelines */}
              <div className="space-y-3">
                <h3 className="font-semibold">Submission</h3>
                <p className="text-sm text-muted-foreground">{project.submissionGuidelines}</p>
              </div>

              {/* Navigation */}
              <div className="flex items-center justify-between pt-4">
                <Link href={`/weeks/${week.slug}`}>
                  <Button variant="outline" size="sm">
                    <ChevronLeft className="h-4 w-4 mr-2" />
                    Back to Week
                  </Button>
                </Link>
              </div>
            </div>
          </ScrollArea>
        </div>
      </div>

      {/* Mobile Navigation */}
      <div className="lg:hidden border-t bg-card p-2">
        <div className="flex items-center justify-around">
          <Sheet>
            <SheetTrigger asChild>
              <Button variant="ghost" size="sm">
                <Folder className="h-5 w-5" />
              </Button>
            </SheetTrigger>
            <SheetContent side="left" className="w-[280px] p-0">
              <div className="p-4 border-b flex items-center justify-between">
                <span className="font-semibold">Files</span>
                <Button variant="ghost" size="sm" className="h-8 w-8 p-0" onClick={handleCreateFile}>
                  <Plus className="h-4 w-4" />
                </Button>
              </div>
              <ScrollArea className="h-[calc(100vh-80px)]">
                <FileTree 
                  files={files} 
                  activePath={activeFile?.path}
                  expandedDirs={expandedDirs}
                  onToggleDir={toggleDir}
                  onSelect={onFileSelect}
                  onDelete={handleDeleteFile}
                />
              </ScrollArea>
            </SheetContent>
          </Sheet>

          <Button 
            variant={activeMobilePanel === 'editor' ? 'default' : 'ghost'} 
            size="sm"
            onClick={() => setActiveMobilePanel('editor')}
          >
            <Layout className="h-5 w-5" />
          </Button>

          <Sheet>
            <SheetTrigger asChild>
              <Button variant="ghost" size="sm">
                <CheckCircle2 className="h-5 w-5" />
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="w-[320px] p-0">
              <ScrollArea className="h-full">
                <div className="p-6 space-y-6">
                  <div>
                    <Badge variant="outline">Week {project.weekOrder}</Badge>
                    <h1 className="text-lg font-bold mt-2">{project.title}</h1>
                  </div>
                  
                  <Progress value={taskProgress} className="h-2" />
                  
                  <div className="space-y-3">
                    <h3 className="font-semibold">Tasks</h3>
                    <div className="space-y-2">
                      {project.tasks.map((task) => (
                        <div 
                          key={task.id}
                          className="flex items-start gap-3 p-3 rounded-lg border"
                          onClick={() => toggleTask(task.id)}
                        >
                          <Checkbox 
                            checked={completedTasks.has(task.id)}
                            onCheckedChange={() => toggleTask(task.id)}
                          />
                          <span className={cn(
                            "text-sm",
                            completedTasks.has(task.id) && "line-through text-muted-foreground"
                          )}>
                            {task.description}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </ScrollArea>
            </SheetContent>
          </Sheet>
        </div>
      </div>

      {/* Submit Dialog */}
      <Dialog open={showSubmitDialog} onOpenChange={setShowSubmitDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Submit Project</DialogTitle>
            <DialogDescription>
              You are about to submit your project for review. Make sure all tasks are completed.
            </DialogDescription>
          </DialogHeader>
          <div className="py-4">
            <div className="space-y-4">
              <div className="flex items-center justify-between text-sm">
                <span>Tasks Completed</span>
                <span className="font-medium">{completedTasks.size} / {project.tasks.length}</span>
              </div>
              <Progress value={taskProgress} className="h-2" />
              {!allTasksComplete && (
                <Alert variant="destructive">
                  <AlertDescription>
                    Please complete all tasks before submitting.
                  </AlertDescription>
                </Alert>
              )}
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowSubmitDialog(false)}>
              Cancel
            </Button>
            <Button onClick={handleSubmit} disabled={!allTasksComplete}>
              Submit Project
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}


// File Tree Component
interface FileTreeProps {
  files: FileNode[];
  activePath?: string;
  expandedDirs: Set<string>;
  onToggleDir: (path: string) => void;
  onSelect: (file: FileNode) => void;
  onDelete: (file: FileNode) => void;
  level?: number;
}

function FileTree({ files, activePath, expandedDirs, onToggleDir, onSelect, onDelete, level = 0 }: FileTreeProps) {
  return (
    <div className="space-y-0.5">
      {files.map((file) => (
        <div key={file.id}>
          {file.type === 'directory' ? (
            <div>
              <button
                onClick={() => onToggleDir(file.path)}
                className={cn(
                  "w-full flex items-center gap-2 px-3 py-1.5 text-sm hover:bg-accent/50 transition-colors"
                )}
                style={{ paddingLeft: `${12 + level * 12}px` }}
              >
                <ChevronRight 
                  className={cn(
                    "h-3.5 w-3.5 transition-transform",
                    expandedDirs.has(file.path) && "rotate-90"
                  )} 
                />
                <Folder className="h-4 w-4 text-yellow-500" />
                <span className="truncate">{file.name}</span>
              </button>
              {expandedDirs.has(file.path) && file.children && (
                <FileTree
                  files={file.children}
                  activePath={activePath}
                  expandedDirs={expandedDirs}
                  onToggleDir={onToggleDir}
                  onSelect={onSelect}
                  onDelete={onDelete}
                  level={level + 1}
                />
              )}
            </div>
          ) : (
            <div className="group relative">
              <button
                onClick={() => onSelect(file)}
                className={cn(
                  "w-full flex items-center gap-2 px-3 py-1.5 text-sm hover:bg-accent/50 transition-colors",
                  activePath === file.path && "bg-accent text-accent-foreground",
                  file.readOnly && "opacity-60"
                )}
                style={{ paddingLeft: `${24 + level * 12}px` }}
              >
                <FileCode className="h-4 w-4 text-blue-500" />
                <span className="truncate flex-1 text-left">{file.name}</span>
                {file.isEntryPoint && (
                  <Badge variant="outline" className="text-[10px] h-4 px-1">main</Badge>
                )}
              </button>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button 
                    variant="ghost" 
                    size="sm" 
                    className="absolute right-1 top-1/2 -translate-y-1/2 h-6 w-6 p-0 opacity-0 group-hover:opacity-100"
                  >
                    <MoreVertical className="h-3 w-3" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuItem onClick={() => onSelect(file)}>
                    Open
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem 
                    onClick={() => onDelete(file)}
                    className="text-red-600"
                    disabled={file.readOnly}
                  >
                    <Trash2 className="h-4 w-4 mr-2" />
                    Delete
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

// Helper Functions
function buildFileTree(projectFiles: ProjectFile[]): FileNode[] {
  const root: FileNode[] = [];
  const dirMap = new Map<string, FileNode>();

  projectFiles.forEach((file, index) => {
    const parts = file.path.split('/');
    let currentPath = '';
    let parent: FileNode[] = root;

    parts.forEach((part, i) => {
      currentPath = currentPath ? `${currentPath}/${part}` : part;
      
      if (i === parts.length - 1) {
        // File
        const node: FileNode = {
          id: `file-${index}`,
          name: part,
          path: file.path,
          type: 'file',
          content: file.content,
          isEntryPoint: file.isEntryPoint,
          readOnly: file.readOnly,
        };
        parent.push(node);
      } else {
        // Directory
        if (!dirMap.has(currentPath)) {
          const node: FileNode = {
            id: `dir-${currentPath}`,
            name: part,
            path: currentPath,
            type: 'directory',
            children: [],
          };
          dirMap.set(currentPath, node);
          parent.push(node);
        }
        parent = dirMap.get(currentPath)!.children!;
      }
    });
  });

  return root;
}

function findFileByPath(files: FileNode[], path: string): FileNode | null {
  for (const file of files) {
    if (file.path === path) return file;
    if (file.children) {
      const found = findFileByPath(file.children, path);
      if (found) return found;
    }
  }
  return null;
}

function updateFileInTree(files: FileNode[], path: string, content: string): FileNode[] {
  return files.map(file => {
    if (file.path === path) {
      return { ...file, content };
    }
    if (file.children) {
      return { ...file, children: updateFileInTree(file.children, path, content) };
    }
    return file;
  });
}

function addFileToTree(files: FileNode[], newFile: FileNode): FileNode[] {
  const parts = newFile.path.split('/');
  if (parts.length === 1) {
    return [...files, newFile];
  }

  return files.map(file => {
    if (file.type === 'directory' && parts[0] === file.name) {
      const remainingPath = parts.slice(1).join('/');
      const childFile = { ...newFile, path: remainingPath };
      return {
        ...file,
        children: file.children ? addFileToTree(file.children, childFile) : [childFile],
      };
    }
    return file;
  });
}

function removeFileFromTree(files: FileNode[], path: string): FileNode[] {
  return files.filter(file => file.path !== path).map(file => {
    if (file.children) {
      return { ...file, children: removeFileFromTree(file.children, path) };
    }
    return file;
  });
}

function extractFileData(files: FileNode[]): { path: string; content: string }[] {
  const result: { path: string; content: string }[] = [];
  
  function traverse(nodes: FileNode[]) {
    for (const node of nodes) {
      if (node.type === 'file') {
        result.push({ path: node.path, content: node.content || '' });
      }
      if (node.children) {
        traverse(node.children);
      }
    }
  }
  
  traverse(files);
  return result;
}

function restoreFileTree(files: FileNode[], savedData: { path: string; content: string }[]) {
  const contentMap = new Map(savedData.map(d => [d.path, d.content]));
  
  function traverse(nodes: FileNode[]) {
    for (const node of nodes) {
      if (node.type === 'file' && contentMap.has(node.path)) {
        node.content = contentMap.get(node.path);
      }
      if (node.children) {
        traverse(node.children);
      }
    }
  }
  
  traverse(files);
}

function generateDefaultFiles(project: Project): ProjectFile[] {
  return [
    {
      path: 'src/main.py',
      content: `# ${project.title}\n# Entry point for your project\n\ndef main():\n    pass\n\nif __name__ == "__main__":\n    main()\n`,
      isEntryPoint: true,
    },
    {
      path: 'src/__init__.py',
      content: '',
    },
    {
      path: 'tests/__init__.py',
      content: '',
    },
    {
      path: 'tests/test_main.py',
      content: `import pytest\nfrom src.main import main\n\ndef test_main():\n    pass\n`,
      readOnly: false,
    },
  ];
}

function generateDefaultTasks(project: Project): ProjectTask[] {
  return [
    { id: 'task-1', description: 'Set up project structure', completed: false },
    { id: 'task-2', description: 'Implement core functionality', completed: false },
    { id: 'task-3', description: 'Write tests', completed: false },
    { id: 'task-4', description: 'Run all tests successfully', completed: false },
  ];
}

function getStatusVariant(status: ProjectStatus): 'default' | 'secondary' | 'destructive' | 'outline' {
  switch (status) {
    case 'completed':
      return 'default';
    case 'in_progress':
      return 'secondary';
    case 'submitted':
      return 'outline';
    default:
      return 'outline';
  }
}

function getStatusLabel(status: ProjectStatus): string {
  switch (status) {
    case 'not_started':
      return 'Not Started';
    case 'in_progress':
      return 'In Progress';
    case 'submitted':
      return 'Submitted';
    case 'completed':
      return 'Completed';
    default:
      return 'Unknown';
  }
}
