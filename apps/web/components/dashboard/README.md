# Dashboard Components

This directory contains all the components for the learner dashboard and homepage experience.

## Components

### `hero-section.tsx`
Hero section with welcome message and primary CTA.
- New user: Shows welcome message, stats preview, and start journey CTA
- Returning user: Shows continue learning CTA, streak info, and overall progress

### `empty-state.tsx`
Onboarding experience for new users with:
- "How it works" 3-step explanation
- Curriculum preview (first 4 weeks)
- Feature highlights
- Start journey CTA

### `stat-card.tsx`
Reusable stat card component with variants:
- `default`: Standard stat display
- `highlight`: Emphasized stat (e.g., problems solved)
- `success`: Achievement stat (e.g., weeks completed)
- `warning`: Attention stat (e.g., streak count)

### `progress-card.tsx`
Week progress card showing:
- Week number and title
- Completion status (not started/in progress/completed)
- Progress bar with percentage
- Click to navigate to week

### `activity-item.tsx`
Recent activity list showing:
- Problem title and location (week/day)
- Status (completed/attempted/failed)
- Timestamp and time spent
- Click to navigate to problem

### `recommendation-card.tsx`
AI-driven recommendations with priority levels:
- High priority: Continue learning, start week
- Medium priority: Review difficult problems
- Low priority: Practice random problem

### `circular-progress.tsx`
Circular progress indicator for current day/week progress.

### `quick-actions.tsx`
Quick action buttons and dropdowns:
- Jump to Week dropdown
- Practice Random Problem
- Review Bookmarks
- View Certificates (coming soon)
- Action button grid (Practice, Review, Learn, Achievements)

## Usage

```tsx
import { HeroSection } from '@/components/dashboard/hero-section';
import { StatCard } from '@/components/dashboard/stat-card';
import { ProgressCard } from '@/components/dashboard/progress-card';
import { ActivityList } from '@/components/dashboard/activity-item';
import { RecommendationList } from '@/components/dashboard/recommendation-card';
import { CircularProgress } from '@/components/dashboard/circular-progress';
import { QuickActions, ActionButtons } from '@/components/dashboard/quick-actions';
```

## Data Hooks

### `use-dashboard-data.ts`
Main hook for dashboard data management:
```tsx
const { 
  data, 
  isLoading, 
  derivedStats, 
  recommendations,
  updateProgress,
  addActivity,
  setCurrentPosition,
  loadMockData 
} = useDashboardData();
```

## Types

### `types/dashboard.ts`
Core type definitions:
- `ActivityItem`: User activity log entry
- `WeekProgress`: Progress for a specific week
- `UserStats`: Aggregated user statistics
- `Recommendation`: Suggested next action
- `DashboardData`: Complete dashboard state

## Features

### For New Users
- Welcome hero with curriculum stats
- "How it works" explanation
- Curriculum preview
- Start journey CTA

### For Returning Users
- Continue learning CTA
- Overall progress stats
- Current week progress widget
- Weekly overview grid
- Recent activity feed
- Personalized recommendations
- Quick action buttons

### Responsive Design
- Desktop: Multi-column grid layout
- Tablet: 2-column layout
- Mobile: Single column stack

### Animations
- Fade-in animations for cards
- Scale-in for stats
- Slide-in for activity items
- Progress bar transitions
- Hover effects on interactive elements

### Data Persistence
- Uses localStorage for progress tracking
- Mock data available for demo purposes
- Ready for API integration
