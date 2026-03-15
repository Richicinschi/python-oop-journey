'use client';

import { useState } from 'react';
import Link from 'next/link';
import { cn } from '@/lib/utils';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Separator } from '@/components/ui/separator';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useSettings } from '@/hooks/use-settings';
import { toast } from 'sonner';
import { 
  ChevronLeft, 
  Settings, 
  Bell, 
  Palette, 
  Globe, 
  Shield, 
  Keyboard,
  Monitor,
  Moon,
  Sun,
  Laptop,
  Eye,
  Clock,
  Mail,
  MessageSquare,
  Trophy,
  Save,
  RotateCcw,
  Loader2
} from 'lucide-react';

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState('general');
  const {
    settings,
    isLoading,
    isSaving,
    hasChanges,
    updateSetting,
    saveSettings,
    resetSettings,
    resetToDefaults,
  } = useSettings();

  // Handle save with toast notifications
  const handleSave = async () => {
    try {
      await saveSettings();
      toast.success('Settings saved', {
        description: 'Your preferences have been saved successfully.',
      });
    } catch (error) {
      toast.error('Failed to save settings', {
        description: error instanceof Error ? error.message : 'Please try again.',
      });
    }
  };

  // Handle reset to defaults
  const handleResetToDefaults = () => {
    resetToDefaults();
    toast.info('Settings reset', {
      description: 'All settings have been reset to defaults. Click Save to apply.',
    });
  };

  // Handle reset to last saved
  const handleReset = () => {
    resetSettings();
    toast.info('Changes discarded', {
      description: 'Your settings have been reverted to the last saved state.',
    });
  };

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-5xl">
        <div className="flex items-center justify-center h-96">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl">
      {/* Header */}
      <div className="mb-8">
        <Button variant="ghost" size="sm" asChild className="mb-4">
          <Link href="/profile">
            <ChevronLeft className="h-4 w-4 mr-2" />
            Back to Profile
          </Link>
        </Button>
        
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-primary/10">
            <Settings className="h-6 w-6 text-primary" />
          </div>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
            <p className="text-muted-foreground">
              Manage your preferences and account settings
            </p>
          </div>
        </div>
      </div>

      {/* Settings Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="grid w-full grid-cols-2 sm:grid-cols-4 lg:w-auto lg:inline-grid">
          <TabsTrigger value="general" className="gap-2">
            <Monitor className="h-4 w-4" />
            <span className="hidden sm:inline">General</span>
          </TabsTrigger>
          <TabsTrigger value="notifications" className="gap-2">
            <Bell className="h-4 w-4" />
            <span className="hidden sm:inline">Notifications</span>
          </TabsTrigger>
          <TabsTrigger value="editor" className="gap-2">
            <Keyboard className="h-4 w-4" />
            <span className="hidden sm:inline">Editor</span>
          </TabsTrigger>
          <TabsTrigger value="privacy" className="gap-2">
            <Shield className="h-4 w-4" />
            <span className="hidden sm:inline">Privacy</span>
          </TabsTrigger>
        </TabsList>

        {/* General Settings */}
        <TabsContent value="general" className="space-y-6">
          {/* Appearance */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Palette className="h-5 w-5" />
                Appearance
              </CardTitle>
              <CardDescription>
                Customize how the platform looks for you
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Theme */}
              <ThemeSelector 
                value={settings.theme} 
                onChange={(value) => updateSetting('theme', value)} 
              />

              <Separator />

              {/* Language */}
              <div className="space-y-3">
                <Label htmlFor="language" className="text-base flex items-center gap-2">
                  <Globe className="h-4 w-4" />
                  Language
                </Label>
                <Select 
                  value={settings.language}
                  onValueChange={(value) => updateSetting('language', value)}
                >
                  <SelectTrigger id="language" className="w-full sm:w-[280px]">
                    <SelectValue placeholder="Select language" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="en">English</SelectItem>
                    <SelectItem value="es">Español</SelectItem>
                    <SelectItem value="fr">Français</SelectItem>
                    <SelectItem value="de">Deutsch</SelectItem>
                    <SelectItem value="zh">中文</SelectItem>
                  </SelectContent>
                </Select>
                <p className="text-sm text-muted-foreground">
                  More languages coming soon
                </p>
              </div>

              <Separator />

              {/* Accessibility */}
              <div className="space-y-4">
                <Label className="text-base flex items-center gap-2">
                  <Eye className="h-4 w-4" />
                  Accessibility
                </Label>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label htmlFor="reduced-motion">Reduced Motion</Label>
                      <p className="text-sm text-muted-foreground">
                        Minimize animations throughout the interface
                      </p>
                    </div>
                    <Switch 
                      id="reduced-motion" 
                      checked={settings.reducedMotion}
                      onCheckedChange={(checked) => updateSetting('reducedMotion', checked)}
                    />
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label htmlFor="high-contrast">High Contrast</Label>
                      <p className="text-sm text-muted-foreground">
                        Increase contrast for better visibility
                      </p>
                    </div>
                    <Switch 
                      id="high-contrast" 
                      checked={settings.highContrast}
                      onCheckedChange={(checked) => updateSetting('highContrast', checked)}
                    />
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Coming Soon */}
          <Card className="border-dashed">
            <CardContent className="p-8 text-center">
              <Settings className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
              <h3 className="font-medium mb-2">More Settings Coming Soon</h3>
              <p className="text-sm text-muted-foreground">
                We&apos;re working on adding more customization options
              </p>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Notifications */}
        <TabsContent value="notifications" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Bell className="h-5 w-5" />
                Notification Preferences
              </CardTitle>
              <CardDescription>
                Choose how and when you want to be notified
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Email Notifications */}
              <div className="space-y-4">
                <div className="flex items-center gap-2 text-base font-medium">
                  <Mail className="h-4 w-4" />
                  Email Notifications
                </div>
                <div className="space-y-4 pl-6">
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label>Weekly Progress Report</Label>
                      <p className="text-sm text-muted-foreground">
                        Get a summary of your learning progress
                      </p>
                    </div>
                    <Switch 
                      checked={settings.emailWeeklyReport}
                      onCheckedChange={(checked) => updateSetting('emailWeeklyReport', checked)}
                    />
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label>New Content Alerts</Label>
                      <p className="text-sm text-muted-foreground">
                        Be notified when new problems or features are added
                      </p>
                    </div>
                    <Switch 
                      checked={settings.emailNewContent}
                      onCheckedChange={(checked) => updateSetting('emailNewContent', checked)}
                    />
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label>Streak Reminders</Label>
                      <p className="text-sm text-muted-foreground">
                        Reminders to keep your learning streak alive
                      </p>
                    </div>
                    <Switch 
                      checked={settings.emailStreakReminders}
                      onCheckedChange={(checked) => updateSetting('emailStreakReminders', checked)}
                    />
                  </div>
                </div>
              </div>

              <Separator />

              {/* Push Notifications */}
              <div className="space-y-4">
                <div className="flex items-center gap-2 text-base font-medium">
                  <MessageSquare className="h-4 w-4" />
                  Push Notifications
                </div>
                <div className="space-y-4 pl-6">
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label>Browser Notifications</Label>
                      <p className="text-sm text-muted-foreground">
                        Enable desktop notifications for important updates
                      </p>
                    </div>
                    <Switch 
                      checked={settings.pushNotifications}
                      onCheckedChange={(checked) => updateSetting('pushNotifications', checked)}
                    />
                  </div>
                </div>
              </div>

              <Separator />

              {/* Achievement Notifications */}
              <div className="space-y-4">
                <div className="flex items-center gap-2 text-base font-medium">
                  <Trophy className="h-4 w-4" />
                  Achievements
                </div>
                <div className="space-y-4 pl-6">
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label>Achievement Unlocked</Label>
                      <p className="text-sm text-muted-foreground">
                        Show notifications when you earn achievements
                      </p>
                    </div>
                    <Switch 
                      checked={settings.achievementNotifications}
                      onCheckedChange={(checked) => updateSetting('achievementNotifications', checked)}
                    />
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label>Milestone Celebrations</Label>
                      <p className="text-sm text-muted-foreground">
                        Celebrate when you complete weeks or projects
                      </p>
                    </div>
                    <Switch 
                      checked={settings.milestoneNotifications}
                      onCheckedChange={(checked) => updateSetting('milestoneNotifications', checked)}
                    />
                  </div>
                </div>
              </div>

              <Separator />

              {/* Quiet Hours */}
              <div className="space-y-4">
                <div className="flex items-center gap-2 text-base font-medium">
                  <Clock className="h-4 w-4" />
                  Quiet Hours
                </div>
                <div className="pl-6">
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label>Enable Quiet Hours</Label>
                      <p className="text-sm text-muted-foreground">
                        Pause non-essential notifications during set hours
                      </p>
                    </div>
                    <Switch 
                      checked={settings.quietHours}
                      onCheckedChange={(checked) => updateSetting('quietHours', checked)}
                    />
                  </div>
                  <p className="text-sm text-muted-foreground mt-4">
                    Quiet hours configuration coming soon
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Editor Settings */}
        <TabsContent value="editor" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Keyboard className="h-5 w-5" />
                Code Editor
              </CardTitle>
              <CardDescription>
                Customize your coding experience
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Font Size */}
              <div className="space-y-3">
                <Label htmlFor="font-size" className="text-base">Font Size</Label>
                <Select 
                  value={settings.fontSize}
                  onValueChange={(value) => updateSetting('fontSize', value)}
                >
                  <SelectTrigger id="font-size" className="w-full sm:w-[200px]">
                    <SelectValue placeholder="Select font size" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="12">12px</SelectItem>
                    <SelectItem value="14">14px (Default)</SelectItem>
                    <SelectItem value="16">16px</SelectItem>
                    <SelectItem value="18">18px</SelectItem>
                    <SelectItem value="20">20px</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <Separator />

              {/* Editor Options */}
              <div className="space-y-4">
                <Label className="text-base">Editor Options</Label>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label htmlFor="word-wrap">Word Wrap</Label>
                      <p className="text-sm text-muted-foreground">
                        Wrap long lines to fit the editor width
                      </p>
                    </div>
                    <Switch 
                      id="word-wrap" 
                      checked={settings.wordWrap}
                      onCheckedChange={(checked) => updateSetting('wordWrap', checked)}
                    />
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label htmlFor="minimap">Minimap</Label>
                      <p className="text-sm text-muted-foreground">
                        Show minimap overview of your code
                      </p>
                    </div>
                    <Switch 
                      id="minimap" 
                      checked={settings.minimap}
                      onCheckedChange={(checked) => updateSetting('minimap', checked)}
                    />
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label htmlFor="line-numbers">Line Numbers</Label>
                      <p className="text-sm text-muted-foreground">
                        Display line numbers in the editor
                      </p>
                    </div>
                    <Switch 
                      id="line-numbers" 
                      checked={settings.lineNumbers}
                      onCheckedChange={(checked) => updateSetting('lineNumbers', checked)}
                    />
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label htmlFor="auto-save">Auto Save</Label>
                      <p className="text-sm text-muted-foreground">
                        Automatically save your code while typing
                      </p>
                    </div>
                    <Switch 
                      id="auto-save" 
                      checked={settings.autoSave}
                      onCheckedChange={(checked) => updateSetting('autoSave', checked)}
                    />
                  </div>
                </div>
              </div>

              <Separator />

              {/* Keyboard Shortcuts */}
              <div className="space-y-3">
                <Label className="text-base flex items-center gap-2">
                  <Keyboard className="h-4 w-4" />
                  Keyboard Shortcuts
                </Label>
                <div className="rounded-lg border bg-muted/50 p-4 space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span>Run Code</span>
                    <kbd className="px-2 py-1 rounded bg-background border text-xs">Ctrl + R</kbd>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span>Save File</span>
                    <kbd className="px-2 py-1 rounded bg-background border text-xs">Ctrl + S</kbd>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span>Run Tests</span>
                    <kbd className="px-2 py-1 rounded bg-background border text-xs">Ctrl + T</kbd>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span>Toggle File Tree</span>
                    <kbd className="px-2 py-1 rounded bg-background border text-xs">Ctrl + B</kbd>
                  </div>
                </div>
                <p className="text-sm text-muted-foreground">
                  Custom keyboard shortcuts coming soon
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Privacy Settings */}
        <TabsContent value="privacy" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Shield className="h-5 w-5" />
                Privacy Settings
              </CardTitle>
              <CardDescription>
                Control your data and privacy preferences
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Data Sharing */}
              <div className="space-y-4">
                <Label className="text-base">Data Sharing</Label>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label htmlFor="analytics">Usage Analytics</Label>
                      <p className="text-sm text-muted-foreground">
                        Help us improve by sharing anonymous usage data
                      </p>
                    </div>
                    <Switch 
                      id="analytics" 
                      checked={settings.analyticsEnabled}
                      onCheckedChange={(checked) => updateSetting('analyticsEnabled', checked)}
                    />
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label htmlFor="public-profile">Public Profile</Label>
                      <p className="text-sm text-muted-foreground">
                        Allow others to see your progress on leaderboards
                      </p>
                    </div>
                    <Switch 
                      id="public-profile" 
                      checked={settings.publicProfile}
                      onCheckedChange={(checked) => updateSetting('publicProfile', checked)}
                    />
                  </div>
                </div>
              </div>

              <Separator />

              {/* Data Management */}
              <div className="space-y-4">
                <Label className="text-base">Data Management</Label>
                <div className="space-y-3">
                  <Button variant="outline" className="w-full sm:w-auto" asChild>
                    <Link href="/profile/data">
                      Manage Your Data
                    </Link>
                  </Button>
                  <p className="text-sm text-muted-foreground">
                    Export, import, or delete your learning data
                  </p>
                </div>
              </div>

              <Separator />

              {/* Account Deletion */}
              <div className="space-y-4">
                <Label className="text-base text-destructive">Danger Zone</Label>
                <div className="rounded-lg border border-destructive/20 bg-destructive/5 p-4 space-y-3">
                  <p className="text-sm text-muted-foreground">
                    Once you delete your account, there is no going back. Please be certain.
                  </p>
                  <Button variant="destructive" size="sm">
                    Delete Account
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Save Changes Bar */}
      <div className={cn(
        "fixed bottom-0 left-0 right-0 border-t bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 p-4 transition-transform duration-300",
        hasChanges ? "translate-y-0" : "translate-y-full"
      )}>
        <div className="container max-w-5xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="h-2 w-2 rounded-full bg-amber-500 animate-pulse" />
            <p className="text-sm text-muted-foreground">
              You have unsaved changes
            </p>
          </div>
          <div className="flex items-center gap-3">
            <Button 
              variant="ghost" 
              size="sm" 
              onClick={handleReset}
              disabled={isSaving}
            >
              <RotateCcw className="h-4 w-4 mr-2" />
              Discard
            </Button>
            <Button 
              variant="outline" 
              size="sm" 
              onClick={handleResetToDefaults}
              disabled={isSaving}
            >
              Reset to Defaults
            </Button>
            <Button 
              size="sm" 
              onClick={handleSave}
              disabled={isSaving}
            >
              {isSaving ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Saving...
                </>
              ) : (
                <>
                  <Save className="h-4 w-4 mr-2" />
                  Save Changes
                </>
              )}
            </Button>
          </div>
        </div>
      </div>

      {/* Spacer for fixed bar */}
      <div className="h-20" />
    </div>
  );
}

