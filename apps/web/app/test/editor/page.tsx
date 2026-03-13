"use client";

import { useCallback, useState } from "react";
import { Code2, Terminal, Settings, Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";

import { CodeEditor } from "@/components/editor/code-editor";
import { EditorToolbar } from "@/components/editor/editor-toolbar";
import { EditorSkeleton } from "@/components/editor/editor-skeleton";
import { useEditorStore, useEditorKeyboardShortcuts } from "@/hooks/use-editor-store";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { cn } from "@/lib/utils";

const SAMPLE_CODE = `# Sample Python Code for Testing
class Person:
    """A simple Person class."""
    
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def greet(self) -> str:
        """Returns a greeting message."""
        return f"Hello, I'm {self.name} and I'm {self.age} years old!"
    
    def is_adult(self) -> bool:
        """Check if person is an adult."""
        return self.age >= 18

# Create instances
alice = Person("Alice", 25)
bob = Person("Bob", 17)

# Test the methods
print(alice.greet())
print(f"Is Alice an adult? {alice.is_adult()}")
print(f"Is Bob an adult? {bob.is_adult()}")

# List comprehension example
numbers = [1, 2, 3, 4, 5]
squares = [n ** 2 for n in numbers]
print(f"Squares: {squares}")
`;

const READONLY_CODE = `# This is read-only code
# You can view it but cannot edit

def calculate_factorial(n: int) -> int:
    """Calculate factorial of n."""
    if n <= 1:
        return 1
    return n * calculate_factorial(n - 1)

# Example usage
result = calculate_factorial(5)
print(f"5! = {result}")
`;

export default function EditorTestPage() {
  const { theme, setTheme } = useTheme();
  const [output, setOutput] = useState<string>("");
  const [isRunning, setIsRunning] = useState(false);
  const [activeTab, setActiveTab] = useState("basic");

  // Editor store for basic editor
  const basicEditor = useEditorStore({
    storageKey: "test-editor-basic",
    initialCode: SAMPLE_CODE,
    enableAutoSave: true,
  });

  // Editor store for minimal editor
  const minimalEditor = useEditorStore({
    storageKey: "test-editor-minimal",
    initialCode: "# Minimal editor example\nprint('Hello, World!')",
    enableAutoSave: true,
  });

  // Handle run code
  const handleRun = useCallback(() => {
    setIsRunning(true);
    setOutput("Running code...\n");

    // Simulate code execution
    setTimeout(() => {
      const code = basicEditor.code;
      setOutput(
        `> Execution started...\n\n` +
        `Code length: ${code.length} characters\n` +
        `Lines: ${code.split('\n').length}\n\n` +
        `> Execution completed successfully!\n`
      );
      setIsRunning(false);
    }, 500);
  }, [basicEditor.code]);

  // Keyboard shortcuts
  useEditorKeyboardShortcuts({
    onRun: handleRun,
    onSave: basicEditor.save,
  });

  const toggleTheme = () => {
    setTheme(theme === "dark" ? "light" : "dark");
  };

  return (
    <div className="container mx-auto py-8 px-4 max-w-6xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold flex items-center gap-3">
          <Code2 className="h-8 w-8" />
          Monaco Editor Test Page
        </h1>
        <p className="text-muted-foreground mt-2">
          Test various Monaco Editor configurations and features.
        </p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="grid w-full grid-cols-4 lg:w-[400px]">
          <TabsTrigger value="basic">Basic</TabsTrigger>
          <TabsTrigger value="minimal">Minimal</TabsTrigger>
          <TabsTrigger value="readonly">Read-only</TabsTrigger>
          <TabsTrigger value="loading">Loading</TabsTrigger>
        </TabsList>

        {/* Basic Editor Tab */}
        <TabsContent value="basic" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span>Basic Editor with Toolbar</span>
                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={toggleTheme}
                    className="gap-2"
                  >
                    {theme === "dark" ? (
                      <>
                        <Sun className="h-4 w-4" />
                        <span className="hidden sm:inline">Light</span>
                      </>
                    ) : (
                      <>
                        <Moon className="h-4 w-4" />
                        <span className="hidden sm:inline">Dark</span>
                      </>
                    )}
                  </Button>
                </div>
              </CardTitle>
              <CardDescription>
                Full-featured editor with toolbar, auto-save, and keyboard shortcuts.
                Try Ctrl+Enter to run, Ctrl+S to save.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <EditorToolbar
                hasUnsavedChanges={basicEditor.hasUnsavedChanges}
                fontSize={basicEditor.fontSize}
                wordWrap={basicEditor.wordWrap}
                onReset={basicEditor.reset}
                onSave={basicEditor.save}
                onRun={handleRun}
                onFontSizeChange={basicEditor.setFontSize}
                onWordWrapChange={basicEditor.setWordWrap}
              />
              
              <div className="grid gap-4 lg:grid-cols-[1fr,300px]">
                <CodeEditor
                  value={basicEditor.code}
                  onChange={basicEditor.setCode}
                  height="500px"
                  fontSize={basicEditor.fontSize}
                  wordWrap={basicEditor.wordWrap ? "on" : "off"}
                  minimap={basicEditor.minimap}
                  onRun={handleRun}
                />

                {/* Output panel */}
                <Card className="h-[500px] flex flex-col">
                  <CardHeader className="py-3">
                    <CardTitle className="text-sm flex items-center gap-2">
                      <Terminal className="h-4 w-4" />
                      Output
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="flex-1 overflow-auto">
                    <pre className="text-xs font-mono text-muted-foreground whitespace-pre-wrap">
                      {output || "Click 'Run' to see output..."}
                    </pre>
                  </CardContent>
                </Card>
              </div>

              {/* Status bar */}
              <div className="flex items-center gap-4 text-xs text-muted-foreground">
                <span>{basicEditor.code.length} chars</span>
                <span>{basicEditor.code.split('\n').length} lines</span>
                {basicEditor.hasUnsavedChanges && (
                  <span className="text-yellow-500">• Unsaved changes</span>
                )}
                {basicEditor.lastSavedAt && (
                  <span>
                    Last saved: {new Date(basicEditor.lastSavedAt).toLocaleTimeString()}
                  </span>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Minimal Editor Tab */}
        <TabsContent value="minimal" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Minimal Editor</CardTitle>
              <CardDescription>
                Editor without minimap, with simpler configuration.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <CodeEditor
                value={minimalEditor.code}
                onChange={minimalEditor.setCode}
                height="400px"
                minimap={false}
                fontSize={16}
                lineNumbers="on"
                options={{
                  renderWhitespace: "all",
                  smoothScrolling: false,
                }}
              />
            </CardContent>
          </Card>
        </TabsContent>

        {/* Read-only Tab */}
        <TabsContent value="readonly" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Read-only Editor</CardTitle>
              <CardDescription>
                Editor in read-only mode for viewing code only.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <CodeEditor
                value={READONLY_CODE}
                height="400px"
                readOnly={true}
                minimap={true}
              />
            </CardContent>
          </Card>
        </TabsContent>

        {/* Loading Tab */}
        <TabsContent value="loading" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Loading States</CardTitle>
              <CardDescription>
                Skeleton loader displayed while Monaco loads.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <Label className="mb-2 block">Default height (400px)</Label>
                <EditorSkeleton height="400px" />
              </div>
              
              <Separator />
              
              <div>
                <Label className="mb-2 block">Small height (200px)</Label>
                <EditorSkeleton height="200px" />
              </div>
              
              <Separator />
              
              <div>
                <Label className="mb-2 block">Large height (600px)</Label>
                <EditorSkeleton height="600px" />
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Settings Panel */}
      <Card className="mt-8">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Settings className="h-5 w-5" />
            Editor Settings
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <div className="flex items-center justify-between space-y-0 rounded-lg border p-4">
              <div className="space-y-0.5">
                <Label htmlFor="word-wrap">Word Wrap</Label>
                <p className="text-xs text-muted-foreground">
                  Wrap long lines
                </p>
              </div>
              <Switch
                id="word-wrap"
                checked={basicEditor.wordWrap}
                onCheckedChange={basicEditor.setWordWrap}
              />
            </div>

            <div className="flex items-center justify-between space-y-0 rounded-lg border p-4">
              <div className="space-y-0.5">
                <Label htmlFor="minimap">Minimap</Label>
                <p className="text-xs text-muted-foreground">
                  Show code overview
                </p>
              </div>
              <Switch
                id="minimap"
                checked={basicEditor.minimap}
                onCheckedChange={basicEditor.setMinimap}
              />
            </div>

            <div className="flex items-center justify-between space-y-0 rounded-lg border p-4">
              <div className="space-y-0.5">
                <Label htmlFor="auto-save">Auto-save</Label>
                <p className="text-xs text-muted-foreground">
                  Save to localStorage
                </p>
              </div>
              <Switch id="auto-save" checked={true} disabled />
            </div>
          </div>

          <div className="mt-6 flex flex-wrap gap-2">
            <Button variant="outline" onClick={basicEditor.clear}>
              Clear Saved Code
            </Button>
            <Button variant="outline" onClick={basicEditor.restore}>
              Restore from Storage
            </Button>
            <Button
              variant="outline"
              onClick={() => basicEditor.setFontSize(14)}
            >
              Reset Font Size
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Feature List */}
      <Card className="mt-8">
        <CardHeader>
          <CardTitle>Implemented Features</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="grid gap-2 sm:grid-cols-2">
            {[
              "✅ Monaco Editor with Python support",
              "✅ Syntax highlighting",
              "✅ Auto-indentation",
              "✅ Bracket matching",
              "✅ Auto-closing brackets",
              "✅ Code folding",
              "✅ Multiple cursors",
              "✅ Find/Replace (Ctrl+F)",
              "✅ Keyboard shortcuts (Ctrl+Enter to run)",
              "✅ Dark/Light theme support",
              "✅ Custom VS Code-like themes",
              "✅ Lazy loading with skeleton",
              "✅ Auto-save to localStorage",
              "✅ Font size persistence",
              "✅ Word wrap toggle",
              "✅ Minimap toggle",
              "✅ Responsive layout",
              "✅ Read-only mode",
              "✅ Debounced auto-save",
            ].map((feature, i) => (
              <li key={i} className="text-sm text-muted-foreground">
                {feature}
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}
