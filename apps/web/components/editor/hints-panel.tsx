'use client';

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion';
import { Button } from '@/components/ui/button';
import { AIHintBadge, AIHintCard } from '@/components/ai/ai-hint';
import { useAIHints } from '@/hooks/use-ai-hints';
import { Lightbulb, Lock, Sparkles } from 'lucide-react';
import { useState } from 'react';
import { cn } from '@/lib/utils';

interface HintsPanelProps {
  hints: string[];
  revealedHints: number[];
  onRevealHint: (hintIndex: number) => void;
  problemSlug: string;
  code: string;
  testResults?: Record<string, unknown> | null;
  onHighlightLines?: (lines: number[]) => void;
}

export function HintsPanel({
  hints,
  revealedHints,
  onRevealHint,
  problemSlug,
  code,
  testResults,
  onHighlightLines,
}: HintsPanelProps) {
  const [openItems, setOpenItems] = useState<string[]>([]);
  const [showAIHint, setShowAIHint] = useState(false);

  const {
    hint,
    isLoadingHint,
    hintError,
    generateHint,
    requestNextLevelHint,
    clearHint,
    submitFeedback,
  } = useAIHints({
    problemSlug,
    code,
    testResults,
  });

  const handleValueChange = (value: string[]) => {
    // Check if a new item was opened
    const newlyOpened = value.find((v) => !openItems.includes(v));
    if (newlyOpened) {
      const hintIndex = Number(newlyOpened.replace('hint-', ''));
      // Check if previous hint is revealed (progressive reveal)
      if (hintIndex > 0 && !revealedHints.includes(hintIndex - 1)) {
        // Don't allow opening this hint yet
        return;
      }
      onRevealHint(hintIndex);
    }
    setOpenItems(value);
  };

  const getHintLabel = (index: number) => {
    switch (index) {
      case 0:
        return 'Conceptual Nudge';
      case 1:
        return 'Structural Guidance';
      case 2:
        return 'Edge Case Reminder';
      default:
        return `Hint ${index + 1}`;
    }
  };

  const getHintDescription = (index: number) => {
    switch (index) {
      case 0:
        return 'A gentle push in the right direction';
      case 1:
        return 'More specific guidance on implementation';
      case 2:
        return 'Watch out for these tricky cases';
      default:
        return '';
    }
  };

  const handleGetAIHint = async () => {
    setShowAIHint(true);
    if (!hint && !isLoadingHint) {
      await generateHint(1);
    }
  };

  const handleCloseAIHint = () => {
    setShowAIHint(false);
    clearHint();
  };

  const hasRevealedAllHints = hints.length > 0 && revealedHints.length >= hints.length;

  return (
    <div className="space-y-4">
      {/* Regular Hints Section */}
      {hints.length > 0 && (
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-sm font-medium text-muted-foreground px-1">
            <Lightbulb className="h-4 w-4" />
            <span>Hints ({revealedHints.length}/{hints.length} revealed)</span>
          </div>
          <Accordion
            type="multiple"
            value={openItems}
            onValueChange={handleValueChange}
            className="space-y-2"
          >
            {hints.map((hint, index) => {
              const isRevealed = revealedHints.includes(index);
              const isLocked = index > 0 && !revealedHints.includes(index - 1);
              const itemValue = `hint-${index}`;

              return (
                <AccordionItem
                  key={index}
                  value={itemValue}
                  className={cn(
                    'border rounded-lg px-3 data-[state=open]:border-primary/50',
                    isLocked && 'opacity-60'
                  )}
                >
                  <AccordionTrigger
                    className="py-3 hover:no-underline"
                    disabled={isLocked}
                  >
                    <div className="flex items-center gap-2 text-left">
                      {isLocked ? (
                        <Lock className="h-4 w-4 text-muted-foreground shrink-0" />
                      ) : (
                        <Lightbulb
                          className={cn(
                            'h-4 w-4 shrink-0',
                            isRevealed
                              ? 'text-yellow-500'
                              : 'text-muted-foreground'
                          )}
                        />
                      )}
                      <div>
                        <span className="font-medium">{getHintLabel(index)}</span>
                        <p className="text-xs text-muted-foreground font-normal">
                          {isLocked
                            ? 'Reveal previous hint first'
                            : getHintDescription(index)}
                        </p>
                      </div>
                    </div>
                  </AccordionTrigger>
                  <AccordionContent className="pb-3">
                    <div className="pl-6 text-sm text-muted-foreground leading-relaxed">
                      {hint}
                    </div>
                  </AccordionContent>
                </AccordionItem>
              );
            })}
          </Accordion>
        </div>
      )}

      {/* AI Hint Section */}
      <div className="space-y-3">
        {/* Show AI hint option when all hints are revealed or no hints available */}
        {(hasRevealedAllHints || hints.length === 0) && !showAIHint && (
          <div className="flex flex-col items-center gap-3 p-4 border border-dashed rounded-lg bg-muted/50">
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Sparkles className="h-4 w-4" />
              <span>
                {hints.length === 0
                  ? 'No built-in hints for this problem'
                  : 'Need more help?'}
              </span>
            </div>
            <AIHintBadge onClick={handleGetAIHint} isLoading={isLoadingHint} />
          </div>
        )}

        {/* Alternative: Always show AI hint button at bottom */}
        {!hasRevealedAllHints && hints.length > 0 && !showAIHint && (
          <div className="pt-2 border-t">
            <Button
              variant="ghost"
              size="sm"
              className="w-full gap-2 text-xs text-muted-foreground hover:text-primary"
              onClick={handleGetAIHint}
            >
              <Sparkles className="h-3.5 w-3.5" />
              Or get an AI-powered hint
            </Button>
          </div>
        )}

        {/* AI Hint Display */}
        {showAIHint && (
          <div className="animate-in fade-in slide-in-from-top-2">
            <AIHintCard
              hint={hint?.hint || ''}
              relevantLines={hint?.relevantLines || []}
              explanation={hint?.explanation || ''}
              hintLevel={hint?.hintLevel || 1}
              onClose={handleCloseAIHint}
              onFeedback={submitFeedback}
              onRequestAnother={hint && hint.hintLevel < 3 ? requestNextLevelHint : undefined}
              onHighlightLines={onHighlightLines}
              isLoading={isLoadingHint}
            />
            {hintError && (
              <div className="mt-2 p-3 text-xs text-red-500 bg-red-50 rounded border border-red-200">
                {hintError}
              </div>
            )}
          </div>
        )}
      </div>

      {hints.length === 0 && !showAIHint && (
        <div className="p-4 text-center text-muted-foreground text-sm">
          No hints available for this problem.
        </div>
      )}
    </div>
  );
}