// Theme selector component
interface ThemeSelectorProps {
  value: 'light' | 'dark' | 'system';
  onChange: (value: 'light' | 'dark' | 'system') => void;
}

function ThemeSelector({ value, onChange }: ThemeSelectorProps) {
  return (
    <div className="space-y-3">
      <Label className="text-base">Theme</Label>
      <div className="grid grid-cols-3 gap-4">
        <button
          onClick={() => onChange('light')}
          className={cn(
            "flex flex-col items-center gap-2 p-4 rounded-lg border-2 transition-colors",
            value === 'light'
              ? "border-primary bg-primary/5"
              : "border hover:border-primary/50"
          )}
        >
          <Sun className="h-8 w-8" />
          <span className="text-sm font-medium">Light</span>
        </button>
        <button
          onClick={() => onChange('dark')}
          className={cn(
            "flex flex-col items-center gap-2 p-4 rounded-lg border-2 transition-colors",
            value === 'dark'
              ? "border-primary bg-primary/5"
              : "border hover:border-primary/50"
          )}
        >
          <Moon className="h-8 w-8" />
          <span className="text-sm font-medium">Dark</span>
        </button>
        <button
          onClick={() => onChange('system')}
          className={cn(
            "flex flex-col items-center gap-2 p-4 rounded-lg border-2 transition-colors",
            value === 'system'
              ? "border-primary bg-primary/5"
              : "border hover:border-primary/50"
          )}
        >
          <Laptop className="h-8 w-8" />
          <span className="text-sm font-medium">System</span>
        </button>
      </div>
    </div>
  );
}
