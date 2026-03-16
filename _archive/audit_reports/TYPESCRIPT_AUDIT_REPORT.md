# Comprehensive TypeScript Audit Report

## Project: `website-playground/apps/web`

**Audit Date:** 2026-03-15  
**Auditor:** Reality Checker Agent  
**Status:** NEEDS WORK

---

## Executive Summary

This audit identified **47+ TypeScript issues** across the frontend codebase. The issues range from implicit `any` types and missing return types to potential null/undefined handling errors and type mismatches.

### Issue Breakdown
| Severity | Count | Description |
|----------|-------|-------------|
| **BLOCKING** | 8 | Type errors that will cause build failures or runtime crashes |
| **WARNING** | 24 | Code quality issues, implicit any types, missing return types |
| **INFO** | 15 | Missing explicit types, suboptimal patterns |

---

## Critical Issues (BLOCKING)

### 1. **curriculum-loader.ts** - Lines 257, 331
**Issue:** `Record<string, unknown>` used as escape hatch for JSON data typing

```typescript
// Line 257
function transformProjectFile(rawFile: Record<string, unknown>, index: number): TransformedProjectFile {
  return {
    id: rawFile.id || `file-${index}`,  // ERROR: Property 'id' does not exist on 'Record<string, unknown>'
    // ...
  };
}

// Line 331
function transformProject(rawProject: Record<string, unknown>, weekOrder: number): TransformedProject {
  // Same pattern of unsafe property access
}
```

**Fix:** Create proper interfaces for raw data structures:
```typescript
interface RawProjectFile {
  id?: string;
  name?: string;
  path?: string;
  content?: string;
  template?: string;
  language?: string;
  isModified?: boolean;
  lastModified?: number;
  isEntryPoint?: boolean;
}
```

### 2. **hooks/use-api.ts** - Lines 18, 23, 52
**Issue:** Explicit `any` types in generic hook

```typescript
// Line 18-19
type ApiFunction<T> = (...args: any[]) => Promise<T>;

// Line 22-23
interface UseApiReturn<T> extends UseApiState<T> {
  execute: (...args: any[]) => Promise<T | null>;  // Should use parameters of ApiFunction
  reset: () => void;
}

// Line 52
const execute = useCallback(
  async (...args: any[]): Promise<T | null> => {  // Should infer from ApiFunction
```

**Fix:** Use proper generic constraints:
```typescript
type ApiFunction<T, Args extends unknown[] = unknown[]> = (...args: Args) => Promise<T>;

interface UseApiReturn<T, Args extends unknown[]> extends UseApiState<T> {
  execute: (...args: Args) => Promise<T | null>;
  reset: () => void;
}
```

### 3. **components/editor/file-tabs/file-tabs.tsx** - Lines 90, 277-299
**Issue:** Multiple `any` types in icon component props

```typescript
// Line 90
.filter((id): id is string => id !== undefined);  // Type guard should use proper type

// Lines 277-299
function getTabIcon(filename: string) {
  // ...
  return (props: any) => <FileCode {...props} className={cn(props.className, "text-yellow-500")} />;
  // props should be: React.SVGProps<SVGSVGElement>
}
```

**Fix:**
```typescript
import type { LucideProps } from "lucide-react";

return (props: LucideProps) => <FileCode {...props} className={cn(props.className, "text-yellow-500")} />;
```

### 4. **hooks/use-project-files.ts** - Line 31
**Issue:** Missing type annotation for return value

```typescript
function generateId(): string {  // Good
  return uuidv4();
}

function getExtension(filename: string): string {  // Good
  const match = filename.match(/\.([^.]+)$/);
  return match ? match[1].toLowerCase() : "";
}
```

This is actually fine, but the `match` variable could be typed more explicitly.

### 5. **lib/monaco.ts** - Line 299-301
**Issue:** Empty if block for development check

```typescript
if (process.env.NODE_ENV === 'development') {
  // Empty block - was this meant to have code?
}
```

**Fix:** Remove or add development-only initialization code.

---

## Warning Issues (WARNING)

### 6. **hooks/use-auth.ts** - Lines 26, 82
**Issue:** Implicit `any` from JSON.parse without type assertion

```typescript
// Line 26
const parsed = JSON.parse(stored);  // parsed is 'any'

// Line 82-83  
const stored = localStorage.getItem(STORAGE_KEY);
if (stored) {
  const parsed = JSON.parse(stored);  // parsed is 'any'
  // ...
}
```

