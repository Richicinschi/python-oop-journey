// Monaco Editor components (Agent 9)
export { CodeEditor, type CodeEditorProps } from './code-editor';
export { EditorToolbar } from './editor-toolbar';
export { EditorSkeleton } from './editor-skeleton';
export { Playground, PlaygroundOutput, type PlaygroundProps, type PlaygroundResult } from './playground';

// Problem page components (Agent 11)
export { HintsPanel } from './hints-panel';
export { InstructionsPanel } from './instructions-panel';
export { OutputPanel } from './output-panel';
export { SolutionModal } from './solution-modal';

// Multi-file editor components (Agent 16)
export { FileTree, type FileTreeProps } from './file-tree/file-tree';
export { FileTreeItem, type FileTreeItemProps } from './file-tree/file-tree-item';
export { FileTreeContextMenu, type FileTreeContextMenuProps } from './file-tree/file-tree-context-menu';

export { FileTabs, type FileTabsProps, type FileTab } from './file-tabs/file-tabs';

export { SplitEditor, type SplitEditorProps } from './split-editor';
export { ProjectToolbar, type ProjectToolbarProps } from './project-toolbar';
export { MultiFileEditor, type MultiFileEditorProps } from './multi-file-editor';

export { NewFileDialog, type NewFileDialogProps } from './new-file-dialog';
export { RenameDialog, type RenameDialogProps } from './rename-dialog';
export { DeleteConfirmDialog, type DeleteConfirmDialogProps } from './delete-confirm-dialog';
export { ImportProjectDialog, type ImportProjectDialogProps } from './import-project-dialog';
