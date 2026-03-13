# Deployment Mistakes & Learnings Log

> This file tracks all TypeScript/build errors encountered during deployment and their solutions.
> Refer to this before making fixes to avoid repeating mistakes.

---

## Last Updated: 2026-03-14

---

## 📋 Common Error Patterns

### Pattern 1: Optional Property Access
**Error:** `Type 'string | undefined' is not assignable to parameter of type 'string'`

**Variation:** `Type 'string | undefined' is not assignable to type 'string | null'`
- State expects `string | null` but optional property gives `string | undefined`

**Root Cause:** Accessing optional properties (`id?: string`, `name?: string`) without null checks.

**Files Affected:**
- `components/editor/file-tabs/file-tabs.tsx`
- `components/editor/file-tree/file-tree.tsx` (dragState setters - use `?? null`)
- `components/editor/file-tree/file-tree-item.tsx`
- `components/editor/file-tree/file-tree-context-menu.tsx`
- `components/editor/multi-file-editor.tsx`
- `components/projects/file-tree.tsx`

**Solution Patterns:**

```typescript
// ❌ BAD - Direct access
onSelect(tab.file.id)
return a.name.localeCompare(b.name)

// ✅ GOOD - Nullish coalescing
onSelect(tab.file.id ?? '')
return (a.name ?? '').localeCompare(b.name ?? '')

// ✅ GOOD - Convert undefined to null for state
setDragState(prev => ({ ...prev, draggingId: item.id ?? null }))

// ✅ GOOD - Optional chaining with guard
if (activeTab?.file.id) onCloseOthers(activeTab.file.id)

// ✅ GOOD - Filter before map
tabs.filter(tab => tab.file.id).map(tab => ...)

// ✅ GOOD - Fallback chain
const folderId = item ? (isFolder ? (item.id ?? parentFolderId ?? "root") : (parentFolderId ?? "root")) : "root";
```

---

### Pattern 2: Type Cast Errors
**Error:** `Conversion of type 'X' to type 'Y' may be a mistake`

**Example:**
```typescript
// ❌ BAD - Wrong type cast
(item as ReturnType<typeof isProjectFile>).isModified

// ✅ GOOD - Cast to actual type
(item as ProjectFile).isModified
```

---

### Pattern 3: Function Return Type Mismatch
**Error:** `Type '(value: string) => void' is not assignable to type '(value: string | undefined) => void'`

**Root Cause:** Monaco Editor's OnChange returns `string | undefined`, but handlers expect `string`.

**Solution:**
```typescript
// ❌ BAD - Type mismatch
onChange={setCode}

// ✅ GOOD - Handle undefined
onChange={(value) => value !== undefined && setCode(value)}
```

---

### Pattern 4: Array Type Mismatch
**Error:** `Type '(string | undefined)[]' is not assignable to parameter of type 'string[]'`

**Example:**
```typescript
// ❌ BAD - Array with possible undefined values
const newOrder = tabs.map(t => t.file.id)

// ✅ GOOD - Filter undefined values
const newOrder = tabs.map(t => t.file.id).filter((id): id is string => id !== undefined)
```

---

### Pattern 5: Syntax Errors from Copy-Paste
**Error:** `Unexpected token 'div'. Expected jsx identifier` or similar syntax errors

**Root Cause:** Broken object literals during edits.

**Example:**
```typescript
// ❌ BROKEN - Stray braces
id: isFile ? file.id : `${current.id}/${part}`}, {
name: part,

// ✅ FIXED - Proper syntax
id: isFile ? file.id : `${current.id}/${part}`,
name: part,
```

---

## 📋 Pattern 9: Missing Required Props / Wrong Prop Types
**Error:** `Type '{}' is missing the following properties from type 'XProps': prop1, prop2`  
**OR:** `Property 'X' does not exist on type 'Y'`

**Root Cause:** Component requires props but none were provided, or wrong props were passed.

**Example 1 - Missing Props:**
```typescript
// ❌ BAD - Missing required props
<HeroSection />

// ✅ GOOD - Provide all required props
<HeroSection data={mockData} overallProgress={overallProgress} />
```

**Example 2 - Wrong Props:**
```typescript
// ❌ BAD - Wrong prop names
interface Props { week: WeekProgress }
<ProgressCard weekNumber={1} weekTitle="Week 1" />

// ✅ GOOD - Pass correct object
<ProgressCard week={mockWeek} />
```

**Example 3 - Missing Required Sub-Props:**
```typescript
// ❌ BAD - Missing trend.label and icon
<StatCard title="Solved" value={42} trend={{ value: 12, positive: true }} />

// ✅ GOOD - Include all required props
<StatCard 
  title="Solved" 
  value={42} 
  icon={CheckCircle}
  trend={{ value: 12, label: '+12%', positive: true }} 
/>
```

**Files Affected:**
- `components/dashboard/dashboard.tsx` - Missing props for HeroSection
- `components/dashboard/dashboard.tsx` - Wrong props for ProgressCard

