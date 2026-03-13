/**
 * Feature Flags Configuration
 * 
 * This module provides a type-safe feature flag system for gradual rollouts,
 * A/B testing, and emergency kill switches.
 * 
 * Usage:
 *   if (isEnabled('aiHints')) { ... }
 *   if (isEnabledForUser('gamification', userId)) { ... }
 */

// Feature flag definitions
export type FeatureFlag = 
  | 'aiHints'           // AI-generated hints
  | 'community'         // Community features (discussions, etc.)
  | 'gamification'      // XP, badges, leaderboards
  | 'collaboration'     // Real-time collaboration
  | 'newProjectEditor'  // New project editor (for gradual rollout)
  | 'darkMode'          // Dark mode UI
  | 'advancedAnalytics' // Detailed progress analytics
  | 'offlineMode'       // Offline exercise support
  | 'betaFeatures';     // Access to beta features

// Feature flag configuration
interface FeatureConfig {
  enabled: boolean;
  rolloutPercentage?: number; // 0-100, for gradual rollouts
  allowedUsers?: string[];    // Specific user IDs to enable for
  allowedRoles?: string[];    // Specific roles to enable for
}

// Default feature configurations
const defaultFeatures: Record<FeatureFlag, FeatureConfig> = {
  aiHints: {
    enabled: process.env.NEXT_PUBLIC_FEATURE_AI_HINTS === 'true',
    rolloutPercentage: 100,
  },
  community: {
    enabled: process.env.NEXT_PUBLIC_FEATURE_COMMUNITY === 'true',
    rolloutPercentage: 0, // Disabled until ready
  },
  gamification: {
    enabled: process.env.NEXT_PUBLIC_FEATURE_GAMIFICATION !== 'false',
    rolloutPercentage: 100,
  },
  collaboration: {
    enabled: process.env.NEXT_PUBLIC_FEATURE_COLLABORATION === 'true',
    rolloutPercentage: 0,
  },
  newProjectEditor: {
    enabled: true,
    rolloutPercentage: 100, // Fully rolled out
  },
  darkMode: {
    enabled: true,
    rolloutPercentage: 100,
  },
  advancedAnalytics: {
    enabled: process.env.NEXT_PUBLIC_FEATURE_ADVANCED_ANALYTICS === 'true',
    rolloutPercentage: 50, // Gradual rollout
  },
  offlineMode: {
    enabled: process.env.NEXT_PUBLIC_FEATURE_OFFLINE_MODE === 'true',
    rolloutPercentage: 0,
  },
  betaFeatures: {
    enabled: false,
    allowedRoles: ['admin', 'beta_tester'],
  },
};

// Runtime feature overrides (can be updated via API)
let runtimeOverrides: Partial<Record<FeatureFlag, Partial<FeatureConfig>>> = {};

/**
 * Check if a feature is enabled
 */
export function isEnabled(flag: FeatureFlag): boolean {
  const config = getConfig(flag);
  return config.enabled;
}

/**
 * Check if a feature is enabled for a specific user
 * Supports gradual rollouts based on user ID hash
 */
export function isEnabledForUser(flag: FeatureFlag, userId: string): boolean {
  const config = getConfig(flag);
  
  if (!config.enabled) {
    return false;
  }
  
  // Check if user is specifically allowed
  if (config.allowedUsers?.includes(userId)) {
    return true;
  }
  
  // Check rollout percentage
  if (config.rolloutPercentage !== undefined && config.rolloutPercentage < 100) {
    const userHash = hashString(userId + flag);
    const userPercentile = userHash % 100;
    return userPercentile < config.rolloutPercentage;
  }
  
  return true;
}

/**
 * Check if a feature is enabled for a specific role
 */
export function isEnabledForRole(flag: FeatureFlag, role: string): boolean {
  const config = getConfig(flag);
  
  if (!config.enabled) {
    return false;
  }
  
  if (config.allowedRoles?.includes(role)) {
    return true;
  }
  
  return config.rolloutPercentage === 100;
}

/**
 * Get all enabled features
 */
export function getEnabledFeatures(): FeatureFlag[] {
  return (Object.keys(defaultFeatures) as FeatureFlag[]).filter(isEnabled);
}

/**
 * Get feature configuration
 */
export function getFeatureConfig(flag: FeatureFlag): FeatureConfig {
  return getConfig(flag);
}

/**
 * Update feature flags at runtime (e.g., from remote config)
 */
export function updateFeatureFlags(overrides: Partial<Record<FeatureFlag, Partial<FeatureConfig>>>): void {
  runtimeOverrides = { ...runtimeOverrides, ...overrides };
}

/**
 * Reset feature flags to defaults
 */
export function resetFeatureFlags(): void {
  runtimeOverrides = {};
}

// Helper: Get merged config
function getConfig(flag: FeatureFlag): FeatureConfig {
  const defaultConfig = defaultFeatures[flag];
  const override = runtimeOverrides[flag];
  
  if (!override) {
    return defaultConfig;
  }
  
  return {
    ...defaultConfig,
    ...override,
    allowedUsers: override.allowedUsers ?? defaultConfig.allowedUsers,
    allowedRoles: override.allowedRoles ?? defaultConfig.allowedRoles,
  };
}

// Helper: Simple hash function for consistent user bucketing
function hashString(str: string): number {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32bit integer
  }
  return Math.abs(hash);
}

// React hook for feature flags
import { useState, useEffect } from 'react';

export function useFeatureFlag(flag: FeatureFlag): boolean {
  const [enabled, setEnabled] = useState(() => isEnabled(flag));
  
  useEffect(() => {
    setEnabled(isEnabled(flag));
  }, [flag]);
  
  return enabled;
}

export function useFeatureFlagForUser(flag: FeatureFlag, userId: string): boolean {
  const [enabled, setEnabled] = useState(() => isEnabledForUser(flag, userId));
  
  useEffect(() => {
    setEnabled(isEnabledForUser(flag, userId));
  }, [flag, userId]);
  
  return enabled;
}
