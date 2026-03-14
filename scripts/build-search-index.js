#!/usr/bin/env node

/**
 * Search Index Generation Script
 * 
 * Scans the curriculum data and generates a search index for Fuse.js
 * Output: website-playground/apps/web/data/search-index.json
 */

const fs = require('fs');
const path = require('path');

const CURRICULUM_PATH = path.join(__dirname, '../../python-oop-journey-v2');
const OUTPUT_PATH = path.join(__dirname, '../apps/web/data/search-index.json');

// Week definitions
const WEEKS = [
  { id: 'week00', number: 0, title: 'Getting Started', slug: 'week-00-getting-started', difficulty: 'beginner' },
  { id: 'week01', number: 1, title: 'Fundamentals', slug: 'week-01-fundamentals', difficulty: 'beginner' },
  { id: 'week02', number: 2, title: 'Advanced Fundamentals', slug: 'week-02-advanced-fundamentals', difficulty: 'intermediate' },
  { id: 'week03', number: 3, title: 'OOP Basics', slug: 'week-03-oop-basics', difficulty: 'intermediate' },
  { id: 'week04', number: 4, title: 'OOP Intermediate', slug: 'week-04-oop-intermediate', difficulty: 'intermediate' },
  { id: 'week05', number: 5, title: 'OOP Advanced', slug: 'week-05-oop-advanced', difficulty: 'advanced' },
  { id: 'week06', number: 6, title: 'Design Patterns', slug: 'week-06-design-patterns', difficulty: 'advanced' },
  { id: 'week07', number: 7, title: 'Real-World OOP', slug: 'week-07-real-world-oop', difficulty: 'advanced' },
  { id: 'week08', number: 8, title: 'Capstone Project', slug: 'week-08-capstone', difficulty: 'advanced' },
];

// Topic keywords mapping
const TOPIC_KEYWORDS = {
  'class': ['oop', 'object-oriented', 'class', 'blueprint', 'instance'],
  'inheritance': ['oop', 'inheritance', 'parent', 'child', 'base', 'derived', 'super'],
  'polymorphism': ['oop', 'polymorphism', 'override', 'interface', 'abstract'],
  'encapsulation': ['oop', 'encapsulation', 'private', 'public', 'protected'],
  'list': ['data-structures', 'list', 'array', 'sequence', 'collection'],
  'dictionary': ['data-structures', 'dictionary', 'dict', 'hash', 'map', 'key-value'],
  'tuple': ['data-structures', 'tuple', 'immutable', 'sequence'],
  'set': ['data-structures', 'set', 'unique', 'collection'],
  'string': ['strings', 'text', 'parsing', 'manipulation'],
  'function': ['functions', 'def', 'call', 'parameter', 'return', 'scope'],
  'loop': ['control-flow', 'loop', 'for', 'while', 'iteration'],
  'condition': ['control-flow', 'if', 'else', 'comparison', 'boolean'],
  'file': ['file-io', 'read', 'write', 'csv', 'json'],
  'exception': ['error-handling', 'exception', 'try', 'except', 'error'],
  'recursion': ['algorithms', 'recursion', 'recursive', 'base-case'],
  'sorting': ['algorithms', 'sort', 'sorted', 'ordering'],
  'searching': ['algorithms', 'search', 'find', 'binary-search'],
  'decorator': ['advanced', 'decorator', '@', 'wrapper'],
  'generator': ['advanced', 'generator', 'yield', 'iterator'],
  'comprehension': ['advanced', 'comprehension', 'list-comprehension'],
  'pattern': ['design-patterns', 'singleton', 'factory', 'observer'],
};

