/**
 * Project File System Types
 * 
 * Type definitions for the multi-file editing system.
 */

/** Represents a file in the project */
export interface ProjectFile {
  id?: string;
  name?: string;
  path: string;
  content?: string;
  language?: string;
  isModified?: boolean;
  isReadOnly?: boolean;
  readOnly?: boolean;
  lastModified?: number;
  template?: string;
  isEntryPoint?: boolean;
}

/** Represents a folder in the project */
export interface ProjectFolder {
  id: string;
  name: string;
  path: string;
  children: (ProjectFile | ProjectFolder)[];
  isExpanded?: boolean;
}

/** Union type for file system items */
export type ProjectItem = ProjectFile | ProjectFolder;

/** Check if an item is a file */
export function isProjectFile(item: ProjectItem): item is ProjectFile {
  return 'content' in item;
}

/** Check if an item is a folder */
export function isProjectFolder(item: ProjectItem): item is ProjectFolder {
  return 'children' in item;
}

/** Open file tab state */
export interface OpenTab {
  fileId: string;
  isActive: boolean;
  cursorPosition?: {
    lineNumber: number;
    column: number;
  };
  scrollPosition?: {
    scrollTop: number;
    scrollLeft: number;
  };
}

/** Project state */
export interface ProjectState {
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
    splitRatio: number; // 0.3 to 0.7
  };
}

/** File operation result */
export interface FileOperationResult {
  success: boolean;
  error?: string;
  item?: ProjectItem;
}

/** Language detection from file extension */
export const LANGUAGE_MAP: Record<string, string> = {
  // Python
  py: 'python',
  pyw: 'python',
  pyi: 'python',
  // JavaScript/TypeScript
  js: 'javascript',
  jsx: 'javascript',
  ts: 'typescript',
  tsx: 'typescript',
  mjs: 'javascript',
  cjs: 'javascript',
  // Web
  html: 'html',
  htm: 'html',
  css: 'css',
  scss: 'scss',
  sass: 'sass',
  less: 'less',
  json: 'json',
  // Data
  yaml: 'yaml',
  yml: 'yaml',
  xml: 'xml',
  csv: 'csv',
  // Markdown
  md: 'markdown',
  mdx: 'markdown',
  // Config
  toml: 'toml',
  ini: 'ini',
  cfg: 'ini',
  env: 'plaintext',
  gitignore: 'plaintext',
  dockerfile: 'dockerfile',
  // Shell
  sh: 'shell',
  bash: 'shell',
  zsh: 'shell',
  ps1: 'powershell',
  bat: 'bat',
  cmd: 'bat',
  // SQL
  sql: 'sql',
  // Other
  txt: 'plaintext',
  log: 'log',
  lock: 'plaintext',
};

/** Get language from file extension */
export function getLanguageFromExtension(filename: string): string {
  const ext = filename.split('.').pop()?.toLowerCase() || '';
  const baseName = filename.toLowerCase();
  
  // Handle special filenames like Dockerfile, .gitignore, etc.
  if (baseName === 'dockerfile') return 'dockerfile';
  if (baseName === 'makefile') return 'makefile';
  if (baseName.startsWith('.env')) return 'plaintext';
  
  return LANGUAGE_MAP[ext] || 'plaintext';
}

/** Get icon type from file extension */
export function getFileIconType(filename: string): string {
  const ext = filename.split('.').pop()?.toLowerCase() || '';
  const baseName = filename.toLowerCase();
  
  // Python
  if (['py', 'pyw', 'pyi'].includes(ext)) return 'python';
  
  // JavaScript/TypeScript
  if (['js', 'jsx', 'mjs', 'cjs'].includes(ext)) return 'javascript';
  if (['ts', 'tsx'].includes(ext)) return 'typescript';
  
  // Web
  if (['html', 'htm'].includes(ext)) return 'html';
  if (['css', 'scss', 'sass', 'less'].includes(ext)) return 'css';
  if (ext === 'json') return 'json';
  
  // Config
  if (['yaml', 'yml'].includes(ext)) return 'yaml';
  if (['xml', 'svg'].includes(ext)) return 'xml';
  if (ext === 'md' || ext === 'mdx') return 'markdown';
  if (baseName === 'dockerfile') return 'docker';
  if (baseName === 'makefile') return 'settings';
  if (['toml', 'ini', 'cfg'].includes(ext)) return 'settings';
  if (baseName === '.gitignore') return 'git';
  if (['sh', 'bash', 'zsh'].includes(ext)) return 'terminal';
  if (['ps1', 'bat', 'cmd'].includes(ext)) return 'terminal';
  
  // Data
  if (['sql', 'sqlite'].includes(ext)) return 'database';
  if (['csv', 'tsv'].includes(ext)) return 'table';
  
  // Images
  if (['png', 'jpg', 'jpeg', 'gif', 'svg', 'ico', 'webp'].includes(ext)) return 'image';
  
  // Archives
  if (['zip', 'tar', 'gz', 'rar', '7z'].includes(ext)) return 'archive';
  
  // Default
  return 'file';
}

/** Default starter code for different languages */
export const DEFAULT_STARTER_CODE: Record<string, string> = {
  python: '# Welcome to your new Python file!\n\ndef main():\n    pass\n\nif __name__ == "__main__":\n    main()',
  javascript: '// Welcome to your new JavaScript file!\n\nfunction main() {\n    console.log("Hello, World!");\n}\n\nmain();',
  typescript: '// Welcome to your new TypeScript file!\n\nfunction main(): void {\n    console.log("Hello, World!");\n}\n\nmain();',
  html: '<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>Document</title>\n</head>\n<body>\n    \n</body>\n</html>',
  css: '/* Welcome to your new CSS file! */\n\n* {\n    margin: 0;\n    padding: 0;\n    box-sizing: border-box;\n}',
  json: '{\n    "name": "new-file",\n    "version": "1.0.0"\n}',
  plaintext: '',
};

/** Get starter code for a file */
export function getStarterCode(language: string): string {
  return DEFAULT_STARTER_CODE[language] || '';
}
