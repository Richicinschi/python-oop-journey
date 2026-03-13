'use client';

/**
 * User Profile Page
 * 
 * Shows user info and links to data management, settings, etc.
 */

import Link from 'next/link';
import { 
  User, 
  Database, 
  Settings, 
  LogOut,
  ChevronRight,
  Cloud,
  Shield,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { SyncStatus } from '@/components/sync';
import { useOnlineStatus } from '@/hooks/use-online-status';

export default function ProfilePage() {
  const { isOnline, status } = useOnlineStatus();

  return (
    <div className="container max-w-4xl py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight">Profile</h1>
        <p className="text-muted-foreground mt-2">
          Manage your account, data, and preferences.
        </p>
      </div>

      {/* Connection Status */}
      <Card className="mb-6">
        <CardHeader className="pb-3">
          <CardTitle className="text-base">Connection Status</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className={`w-3 h-3 rounded-full ${isOnline ? 'bg-green-500' : 'bg-amber-500'}`} />
              <div>
                <p className="font-medium">{isOnline ? 'Online' : 'Offline'}</p>
                <p className="text-sm text-muted-foreground">
                  {isOnline 
                    ? 'Your changes are syncing automatically.' 
                    : 'Changes will sync when you reconnect.'}
                </p>
              </div>
            </div>
            <SyncStatus showLabel />
          </div>
        </CardContent>
      </Card>

      {/* Menu Items */}
      <div className="space-y-4">
        <Card>
          <CardHeader>
            <CardTitle>Account</CardTitle>
            <CardDescription>Manage your account settings and data</CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            <MenuItem
              href="/profile/data"
              icon={<Database className="h-5 w-5" />}
              title="Data Management"
              description="Export, import, and manage your learning data"
            />
            <Separator />
            <MenuItem
              href="#"
              icon={<Settings className="h-5 w-5" />}
              title="Preferences"
              description="Theme, notifications, and other settings"
            />
            <Separator />
            <MenuItem
              href="#"
              icon={<Shield className="h-5 w-5" />}
              title="Privacy & Security"
              description="Manage your privacy settings"
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Support</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <MenuItem
              href="#"
              icon={<Cloud className="h-5 w-5" />}
              title="Help & Documentation"
              description="Get help with using the platform"
            />
          </CardContent>
        </Card>

        <Button variant="outline" className="w-full gap-2 text-destructive hover:text-destructive">
          <LogOut className="h-4 w-4" />
          Sign Out
        </Button>
      </div>
    </div>
  );
}

interface MenuItemProps {
  href: string;
  icon: React.ReactNode;
  title: string;
  description: string;
}

function MenuItem({ href, icon, title, description }: MenuItemProps) {
  return (
    <Link 
      href={href}
      className="flex items-center gap-4 p-3 -mx-2 rounded-lg hover:bg-muted transition-colors"
    >
      <div className="flex-shrink-0 w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center text-primary">
        {icon}
      </div>
      <div className="flex-1 min-w-0">
        <p className="font-medium truncate">{title}</p>
        <p className="text-sm text-muted-foreground truncate">{description}</p>
      </div>
      <ChevronRight className="h-5 w-5 text-muted-foreground" />
    </Link>
  );
}