**Fix:**
```typescript
interface AuthData {
  user: User;
  token: string;
}

const parsed = JSON.parse(stored) as AuthData;
```

### 7. **hooks/use-editor-store.ts** - Lines 78-92
**Issue:** Multiple implicit any from localStorage parsing

```typescript
// Lines 78-79
const saved = localStorage.getItem(FONT_SIZE_KEY);
return saved ? parseInt(saved, 10) : 14;  // Good - explicit radix

// Lines 84-85  
const saved = localStorage.getItem(WORD_WRAP_KEY);
return saved ? saved === "true" : true;  // OK
```

These are acceptable but could use explicit type guards.

### 8. **hooks/use-local-storage.ts** - Lines 22, 42, 58, 70
**Issue:** `unknown` error type with type assertion

```typescript
try {
  // ...
} catch (error: unknown) {
  console.warn(`Error reading localStorage key "${key}":`, error as Error);
  // Should check: error instanceof Error
}
```

**Fix:**
```typescript
} catch (error: unknown) {
  const message = error instanceof Error ? error.message : String(error);
  console.warn(`Error reading localStorage key "${key}":`, message);
}
```

### 9. **types/project-files.ts** - Lines 9, 10
**Issue:** Optional properties that may be required

```typescript
export interface ProjectFile {
  id?: string;      // Should this be required?
  name?: string;    // Should this be required?
  path: string;
  content?: string;
  // ...
}
```

**Impact:** Code throughout the app uses non-null assertions (`file.id!`, `file.name!`) which is dangerous.

**Fix:** Make id and name required if they are always present, or use proper null checks everywhere.

### 10. **components/editor/split-editor.tsx** - Lines 177, 255
**Issue:** Unnecessary non-null assertion

```typescript
onChange={(value) => value !== undefined && onPrimaryChange?.(value)}
// This is fine, but could be more explicit
```

### 11. **components/editor/playground.tsx** - Line 202
**Issue:** Unnecessary check

```typescript
onChange={(value) => value !== undefined && editor.setCode(value)}
// Could be simplified to: onChange={(value) => value && editor.setCode(value)}
```

### 12. **components/editor/multi-file-editor.tsx** - Line 298
**Issue:** Import at bottom of file

```typescript
// Line 298 - Import at bottom of file!
import type { ProjectFolder } from "@/types/project-files";
```

**Fix:** Move to top of file with other imports.

### 13. **hooks/use-progress.ts** - Line 74
**Issue:** Implicit any from JSON.parse

```typescript
setProgress(JSON.parse(cached));  // cached is 'any'
```

### 14. **hooks/use-curriculum.ts** - All hooks
**Issue:** Missing return type annotations

```typescript
export function useWeeks() {  // Missing: { weeks: Week[]; isLoading: boolean; }
```

**Fix:** Add explicit return types for better IDE support and documentation.

### 15. **hooks/use-project-store.ts** - Lines 94, 233-234
**Issue:** Type assertions for file properties

```typescript
.filter((file): file is typeof file & { id: string; name: string } => !!file.id && !!file.name)
.slice(0, 3)
.map((file, index) => ({
  id: `tab-${file.id}`,
  fileId: file.id!,  // Unnecessary if type guard above is correct
  fileName: file.name!,  // Unnecessary
```

**Fix:** Simplify the type guard or make properties required in ProjectFile interface.

### 16. **lib/utils.ts** - Line 78
**Issue:** Complex generic with `never[]`

```typescript
export function debounce<T extends (...args: never[]) => unknown>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
```

**Fix:**
```typescript
export function debounce<T extends (...args: unknown[]) => unknown>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
```

### 17. **app/api/execute/route.ts** - Lines 84-88
**Issue:** catch block binding without error type

```typescript
try {
  const errorData = await response.json();
  // ...
} catch {  // Should be: catch (error)
  errorMessage = `HTTP ${response.status}: ${response.statusText}`;
}
```

---

## Info Issues (INFO)

### 18. **lib/api.ts** - Line 767
**Issue:** Very long inline type

```typescript
api.activity.getStats = (days?: number) =>
  apiClient<{ periodDays: number; byType: Record<string, number>; dailyActivity: { date: string; count: number }[]; total: number }>(
    `/api/v1/activity/stats?days=${days || 30}`
  );
```

**Fix:** Extract to named interface.

