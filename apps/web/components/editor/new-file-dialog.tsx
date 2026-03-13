"use client";

import { useState, useCallback, useEffect } from "react";
import { FilePlus, FolderPlus } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export interface NewFileDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onCreateFile: (name: string) => void;
  onCreateFolder: (name: string) => void;
  defaultType?: "file" | "folder";
  parentPath?: string;
}

const FILE_TEMPLATES = [
  { label: "Python", extension: "py", default: true },
  { label: "JavaScript", extension: "js" },
  { label: "TypeScript", extension: "ts" },
  { label: "HTML", extension: "html" },
  { label: "CSS", extension: "css" },
  { label: "JSON", extension: "json" },
  { label: "Markdown", extension: "md" },
  { label: "Text", extension: "txt" },
];

export function NewFileDialog({
  isOpen,
  onClose,
  onCreateFile,
  onCreateFolder,
  defaultType = "file",
  parentPath = "",
}: NewFileDialogProps) {
  const [activeTab, setActiveTab] = useState<"file" | "folder">(defaultType);
  const [name, setName] = useState("");
  const [selectedExtension, setSelectedExtension] = useState("py");
  const [error, setError] = useState<string | null>(null);

  // Reset state when dialog opens
  useEffect(() => {
    if (isOpen) {
      setActiveTab(defaultType);
      setName("");
      setError(null);
      // Auto-focus input after a short delay
      setTimeout(() => {
        const input = document.getElementById("new-item-name");
        input?.focus();
      }, 100);
    }
  }, [isOpen, defaultType]);

  const validateName = useCallback((value: string, type: "file" | "folder"): string | null => {
    const trimmed = value.trim();
    
    if (!trimmed) {
      return `${type === "file" ? "File" : "Folder"} name is required`;
    }
    
    // Check for invalid characters
    if (/[<>:"|?*]/.test(trimmed)) {
      return "Name contains invalid characters";
    }
    
    // Check for slashes
    if (trimmed.includes("/") || trimmed.includes("\\")) {
      return "Name cannot contain slashes";
    }
    
    // Check for leading/trailing dots or spaces
    if (trimmed !== value || trimmed.startsWith(".") || trimmed.endsWith(".")) {
      return "Name cannot start or end with spaces or dots";
    }
    
    // File-specific validation
    if (type === "file") {
      // Check if it has an extension or user selected one
      const hasExtension = trimmed.includes(".");
      if (!hasExtension && !selectedExtension) {
        return "Please select a file type or include an extension";
      }
    }
    
    return null;
  }, [selectedExtension]);

  const handleSubmit = useCallback((e?: React.FormEvent) => {
    e?.preventDefault();
    
    const validationError = validateName(name, activeTab);
    if (validationError) {
      setError(validationError);
      return;
    }
    
    const finalName = name.trim();
    
    if (activeTab === "file") {
      // Add extension if not present
      const hasExtension = finalName.includes(".");
      const fullName = hasExtension ? finalName : `${finalName}.${selectedExtension}`;
      onCreateFile(fullName);
    } else {
      onCreateFolder(finalName);
    }
    
    onClose();
  }, [name, activeTab, selectedExtension, validateName, onCreateFile, onCreateFolder, onClose]);

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSubmit();
    } else if (e.key === "Escape") {
      onClose();
    }
  }, [handleSubmit, onClose]);

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Create New</DialogTitle>
          <DialogDescription>
            {parentPath ? `In: ${parentPath}` : "Add a new file or folder to your project"}
          </DialogDescription>
        </DialogHeader>

        <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as "file" | "folder")}>
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="file">
              <FilePlus className="mr-2 h-4 w-4" />
              File
            </TabsTrigger>
            <TabsTrigger value="folder">
              <FolderPlus className="mr-2 h-4 w-4" />
              Folder
            </TabsTrigger>
          </TabsList>

          <TabsContent value="file" className="mt-4">
            <form onSubmit={handleSubmit}>
              <div className="grid gap-4">
                <div className="grid gap-2">
                  <Label htmlFor="new-item-name">File Name</Label>
                  <Input
                    id="new-item-name"
                    placeholder="my_script"
                    value={name}
                    onChange={(e) => {
                      setName(e.target.value);
                      setError(null);
                    }}
                    onKeyDown={handleKeyDown}
                    className={cn(error && "border-destructive")}
                  />
                  {error && (
                    <p className="text-sm text-destructive">{error}</p>
                  )}
                </div>

                <div className="grid gap-2">
                  <Label>File Type</Label>
                  <div className="grid grid-cols-4 gap-2">
                    {FILE_TEMPLATES.map((template) => (
                      <button
                        key={template.extension}
                        type="button"
                        onClick={() => setSelectedExtension(template.extension)}
                        className={cn(
                          "px-2 py-1.5 text-xs rounded-md border transition-colors",
                          selectedExtension === template.extension
                            ? "bg-primary text-primary-foreground border-primary"
                            : "bg-background hover:bg-accent border-input"
                        )}
                      >
                        {template.label}
                      </button>
                    ))}
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Or type the full name with extension (e.g., script.py)
                  </p>
                </div>
              </div>
            </form>
          </TabsContent>

          <TabsContent value="folder" className="mt-4">
            <form onSubmit={handleSubmit}>
              <div className="grid gap-4">
                <div className="grid gap-2">
                  <Label htmlFor="new-folder-name">Folder Name</Label>
                  <Input
                    id="new-folder-name"
                    placeholder="my_folder"
                    value={name}
                    onChange={(e) => {
                      setName(e.target.value);
                      setError(null);
                    }}
                    onKeyDown={handleKeyDown}
                    className={cn(error && "border-destructive")}
                  />
                  {error && (
                    <p className="text-sm text-destructive">{error}</p>
                  )}
                </div>
              </div>
            </form>
          </TabsContent>
        </Tabs>

        <DialogFooter>
          <Button variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button onClick={() => handleSubmit()}>
            Create {activeTab === "file" ? "File" : "Folder"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

export default NewFileDialog;
