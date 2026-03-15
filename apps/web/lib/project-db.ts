/**
 * Project Database - IndexedDB for multi-file projects
 * 
 * Database: oop-journey-projects
 * Stores:
 *   - projects: Project metadata and structure
 *   - files: Individual file contents
 */

import { openDB, DBSchema, type IDBPDatabase } from 'idb';
import type { ProjectState, ProjectFile, ProjectFolder } from '@/types/project-files';
import { isProjectFile } from '@/types/project-files';

const DB_NAME = 'oop-journey-projects';
const DB_VERSION = 1;

// Database schema definition
interface ProjectDBSchema extends DBSchema {
  projects: {
    key: string;
    value: ProjectState;
  };
  files: {
    key: string;
    value: ProjectFile;
  };
}

let dbPromise: Promise<IDBPDatabase<ProjectDBSchema>> | null = null;

/**
 * Get or create the IndexedDB database instance for projects
 */
export function getProjectDB(): Promise<IDBPDatabase<ProjectDBSchema>> {
  if (!dbPromise) {
    dbPromise = openDB<ProjectDBSchema>(DB_NAME, DB_VERSION, {
      upgrade(db) {
        // Projects store
        if (!db.objectStoreNames.contains('projects')) {
          db.createObjectStore('projects', { keyPath: 'id' });
        }
        
        // Files store
        if (!db.objectStoreNames.contains('files')) {
          db.createObjectStore('files', { keyPath: 'id' });
        }
      },
    });
  }
  return dbPromise;
}

/**
 * Close the database connection
 */
export async function closeProjectDB(): Promise<void> {
  if (dbPromise) {
    const db = await dbPromise;
    db.close();
    dbPromise = null;
  }
}

/**
 * Delete the entire project database
 */
export async function deleteProjectDatabase(): Promise<void> {
  await closeProjectDB();
  const { deleteDB } = await import('idb');
  await deleteDB(DB_NAME);
}

// ==================== Project Operations ====================

/**
 * Save a project to the database
 */
export async function saveProject(project: ProjectState): Promise<void> {
  const db = await getProjectDB();
  await db.put('projects', project);
}

/**
 * Get a project by ID
 */
export async function getProject(projectId: string): Promise<ProjectState | undefined> {
  const db = await getProjectDB();
  return db.get('projects', projectId);
}

/**
 * Get all projects
 */
export async function getAllProjects(): Promise<ProjectState[]> {
  const db = await getProjectDB();
  return db.getAll('projects');
}

/**
 * Delete a project
 */
export async function deleteProject(projectId: string): Promise<void> {
  const db = await getProjectDB();
  await db.delete('projects', projectId);
  
  // TODO: Also delete all associated files
  // Files don't have projectId in current schema, 
  // so we'd need to track which files belong to which project
  // For now, we skip this cleanup
}

/**
 * Check if a project exists
 */
export async function projectExists(projectId: string): Promise<boolean> {
  const db = await getProjectDB();
  const project = await db.get('projects', projectId);
  return project !== undefined;
}

// ==================== File Operations ====================

/**
 * Save a file to the database
 */
export async function saveFile(file: ProjectFile): Promise<void> {
  const db = await getProjectDB();
  await db.put('files', file);
}

/**
 * Save multiple files to the database
 */
export async function saveFiles(files: ProjectFile[]): Promise<void> {
  const db = await getProjectDB();
  const tx = db.transaction('files', 'readwrite');
  for (const file of files) {
    await tx.store.put(file);
  }
  await tx.done;
}

/**
 * Get a file by ID
 */
export async function getFile(fileId: string): Promise<ProjectFile | undefined> {
  const db = await getProjectDB();
  return db.get('files', fileId);
}

/**
 * Get multiple files by IDs
 */
export async function getFiles(fileIds: string[]): Promise<ProjectFile[]> {
  const db = await getProjectDB();
  const files: ProjectFile[] = [];
  for (const id of fileIds) {
    const file = await db.get('files', id);
    if (file) files.push(file);
  }
  return files;
}

/**
 * Delete a file
 */
export async function deleteFile(fileId: string): Promise<void> {
  const db = await getProjectDB();
  await db.delete('files', fileId);
}

/**
 * Delete multiple files
 */
export async function deleteFiles(fileIds: string[]): Promise<void> {
  const db = await getProjectDB();
  const tx = db.transaction('files', 'readwrite');
  for (const id of fileIds) {
    await tx.store.delete(id);
  }
  await tx.done;
}

// ==================== Import/Export ====================

/**
 * Export a project as a JSON object
 */
export async function exportProject(projectId: string): Promise<{
  project: ProjectState;
  files: ProjectFile[];
  exportedAt: string;
} | null> {
  const project = await getProject(projectId);
  if (!project) return null;
  
  // Collect all file IDs from the project tree
  const fileIds: string[] = [];
  function collectFiles(folder: ProjectFolder) {
    for (const child of folder.children) {
      if (isProjectFile(child)) {
        if (child.id) fileIds.push(child.id);
      } else {
        collectFiles(child);
      }
    }
  }
  collectFiles(project.root);
  
  const files = await getFiles(fileIds);
  
  return {
    project,
    files,
    exportedAt: new Date().toISOString(),
  };
}

/**
 * Import a project from a JSON object
 */
export async function importProject(data: {
  project: ProjectState;
  files: ProjectFile[];
}): Promise<void> {
  const db = await getProjectDB();
  
  const tx = db.transaction(['projects', 'files'], 'readwrite');
  
  // Save project
  await tx.objectStore('projects').put(data.project);
  
  // Save files
  for (const file of data.files) {
    await tx.objectStore('files').put(file);
  }
  
  await tx.done;
}

// ==================== Utility ====================

/**
 * Get database statistics
 */
export async function getProjectDBStats(): Promise<{
  projectCount: number;
  fileCount: number;
}> {
  const db = await getProjectDB();
  const projectCount = await db.count('projects');
  const fileCount = await db.count('files');
  
  return { projectCount, fileCount };
}

/**
 * Clear all project data
 */
export async function clearAllProjects(): Promise<void> {
  const db = await getProjectDB();
  const tx = db.transaction(['projects', 'files'], 'readwrite');
  await tx.objectStore('projects').clear();
  await tx.objectStore('files').clear();
  await tx.done;
}

export default {
  getProjectDB,
  closeProjectDB,
  deleteProjectDatabase,
  // Projects
  saveProject,
  getProject,
  getAllProjects,
  deleteProject,
  projectExists,
  // Files
  saveFile,
  saveFiles,
  getFile,
  getFiles,
  deleteFile,
  deleteFiles,
  // Import/Export
  exportProject,
  importProject,
  // Utility
  getProjectDBStats,
  clearAllProjects,
};