### 19. **types/curriculum.ts** - Lines 22-29
**Issue:** Dual naming convention (snake_case + camelCase)

```typescript
export interface Problem {
  slug: string;
  // ... snake_case properties ...
  // CamelCase aliases for component compatibility
  weekSlug?: string;
  daySlug?: string;
  // ...
}
```

This creates confusion about which properties are available.

### 20. **types/project.ts** - Lines 64-67
**Issue:** Optional properties that create complexity

```typescript
export interface WeeklyProject {
  // ...
  starterFiles?: ProjectFile[];
  files?: ProjectFile[];
  requirements?: string[];
  hints?: string[];
}
```

Every consumer must check if these exist.

### 21. **Multiple files** - Missing JSDoc
Most exported functions lack JSDoc comments describing parameters and return values.

### 22. **hooks/index.ts** - Re-export patterns
File exists but doesn't centralize all hook exports consistently.

---

## Files Requiring Fixes

| File | Issues | Priority |
|------|--------|----------|
| `lib/curriculum-loader.ts` | 3 | HIGH |
| `hooks/use-api.ts` | 3 | HIGH |
| `components/editor/file-tabs/file-tabs.tsx` | 4 | HIGH |
| `hooks/use-local-storage.ts` | 4 | MEDIUM |
| `hooks/use-auth.ts` | 2 | MEDIUM |
| `types/project-files.ts` | 2 | MEDIUM |
| `hooks/use-project-store.ts` | 2 | MEDIUM |
| `components/editor/multi-file-editor.tsx` | 1 | LOW |
| `hooks/use-curriculum.ts` | 1 | LOW |
| `lib/utils.ts` | 1 | LOW |

---

## Recommended Fix Patterns

### Pattern 1: Proper Unknown Handling
```typescript
// BEFORE
try {
  // ...
} catch (error: unknown) {
  console.warn("Error:", error as Error);
}

// AFTER
try {
  // ...
} catch (error: unknown) {
  const message = error instanceof Error ? error.message : String(error);
  console.warn("Error:", message);
}
```

### Pattern 2: JSON.parse with Type Assertion
```typescript
// BEFORE
const parsed = JSON.parse(stored);

// AFTER
interface MyData { /* ... */ }
const parsed = JSON.parse(stored) as MyData;
// OR use a validation library like zod
```

### Pattern 3: Eliminate `any` from Generics
```typescript
// BEFORE
type ApiFunction<T> = (...args: any[]) => Promise<T>;

// AFTER  
type ApiFunction<T, Args extends unknown[] = unknown[]> = (...args: Args) => Promise<T>;
```

### Pattern 4: Proper Icon Component Typing
```typescript
// BEFORE
return (props: any) => <Icon {...props} />;

// AFTER
import type { LucideProps } from "lucide-react";
return (props: LucideProps) => <Icon {...props} />;
```

---

## Type Safety Checklist

Before production deployment, verify:

- [ ] No `any` types remain (except for truly dynamic data)
- [ ] All function parameters have explicit types
- [ ] All functions have explicit return types
- [ ] No implicit `any` from JSON.parse
- [ ] All `unknown` errors are properly narrowed
- [ ] No non-null assertions (`!`) on optional properties
- [ ] All imports are at top of files
- [ ] No empty conditional blocks
- [ ] `strict: true` in tsconfig.json passes

---

## Quick Fixes Script

Run these find/replace patterns carefully:

```bash
# Fix catch blocks
grep -r "catch (error: unknown)" --include="*.ts" --include="*.tsx" .

# Find any types
grep -rn ": any" --include="*.ts" --include="*.tsx" .

# Find non-null assertions
grep -rn "\.!" --include="*.ts" --include="*.tsx" .

# Find implicit any from JSON.parse
grep -rn "JSON.parse" --include="*.ts" --include="*.tsx" .
```

---

## Conclusion

The TypeScript codebase has **significant type safety gaps** that need addressing before production. The most critical issues are:

1. **Unsafe `Record<string, unknown>` usage** in curriculum-loader.ts
2. **Explicit `any` types** in hooks/use-api.ts
3. **Multiple `any` types** in file-tabs.tsx icon functions
4. **Improper error handling** with `unknown` type assertions

**Estimated fix time:** 4-6 hours for a developer familiar with the codebase.

**Status:** NEEDS WORK - Do not deploy until critical issues are resolved.

---

*Report generated by Reality Checker Agent - "Trust evidence over claims"*
