'use client';

import { useEffect, useState } from 'react';
import { cn } from '@/lib/utils';
import { ScrollArea } from '@/components/ui/scroll-area';

interface TocItem {
  id: string;
  text: string;
  level: number;
}

interface TableOfContentsProps {
  content: string;
  className?: string;
}

export function TableOfContents({ content, className }: TableOfContentsProps) {
  const [toc, setToc] = useState<TocItem[]>([]);
  const [activeId, setActiveId] = useState<string>('');

  // Parse headings from markdown content
  useEffect(() => {
    const headings: TocItem[] = [];
    const lines = content.split('\n');
    
    for (const line of lines) {
      const match = line.match(/^(#{2,3})\s+(.+)$/);
      if (match) {
        const level = match[1].length;
        const text = match[2].trim();
        const id = text.toLowerCase().replace(/[^\w]+/g, '-');
        headings.push({ id, text, level });
      }
    }
    
    setToc(headings);
  }, [content]);

  // Track active heading on scroll
  useEffect(() => {
    if (toc.length === 0) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setActiveId(entry.target.id);
          }
        });
      },
      { rootMargin: '-100px 0px -80% 0px' }
    );

    toc.forEach((item) => {
      const element = document.getElementById(item.id);
      if (element) {
        observer.observe(element);
      }
    });

    return () => observer.disconnect();
  }, [toc]);

  const handleClick = (e: React.MouseEvent<HTMLAnchorElement>, id: string) => {
    e.preventDefault();
    const element = document.getElementById(id);
    if (element) {
      const offset = 100; // Account for header
      const elementPosition = element.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - offset;
      
      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
    }
  };

  if (toc.length === 0) {
    return null;
  }

  return (
    <div className={cn('hidden xl:block w-64 shrink-0', className)}>
      <div className="sticky top-24">
        <p className="font-semibold mb-3 text-sm text-muted-foreground uppercase tracking-wider">
          On this page
        </p>
        <ScrollArea className="h-[calc(100vh-200px)]">
          <nav className="space-y-1">
            {toc.map((item) => (
              <a
                key={item.id}
                href={`#${item.id}`}
                onClick={(e) => handleClick(e, item.id)}
                className={cn(
                  'block py-1.5 text-sm transition-colors hover:text-foreground',
                  item.level === 2 ? 'pl-0' : 'pl-4',
                  activeId === item.id 
                    ? 'text-primary font-medium' 
                    : 'text-muted-foreground'
                )}
              >
                {item.text}
              </a>
            ))}
          </nav>
        </ScrollArea>
      </div>
    </div>
  );
}
