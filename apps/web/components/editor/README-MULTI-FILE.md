# Multi-File Editor System

A comprehensive multi-file editing system for the website playground, built with React, Monaco Editor, and IndexedDB persistence.

## Components

### Core Components

- **`MultiFileEditor`** - Main integrated editor component
- **`FileTree`** - Hierarchical file/folder explorer with drag-and-drop
- **`FileTabs`** - Tab bar for open files with drag reordering
- **`SplitEditor`** - Side-by-side file editing with resizeable panes
- **`ProjectToolbar`** - Toolbar with save, run, download, and import actions

### Dialog Components

- **`NewFileDialog`** - Create new files or folders
- **`RenameDialog`** - Rename existing items
- **`DeleteConfirmDialog`** - Confirm deletion with content warnings
- **`ImportProjectDialog`** - Import projects from ZIP files

### Hooks

- **`useProjectFiles`** - Core hook for managing project state
  - CRUD operations for files/folders
  - Tab management
  - Split view state
  - Auto-save to IndexedDB
  - Import/export ZIP functionality

## Usage

### Basic Usage

```tsx
import { MultiFileEditor } from "@/components/editor";

function MyPage() {
  return (
    <MultiFileEditor
      projectId="my-project"
      projectName="My Project"
      onSave={(files) => console.log("Saved:", files)}
      onRun={() => console.log("Running project...")}
      onFileChange={(fileId, content) => console.log("Changed:", fileId)}
    />
  );
}
```

### Advanced Usage with useProjectFiles

```tsx
import { useProjectFiles } from "@/hooks/use-project-files";
import { FileTree, FileTabs, SplitEditor, ProjectToolbar } from "@/components/editor";

function CustomEditor() {
  const project = useProjectFiles({
    projectId: "custom",
    projectName: "Custom Project",
    initialFiles: [
      {
        id: "1",
        name: "main.py",
        path: "main.py",
        content: "print('Hello World')",
        language: "python",
        isModified: false,
      },
    ],
  });

  return (
    <div className="h-full flex flex-col">
      <ProjectToolbar
        hasUnsavedChanges={project.hasUnsavedChanges}
        modifiedCount={project.modifiedFiles.length}
        onSaveAll={project.saveAllFiles}
        onToggleSplit={project.toggleSplitView}
        isSplitEnabled={project.state.splitView.enabled}
      />
      
      <div className="flex-1 flex">
        <FileTree
          root={project.state.root}
          activeFileId={project.state.activeFileId}
          onSelectFile={(file) => project.openFile(file.id)}
          onNewFile={project.createFile}
          onNewFolder={project.createFolder}
          onRename={(item) => {/* show rename dialog */}}
          onDelete={(item) => {/* show delete dialog */}}
        />
        
        <div className="flex-1 flex flex-col">
          <FileTabs
            tabs={project.openFiles.map(f => ({
              file: f,
              isActive: f.id === project.state.activeFileId,
              isModified: f.isModified,
            }))}
            onSelect={project.openFile}
            onClose={project.closeTab}
          />
          
          <SplitEditor
            primaryFile={project.getActiveFile()}
            secondaryFile={project.getFileById(project.state.splitView.secondaryFileId || "")}
            isSplitEnabled={project.state.splitView.enabled}
            onPrimaryChange={(content) => {
              const file = project.getActiveFile();
              if (file) project.updateFileContent(file.id, content);
            }}
          />
        </div>
      </div>
    </div>
  );
}
```

## Features

### File Management
- ✅ Create files and folders
- ✅ Rename items
- ✅ Delete items with confirmation
- ✅ Drag-and-drop to move items
- ✅ Context menus for all operations

### Editor Features
- ✅ Monaco Editor integration
- ✅ Multiple open tabs
- ✅ Split view for side-by-side editing
- ✅ Resizable split panes
- ✅ Language detection from file extension
- ✅ Per-file cursor and scroll position (via Monaco)

### Persistence
- ✅ IndexedDB storage for offline access
- ✅ Auto-save with debouncing
- ✅ Export project as ZIP
- ✅ Import project from ZIP

### Keyboard Shortcuts
- `Ctrl+S` - Save all files
- `Ctrl+Enter` - Run project
- `Ctrl+B` - Toggle sidebar

## File Structure

```
components/editor/
├── file-tree/
│   ├── file-tree.tsx           # Main tree component
│   ├── file-tree-item.tsx      # Individual item row
│   ├── file-tree-context-menu.tsx  # Right-click menus
│   └── index.ts
├── file-tabs/
│   ├── file-tabs.tsx           # Tab bar component
│   └── index.ts
├── split-editor.tsx            # Split view editor
├── project-toolbar.tsx         # Project actions toolbar
├── multi-file-editor.tsx       # Integrated editor
├── new-file-dialog.tsx         # Create new dialog
├── rename-dialog.tsx           # Rename dialog
├── delete-confirm-dialog.tsx   # Delete confirmation
├── import-project-dialog.tsx   # Import ZIP dialog
└── README-MULTI-FILE.md        # This file

hooks/
└── use-project-files.ts        # Core state management

types/
└── project-files.ts            # TypeScript types

lib/
└── project-db.ts               # IndexedDB operations
```

## Types

### ProjectFile
```typescript
interface ProjectFile {
  id: string;
  name: string;
  path: string;
  content: string;
  language: string;
  isModified: boolean;
  isReadOnly?: boolean;
  lastModified?: number;
}
```

### ProjectFolder
```typescript
interface ProjectFolder {
  id: string;
  name: string;
  path: string;
  children: (ProjectFile | ProjectFolder)[];
  isExpanded?: boolean;
}
```

### ProjectState
```typescript
interface ProjectState {
  id: string;
  name: string;
  root: ProjectFolder;
  openTabs: OpenTab[];
  activeFileId: string | null;
  lastSavedAt: number | null;
  isModified: boolean;
  splitView: {
    enabled: boolean;
    primaryFileId: string | null;
    secondaryFileId: string | null;
    splitRatio: number;
  };
}
```

## Dependencies Added

```json
{
  "jszip": "^3.10.1",
  "@radix-ui/react-context-menu": "^2.1.5"
}
```

## Testing

### Manual Testing Checklist

1. **File Tree**
   - [ ] Create nested folders
   - [ ] Create files in different folders
   - [ ] Rename files and folders
   - [ ] Delete files and folders
   - [ ] Drag and drop to move items
   - [ ] Context menu on all items

2. **Tabs**
   - [ ] Open multiple files
   - [ ] Close tabs individually
   - [ ] Close all tabs
   - [ ] Reorder tabs via drag
   - [ ] Unsaved indicators

3. **Editor**
   - [ ] Edit files
   - [ ] Language detection
   - [ ] Split view toggle
   - [ ] Resize split panes
   - [ ] Swap panes

4. **Persistence**
   - [ ] Auto-save after changes
   - [ ] Reload page - data persists
   - [ ] Download as ZIP
   - [ ] Import ZIP - structure preserved

5. **Keyboard Shortcuts**
   - [ ] Ctrl+S saves all
   - [ ] Ctrl+Enter runs
   - [ ] Ctrl+B toggles sidebar

## Future Enhancements

- [ ] File search/filter in tree
- [ ] Git integration (status, diff)
- [ ] Collaborative editing
- [ ] File history/versions
- [ ] Custom file templates
- [ ] External file drop support
- [ ] Minimap in editor
- [ ] Code folding
- [ ] Find and replace across files
