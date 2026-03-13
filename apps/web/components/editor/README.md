# Monaco Editor Components

This directory contains the Monaco Editor integration for the Python OOP Journey playground.

## Components

### CodeEditor
The main Monaco Editor wrapper component.

```tsx
import { CodeEditor } from "@/components/editor";

<CodeEditor
  value={code}
  onChange={setCode}
  height="500px"
  fontSize={14}
  wordWrap="on"
  minimap={true}
  readOnly={false}
  onRun={handleRun}
/>
```

### EditorToolbar
Toolbar with editor controls.

```tsx
import { EditorToolbar } from "@/components/editor";

<EditorToolbar
  hasUnsavedChanges={true}
  fontSize={14}
  wordWrap={true}
  onReset={handleReset}
  onSave={handleSave}
  onRun={handleRun}
  onFontSizeChange={setFontSize}
  onWordWrapChange={setWordWrap}
/>
```

### EditorSkeleton
Loading skeleton for editor.

```tsx
import { EditorSkeleton } from "@/components/editor";

<EditorSkeleton height="400px" />
```

### Playground
Combined editor with toolbar and output panel for problem pages.

```tsx
import { Playground } from "@/components/editor";

<Playground
  problemId="week1-day1-problem1"
  starterCode={starterCode}
  onRun={async (code) => {
    // Execute code and return result
    return { output: "...", success: true };
  }}
/>
```

## Features

- **Python Language Support**: Full syntax highlighting and language features
- **VS Code-like Experience**: Familiar keybindings and behavior
- **Theme Support**: Automatic dark/light theme switching
- **Auto-save**: Debounced save to localStorage
- **Keyboard Shortcuts**: Ctrl+Enter to run, Ctrl+S to save
- **Lazy Loading**: Editor loads dynamically to avoid blocking initial render

## Test Page

Visit `/test/editor` to see all editor configurations and features in action.
