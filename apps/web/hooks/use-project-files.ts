"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { v4 as uuidv4 } from "uuid";
import type { ProjectFile, ProjectFolder, ProjectItem, ProjectState, OpenTab } from "@/types/project-files";
import { isProjectFile, isProjectFolder, getLanguageFromExtension, getStarterCode } from "@/types/project-files";
import { openDB, type IDBPDatabase } from "idb";

// Database configuration
const PROJECT_DB_NAME = "oop-journey-projects";
const PROJECT_DB_VERSION = 1;

// Project schema interface
interface ProjectDB {
  projects: {
    key: string;
    value: ProjectState;
  };
  files: {
    key: string;
    value: ProjectFile;
  };
}

// Auto-save delay in ms
const AUTO_SAVE_DELAY = 2000;

/** Generate unique ID */
function generateId(): string {
  return uuidv4();
}

/** Get file extension */
function getExtension(filename: string): string {
  const match = filename.match(/\.([^.]+)$/);
  return match ? match[1].toLowerCase() : "";
}

/** Validate filename */
function isValidFilename(name: string): boolean {
  // No empty names
  if (!name.trim()) return false;
  // No slashes
  if (name.includes("/") || name.includes("\\")) return false;
  // No reserved characters
  if (/[<>:"|?*]/.test(name)) return false;
  // No leading/trailing dots or spaces
  if (name.trim() !== name || name.startsWith(".") || name.endsWith(".")) return false;
  return true;
}

/** Find item by ID in tree */
function findItemById(root: ProjectFolder, id: string): ProjectItem | null {
  for (const child of root.children) {
    if (child.id === id) return child;
    if (isProjectFolder(child)) {
      const found = findItemById(child, id);
      if (found) return found;
    }
  }
  return null;
}

/** Find parent folder of an item */
function findParentFolder(root: ProjectFolder, itemId: string): ProjectFolder | null {
  for (const child of root.children) {
    if (child.id === itemId) return root;
    if (isProjectFolder(child)) {
      const found = findParentFolder(child, itemId);
      if (found) return found;
    }
  }
  return null;
}

/** Find item by path */
function findItemByPath(root: ProjectFolder, path: string): ProjectItem | null {
  for (const child of root.children) {
    if (child.path === path) return child;
    if (isProjectFolder(child)) {
      const found = findItemByPath(child, path);
      if (found) return found;
    }
  }
  return null;
}

/** Update item in tree (returns new root) */
function updateItemInTree(root: ProjectFolder, itemId: string, updates: Partial<ProjectItem>): ProjectFolder {
  const newRoot = { ...root, children: [...root.children] };
  
  function updateInFolder(folder: ProjectFolder): boolean {
    for (let i = 0; i < folder.children.length; i++) {
      const child = folder.children[i];
      if (child.id === itemId) {
        folder.children[i] = { ...child, ...updates } as ProjectItem;
        return true;
      }
      if (isProjectFolder(child)) {
        if (updateInFolder(child)) return true;
      }
    }
    return false;
  }
  
  updateInFolder(newRoot);
  return newRoot;
}

/** Remove item from tree (returns new root) */
function removeItemFromTree(root: ProjectFolder, itemId: string): ProjectFolder {
  const newRoot = { ...root, children: [...root.children] };
  
  function removeFromFolder(folder: ProjectFolder): boolean {
    const index = folder.children.findIndex(c => c.id === itemId);
    if (index !== -1) {
      folder.children.splice(index, 1);
      return true;
    }
    for (const child of folder.children) {
      if (isProjectFolder(child)) {
        if (removeFromFolder(child)) return true;
      }
    }
    return false;
  }
  
  removeFromFolder(newRoot);
  return newRoot;
}

/** Move item in tree */
function moveItemInTree(root: ProjectFolder, itemId: string, targetFolderId: string): ProjectFolder {
  // Find the item to move
  const item = findItemById(root, itemId);
  if (!item) return root;
  
  // Can't move into itself or its descendants
  if (isProjectFolder(item) && (item.id === targetFolderId || findItemById(item, targetFolderId))) {
    return root;
  }
  
  // Find target folder
  const targetFolder = findItemById(root, targetFolderId);
  if (!targetFolder || !isProjectFolder(targetFolder)) return root;
  
  // Check for name collision
  const nameCollision = targetFolder.children.find(c => c.name === item.name && c.id !== item.id);
  if (nameCollision) return root;
  
  // Remove from current location
  let newRoot = removeItemFromTree(root, itemId);
  
  // Find target folder in new root (it may have been recreated)
  const newTargetFolder = findItemById(newRoot, targetFolderId);
  if (!newTargetFolder || !isProjectFolder(newTargetFolder)) return newRoot;
  
  // Update path and add to target
  const newPath = `${newTargetFolder.path}/${item.name}`;
  const movedItem = { ...item, path: newPath };
  
  // Update paths for all descendants if it's a folder
  function updatePaths(folder: ProjectFolder, parentPath: string): ProjectFolder {
    const newFolder: ProjectFolder = { ...folder, path: `${parentPath}/${folder.name}` };
    newFolder.children = folder.children.map(child => {
      if (isProjectFolder(child)) {
        return updatePaths(child, newFolder.path);
      }
      return { ...child, path: `${newFolder.path}/${child.name}` };
    });
    return newFolder;
  }
  
  const finalItem = isProjectFolder(movedItem) 
    ? updatePaths(movedItem, newTargetFolder.path)
    : movedItem;
  
  // Add to target folder
  const finalTarget = findItemById(newRoot, targetFolderId) as ProjectFolder;
  if (finalTarget) {
    finalTarget.children = [...finalTarget.children, finalItem];
  }
  
  return newRoot;
}

/** Get all file IDs in a folder recursively */
function getAllFileIds(folder: ProjectFolder): string[] {
  const ids: string[] = [];
  for (const child of folder.children) {
    if (isProjectFile(child)) {
      if (child.id) ids.push(child.id);
    } else {
      ids.push(...getAllFileIds(child));
    }
  }
  return ids;
}

/** Collect all files from tree */
function collectAllFiles(folder: ProjectFolder): ProjectFile[] {
  const files: ProjectFile[] = [];
  for (const child of folder.children) {
    if (isProjectFile(child)) {
      files.push(child);
    } else {
      files.push(...collectAllFiles(child));
    }
  }
  return files;
}

/** Options for useProjectFiles hook */
export interface UseProjectFilesOptions {
  projectId?: string;
  projectName?: string;
  initialFiles?: ProjectFile[];
  enableAutoSave?: boolean;
  onSave?: (state: ProjectState) => void;
}

/** Return type for useProjectFiles hook */
export interface UseProjectFilesReturn {
  // State
  state: ProjectState;
  isLoading: boolean;
  error: string | null;
  
  // File operations
  createFile: (name: string, parentFolderId?: string, content?: string) => ProjectFile | null;
  createFolder: (name: string, parentFolderId?: string) => ProjectFolder | null;
  renameItem: (itemId: string, newName: string) => boolean;
  deleteItem: (itemId: string) => boolean;
  moveItem: (itemId: string, targetFolderId: string) => boolean;
  updateFileContent: (fileId: string, content: string) => boolean;
  
  // Tab operations
  openFile: (fileId: string) => void;
  closeTab: (fileId: string) => void;
  closeAllTabs: () => void;
  closeOtherTabs: (keepFileId: string) => void;
  setActiveFile: (fileId: string | null) => void;
  reorderTabs: (newOrder: string[]) => void;
  updateTabState: (fileId: string, state: Partial<OpenTab>) => void;
  
  // Split view
  toggleSplitView: () => void;
  setSplitView: (enabled: boolean) => void;
  setSplitFiles: (primaryId: string | null, secondaryId: string | null) => void;
  setSplitRatio: (ratio: number) => void;
  swapSplitPanes: () => void;
  
  // Save/Load
  saveAllFiles: () => Promise<boolean>;
  exportAsZip: () => Promise<Blob>;
  importFromZip: (zipBlob: Blob) => Promise<boolean>;
  resetProject: () => void;
  
  // Navigation
  getActiveFile: () => ProjectFile | null;
  getFileById: (fileId: string) => ProjectFile | null;
  getFolderById: (folderId: string) => ProjectFolder | null;
  
  // Derived state
  modifiedFiles: ProjectFile[];
  openFiles: ProjectFile[];
  hasUnsavedChanges: boolean;
}

/** Hook for managing project files */
export function useProjectFiles(options: UseProjectFilesOptions = {}): UseProjectFilesReturn {
  const { projectId = "default", projectName = "My Project", enableAutoSave = true, onSave } = options;
  
  // Initialize state
  const [state, setState] = useState<ProjectState>(() => createInitialState(projectId, projectName));
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Refs for auto-save
  const autoSaveTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const dbRef = useRef<IDBPDatabase<ProjectDB> | null>(null);
  
  // Initialize database and load saved state
  useEffect(() => {
    let isMounted = true;
    
    async function init() {
      try {
        const { openDB } = await import("idb");
        const db = await openDB<ProjectDB>(PROJECT_DB_NAME, PROJECT_DB_VERSION, {
          upgrade(db) {
            if (!db.objectStoreNames.contains("projects")) {
              db.createObjectStore("projects", { keyPath: "id" });
            }
            if (!db.objectStoreNames.contains("files")) {
              db.createObjectStore("files", { keyPath: "id" });
            }
          },
        });
        
        if (!isMounted) return;
        dbRef.current = db;
        
        // Load saved project state
        const savedState = await db.get("projects", projectId);
        if (savedState && isMounted) {
          setState(savedState);
        } else if (options.initialFiles && isMounted) {
          // Create initial files
          const root: ProjectFolder = {
            id: "root",
            name: projectName,
            path: "",
            children: options.initialFiles,
            isExpanded: true,
          };
          setState(prev => ({ ...prev, root }));
        }
      } catch (err) {
        console.error("Failed to initialize project database:", err);
        if (isMounted) {
          setError("Failed to load project");
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }
    
    init();
    
    return () => {
      isMounted = false;
    };
  }, [projectId, projectName]);
  
  // Auto-save effect
  useEffect(() => {
    if (!enableAutoSave || !state.isModified) return;
    
    if (autoSaveTimeoutRef.current) {
      clearTimeout(autoSaveTimeoutRef.current);
    }
    
    autoSaveTimeoutRef.current = setTimeout(() => {
      saveAllFiles();
    }, AUTO_SAVE_DELAY);
    
    return () => {
      if (autoSaveTimeoutRef.current) {
        clearTimeout(autoSaveTimeoutRef.current);
      }
    };
  }, [state, enableAutoSave]);
  
  // ===== File Operations =====
  
  const createFile = useCallback((name: string, parentFolderId = "root", content?: string): ProjectFile | null => {
    if (!isValidFilename(name)) {
      setError("Invalid filename");
      return null;
    }
    
    const parentFolder = findItemById(state.root, parentFolderId);
    if (!parentFolder || !isProjectFolder(parentFolder)) {
      setError("Parent folder not found");
      return null;
    }
    
    // Check for name collision
    if (parentFolder.children.some(c => c.name === name)) {
      setError(`A file named "${name}" already exists`);
      return null;
    }
    
    const language = getLanguageFromExtension(name);
    const fileContent = content ?? getStarterCode(language);
    
    const newFile: ProjectFile = {
      id: generateId(),
      name,
      path: `${parentFolder.path}/${name}`.replace(/^\//, ""),
      content: fileContent,
      language,
      isModified: false,
      lastModified: Date.now(),
    };
    
    setState(prev => ({
      ...prev,
      root: {
        ...prev.root,
        children: prev.root.id === parentFolderId
          ? [...prev.root.children, newFile]
          : updateItemInTree(prev.root, parentFolderId, {
              children: [...parentFolder.children, newFile]
            }).children,
      },
      isModified: true,
    }));
    
    // Auto-open the new file
    if (newFile.id) openFile(newFile.id);
    
    return newFile;
  }, [state.root]);
  
  const createFolder = useCallback((name: string, parentFolderId = "root"): ProjectFolder | null => {
    if (!isValidFilename(name)) {
      setError("Invalid folder name");
      return null;
    }
    
    const parentFolder = findItemById(state.root, parentFolderId);
    if (!parentFolder || !isProjectFolder(parentFolder)) {
      setError("Parent folder not found");
      return null;
    }
    
    // Check for name collision
    if (parentFolder.children.some(c => c.name === name)) {
      setError(`A folder named "${name}" already exists`);
      return null;
    }
    
    const newFolder: ProjectFolder = {
      id: generateId(),
      name,
      path: `${parentFolder.path}/${name}`.replace(/^\//, ""),
      children: [],
      isExpanded: true,
    };
    
    setState(prev => ({
      ...prev,
      root: updateItemInTree(prev.root, parentFolderId, {
        children: [...parentFolder.children, newFolder]
      }),
      isModified: true,
    }));
    
    return newFolder;
  }, [state.root]);
  
  const renameItem = useCallback((itemId: string, newName: string): boolean => {
    if (!isValidFilename(newName)) {
      setError("Invalid name");
      return false;
    }
    
    const item = findItemById(state.root, itemId);
    if (!item) {
      setError("Item not found");
      return false;
    }
    
    const parentFolder = findParentFolder(state.root, itemId);
    if (!parentFolder) {
      setError("Cannot rename root");
      return false;
    }
    
    // Check for name collision
    if (parentFolder.children.some(c => c.name === newName && c.id !== itemId)) {
      setError(`An item named "${newName}" already exists`);
      return false;
    }
    
    // Update path
    const newPath = `${parentFolder.path}/${newName}`.replace(/^\//, "");
    
    setState(prev => {
      let newRoot = updateItemInTree(prev.root, itemId, { name: newName, path: newPath });
      
      // If it's a folder, update all descendant paths
      if (isProjectFolder(item)) {
        function updateFolderPaths(folder: ProjectFolder, parentPath: string): ProjectFolder {
          const updatedFolder = { ...folder };
          updatedFolder.path = `${parentPath}/${folder.name}`;
          updatedFolder.children = folder.children.map(child => {
            if (isProjectFolder(child)) {
              return updateFolderPaths(child, updatedFolder.path);
            }
            return { ...child, path: `${updatedFolder.path}/${child.name}` };
          });
          return updatedFolder;
        }
        
        // Find and update the renamed folder
        const renamedFolder = findItemById(newRoot, itemId) as ProjectFolder;
        if (renamedFolder) {
          newRoot = updateItemInTree(newRoot, itemId, updateFolderPaths(renamedFolder, parentFolder.path));
        }
      }
      
      return {
        ...prev,
        root: newRoot,
        isModified: true,
      };
    });
    
    return true;
  }, [state.root]);
  
  const deleteItem = useCallback((itemId: string): boolean => {
    if (itemId === "root") {
      setError("Cannot delete root folder");
      return false;
    }
    
    const item = findItemById(state.root, itemId);
    if (!item) {
      setError("Item not found");
      return false;
    }
    
    // Close any open tabs for this item (and its children if folder)
    const filesToClose = isProjectFolder(item) 
      ? getAllFileIds(item)
      : [itemId];
    
    setState(prev => ({
      ...prev,
      root: removeItemFromTree(prev.root, itemId),
      openTabs: prev.openTabs.filter(t => !filesToClose.includes(t.fileId)),
      activeFileId: filesToClose.includes(prev.activeFileId || "") 
        ? (prev.openTabs.find(t => !filesToClose.includes(t.fileId))?.fileId || null)
        : prev.activeFileId,
      isModified: true,
    }));
    
    return true;
  }, [state.root]);
  
  const moveItem = useCallback((itemId: string, targetFolderId: string): boolean => {
    if (itemId === targetFolderId) return false;
    
    const item = findItemById(state.root, itemId);
    if (!item) return false;
    
    const targetFolder = findItemById(state.root, targetFolderId);
    if (!targetFolder || !isProjectFolder(targetFolder)) return false;
    
    // Check if target is a descendant of item
    if (isProjectFolder(item) && findItemById(item, targetFolderId)) {
      setError("Cannot move a folder into itself");
      return false;
    }
    
    setState(prev => ({
      ...prev,
      root: moveItemInTree(prev.root, itemId, targetFolderId),
      isModified: true,
    }));
    
    return true;
  }, [state.root]);
  
  const updateFileContent = useCallback((fileId: string, content: string): boolean => {
    const file = findItemById(state.root, fileId);
    if (!file || !isProjectFile(file)) return false;
    
    setState(prev => ({
      ...prev,
      root: updateItemInTree(prev.root, fileId, { 
        content, 
        isModified: content !== file.content,
        lastModified: Date.now(),
      }),
      isModified: true,
    }));
    
    return true;
  }, [state.root]);
  
  // ===== Tab Operations =====
  
  const openFile = useCallback((fileId: string) => {
    setState(prev => {
      // Check if already open
      if (prev.openTabs.some(t => t.fileId === fileId)) {
        return {
          ...prev,
          activeFileId: fileId,
          openTabs: prev.openTabs.map(t => ({
            ...t,
            isActive: t.fileId === fileId,
          })),
        };
      }
      
      // Add new tab
      return {
        ...prev,
        activeFileId: fileId,
        openTabs: [
          ...prev.openTabs.map(t => ({ ...t, isActive: false })),
          { fileId, isActive: true },
        ],
      };
    });
  }, []);
  
  const closeTab = useCallback((fileId: string) => {
    setState(prev => {
      const tabIndex = prev.openTabs.findIndex(t => t.fileId === fileId);
      const newTabs = prev.openTabs.filter(t => t.fileId !== fileId);
      
      // If closing active tab, activate another
      let newActiveId = prev.activeFileId;
      if (prev.activeFileId === fileId && newTabs.length > 0) {
        const newActiveTab = newTabs[Math.min(tabIndex, newTabs.length - 1)];
        newActiveId = newActiveTab.fileId;
        newActiveTab.isActive = true;
      } else if (newTabs.length === 0) {
        newActiveId = null;
      }
      
      return {
        ...prev,
        openTabs: newTabs,
        activeFileId: newActiveId,
      };
    });
  }, []);
  
  const closeAllTabs = useCallback(() => {
    setState(prev => ({
      ...prev,
      openTabs: [],
      activeFileId: null,
    }));
  }, []);
  
  const closeOtherTabs = useCallback((keepFileId: string) => {
    setState(prev => ({
      ...prev,
      openTabs: prev.openTabs.filter(t => t.fileId === keepFileId),
      activeFileId: keepFileId,
    }));
  }, []);
  
  const setActiveFile = useCallback((fileId: string | null) => {
    setState(prev => ({
      ...prev,
      activeFileId: fileId,
      openTabs: prev.openTabs.map(t => ({
        ...t,
        isActive: t.fileId === fileId,
      })),
    }));
  }, []);
  
  const reorderTabs = useCallback((newOrder: string[]) => {
    setState(prev => {
      const tabMap = new Map(prev.openTabs.map(t => [t.fileId, t]));
      return {
        ...prev,
        openTabs: newOrder
          .map(id => tabMap.get(id))
          .filter((t): t is OpenTab => t !== undefined),
      };
    });
  }, []);
  
  const updateTabState = useCallback((fileId: string, tabState: Partial<OpenTab>) => {
    setState(prev => ({
      ...prev,
      openTabs: prev.openTabs.map(t =>
        t.fileId === fileId ? { ...t, ...tabState } : t
      ),
    }));
  }, []);
  
  // ===== Split View =====
  
  const toggleSplitView = useCallback(() => {
    setState(prev => ({
      ...prev,
      splitView: {
        ...prev.splitView,
        enabled: !prev.splitView.enabled,
        secondaryFileId: !prev.splitView.enabled && prev.activeFileId
          ? prev.openTabs.find(t => t.fileId !== prev.activeFileId)?.fileId || null
          : prev.splitView.secondaryFileId,
      },
    }));
  }, []);
  
  const setSplitView = useCallback((enabled: boolean) => {
    setState(prev => ({
      ...prev,
      splitView: {
        ...prev.splitView,
        enabled,
      },
    }));
  }, []);
  
  const setSplitFiles = useCallback((primaryId: string | null, secondaryId: string | null) => {
    setState(prev => ({
      ...prev,
      splitView: {
        ...prev.splitView,
        primaryFileId: primaryId,
        secondaryFileId: secondaryId,
        enabled: !!(primaryId && secondaryId),
      },
    }));
  }, []);
  
  const setSplitRatio = useCallback((ratio: number) => {
    setState(prev => ({
      ...prev,
      splitView: {
        ...prev.splitView,
        splitRatio: Math.max(0.2, Math.min(0.8, ratio)),
      },
    }));
  }, []);
  
  const swapSplitPanes = useCallback(() => {
    setState(prev => ({
      ...prev,
      splitView: {
        ...prev.splitView,
        primaryFileId: prev.splitView.secondaryFileId,
        secondaryFileId: prev.splitView.primaryFileId,
      },
    }));
  }, []);
  
  // ===== Save/Load =====
  
  const saveAllFiles = useCallback(async (): Promise<boolean> => {
    try {
      const db = dbRef.current;
      if (!db) return false;
      
      // Mark all files as saved
      const allFiles = collectAllFiles(state.root);
      const savedFiles = allFiles.map(f => ({ ...f, isModified: false }));
      
      // Save to IndexedDB
      const tx = db.transaction(["projects", "files"], "readwrite");
      
      // Update files
      for (const file of savedFiles) {
        await tx.objectStore("files").put(file);
      }
      
      // Update project state
      const newState: ProjectState = {
        ...state,
        root: updateAllFilesInTree(state.root, savedFiles),
        lastSavedAt: Date.now(),
        isModified: false,
      };
      
      await tx.objectStore("projects").put(newState);
      await tx.done;
      
      setState(newState);
      onSave?.(newState);
      
      return true;
    } catch (err) {
      console.error("Failed to save files:", err);
      setError("Failed to save files");
      return false;
    }
  }, [state, onSave]);
  
  const exportAsZip = useCallback(async (): Promise<Blob> => {
    const JSZip = (await import("jszip")).default;
    const zip = new JSZip();
    
    function addFolderToZip(folder: ProjectFolder, zipFolder: InstanceType<typeof JSZip>) {
      for (const child of folder.children) {
        if (isProjectFile(child)) {
          if (child.name) zipFolder.file(child.name, child.content ?? '');
        } else {
          if (child.name) {
            const newFolder = zipFolder.folder(child.name);
            if (newFolder) {
              addFolderToZip(child, newFolder);
            }
          }
        }
      }
    }
    
    addFolderToZip(state.root, zip);
    
    return zip.generateAsync({ type: "blob" });
  }, [state.root]);
  
  const importFromZip = useCallback(async (zipBlob: Blob): Promise<boolean> => {
    try {
      const JSZip = (await import("jszip")).default;
      const zip = await JSZip.loadAsync(zipBlob);
      
      const newRoot: ProjectFolder = {
        id: "root",
        name: state.root.name,
        path: "",
        children: [],
        isExpanded: true,
      };
      
      // Build folder structure
      const folderMap = new Map<string, ProjectFolder>();
      folderMap.set("", newRoot);
      
      for (const [path, zipEntry] of Object.entries(zip.files)) {
        if (zipEntry.dir) continue;
        
        const parts = path.split("/");
        const fileName = parts.pop() || "";
        const folderPath = parts.join("/");
        
        // Ensure parent folder exists
        let currentFolder = newRoot;
        let currentPath = "";
        
        for (const part of parts) {
          currentPath = currentPath ? `${currentPath}/${part}` : part;
          
          let folder = folderMap.get(currentPath);
          if (!folder) {
            folder = {
              id: generateId(),
              name: part,
              path: currentPath,
              children: [],
              isExpanded: true,
            };
            folderMap.set(currentPath, folder);
            currentFolder.children.push(folder);
          }
          currentFolder = folder;
        }
        
        // Create file
        const content = await zipEntry.async("string");
        const newFile: ProjectFile = {
          id: generateId(),
          name: fileName,
          path: path,
          content,
          language: getLanguageFromExtension(fileName),
          isModified: false,
        };
        
        currentFolder.children.push(newFile);
      }
      
      setState(prev => ({
        ...prev,
        root: newRoot,
        openTabs: [],
        activeFileId: null,
        isModified: true,
      }));
      
      return true;
    } catch (err) {
      console.error("Failed to import ZIP:", err);
      setError("Failed to import project");
      return false;
    }
  }, [state.root.name]);
  
  const resetProject = useCallback(() => {
    setState(createInitialState(projectId, projectName));
  }, [projectId, projectName]);
  
  // ===== Navigation =====
  
  const getActiveFile = useCallback((): ProjectFile | null => {
    if (!state.activeFileId) return null;
    const item = findItemById(state.root, state.activeFileId);
    return item && isProjectFile(item) ? item : null;
  }, [state.root, state.activeFileId]);
  
  const getFileById = useCallback((fileId: string): ProjectFile | null => {
    const item = findItemById(state.root, fileId);
    return item && isProjectFile(item) ? item : null;
  }, [state.root]);
  
  const getFolderById = useCallback((folderId: string): ProjectFolder | null => {
    const item = findItemById(state.root, folderId);
    return item && isProjectFolder(item) ? item : null;
  }, [state.root]);
  
  // ===== Derived State =====
  
  const modifiedFiles = useMemo(() => {
    return collectAllFiles(state.root).filter(f => f.isModified);
  }, [state.root]);
  
  const openFiles = useMemo(() => {
    return state.openTabs
      .map(tab => getFileById(tab.fileId))
      .filter((f): f is ProjectFile => f !== null);
  }, [state.openTabs, getFileById]);
  
  const hasUnsavedChanges = useMemo(() => {
    return modifiedFiles.length > 0;
  }, [modifiedFiles]);
  
  return {
    state,
    isLoading,
    error,
    createFile,
    createFolder,
    renameItem,
    deleteItem,
    moveItem,
    updateFileContent,
    openFile,
    closeTab,
    closeAllTabs,
    closeOtherTabs,
    setActiveFile,
    reorderTabs,
    updateTabState,
    toggleSplitView,
    setSplitView,
    setSplitFiles,
    setSplitRatio,
    swapSplitPanes,
    saveAllFiles,
    exportAsZip,
    importFromZip,
    resetProject,
    getActiveFile,
    getFileById,
    getFolderById,
    modifiedFiles,
    openFiles,
    hasUnsavedChanges,
  };
}

// ===== Helper Functions =====

function createInitialState(projectId: string, projectName: string): ProjectState {
  return {
    id: projectId,
    name: projectName,
    root: {
      id: "root",
      name: projectName,
      path: "",
      children: [],
      isExpanded: true,
    },
    openTabs: [],
    activeFileId: null,
    lastSavedAt: null,
    isModified: false,
    splitView: {
      enabled: false,
      primaryFileId: null,
      secondaryFileId: null,
      splitRatio: 0.5,
    },
  };
}

function updateAllFilesInTree(root: ProjectFolder, files: ProjectFile[]): ProjectFolder {
  const fileMap = new Map(files.map(f => [f.id, f]));
  
  function updateFolder(folder: ProjectFolder): ProjectFolder {
    return {
      ...folder,
      children: folder.children.map(child => {
        if (isProjectFile(child)) {
          const updated = fileMap.get(child.id);
          return updated || child;
        }
        return updateFolder(child);
      }),
    };
  }
  
  return updateFolder(root);
}

export default useProjectFiles;
