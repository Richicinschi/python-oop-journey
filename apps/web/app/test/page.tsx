'use client';

import {
  // Base Components
  Button,
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
  Badge,
  Separator,
  ScrollArea,
  Tabs,
  TabsList,
  TabsTrigger,
  TabsContent,
  Accordion,
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
  Tooltip,
  TooltipProvider,
  TooltipTrigger,
  TooltipContent,
  Skeleton,
  SkeletonText,
  SkeletonCard,
  // Navigation Components
  Sidebar,
  SidebarSection,
  SidebarItem,
  NavLink,
  NavGroup,
  Breadcrumbs,
  MobileNav,
  MobileNavSection,
  MobileNavItem,
  // Utilities
  cn,
} from '@oop-journey/ui';
import {
  Home,
  BookOpen,
  Code,
  Trophy,
  Settings,
  User,
  Menu,
  ChevronRight,
} from 'lucide-react';

export default function TestPage() {
  return (
    <TooltipProvider>
      <div className="min-h-screen bg-background">
        {/* Header */}
        <header className="border-b bg-background px-4 py-4">
          <div className="mx-auto max-w-7xl">
            <div className="flex items-center justify-between">
              <h1 className="text-2xl font-bold">UI Component Test</h1>
              <MobileNav
                header={<span className="font-bold">Navigation</span>}
              >
                <MobileNavSection title="Menu">
                  <MobileNavItem href="/" icon={<Home className="h-4 w-4" />} active>
                    Home
                  </MobileNavItem>
                  <MobileNavItem href="/curriculum" icon={<BookOpen className="h-4 w-4" />}>
                    Curriculum
                  </MobileNavItem>
                  <MobileNavItem href="/playground" icon={<Code className="h-4 w-4" />}>
                    Playground
                  </MobileNavItem>
                  <MobileNavItem href="/achievements" icon={<Trophy className="h-4 w-4" />}>
                    Achievements
                  </MobileNavItem>
                </MobileNavSection>
              </MobileNav>
            </div>
            <div className="mt-4">
              <Breadcrumbs
                items={[
                  { label: 'Home', href: '/' },
                  { label: 'Components', href: '/components' },
                  { label: 'Test Page' },
                ]}
              />
            </div>
          </div>
        </header>

        <div className="flex">
          {/* Sidebar */}
          <Sidebar
            header={<span className="font-bold text-lg">OOP Journey</span>}
            className="hidden lg:flex h-[calc(100vh-5rem)] sticky top-0"
          >
            <SidebarSection title="Navigation">
              <SidebarItem href="/" icon={<Home className="h-4 w-4" />} active>
                Home
              </SidebarItem>
              <SidebarItem href="/curriculum" icon={<BookOpen className="h-4 w-4" />}>
                Curriculum
              </SidebarItem>
              <SidebarItem href="/playground" icon={<Code className="h-4 w-4" />}>
                Playground
              </SidebarItem>
              <SidebarItem href="/achievements" icon={<Trophy className="h-4 w-4" />}>
                Achievements
              </SidebarItem>
            </SidebarSection>
            <SidebarSection title="Settings">
              <SidebarItem href="/profile" icon={<User className="h-4 w-4" />}>
                Profile
              </SidebarItem>
              <SidebarItem href="/settings" icon={<Settings className="h-4 w-4" />}>
                Settings
              </SidebarItem>
            </SidebarSection>
          </Sidebar>

          {/* Main Content */}
          <main className="flex-1 p-8">
            <div className="mx-auto max-w-4xl space-y-12">
              {/* Button Section */}
              <section>
                <h2 className="mb-4 text-xl font-semibold">Buttons</h2>
                <div className="flex flex-wrap gap-4">
                  <Button variant="primary">Primary</Button>
                  <Button variant="secondary">Secondary</Button>
                  <Button variant="ghost">Ghost</Button>
                  <Button variant="danger">Danger</Button>
                  <Button variant="outline">Outline</Button>
                  <Button variant="link">Link</Button>
                </div>
                <div className="mt-4 flex flex-wrap gap-4">
                  <Button size="sm">Small</Button>
                  <Button size="default">Default</Button>
                  <Button size="lg">Large</Button>
                  <Button size="icon">
                    <Settings className="h-4 w-4" />
                  </Button>
                </div>
              </section>

              <Separator />

              {/* Badge Section */}
              <section>
                <h2 className="mb-4 text-xl font-semibold">Badges</h2>
                <div className="flex flex-wrap gap-4">
                  <Badge>Default</Badge>
                  <Badge variant="secondary">Secondary</Badge>
                  <Badge variant="muted">Muted</Badge>
                  <Badge variant="outline">Outline</Badge>
                </div>
                <div className="mt-4 flex flex-wrap gap-4">
                  <Badge variant="beginner">Beginner</Badge>
                  <Badge variant="easy">Easy</Badge>
                  <Badge variant="medium">Medium</Badge>
                  <Badge variant="hard">Hard</Badge>
                  <Badge variant="challenge">Challenge</Badge>
                </div>
                <div className="mt-4 flex flex-wrap gap-4">
                  <Badge variant="not_started">Not Started</Badge>
                  <Badge variant="in_progress">In Progress</Badge>
                  <Badge variant="completed">Completed</Badge>
                  <Badge variant="locked">Locked</Badge>
                </div>
              </section>

              <Separator />

              {/* Card Section */}
              <section>
                <h2 className="mb-4 text-xl font-semibold">Cards</h2>
                <div className="grid gap-4 md:grid-cols-2">
                  <Card>
                    <CardHeader>
                      <CardTitle>Problem Title</CardTitle>
                      <CardDescription>
                        This is a description of the problem and what you need to accomplish.
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="flex gap-2">
                        <Badge variant="medium">Medium</Badge>
                        <Badge variant="in_progress">In Progress</Badge>
                      </div>
                    </CardContent>
                    <CardFooter className="gap-2">
                      <Button size="sm">Start</Button>
                      <Button variant="ghost" size="sm">
                        View Hints
                      </Button>
                    </CardFooter>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle>Week 1: Foundations</CardTitle>
                      <CardDescription>
                        Learn the basics of object-oriented programming in Python.
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span>Progress</span>
                          <span>3/7 days</span>
                        </div>
                        <div className="h-2 rounded-full bg-muted">
                          <div className="h-2 w-[43%] rounded-full bg-primary" />
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </section>

              <Separator />

              {/* Tabs Section */}
              <section>
                <h2 className="mb-4 text-xl font-semibold">Tabs</h2>
                <Tabs defaultValue="theory" className="w-full">
                  <TabsList className="grid w-full grid-cols-3">
                    <TabsTrigger value="theory">Theory</TabsTrigger>
                    <TabsTrigger value="code">Code</TabsTrigger>
                    <TabsTrigger value="tests">Tests</TabsTrigger>
                  </TabsList>
                  <TabsContent value="theory" className="rounded-md border p-4">
                    <h3 className="font-semibold">Object-Oriented Programming</h3>
                    <p className="mt-2 text-muted-foreground">
                      OOP is a programming paradigm based on the concept of &quot;objects&quot;,
                      which can contain data and code.
                    </p>
                  </TabsContent>
                  <TabsContent value="code" className="rounded-md border p-4">
                    <pre className="rounded bg-muted p-4 text-sm">
                      <code>{`class Person:
    def __init__(self, name):
        self.name = name`}</code>
                    </pre>
                  </TabsContent>
                  <TabsContent value="tests" className="rounded-md border p-4">
                    <p className="text-muted-foreground">Test results will appear here.</p>
                  </TabsContent>
                </Tabs>
              </section>

              <Separator />

              {/* Accordion Section */}
              <section>
                <h2 className="mb-4 text-xl font-semibold">Accordion</h2>
                <Accordion type="single" collapsible className="w-full">
                  <AccordionItem value="item-1">
                    <AccordionTrigger>What is a class?</AccordionTrigger>
                    <AccordionContent>
                      A class is a blueprint for creating objects. It defines the properties
                      and methods that the objects created from it will have.
                    </AccordionContent>
                  </AccordionItem>
                  <AccordionItem value="item-2">
                    <AccordionTrigger>What is an object?</AccordionTrigger>
                    <AccordionContent>
                      An object is an instance of a class. It contains real values instead
                      of variables and can perform actions defined by its class methods.
                    </AccordionContent>
                  </AccordionItem>
                  <AccordionItem value="item-3">
                    <AccordionTrigger>What is inheritance?</AccordionTrigger>
                    <AccordionContent>
                      Inheritance is a mechanism where a new class derives properties
                      and behaviors from an existing class.
                    </AccordionContent>
                  </AccordionItem>
                </Accordion>
              </section>

              <Separator />

              {/* Dialog Section */}
              <section>
                <h2 className="mb-4 text-xl font-semibold">Dialog</h2>
                <Dialog>
                  <DialogTrigger asChild>
                    <Button variant="outline">Open Dialog</Button>
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader>
                      <DialogTitle>Confirm Action</DialogTitle>
                      <DialogDescription>
                        Are you sure you want to submit your solution? This action cannot
                        be undone.
                      </DialogDescription>
                    </DialogHeader>
                    <DialogFooter>
                      <Button variant="outline">Cancel</Button>
                      <Button>Confirm</Button>
                    </DialogFooter>
                  </DialogContent>
                </Dialog>
              </section>

              <Separator />

              {/* Tooltip Section */}
              <section>
                <h2 className="mb-4 text-xl font-semibold">Tooltip</h2>
                <div className="flex gap-4">
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button variant="outline" size="icon">
                        <Home className="h-4 w-4" />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Go to home page</p>
                    </TooltipContent>
                  </Tooltip>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button variant="outline" size="icon">
                        <Settings className="h-4 w-4" />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Open settings</p>
                    </TooltipContent>
                  </Tooltip>
                </div>
              </section>

              <Separator />

              {/* Skeleton Section */}
              <section>
                <h2 className="mb-4 text-xl font-semibold">Skeleton Loading States</h2>
                <div className="grid gap-4 md:grid-cols-2">
                  <div className="space-y-4">
                    <Skeleton height={24} width="60%" />
                    <SkeletonText lines={3} />
                    <div className="flex gap-2">
                      <Skeleton height={32} width={80} rounded="sm" />
                      <Skeleton height={32} width={80} rounded="sm" />
                    </div>
                  </div>
                  <SkeletonCard />
                </div>
              </section>

              <Separator />

              {/* Navigation Link Section */}
              <section>
                <h2 className="mb-4 text-xl font-semibold">Navigation Links</h2>
                <NavGroup label="Main Navigation">
                  <NavLink href="/" active icon={<Home className="h-4 w-4" />}>
                    Home
                  </NavLink>
                  <NavLink href="/curriculum" icon={<BookOpen className="h-4 w-4" />}>
                    Curriculum
                  </NavLink>
                  <NavLink href="/playground" icon={<Code className="h-4 w-4" />}>
                    Playground
                  </NavLink>
                  <NavLink href="/achievements" icon={<Trophy className="h-4 w-4" />}>
                    Achievements
                  </NavLink>
                </NavGroup>
              </section>

              <Separator />

              {/* ScrollArea Section */}
              <section>
                <h2 className="mb-4 text-xl font-semibold">Scroll Area</h2>
                <ScrollArea className="h-[200px] w-full rounded-md border p-4">
                  <div className="space-y-4">
                    {Array.from({ length: 20 }).map((_, i) => (
                      <p key={i} className="text-sm">
                        Line {i + 1}: This is some content that demonstrates the
                        scrollable area functionality.
                      </p>
                    ))}
                  </div>
                </ScrollArea>
              </section>
            </div>
          </main>
        </div>
      </div>
    </TooltipProvider>
  );
}
