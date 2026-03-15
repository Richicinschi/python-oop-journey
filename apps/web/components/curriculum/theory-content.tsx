'use client';

import { useEffect, useState, useCallback, type PropsWithChildren, type ComponentPropsWithoutRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import type { Components } from 'react-markdown';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Check, Copy } from 'lucide-react';

interface TheoryContentProps {
  content: string;
  className?: string;
}

interface CodeBlockProps {
  language: string;
  children: string;
}

// Code block component with copy functionality
function CodeBlock({ language, children }: CodeBlockProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = useCallback(async () => {
    await navigator.clipboard.writeText(children);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }, [children]);

  return (
    <div className="relative group my-6">
      <div className="absolute right-2 top-2 opacity-0 group-hover:opacity-100 transition-opacity z-10">
        <Button
          variant="secondary"
          size="icon"
          className="h-8 w-8"
          onClick={handleCopy}
        >
          {copied ? (
            <Check className="h-4 w-4 text-green-500" />
          ) : (
            <Copy className="h-4 w-4" />
          )}
        </Button>
      </div>
      <div className="text-xs text-muted-foreground absolute left-4 top-2 font-mono">
        {language}
      </div>
      <pre className="rounded-lg bg-muted p-4 pt-10 overflow-x-auto">
        <code className="text-sm font-mono">{children}</code>
      </pre>
    </div>
  );
}

// Type for code component props
interface CodeComponentProps extends ComponentPropsWithoutRef<'code'> {
  inline?: boolean;
  className?: string;
}

// Type for heading component props
interface HeadingComponentProps extends PropsWithChildren {
  id?: string;
}

// Type for link component props
interface LinkComponentProps extends ComponentPropsWithoutRef<'a'> {
  href?: string;
}

// Custom components for ReactMarkdown
const components: Components = {
  code({ inline, className, children, ...props }: CodeComponentProps) {
    const match = /language-(\w+)/.exec(className || '');
    const language = match ? match[1] : 'text';
    const codeString = String(children).replace(/\n$/, '');

    if (inline) {
      return (
        <code 
          className="px-1.5 py-0.5 rounded bg-muted font-mono text-sm" 
          {...props}
        >
          {children}
        </code>
      );
    }

    return <CodeBlock language={language}>{codeString}</CodeBlock>;
  },
  h1({ children }: HeadingComponentProps) {
    const id = children?.toString().toLowerCase().replace(/[^\w]+/g, '-');
    return (
      <h1 
        id={id}
        className="text-3xl font-bold mt-8 mb-4 scroll-mt-20"
      >
        {children}
      </h1>
    );
  },
  h2({ children }: HeadingComponentProps) {
    const id = children?.toString().toLowerCase().replace(/[^\w]+/g, '-');
    return (
      <h2 
        id={id}
        className="text-2xl font-semibold mt-10 mb-4 scroll-mt-20 border-b pb-2"
      >
        {children}
      </h2>
    );
  },
  h3({ children }: HeadingComponentProps) {
    const id = children?.toString().toLowerCase().replace(/[^\w]+/g, '-');
    return (
      <h3 
        id={id}
        className="text-xl font-semibold mt-8 mb-3 scroll-mt-20"
      >
        {children}
      </h3>
    );
  },
  h4({ children }: PropsWithChildren) {
    return <h4 className="text-lg font-semibold mt-6 mb-2">{children}</h4>;
  },
  p({ children }: PropsWithChildren) {
    return <p className="leading-7 mb-4">{children}</p>;
  },
  ul({ children }: PropsWithChildren) {
    return <ul className="list-disc pl-6 mb-4 space-y-1">{children}</ul>;
  },
  ol({ children }: PropsWithChildren) {
    return <ol className="list-decimal pl-6 mb-4 space-y-1">{children}</ol>;
  },
  li({ children }: PropsWithChildren) {
    return <li className="leading-7">{children}</li>;
  },
  blockquote({ children }: PropsWithChildren) {
    return (
      <blockquote className="border-l-4 border-primary pl-4 italic my-6 text-muted-foreground">
        {children}
      </blockquote>
    );
  },
  table({ children }: PropsWithChildren) {
    return (
      <div className="overflow-x-auto my-6 rounded-lg border">
        <table className="w-full border-collapse">
          {children}
        </table>
      </div>
    );
  },
  thead({ children }: PropsWithChildren) {
    return <thead className="bg-muted">{children}</thead>;
  },
  th({ children }: PropsWithChildren) {
    return (
      <th className="border-b px-4 py-3 text-left font-semibold">
        {children}
      </th>
    );
  },
  td({ children }: PropsWithChildren) {
    return (
      <td className="border-b px-4 py-3">
        {children}
      </td>
    );
  },
  hr() {
    return <hr className="my-8 border-border" />;
  },
  a({ href, children, ...props }: LinkComponentProps) {
    return (
      <a 
        href={href}
        className="text-primary underline hover:text-primary/80 font-medium"
        target={href?.startsWith('http') ? '_blank' : undefined}
        rel={href?.startsWith('http') ? 'noopener noreferrer' : undefined}
        {...props}
      >
        {children}
      </a>
    );
  },
  strong({ children }: PropsWithChildren) {
    return <strong className="font-semibold text-foreground">{children}</strong>;
  },
  em({ children }: PropsWithChildren) {
    return <em className="italic">{children}</em>;
  },
};

export function TheoryContent({ content, className }: TheoryContentProps) {
  // Restore scroll position if available
  useEffect(() => {
    const savedPosition = sessionStorage.getItem('theory-scroll-position');
    if (savedPosition) {
      window.scrollTo(0, parseInt(savedPosition, 10));
      sessionStorage.removeItem('theory-scroll-position');
    }
  }, []);

  // Save scroll position before unload
  useEffect(() => {
    const handleBeforeUnload = () => {
      sessionStorage.setItem('theory-scroll-position', window.scrollY.toString());
    };
    window.addEventListener('beforeunload', handleBeforeUnload);
    return () => window.removeEventListener('beforeunload', handleBeforeUnload);
  }, []);

  return (
    <div className={cn('theory-content', className)}>
      <ReactMarkdown 
        remarkPlugins={[remarkGfm]}
        components={components}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
