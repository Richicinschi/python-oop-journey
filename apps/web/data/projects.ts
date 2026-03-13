/**
 * Sample Projects Data
 * 
 * These projects correspond to the weekly curriculum and provide
 * hands-on practice for each week's concepts.
 */

import { WeeklyProject } from '@/types/project';

export const sampleProjects: WeeklyProject[] = [
  // Week 1: Simple CLI Tool
  {
    slug: 'week-01-cli-calculator',
    title: 'CLI Calculator',
    description: 'Build a command-line calculator that performs basic arithmetic operations. Practice using variables, functions, and user input while creating a useful utility.',
    difficulty: 'beginner',
    estimatedHours: 2,
    week: 1,
    status: 'not_started',
    completedTasks: 0,
    totalTasks: 3,
  },
  // Week 2: Contact Book
  {
    slug: 'week-02-contact-book',
    title: 'Contact Book',
    description: 'Create a contact management system with add, search, update, and delete functionality. Practice working with dictionaries and file I/O.',
    difficulty: 'beginner',
    estimatedHours: 3,
    week: 2,
    status: 'not_started',
    completedTasks: 0,
    totalTasks: 4,
  },
  // Week 3: Bank Account
  {
    slug: 'week-03-bank-account',
    title: 'Bank Account Manager',
    description: 'Build a banking system with deposits, withdrawals, and transaction history. Master encapsulation and private attributes.',
    difficulty: 'intermediate',
    estimatedHours: 3,
    week: 3,
    status: 'not_started',
    completedTasks: 0,
    totalTasks: 4,
  },
  // Week 4: Library System
  {
    slug: 'week-04-library-system',
    title: 'Library Management System',
    description: 'Design a library system with books, patrons, and checkout tracking. Apply inheritance and composition principles.',
    difficulty: 'intermediate',
    estimatedHours: 4,
    week: 4,
    status: 'not_started',
    completedTasks: 0,
    totalTasks: 5,
  },
  // Week 5: Shape Drawing
  {
    slug: 'week-05-shape-drawing',
    title: 'Shape Drawing App',
    description: 'Create a polymorphic shape system with area calculations and drawing. Explore abstract classes and method overriding.',
    difficulty: 'intermediate',
    estimatedHours: 3,
    week: 5,
    status: 'not_started',
    completedTasks: 0,
    totalTasks: 4,
  },
  // Week 6: Custom Collection
  {
    slug: 'week-06-custom-collection',
    title: 'Custom Collection',
    description: 'Build your own list-like container with full iterator support. Master special methods and Python data model.',
    difficulty: 'advanced',
    estimatedHours: 4,
    week: 6,
    status: 'not_started',
    completedTasks: 0,
    totalTasks: 4,
  },
  // Week 7: Plugin System
  {
    slug: 'week-07-plugin-system',
    title: 'Plugin System',
    description: 'Design an extensible plugin architecture using design patterns. Apply Factory, Observer, and Strategy patterns.',
    difficulty: 'advanced',
    estimatedHours: 5,
    week: 7,
    status: 'not_started',
    completedTasks: 0,
    totalTasks: 5,
  },
  // Week 8: E-Commerce System
  {
    slug: 'week-08-ecommerce',
    title: 'E-Commerce System',
    description: 'Build a complete e-commerce backend with inventory, cart, and checkout. Apply all OOP principles in a capstone project.',
    difficulty: 'advanced',
    estimatedHours: 8,
    week: 8,
    status: 'not_started',
    completedTasks: 0,
    totalTasks: 6,
  },
];

// Helper function to get project by slug
export function getProjectBySlug(slug: string): WeeklyProject | undefined {
  return sampleProjects.find(p => p.slug === slug);
}

// Helper function to get projects by week
export function getProjectsByWeek(week: number): WeeklyProject[] {
  return sampleProjects.filter(p => p.week === week);
}
