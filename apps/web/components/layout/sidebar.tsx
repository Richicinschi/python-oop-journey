'use client';

import { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible';
import { WeekNavigator } from '@/components/curriculum/week-navigator';
import { 
  BookOpen, 
  ChevronLeft, 
  ChevronRight, 
  Code, 
  Home,
  Settings,
  Search,
  GraduationCap,
  FolderGit2,
  ChevronDown,
  Play,
  CheckCircle2,
  Circle,
  LogIn,
  X
} from 'lucide-react';
import { getWeeks } from '@/lib/curriculum-loader';
import { useLocalStorage } from '@/hooks/use-local-storage';

interface SidebarProps {
  className?: string;
  /**
   * Whether this is the mobile sidebar (affects styling)
   */
  isMobile?: boolean;
  /**
   * Callback when a link is clicked (used to close mobile sidebar)
   */
  onLinkClick?: () => void;
}

// Mock active projects - in real app, fetch from store
const mockActiveProjects = [
  { slug: 'week-01-project', title: 'CLI Calculator', weekNumber: 1, status: 'in_progress' as const },
];

export function Sidebar({ className, isMobile, onLinkClick }: SidebarProps) {
  const pathname = usePathname();
  const weeks = getWeeks();
  
  // Persist collapsed state in localStorage (desktop only)
  const [collapsed, setCollapsed] = useLocalStorage('oop-journey-sidebar-collapsed', false);
  
  // Track projects section expansion
  const [projectsOpen, setProjectsOpen] = useLocalStorage('oop-journey-projects-expanded', true);
  
  // Track if component is mounted (for hydration mismatch prevention)
  const [mounted, setMounted] = useState(false);
  
  useEffect(() => {
    setMounted(true);
  }, []);

  const hasActiveProjects = mockActiveProjects.length > 0;

  // Handle link click with mobile close callback
  const handleLinkClick = useCallback(() => {
    onLinkClick?.();
  }, [onLinkClick]);

  // Mobile sidebar has different styling
  if (isMobile) {
    return (
      <div className={cn('flex flex-col h-full bg-card', className)}>
        {/* Logo Area */}
        <div className="flex h-16 items-center justify-between px-4 border-b">
          <Link href="/" className="flex items-center gap-2 font-bold text-lg" onClick={handleLinkClick}>
            <GraduationCap className="h-6 w-6 text-primary" />
            <span className="truncate">OOP Journey</span>
          </Link>
          <Button
            variant="ghost"
            size="icon"
            onClick={handleLinkClick}
            aria-label="Close menu"
          >
            <X className="h-5 w-5" />
          </Button>
        </div>

        {/* Navigation */}
        <ScrollArea className="flex-1">
          <nav className="p-4 space-y-2">
            <SidebarItem
              href="/"
              icon={Home}
              label="Dashboard"
              collapsed={false}
              active={pathname === '/'}
              onClick={handleLinkClick}
            />
            <SidebarItem
              href="/weeks"
              icon={BookOpen}
              label="Curriculum"
              collapsed={false}
              active={pathname.startsWith('/weeks')}
              onClick={handleLinkClick}
            />
            <SidebarItem
              href="/problems"
              icon={Code}
              label="Problems"
              collapsed={false}
              active={pathname.startsWith('/problems')}
              onClick={handleLinkClick}
            />
            
            {/* Projects Section */}
            <Collapsible open={projectsOpen} onOpenChange={setProjectsOpen}>
              <CollapsibleTrigger asChild>
                <button
                  className={cn(
                    'w-full flex items-center gap-3 rounded-md px-2 py-2 text-sm font-medium transition-colors',
                    pathname.startsWith('/projects') || pathname.includes('/project')
                      ? 'bg-accent text-accent-foreground'
                      : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
                  )}
                >
                  <FolderGit2 className="h-4 w-4 shrink-0" />
                  <span className="flex-1 text-left">Projects</span>
                  <ChevronDown 
                    className={cn(
                      'h-4 w-4 shrink-0 transition-transform',
                      projectsOpen && 'rotate-180'
                    )} 
                  />
                </button>
              </CollapsibleTrigger>
              <CollapsibleContent>
                <div className="ml-4 mt-1 space-y-1">
                  <Link
                    href="/projects"
                    onClick={handleLinkClick}
                    className={cn(
                      'flex items-center gap-2 rounded-md px-2 py-1.5 text-sm transition-colors',
                      pathname === '/projects'
                        ? 'bg-accent text-accent-foreground'
                        : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
                    )}
                  >
                    <span className="truncate">All Projects</span>
                  </Link>
                  {hasActiveProjects && (
                    <>
                      <div className="pt-2 pb-1">
                        <p className="text-xs font-medium text-muted-foreground px-2">
                          Active
                        </p>
                      </div>
                      {mockActiveProjects.map(project => (
                        <Link
                          key={project.slug}
                          href={`/weeks/week-0${project.weekNumber}/project`}
                          onClick={handleLinkClick}
                          className="flex items-center gap-2 rounded-md px-2 py-1.5 text-sm text-muted-foreground hover:bg-accent hover:text-accent-foreground transition-colors"
                        >
                          {project.status === 'in_progress' ? (
                            <Play className="h-3 w-3 text-blue-500" />
                          ) : project.status === 'submitted' ? (
                            <CheckCircle2 className="h-3 w-3 text-green-500" />
                          ) : (
                            <Circle className="h-3 w-3" />
                          )}
                          <span className="truncate">{project.title}</span>
                        </Link>
                      ))}
                    </>
                  )}
                </div>
              </CollapsibleContent>
            </Collapsible>
          </nav>

          <Separator className="my-4" />
          
          {/* Week Navigator for Mobile */}
          <WeekNavigator weeks={weeks} onLinkClick={handleLinkClick} />
        </ScrollArea>

        {/* Footer */}
        <div className="border-t p-2 space-y-2">
          <SidebarItem
            href="/search"
            icon={Search}
            label="Search"
            collapsed={false}
            active={pathname === '/search' || pathname.startsWith('/problems')}
            onClick={handleLinkClick}
          />
          <SidebarItem
            href="/settings"
            icon={Settings}
            label="Settings"
            collapsed={false}
            active={pathname === '/settings'}
            onClick={handleLinkClick}
          />
          <SidebarItem
            href="/auth/login"
            icon={LogIn}
            label="Sign In"
            collapsed={false}
            active={pathname === '/auth/login'}
            onClick={handleLinkClick}
          />
        </div>
      </div>
    );
  }

  // Desktop sidebar
  return (
    <div
      className={cn(
        'flex flex-col border-r bg-card transition-all duration-300 hidden md:flex',
        collapsed ? 'w-16' : 'w-64',
        className
      )}
    >
      {/* Logo Area */}
      <div className="flex h-16 items-center justify-between px-4 border-b">
        {!collapsed && (
          <Link href="/" className="flex items-center gap-2 font-bold text-lg">
            <GraduationCap className="h-6 w-6 text-primary" />
            <span className="truncate">OOP Journey</span>
          </Link>
        )}
        {collapsed && (
          <GraduationCap className="h-6 w-6 text-primary mx-auto" />
        )}
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setCollapsed(!collapsed)}
          className={cn('shrink-0', collapsed && 'mx-auto')}
          aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {collapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
        </Button>
      </div>

      {/* Navigation */}
      <ScrollArea className="flex-1">
        <nav className={cn('space-y-2', collapsed ? 'p-2' : 'p-4')}>
          <SidebarItem
            href="/"
            icon={Home}
            label="Dashboard"
            collapsed={collapsed}
            active={pathname === '/'}
          />
          <SidebarItem
            href="/weeks"
            icon={BookOpen}
            label="Curriculum"
            collapsed={collapsed}
            active={pathname.startsWith('/weeks')}
          />
          <SidebarItem
            href="/problems"
            icon={Code}
            label="Problems"
            collapsed={collapsed}
            active={pathname.startsWith('/problems')}
          />
          
          {/* Projects Section */}
          {!collapsed ? (
            <Collapsible open={projectsOpen} onOpenChange={setProjectsOpen}>
              <CollapsibleTrigger asChild>
                <button
                  className={cn(
                    'w-full flex items-center gap-3 rounded-md px-2 py-2 text-sm font-medium transition-colors',
                    pathname.startsWith('/projects') || pathname.includes('/project')
                      ? 'bg-accent text-accent-foreground'
                      : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
                  )}
                >
                  <FolderGit2 className="h-4 w-4 shrink-0" />
                  <span className="flex-1 text-left">Projects</span>
                  <ChevronDown 
                    className={cn(
                      'h-4 w-4 shrink-0 transition-transform',
                      projectsOpen && 'rotate-180'
                    )} 
                  />
                </button>
              </CollapsibleTrigger>
              <CollapsibleContent>
                <div className="ml-4 mt-1 space-y-1">
                  <Link
                    href="/projects"
                    className={cn(
                      'flex items-center gap-2 rounded-md px-2 py-1.5 text-sm transition-colors',
                      pathname === '/projects'
                        ? 'bg-accent text-accent-foreground'
                        : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
                    )}
                  >
                    <span className="truncate">All Projects</span>
                  </Link>
                  {hasActiveProjects && (
                    <>
                      <div className="pt-2 pb-1">
                        <p className="text-xs font-medium text-muted-foreground px-2">
                          Active
                        </p>
                      </div>
                      {mockActiveProjects.map(project => (
                        <Link
                          key={project.slug}
                          href={`/weeks/week-0${project.weekNumber}/project`}
                          className="flex items-center gap-2 rounded-md px-2 py-1.5 text-sm text-muted-foreground hover:bg-accent hover:text-accent-foreground transition-colors"
                        >
                          {project.status === 'in_progress' ? (
                            <Play className="h-3 w-3 text-blue-500" />
                          ) : project.status === 'submitted' ? (
                            <CheckCircle2 className="h-3 w-3 text-green-500" />
                          ) : (
                            <Circle className="h-3 w-3" />
                          )}
                          <span className="truncate">{project.title}</span>
                        </Link>
                      ))}
                    </>
                  )}
                </div>
              </CollapsibleContent>
            </Collapsible>
          ) : (
            <SidebarItem
              href="/projects"
              icon={FolderGit2}
              label="Projects"
              collapsed={collapsed}
              active={pathname.startsWith('/projects') || pathname.includes('/project')}
            />
          )}
        </nav>

        {!collapsed && (
          <>
            <Separator className="my-4" />
            <WeekNavigator weeks={weeks} />
          </>
        )}
      </ScrollArea>

      {/* Footer */}
      <div className="border-t p-2 space-y-2">
        <SidebarItem
          href="/search"
          icon={Search}
          label="Search"
          collapsed={collapsed}
          active={pathname === '/search'}
        />
        <SidebarItem
          href="/settings"
          icon={Settings}
          label="Settings"
          collapsed={collapsed}
          active={pathname === '/settings'}
        />
        <SidebarItem
          href="/auth/login"
          icon={LogIn}
          label="Sign In"
          collapsed={collapsed}
          active={pathname === '/auth/login'}
        />
      </div>
    </div>
  );
}

interface SidebarItemProps {
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  label: string;
  collapsed: boolean;
  active: boolean;
  onClick?: () => void;
}

function SidebarItem({ href, icon: Icon, label, collapsed, active, onClick }: SidebarItemProps) {
  return (
    <Link
      href={href}
      onClick={onClick}
      className={cn(
        'flex items-center gap-3 rounded-md px-2 py-2 text-sm font-medium transition-colors',
        active
          ? 'bg-accent text-accent-foreground'
          : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground',
        collapsed && 'justify-center'
      )}
    >
      <Icon className="h-4 w-4 shrink-0" />
      {!collapsed && <span>{label}</span>}
    </Link>
  );
}
