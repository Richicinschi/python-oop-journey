'use client';

import { useState, useEffect, useCallback } from 'react';

// Settings types
export interface UserSettings {
  // Appearance
  theme: 'light' | 'dark' | 'system';
  language: string;
  reducedMotion: boolean;
  highContrast: boolean;

  // Notifications
  emailWeeklyReport: boolean;
  emailNewContent: boolean;
  emailStreakReminders: boolean;
  pushNotifications: boolean;
  achievementNotifications: boolean;
  milestoneNotifications: boolean;
  quietHours: boolean;

  // Editor
  fontSize: string;
  wordWrap: boolean;
  minimap: boolean;
  lineNumbers: boolean;
  autoSave: boolean;

  // Privacy
  analyticsEnabled: boolean;
  publicProfile: boolean;
}

// Default settings
export const defaultSettings: UserSettings = {
  // Appearance
  theme: 'system',
  language: 'en',
  reducedMotion: false,
  highContrast: false,

  // Notifications
  emailWeeklyReport: true,
  emailNewContent: true,
  emailStreakReminders: false,
  pushNotifications: false,
  achievementNotifications: true,
  milestoneNotifications: true,
  quietHours: false,

  // Editor
  fontSize: '14',
  wordWrap: true,
  minimap: true,
  lineNumbers: true,
  autoSave: false,

  // Privacy
  analyticsEnabled: true,
  publicProfile: false,
};

const SETTINGS_STORAGE_KEY = 'python-oop-journey-settings';

// Load settings from localStorage
function loadSettings(): UserSettings {
  if (typeof window === 'undefined') {
    return defaultSettings;
  }

  try {
    const stored = localStorage.getItem(SETTINGS_STORAGE_KEY);
    if (stored) {
      const parsed = JSON.parse(stored);
      // Merge with defaults to ensure all fields exist
      return { ...defaultSettings, ...parsed };
    }
  } catch (error) {
    console.error('Failed to load settings:', error);
  }

  return defaultSettings;
}

// Save settings to localStorage
function saveSettingsToStorage(settings: UserSettings): void {
  if (typeof window === 'undefined') {
    return;
  }

  try {
    localStorage.setItem(SETTINGS_STORAGE_KEY, JSON.stringify(settings));
  } catch (error) {
    console.error('Failed to save settings:', error);
    throw new Error('Failed to save settings to storage');
  }
}

// Hook return type
interface UseSettingsReturn {
  settings: UserSettings;
  isLoading: boolean;
  isSaving: boolean;
  hasChanges: boolean;
  updateSetting: <K extends keyof UserSettings>(key: K, value: UserSettings[K]) => void;
  updateSettings: (updates: Partial<UserSettings>) => void;
  saveSettings: () => Promise<void>;
  resetSettings: () => void;
  resetToDefaults: () => void;
}

export function useSettings(): UseSettingsReturn {
  const [settings, setSettings] = useState<UserSettings>(defaultSettings);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [originalSettings, setOriginalSettings] = useState<UserSettings>(defaultSettings);

  // Load settings on mount
  useEffect(() => {
    const loaded = loadSettings();
    setSettings(loaded);
    setOriginalSettings(loaded);
    setIsLoading(false);
  }, []);

  // Check if there are unsaved changes
  const hasChanges = JSON.stringify(settings) !== JSON.stringify(originalSettings);

  // Update a single setting
  const updateSetting = useCallback(<K extends keyof UserSettings>(
    key: K,
    value: UserSettings[K]
  ) => {
    setSettings((prev) => ({ ...prev, [key]: value }));
  }, []);

  // Update multiple settings at once
  const updateSettings = useCallback((updates: Partial<UserSettings>) => {
    setSettings((prev) => ({ ...prev, ...updates }));
  }, []);

  // Save settings to storage
  const saveSettings = useCallback(async (): Promise<void> => {
    setIsSaving(true);
    
    try {
      // Simulate API call delay for better UX
      await new Promise((resolve) => setTimeout(resolve, 500));
      
      saveSettingsToStorage(settings);
      setOriginalSettings(settings);
    } catch (error) {
      console.error('Failed to save settings:', error);
      throw error;
    } finally {
      setIsSaving(false);
    }
  }, [settings]);

  // Reset to last saved state
  const resetSettings = useCallback(() => {
    setSettings(originalSettings);
  }, [originalSettings]);

  // Reset to factory defaults
  const resetToDefaults = useCallback(() => {
    setSettings(defaultSettings);
  }, []);

  return {
    settings,
    isLoading,
    isSaving,
    hasChanges,
    updateSetting,
    updateSettings,
    saveSettings,
    resetSettings,
    resetToDefaults,
  };
}

export default useSettings;