function extractProblemInfo(filePath, content, weekNum, dayNum) {
  const fileName = path.basename(filePath, '.py');
  const match = fileName.match(/problem_(\d+)_(.+)/);
  
  if (!match) return null;
  
  const problemNum = parseInt(match[1], 10);
  const problemSlug = match[2];
  
  // Extract function name and docstring
  const funcMatch = content.match(/def\s+(\w+)\s*\([^)]*\)(?:\s*->\s*[^:]+)?:\s*(?:"""|''')?\s*([\s\S]*?)(?:"""|'''|\n\n|\n(?:def|class)\s)/);
  const functionName = funcMatch ? funcMatch[1] : '';
  const docstring = funcMatch ? funcMatch[2].trim().substring(0, 200) : '';
  
  // Extract description from docstring or comments
  const commentMatch = content.match(/(?:#|"""|''')\s*(.+?)(?:\n|$)/);
  const description = docstring || (commentMatch ? commentMatch[1].trim() : '');
  
  // Determine difficulty based on problem number and content complexity
  let difficulty = 'easy';
  if (problemNum > 7) difficulty = 'hard';
  else if (problemNum > 4) difficulty = 'medium';
  
  // Check for specific patterns in code
  const topics = [];
  const keywords = [];
  
  // Check for OOP concepts
  if (content.includes('class ')) {
    topics.push('oop', 'classes');
    keywords.push('class', 'object', 'instance');
  }
  if (content.includes('def __')) {
    topics.push('dunder-methods', 'magic-methods');
    keywords.push('__init__', 'constructor', 'magic-method');
  }
  if (content.includes('@property')) {
    topics.push('properties', 'encapsulation');
    keywords.push('@property', 'getter', 'setter');
  }
  if (content.includes('@staticmethod')) {
    topics.push('static-methods');
    keywords.push('@staticmethod');
  }
  if (content.includes('@classmethod')) {
    topics.push('class-methods');
    keywords.push('@classmethod', 'cls');
  }
  if (content.includes('raise ')) {
    topics.push('exceptions');
    keywords.push('raise', 'exception', 'error');
  }
  if (content.includes('try:') || content.includes('except ')) {
    topics.push('error-handling');
    keywords.push('try', 'except', 'error-handling');
  }
  if (content.includes('with ')) {
    topics.push('context-managers');
    keywords.push('with', 'context-manager');
  }
  if (content.includes('yield ')) {
    topics.push('generators');
    keywords.push('yield', 'generator');
  }
  if (content.includes('lambda ')) {
    topics.push('lambda');
    keywords.push('lambda', 'anonymous-function');
  }
  if (content.includes('import ') || content.includes('from ')) {
    topics.push('modules');
    keywords.push('import', 'module', 'package');
  }
  
  // Data structures
  if (content.includes('list') || content.includes('[]')) {
    topics.push('lists');
    keywords.push('list', 'array');
  }
  if (content.includes('dict') || content.includes('{}')) {
    topics.push('dictionaries');
    keywords.push('dict', 'dictionary', 'hash-map');
  }
  if (content.includes('set(') || content.includes('{') && !content.includes('{}')) {
    topics.push('sets');
    keywords.push('set', 'unique');
  }
  if (content.includes('tuple') || content.match(/\([^)]*,[^)]+\)/)) {
    topics.push('tuples');
    keywords.push('tuple');
  }
  
  // Algorithms
  if (content.includes('for ') && (content.includes('range') || content.match(/for\s+\w+\s+in/))) {
    topics.push('loops', 'iteration');
    keywords.push('for', 'loop', 'iteration');
  }
  if (content.includes('while ')) {
    topics.push('loops');
    keywords.push('while', 'loop');
  }
  if (content.includes('if ') && content.includes('else')) {
    topics.push('conditionals');
    keywords.push('if', 'else', 'conditional');
  }
  if (content.includes('def ') && functionName && functionName.includes(functionName.toLowerCase())) {
    topics.push('functions');
    keywords.push('function', 'def', 'return');
  }
  if (content.includes('recurs')) {
    topics.push('recursion');
    keywords.push('recursion', 'recursive');
  }
  
  // Design patterns
  if (content.includes('abstract') || content.includes('ABC')) {
    topics.push('abstract-base-classes');
    keywords.push('abstract', 'ABC', 'base-class');
  }
  if (content.includes('dataclass')) {
    topics.push('dataclasses');
    keywords.push('@dataclass', 'data-class');
  }
  if (content.includes('enum') || content.includes('Enum')) {
    topics.push('enums');
    keywords.push('enum', 'enumeration');
  }
  if (content.includes('Protocol') || content.includes('TypedDict')) {
    topics.push('typing');
    keywords.push('protocol', 'typing', 'type-hints');
  }
  if (content.includes('Generic') || content.includes('TypeVar')) {
    topics.push('generics');
    keywords.push('generic', 'type-var', 'typing');
  }
  
  // File operations
  if (content.includes('open(') || content.includes('.read') || content.includes('.write')) {
    topics.push('file-io');
    keywords.push('file', 'read', 'write', 'open');
  }
  if (content.includes('csv')) {
    topics.push('csv');
    keywords.push('csv', 'comma-separated');
  }
  if (content.includes('json')) {
    topics.push('json');
    keywords.push('json', 'parse');
  }
  
  // Unique keywords
  const uniqueTopics = [...new Set(topics)];
  const uniqueKeywords = [...new Set(keywords)];
  
  return {
    id: `week${weekNum.toString().padStart(2, '0')}-day${dayNum.toString().padStart(2, '0')}-problem${problemNum.toString().padStart(2, '0')}`,
    type: 'problem',
    title: problemSlug.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
    slug: problemSlug,
    description: description,
    content: content.substring(0, 1000), // Limit content length
    week: weekNum,
    day: dayNum,
    difficulty: difficulty,
    topics: uniqueTopics,
    keywords: uniqueKeywords,
    url: `/weeks/${weekNum}/days/${dayNum}/problems/${problemNum}`,
    functionName: functionName,
  };
}

