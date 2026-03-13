# Projects Components

This directory contains components for the multi-file project editor feature.

## Components

### Core Components

- **project-card.tsx** - Displays project information in various formats (default, compact, detailed)
- **file-tree.tsx** - Hierarchical file explorer with create/delete operations
- **empty-state.tsx** - Empty state messages for different contexts
- **skeletons.tsx** - Loading skeletons for various project UI elements

### UX Components

- **project-tour.tsx** - First-time user onboarding tour
- **error-boundary.tsx** - Error handling for project page
- **keyboard-shortcuts.tsx** - Shortcuts dialog and helpers
- **active-projects-section.tsx** - Dashboard section for active projects

## Usage

```tsx
import { 
  ProjectCard, 
  FileTree, 
  ProjectEmptyState,
  ActiveProjectsSection 
} from '@/components/projects';
```

## File Tree Component

```tsx
<FileTree
  files={projectFiles}
  activeFileId={activeFileId}
  onFileSelect={(fileId) => openTab(fileId)}
  onFileCreate={(name) => createFile(name)}
  onFileDelete={(fileId) => deleteFile(fileId)}
  onFileSave={(fileId) => saveFile(fileId)}
/>
```

## Project Card

```tsx
<ProjectCard
  project={weeklyProject}
  progress={userProgress}
  variant="detailed"
  onStart={() => startProject(project)}
  onContinue={() => continueProject(project)}
/>
```

## Active Projects Section

```tsx
<ActiveProjectsSection
  projects={allProjects}
  progressMap={userProgress}
  currentWeekNumber={1}
  variant="full"
/>
```