---

## 📋 Pattern 8: Missing Component Export
**Error:** `Property 'X' does not exist on type 'typeof import("...")'`

**Root Cause:** A lazy-loaded component tries to import something that isn't exported from the module.

**Example:**
```typescript
// ❌ BAD - Importing non-existent export
export const LazyDashboard = dynamic(
  () => import("@/components/dashboard").then((mod) => ({ default: mod.Dashboard })),
);
// But Dashboard is not exported from components/dashboard/index.ts

// ✅ GOOD - Create and export the component
// components/dashboard/dashboard.tsx
export function Dashboard() { ... }

// components/dashboard/index.ts
export { Dashboard } from './dashboard';
```

**Files Affected:**
- `components/dashboard/index.ts` - Missing Dashboard export
- `components/lazy-components.tsx` - Tries to lazy-load Dashboard

---

## 📋 Pattern 7: JSON Import Type Mismatch
**Error:** `Type 'string' is not assignable to type '"week" | "day" | "problem" | ...'`

**Root Cause:** When importing JSON files, TypeScript infers string fields as `string` type, not as specific string literals.

**Example:**
```typescript
// ❌ BAD - Type inferred as string
import searchIndex from "@/data/search-index.json";
// searchIndex[0].type is inferred as 'string'

// ✅ GOOD - Type assertion
import searchIndexRaw from "@/data/search-index.json";
import type { SearchIndexItem } from "@/lib/search";
const searchIndex = searchIndexRaw as SearchIndexItem[];
```

**Files Affected:**
- `components/layout/client-layout.tsx` - search-index.json import

---

## 📋 Pattern 6: Missing Module Import
**Error:** `Cannot find module '@/components/ui/use-toast' or its corresponding type declarations`

**Root Cause:** Code imports from a file that doesn't exist.

**Files Affected:**
- `components/editor/post-solve-recommendations.tsx`
- `components/notifications/smart-notifications.tsx`

**Solution:**
Create the missing module with compatible API:

```typescript
// components/ui/use-toast.ts
'use client';

import { toast as sonnerToast } from 'sonner';
import { ReactNode } from 'react';

interface ToastOptions {
  title?: string | ReactNode;
  description?: string;
  variant?: 'default' | 'destructive';
  duration?: number;
}

export function useToast() {
  const toast = (options: ToastOptions) => {
    // Map to Sonner's API
    if (options.variant === 'destructive') {
      sonnerToast.error(options.title as string, {
        description: options.description,
      });
    } else {
      sonnerToast.success(options.title as string, {
        description: options.description,
      });
    }
  };

  return { toast };
}
```

**Note:** This project uses Sonner for toasts, but some components expect a custom `useToast` hook.

---

## 🚫 Anti-Patterns to Avoid

### Anti-Pattern 1: Changing Type Definitions
**NEVER do this:**
```typescript
// ❌ DON'T CHANGE TYPE DEFINITIONS
export interface ProjectFile {
  id: string;      // was optional, made required
  name: string;    // was optional, made required
}
```

**Why it fails:** Creates cascade of errors across all files creating ProjectFile objects.

**Instead:** Add null checks at usage sites.

---

### Anti-Pattern 2: Fix-One-File-At-A-Time
**NEVER do this:**
- Fix one file
- Commit
- Deploy
- Fix next error in different file

**Why it fails:** Same pattern exists in multiple files, causing 10+ deploy cycles.

**Instead:** Search for pattern across all files and fix together.

---

### Anti-Pattern 3: Assuming Props Are Always Defined
**NEVER do this:**
```typescript
// ❌ DON'T ASSUME
{activeTab.file.id}  // activeTab might be undefined
{item.name}          // name might be undefined
```

**Instead:** Always use guards or fallbacks.

---

### Anti-Pattern 4: Losing Fixes in Reverts
**What happens:** When reverting type changes, null check fixes also get reverted.

**Example:**
```typescript
// Fix added:
if (file.id) project.openFile(file.id);

// Later reverted back to:
project.openFile(file.id);  // Error returns!
```

**Files most affected:**
- `components/editor/multi-file-editor.tsx` - Multiple `.id` accesses lost
  - Line 109: `dialogState.item.id` ✓ fixed
  - Line 120: `dialogState.item.id` ✓ fixed  
  - Line 126: `file.id` ✓ fixed (was lost, fixed again)
  - Line 161: `activeFile.id` ✓ fixed (was lost, fixed again)
- `components/editor/rename-dialog.tsx` - `.name` access lost
  - Line 42: `item.name` ✓ fixed (was lost, fixed again)
  - Line 51: `item.name` ✓ fixed (was lost, fixed again)

**Prevention:**
- After any revert, re-scan previously fixed files
- Keep fixes minimal and separate from type changes
- Use `git diff` to verify fixes are still in place
- Check ALL lines with the pattern, not just the first one found

---

