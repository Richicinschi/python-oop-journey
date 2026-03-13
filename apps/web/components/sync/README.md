# Sync Components

Components for managing offline/sync functionality in Python OOP Journey.

## Components

### SyncStatus

Small indicator in the header showing current sync state:
- **Synced**: All changes saved to server
- **Syncing**: Currently syncing pending operations
- **Offline**: Device is offline, changes queued
- **Conflict**: Data conflict detected, needs resolution
- **Error**: Sync failed, retry available

```tsx
import { SyncStatus } from '@/components/sync';

// Basic usage
<SyncStatus />

// With label
<SyncStatus showLabel />
```

### SyncQueue

Modal dialog showing pending operations:
- List all queued operations
- Show retry count per operation
- Manual retry button
- Cancel operation button
- Clear all operations

```tsx
import { SyncQueue } from '@/components/sync';

<SyncQueue isOpen={isOpen} onClose={handleClose} />
```

### ConflictResolution

Modal for resolving sync conflicts:
- Side-by-side comparison (local vs server)
- Three resolution options:
  - Keep Local: Force local version
  - Keep Server: Accept server version
  - Merge Manually: Combine both (for code only)
- Diff view highlighting changes

```tsx
import { ConflictResolution } from '@/components/sync';

<ConflictResolution
  conflict={conflictInfo}
  isOpen={isOpen}
  onClose={handleClose}
/>
```

### MigrationModal

Modal for migrating legacy localStorage data:
- Detects old progress data
- Shows estimated items to migrate
- Progress indicator during migration
- Error handling and retry

```tsx
import { MigrationModal } from '@/components/sync';

<MigrationModal
  isOpen={showMigration}
  onClose={handleClose}
  onComplete={handleComplete}
/>
```

## Usage Example

```tsx
'use client';

import { useEffect, useState } from 'react';
import { SyncStatus, ConflictResolution } from '@/components/sync';
import { useSync } from '@/hooks/use-sync';
import { initSyncEngine } from '@/lib/sync-engine';

export default function App() {
  const [showConflict, setShowConflict] = useState(false);
  const [currentConflict, setCurrentConflict] = useState(null);
  
  const sync = useSync((conflict) => {
    setCurrentConflict(conflict);
    setShowConflict(true);
  });

  useEffect(() => {
    // Initialize sync engine on app start
    initSyncEngine({
      onConflict: (conflict) => {
        setCurrentConflict(conflict);
        setShowConflict(true);
      },
    });

    return () => {
      cleanupSyncEngine();
    };
  }, []);

  return (
    <>
      <header>
        <SyncStatus />
      </header>
      
      <main>{/* App content */}</main>
      
      <ConflictResolution
        conflict={currentConflict}
        isOpen={showConflict}
        onClose={() => setShowConflict(false)}
      />
    </>
  );
}
```

## Sync Flow

1. **User makes change** (e.g., completes problem)
2. **Optimistic update** - UI updates immediately
3. **Local save** - Data saved to IndexedDB
4. **Queue operation** - Sync operation added to queue
5. **Try immediate sync** - If online, sync right away
6. **Background sync** - If offline, wait for connection
7. **Conflict detection** - Server checks for conflicts
8. **Resolution** - User resolves conflicts if needed

## File Structure

```
components/sync/
├── index.ts                 # Component exports
├── sync-status.tsx          # Header sync indicator
├── sync-queue.tsx           # Pending operations modal
├── conflict-resolution.tsx  # Conflict resolution UI
├── migration-modal.tsx      # Data migration modal
└── README.md               # This file
```