function scanDirectory(dirPath, weekNum, dayNum) {
  const items = [];
  
  if (!fs.existsSync(dirPath)) {
    return items;
  }
  
  const files = fs.readdirSync(dirPath);
  
  for (const file of files) {
    const filePath = path.join(dirPath, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory()) {
      // Recursively scan subdirectories
      items.push(...scanDirectory(filePath, weekNum, dayNum));
    } else if (file.endsWith('.py') && file.startsWith('problem_')) {
      try {
        const content = fs.readFileSync(filePath, 'utf-8');
        const info = extractProblemInfo(filePath, content, weekNum, dayNum);
        if (info) {
          items.push(info);
        }
      } catch (err) {
        console.warn(`Warning: Could not read ${filePath}:`, err.message);
      }
    }
  }
  
  return items;
}

function findDayDirectories(weekPath) {
  const days = [];
  
  if (!fs.existsSync(weekPath)) {
    return days;
  }
  
  const entries = fs.readdirSync(weekPath);
  
  for (const entry of entries) {
    const entryPath = path.join(weekPath, entry);
    const stat = fs.statSync(entryPath);
    
    if (stat.isDirectory()) {
      // Match day patterns like day01, day02, day1, exercises/day01, etc.
      const dayMatch = entry.match(/day0*(\d+)/i);
      if (dayMatch) {
        days.push({
          number: parseInt(dayMatch[1], 10),
          name: entry,
          path: entryPath,
        });
      }
      
      // Check for nested day directories in exercises, solutions folders
      if (entry === 'exercises' || entry === 'solutions' || entry === 'day01_exercises') {
        const subEntries = fs.readdirSync(entryPath);
        for (const subEntry of subEntries) {
          const subEntryPath = path.join(entryPath, subEntry);
          const subStat = fs.statSync(subEntryPath);
          if (subStat.isDirectory()) {
            const subDayMatch = subEntry.match(/day0*(\d+)/i);
            if (subDayMatch) {
              days.push({
                number: parseInt(subDayMatch[1], 10),
                name: subEntry,
                path: subEntryPath,
              });
            }
          }
        }
      }
    }
  }
  
  return days;
}

