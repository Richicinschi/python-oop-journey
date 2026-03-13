/**
 * @oop-journey/ui
 * UI component library for the Python OOP Journey application
 */

// Styles
import './styles/globals.css';

// Utilities
export { cn, formatDuration, getDifficultyColor, getStatusColor } from './lib/utils';

// Base Components
export {
  Button,
  buttonVariants,
  type ButtonProps,
} from './components/button';

export {
  Card,
  CardHeader,
  CardFooter,
  CardTitle,
  CardDescription,
  CardContent,
} from './components/card';

export {
  Badge,
  badgeVariants,
  type BadgeProps,
} from './components/badge';

export { Separator } from './components/separator';

export {
  ScrollArea,
  ScrollBar,
} from './components/scroll-area';

export {
  Tabs,
  TabsList,
  TabsTrigger,
  TabsContent,
} from './components/tabs';

export {
  Accordion,
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from './components/accordion';

export {
  Dialog,
  DialogPortal,
  DialogOverlay,
  DialogClose,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogTitle,
  DialogDescription,
} from './components/dialog';

export {
  Tooltip,
  TooltipTrigger,
  TooltipContent,
  TooltipProvider,
} from './components/tooltip';

export {
  Skeleton,
  SkeletonText,
  SkeletonCard,
} from './components/skeleton';

// Navigation Components
export {
  Sidebar,
  SidebarSection,
  SidebarItem,
} from './components/navigation/sidebar';

export {
  NavLink,
  navLinkVariants,
  NavGroup,
  type NavLinkProps,
} from './components/navigation/nav-link';

export {
  Breadcrumbs,
  type BreadcrumbsProps,
  type BreadcrumbItem,
} from './components/navigation/breadcrumbs';

export {
  MobileNav,
  MobileNavSection,
  MobileNavItem,
} from './components/navigation/mobile-nav';
