"use client";

import { useState, useCallback, useEffect } from "react";
import { PanelLeftClose, PanelLeftOpen } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
// Note: Resizable panels can be added later if needed
import { useProjectFiles } from "@/hooks/use-project-files";
import type { ProjectItem, ProjectFile } from "@/types/project-files";
import { FileTree } from "./file-tree/file-tree";
import { FileTabs } from "./file-tabs/file-tabs";
import { SplitEditor } from "./split-editor";
import { ProjectToolbar } from "./project-toolbar";
import { NewFileDialog } from "./new-file-dialog";
import { RenameDialog } from "./rename-dialog";
import { DeleteConfirmDialog } from "./delete-confirm-dialog";
import { ImportProjectDialog } from "./import-project-dialog";

export interface MultiFileEditorProps {
  /** Project ID */
  projectId?: string;
  /** Project name */
  projectName?: string;
  /** Initial files to populate */
  initialFiles?: ProjectFile[];
  /** Callback when files are saved */
  onSave?: (files: ProjectFile[]) => void;
  /** Callback when project is run */
  onRun?: () => void;
  /** Callback when file changes */
  onFileChange?: (fileId: string, content: string) => void;
  /** Additional className */
  className?: string;
}

export function MultiFileEditor({
  projectId = "default",
  projectName = "My Project",
  initialFiles,
  onSave,
  onRun,
  onFileChange,
  className,
}: MultiFileEditorProps) {
  // Project files hook
  const project = useProjectFiles({
    projectId,
    projectName,
    initialFiles,
  });

  // UI State
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [dialogState, setDialogState] = useState<{
    type: "new-file" | "rename" | "delete" | "import" | null;
    item: ProjectItem | null;
    defaultType?: "file" | "folder";
  }>({ type: null, item: null });

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Ctrl+S to save all
      if (e.ctrlKey && e.key === "s") {
        e.preventDefault();
        project.saveAllFiles();
      }
      // Ctrl+Enter to run
      if (e.ctrlKey && e.key === "Enter" && onRun) {
        e.preventDefault();
        onRun();
      }
      // Ctrl+B to toggle sidebar
      if (e.ctrlKey && e.key === "b") {
        e.preventDefault();
        setIsSidebarOpen(prev => !prev);
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [project, onRun]);

  // Handlers
  const handleNewFile = useCallback((parentFolderId?: string) => {
    setDialogState({ type: "new-file", item: null, defaultType: "file" });
  }, []);

  const handleNewFolder = useCallback((parentFolderId?: string) => {
    setDialogState({ type: "new-file", item: null, defaultType: "folder" });
  }, []);

  const handleCreateFile = useCallback((name: string) => {
    project.createFile(name, "root");
    setDialogState({ type: null, item: null });
  }, [project]);

  const handleCreateFolder = useCallback((name: string) => {
    project.createFolder(name, "root");
    setDialogState({ type: null, item: null });
  }, [project]);

  const handleRename = useCallback((item: ProjectItem) => {
    setDialogState({ type: "rename", item });
  }, []);

  const handleConfirmRename = useCallback((newName: string) => {
    if (dialogState.item) {
      project.renameItem(dialogState.item.id, newName);
    }
    setDialogState({ type: null, item: null });
  }, [dialogState.item, project]);

  const handleDelete = useCallback((item: ProjectItem) => {
    setDialogState({ type: "delete", item });
  }, []);

  const handleConfirmDelete = useCallback(async () => {
    if (dialogState.item) {
      project.deleteItem(dialogState.item.id);
    }
    setDialogState({ type: null, item: null });
  }, [dialogState.item, project]);

  const handleSelectFile = useCallback((file: ProjectFile) => {
    project.openFile(file.id);
  }, [project]);

  const handleToggleFolder = useCallback((folder: ProjectFolder) => {
    // Toggle folder expansion in the tree
    // This is handled by the useProjectFiles hook
  }, []);

  const handleSaveAll = useCallback(async () => {
    const success = await project.saveAllFiles();
    if (success) {
      onSave?.(project.modifiedFiles);
    }
  }, [project, onSave]);

  const handleDownloadZip = useCallback(async () => {
    const blob = await project.exportAsZip();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${project.state.name}.zip`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }, [project]);

  const handleImport = useCallback(async (file: File) => {
    const success = await project.importFromZip(file);
    return success;
  }, [project]);

  const handlePrimaryChange = useCallback((content: string) => {
    const activeFile = project.getActiveFile();
    if (activeFile) {
      project.updateFileContent(activeFile.id, content);
      onFileChange?.(activeFile.id, content);
    }
  }, [project, onFileChange]);

  const handleSecondaryChange = useCallback((content: string) => {
    if (project.state.splitView.secondaryFileId) {
      project.updateFileContent(project.state.splitView.secondaryFileId, content);
      onFileChange?.(project.state.splitView.secondaryFileId, content);
    }
  }, [project, onFileChange]);

  // Derived state
  const activeFile = project.getActiveFile();
  const secondaryFile = project.state.splitView.secondaryFileId
    ? project.getFileById(project.state.splitView.secondaryFileId)
    : null;

  const tabs = project.openFiles.map(file => ({
    file,
    isActive: file.id === project.state.activeFileId || false,
    isModified: file.isModified || false,
  }));

  return (
    <div className={cn("flex flex-col h-full bg-background", className)}>
      {/* Toolbar */}
      <ProjectToolbar
        hasUnsavedChanges={project.hasUnsavedChanges}
        modifiedCount={project.modifiedFiles.length}
        isRunning={false}
        isSplitEnabled={project.state.splitView.enabled}
        onSaveAll={handleSaveAll}
        onRun={onRun}
        onDownloadZip={handleDownloadZip}
        onImport={() => setDialogState({ type: "import", item: null })}
        onReset={project.resetProject}
        onToggleSplit={project.toggleSplitView}
      />

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar Toggle */}
        <Button
          variant="ghost"
          size="icon"
          className="absolute left-0 top-14 z-10 h-8 w-8 rounded-r-md rounded-l-none border border-l-0"
          onClick={() => setIsSidebarOpen(!isSidebarOpen)}
        >
          {isSidebarOpen ? (
            <PanelLeftClose className="h-4 w-4" />
          ) : (
            <PanelLeftOpen className="h-4 w-4" />
          )}
        </Button>

        {/* File Tree Sidebar */}
        {isSidebarOpen && (
          <div className="w-64 flex-shrink-0 border-r">
            <FileTree
              root={project.state.root}
              activeFileId={project.state.activeFileId}
              onSelectFile={handleSelectFile}
              onToggleFolder={handleToggleFolder}
              onNewFile={handleNewFile}
              onNewFolder={handleNewFolder}
              onRename={handleRename}
              onDelete={handleDelete}
              onMove={project.moveItem}
            />
          </div>
        )}

        {/* Editor Area */}
        <div className="flex-1 flex flex-col min-w-0">
          {/* Tabs */}
          <FileTabs
            tabs={tabs}
            onSelect={project.openFile}
            onClose={project.closeTab}
            onCloseAll={project.closeAllTabs}
            onCloseOthers={project.closeOtherTabs}
            onReorder={project.reorderTabs}
          />

          {/* Editor */}
          <div className="flex-1 overflow-hidden">
            <SplitEditor
              primaryFile={activeFile}
              secondaryFile={secondaryFile}
              isSplitEnabled={project.state.splitView.enabled}
              splitRatio={project.state.splitView.splitRatio}
              onPrimaryChange={handlePrimaryChange}
              onSecondaryChange={handleSecondaryChange}
              onToggleSplit={project.toggleSplitView}
              onSplitRatioChange={project.setSplitRatio}
              onSwapPanes={project.swapSplitPanes}
              onCloseSecondary={() => project.setSplitView(false)}
              height="100%"
            />
          </div>
        </div>
      </div>

      {/* Dialogs */}
      <NewFileDialog
        isOpen={dialogState.type === "new-file"}
        onClose={() => setDialogState({ type: null, item: null })}
        onCreateFile={handleCreateFile}
        onCreateFolder={handleCreateFolder}
        defaultType={dialogState.defaultType}
      />

      <RenameDialog
        isOpen={dialogState.type === "rename"}
        onClose={() => setDialogState({ type: null, item: null })}
        item={dialogState.item}
        onRename={handleConfirmRename}
      />

      <DeleteConfirmDialog
        isOpen={dialogState.type === "delete"}
        onClose={() => setDialogState({ type: null, item: null })}
        item={dialogState.item}
        onConfirm={handleConfirmDelete}
      />

      <ImportProjectDialog
        isOpen={dialogState.type === "import"}
        onClose={() => setDialogState({ type: null, item: null })}
        onImport={handleImport}
      />
    </div>
  );
}

// Need to import ProjectFolder for type
import type { ProjectFolder } from "@/types/project-files";

export default MultiFileEditor;