function buildSearchIndex() {
  console.log('Building search index...');
  console.log(`Curriculum path: ${CURRICULUM_PATH}`);
  
  const index = [];
  
  // Add weeks
  for (const week of WEEKS) {
    index.push({
      id: week.id,
      type: 'week',
      title: week.title,
      slug: week.slug,
      description: `Week ${week.number}: ${week.title}`,
      content: `Week ${week.number} covers ${week.title.toLowerCase()} topics and exercises.`,
      week: week.number,
      difficulty: week.difficulty,
      topics: [],
      keywords: ['week', `week-${week.number}`, week.title.toLowerCase()],
      url: `/weeks/${week.number}`,
    });
  }
  
  // Scan weeks for problems
  for (let weekNum = 0; weekNum <= 8; weekNum++) {
    const weekFolder = weekNum === 0 ? 'week00_getting_started' : `week0${weekNum}_fundamentals`;
    const weekPath = path.join(CURRICULUM_PATH, weekFolder);
    
    if (!fs.existsSync(weekPath)) {
      // Try alternative naming
      const altWeekFolder = weekNum === 0 ? 'week00' : `week0${weekNum}`;
      const altWeekPath = path.join(CURRICULUM_PATH, altWeekFolder);
      if (!fs.existsSync(altWeekPath)) {
        console.warn(`Week ${weekNum} not found at ${weekPath}`);
        continue;
      }
    }
    
    console.log(`Scanning Week ${weekNum}...`);
    
    // Find day directories
    const days = findDayDirectories(weekPath);
    const processedDays = new Set();
    
    for (const day of days) {
      if (processedDays.has(day.number)) {
        continue;
      }
      processedDays.add(day.number);
      
      // Add day entry
      index.push({
        id: `week${weekNum.toString().padStart(2, '0')}-day${day.number.toString().padStart(2, '0')}`,
        type: 'day',
        title: `Day ${day.number}`,
        slug: `day-${day.number}`,
        description: `Day ${day.number} exercises for Week ${weekNum}`,
        content: `Day ${day.number} covers various programming exercises and problems.`,
        week: weekNum,
        day: day.number,
        difficulty: weekNum < 2 ? 'beginner' : weekNum < 5 ? 'intermediate' : 'advanced',
        topics: [],
        keywords: ['day', `day-${day.number}`, `week-${weekNum}`],
        url: `/weeks/${weekNum}/days/${day.number}`,
      });
      
      // Scan for problems
      const problems = scanDirectory(day.path, weekNum, day.number);
      index.push(...problems);
      
      // Also check exercises and solutions subdirectories
      const exercisesPath = path.join(day.path, 'exercises');
      const solutionsPath = path.join(day.path, 'solutions');
      
      if (fs.existsSync(exercisesPath)) {
        index.push(...scanDirectory(exercisesPath, weekNum, day.number));
      }
      if (fs.existsSync(solutionsPath)) {
        index.push(...scanDirectory(solutionsPath, weekNum, day.number));
      }
    }
  }
  
  // Add topic entries
  const topicEntries = Object.entries(TOPIC_KEYWORDS);
  for (const [topic, keywords] of topicEntries) {
    index.push({
      id: `topic-${topic}`,
      type: 'topic',
      title: topic.charAt(0).toUpperCase() + topic.slice(1),
      slug: topic,
      description: `Problems and exercises related to ${topic}`,
      content: `Learn about ${topic} in Python OOP. Topics include: ${keywords.join(', ')}`,
      difficulty: 'intermediate',
      topics: [topic],
      keywords: keywords,
      url: `/topics/${topic}`,
    });
  }
  
  // Sort index by week and day
  index.sort((a, b) => {
    if (a.week !== undefined && b.week !== undefined) {
      if (a.week !== b.week) return a.week - b.week;
    }
    if (a.day !== undefined && b.day !== undefined) {
      return a.day - b.day;
    }
    return 0;
  });
  
  // Write index to file
  fs.writeFileSync(OUTPUT_PATH, JSON.stringify(index, null, 2));
  
  console.log(`\nSearch index built successfully!`);
  console.log(`Total items: ${index.length}`);
  console.log(`Weeks: ${index.filter(i => i.type === 'week').length}`);
  console.log(`Days: ${index.filter(i => i.type === 'day').length}`);
  console.log(`Problems: ${index.filter(i => i.type === 'problem').length}`);
  console.log(`Topics: ${index.filter(i => i.type === 'topic').length}`);
  console.log(`\nOutput: ${OUTPUT_PATH}`);
}

// Run if called directly
if (require.main === module) {
  buildSearchIndex();
}

module.exports = { buildSearchIndex };
