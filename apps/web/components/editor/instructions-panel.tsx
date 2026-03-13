'use client';

import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { ScrollArea } from '@/components/ui/scroll-area';
import { getDifficultyColor } from '@/lib/utils';
import {
  BookOpen,
  CheckCircle2,
  Clock,
  AlertTriangle,
  Lightbulb,
} from 'lucide-react';
import Link from 'next/link';
import { cn } from '@/lib/utils';

interface ProblemExample {
  input: string;
  output: string;
  explanation?: string;
}

interface InstructionsPanelProps {
  title: string;
  difficulty: string;
  topic: string;
  instructions: string;
  examples?: ProblemExample[];
  behaviorNotes?: string[];
  edgeCases?: string[];
  theoryLink?: string;
  isCompleted?: boolean;
  isStarted?: boolean;
}

export function InstructionsPanel({
  title,
  difficulty,
  topic,
  instructions,
  examples = [],
  behaviorNotes = [],
  edgeCases = [],
  theoryLink,
  isCompleted,
  isStarted,
}: InstructionsPanelProps) {
  // Parse instructions to extract sections
  const sections = parseInstructions(instructions);

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="p-6 border-b space-y-4">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1">
            <h1 className="text-2xl font-bold tracking-tight">{title}</h1>
            <div className="flex items-center gap-2 mt-2 flex-wrap">
              <Badge className={cn(getDifficultyColor(difficulty))}>
                {difficulty}
              </Badge>
              <Badge variant="outline">{topic}</Badge>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {isCompleted && (
              <Badge className="bg-green-500/10 text-green-600 border-green-500/20 gap-1">
                <CheckCircle2 className="h-3 w-3" />
                Completed
              </Badge>
            )}
            {!isCompleted && isStarted && (
              <Badge variant="secondary" className="gap-1">
                <Clock className="h-3 w-3" />
                In Progress
              </Badge>
            )}
          </div>
        </div>

        {theoryLink && (
          <Link
            href={theoryLink}
            className="inline-flex items-center gap-2 text-sm text-primary hover:underline"
          >
            <BookOpen className="h-4 w-4" />
            Read Theory First
          </Link>
        )}
      </div>

      {/* Content */}
      <ScrollArea className="flex-1">
        <div className="p-6 space-y-6">
          {/* Requirements Section */}
          {sections.requirements && (
            <div className="space-y-2">
              <h3 className="font-semibold flex items-center gap-2">
                <Lightbulb className="h-4 w-4" />
                Requirements
              </h3>
              <div className="text-sm text-muted-foreground leading-relaxed whitespace-pre-wrap">
                {sections.requirements}
              </div>
            </div>
          )}

          {/* Main Instructions */}
          {sections.description && (
            <div className="space-y-2">
              <h3 className="font-semibold">Problem Description</h3>
              <div className="text-sm text-muted-foreground leading-relaxed whitespace-pre-wrap">
                {sections.description}
              </div>
            </div>
          )}

          {/* Examples */}
          {examples.length > 0 && (
            <div className="space-y-3">
              <h3 className="font-semibold">Examples</h3>
              <div className="space-y-3">
                {examples.map((example, index) => (
                  <Card key={index} className="bg-muted/50">
                    <CardContent className="p-4 space-y-2">
                      <div className="text-sm">
                        <span className="font-medium">Input:</span>{' '}
                        <code className="bg-background px-1.5 py-0.5 rounded text-xs">
                          {example.input}
                        </code>
                      </div>
                      <div className="text-sm">
                        <span className="font-medium">Output:</span>{' '}
                        <code className="bg-background px-1.5 py-0.5 rounded text-xs">
                          {example.output}
                        </code>
                      </div>
                      {example.explanation && (
                        <div className="text-sm text-muted-foreground">
                          <span className="font-medium">Explanation:</span>{' '}
                          {example.explanation}
                        </div>
                      )}
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          )}

          {/* Behavior Notes */}
          {behaviorNotes.length > 0 && (
            <div className="space-y-2">
              <h3 className="font-semibold">Behavior Notes</h3>
              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1">
                {behaviorNotes.map((note, index) => (
                  <li key={index}>{note}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Edge Cases */}
          {edgeCases.length > 0 && (
            <div className="space-y-2">
              <h3 className="font-semibold flex items-center gap-2">
                <AlertTriangle className="h-4 w-4 text-yellow-500" />
                Edge Cases
              </h3>
              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1">
                {edgeCases.map((edgeCase, index) => (
                  <li key={index}>{edgeCase}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Raw Instructions (fallback) */}
          {!sections.requirements && !sections.description && (
            <div className="text-sm text-muted-foreground leading-relaxed whitespace-pre-wrap">
              {instructions}
            </div>
          )}
        </div>
      </ScrollArea>
    </div>
  );
}

function parseInstructions(instructions: string) {
  const sections: {
    description?: string;
    requirements?: string;
  } = {};

  // Try to extract requirements section
  const reqMatch = instructions.match(
    /Requirements:([\s\S]*?)(?=Examples:|Constraints:|$)/i
  );
  if (reqMatch) {
    sections.requirements = reqMatch[1].trim();
  }

  // Try to extract description (everything before Requirements)
  const descMatch = instructions.match(/([\s\S]*?)(?=Requirements:|$)/i);
  if (descMatch) {
    sections.description = descMatch[1].trim();
  }

  return sections;
}