### Anti-Pattern 5: Not Fixing All Instances (Rule 2 Violation)
**What happened:** Pattern 8 (Missing Component Export) appeared in 3 files but was fixed one at a time over multiple deploy cycles.

**Timeline of failures:**
1. Deploy failed: `Dashboard` not exported → Fixed `dashboard/index.ts`
2. Deploy failed: `CurriculumNav` not exported → Fixed `curriculum/index.ts`  
3. Deploy failed: `SearchDialog` not exported → Fixed `search/index.ts`

**Root cause:** `lazy-components.tsx` imports from all 3 modules:
```typescript
export const LazyDashboard = dynamic(() => import("@/components/dashboard")...);
export const LazyCurriculumNav = dynamic(() => import("@/components/curriculum")...);
export const LazySearchDialog = dynamic(() => import("@/components/search")...);
```

**Should have done in ONE commit:**
1. Check what `lazy-components.tsx` imports from each module
2. Create all missing components
3. Export all from index.ts files
4. Deploy once

**Lesson:** When fixing "missing export" errors, always check what OTHER exports the importer expects from related modules.

---

## ✅ Correct Fix Checklist

Before committing a fix, verify:

- [ ] Are there 3+ files with this same pattern? (Search with grep)
- [ ] Did I add proper fallbacks (`?? ''`, `?? 'unnamed'`, `|| false`)?
- [ ] Did I add guards where needed (`if (x)`, `?.`, `&&`)?
- [ ] Did I check for syntax errors (missing `}`, extra `,`)?
- [ ] Did I verify the type is not being changed (just the usage)?
- [ ] After any revert, re-check previously fixed files

---

## 🔍 Search Patterns for Common Issues

```bash
# Find all optional property accesses
grep -r "file\.id\b" --include="*.tsx" .
grep -r "file\.name\b" --include="*.tsx" .
grep -r "item\.id\b" --include="*.tsx" .
grep -r "item\.name\b" --include="*.tsx" .
grep -r "tab\.file\." --include="*.tsx" .

# Find all localeCompare (sorting by name)
grep -r "localeCompare" --include="*.tsx" .

# Find all type casts
grep -r "as ProjectFile" --include="*.tsx" .
grep -r "as ProjectItem" --include="*.tsx" .

# Find ProjectFile object creation
grep -r ": ProjectFile = {" --include="*.tsx" .
grep -r "as ProjectFile" --include="*.tsx" .
```

---

## 📁 Files That Commonly Have Issues

1. **`components/editor/file-tabs/file-tabs.tsx`**
   - `tab.file.id` access
   - `tab.file.name` display
   - Drag/drop handlers

2. **`components/editor/file-tree/file-tree.tsx`**
   - `item.id` in sorting
   - `item.name` in display
   - `child.id` in recursion

3. **`components/editor/file-tree/file-tree-item.tsx`**
   - `item.name` display
   - `item.id` in drag data

4. **`components/editor/file-tree/file-tree-context-menu.tsx`**
   - `folderId` calculation
   - `item.id` access

5. **`components/editor/multi-file-editor.tsx`**
   - `dialogState.item.id` access
   - `file.id` access

6. **`components/projects/file-tree.tsx`**
   - `file.id` in tree building
   - `file.name` display

7. **`app/projects/[projectSlug]/page.tsx`**
   - `generateDefaultFiles()` - must include all required fields
   - `file.id`, `file.name` access

---

## 🎯 Key Insights

1. **`ProjectFile.id` and `ProjectFile.name` are OPTIONAL** - always handle undefined
2. **`ProjectFolder.id` and `ProjectFolder.name` are REQUIRED** - but be careful with union types
3. **Always provide fallbacks for display** - `name ?? 'unnamed'`, `id ?? ''`
4. **Always guard function calls** - `if (file.id) onSelect(file.id)`
5. **Filter before mapping** - `tabs.filter(t => t.file.id).map(...)`

---

## 📚 Related Type Definitions

### ProjectFile (types/project-files.ts)
```typescript
export interface ProjectFile {
  id?: string;           // OPTIONAL - always check
  name?: string;         // OPTIONAL - always check
  path: string;          // REQUIRED
  content?: string;
  language?: string;
  isModified?: boolean;
  isReadOnly?: boolean;
  // ...
}
```

### ProjectFolder (types/project-files.ts)
```typescript
export interface ProjectFolder {
  id: string;            // REQUIRED
  name: string;          // REQUIRED
  path: string;
  children: (ProjectFile | ProjectFolder)[];
  // ...
}
```

### ProjectItem
```typescript
type ProjectItem = ProjectFile | ProjectFolder;
// Must check which one before accessing id/name
```

---

## 📝 Template for New Entries

```markdown
### Pattern N: [Error Name]
**Error:** [Full error message]

**Root Cause:** [Why it happens]

**Files Affected:**
- [file path]

**Solution:**
```typescript
// ❌ BAD
[bad code]

// ✅ GOOD
[good code]
```

**Added:** [Date]
```

---

*Remember: Always check this file before fixing new errors!*
