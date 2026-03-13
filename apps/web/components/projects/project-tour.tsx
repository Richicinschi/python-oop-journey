'use client';

import { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { TourStep } from '@/types/project';
import { ChevronRight, ChevronLeft, X, Sparkles } from 'lucide-react';
import { cn } from '@/lib/utils';

const TOUR_STORAGE_KEY = 'oop-journey-project-tour-completed';

const defaultTourSteps: TourStep[] = [
  {
    id: 'welcome',
    title: 'Welcome to Project Mode! 🎉',
    content: 'This is where you\'ll build real applications. Let me show you around the workspace.',
    targetSelector: 'body',
    position: 'bottom',
  },
  {
    id: 'file-tree',
    title: 'File Explorer',
    content: 'Browse and manage your project files here. Click any file to open it in the editor. You can create new files and folders too!',
    targetSelector: '[data-tour="file-tree"]',
    position: 'right',
  },
  {
    id: 'editor',
    title: 'Code Editor',
    content: 'This is where you write your code. It has syntax highlighting, auto-completion, and error detection to help you code faster.',
    targetSelector: '[data-tour="editor"]',
    position: 'left',
  },
  {
    id: 'tabs',
    title: 'File Tabs',
    content: 'Open files appear as tabs. You can have multiple files open and switch between them easily. Unsaved changes are indicated with a dot.',
    targetSelector: '[data-tour="editor-tabs"]',
    position: 'bottom',
  },
  {
    id: 'run-button',
    title: 'Run Your Code',
    content: 'Click this button (or press Ctrl+R) to run your code and see the output. You can also run tests to check if your solution is correct.',
    targetSelector: '[data-tour="run-button"]',
    position: 'bottom',
  },
  {
    id: 'submit',
    title: 'Submit When Ready',
    content: 'Once you\'re happy with your project, click Submit. Your work will be saved and you can always come back to make improvements.',
    targetSelector: '[data-tour="submit-button"]',
    position: 'bottom',
  },
  {
    id: 'shortcuts',
    title: 'Keyboard Shortcuts',
    content: 'Speed up your workflow with shortcuts: Ctrl+S to save, Ctrl+R to run, Ctrl+T for tests, Ctrl+B to toggle the file tree.',
    targetSelector: 'body',
    position: 'bottom',
  },
];

interface ProjectTourProps {
  steps?: TourStep[];
  onComplete?: () => void;
  onSkip?: () => void;
  forceShow?: boolean;
}

export function ProjectTour({ 
  steps = defaultTourSteps,
  onComplete,
  onSkip,
  forceShow = false,
}: ProjectTourProps) {
  const [isVisible, setIsVisible] = useState(false);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [targetRect, setTargetRect] = useState<DOMRect | null>(null);

  const currentStep = steps[currentStepIndex];
  const isFirstStep = currentStepIndex === 0;
  const isLastStep = currentStepIndex === steps.length - 1;

  useEffect(() => {
    if (forceShow) {
      setIsVisible(true);
      return;
    }

    const hasCompleted = localStorage.getItem(TOUR_STORAGE_KEY);
    if (!hasCompleted) {
      // Delay showing the tour to let the page load
      const timer = setTimeout(() => setIsVisible(true), 500);
      return () => clearTimeout(timer);
    }
  }, [forceShow]);

  useEffect(() => {
    if (!isVisible || !currentStep) return;

    const updateTargetRect = () => {
      if (currentStep.targetSelector === 'body') {
        setTargetRect(null);
        return;
      }

      const element = document.querySelector(currentStep.targetSelector);
      if (element) {
        setTargetRect(element.getBoundingClientRect());
        // Highlight the element
        element.classList.add('tour-highlight');
      }
    };

    updateTargetRect();

    // Update on resize
    window.addEventListener('resize', updateTargetRect);
    
    // Cleanup highlight from previous step
    return () => {
      window.removeEventListener('resize', updateTargetRect);
      if (currentStep.targetSelector !== 'body') {
        const element = document.querySelector(currentStep.targetSelector);
        element?.classList.remove('tour-highlight');
      }
    };
  }, [isVisible, currentStep]);

  const handleNext = useCallback(() => {
    if (isLastStep) {
      handleComplete();
    } else {
      setCurrentStepIndex(prev => prev + 1);
    }
  }, [isLastStep]);

  const handlePrevious = useCallback(() => {
    setCurrentStepIndex(prev => Math.max(0, prev - 1));
  }, []);

  const handleComplete = useCallback(() => {
    localStorage.setItem(TOUR_STORAGE_KEY, 'true');
    setIsVisible(false);
    onComplete?.();
  }, [onComplete]);

  const handleSkip = useCallback(() => {
    localStorage.setItem(TOUR_STORAGE_KEY, 'true');
    setIsVisible(false);
    onSkip?.();
  }, [onSkip]);

  if (!isVisible || !currentStep) return null;

  // Calculate tooltip position
  const getTooltipStyle = (): React.CSSProperties => {
    if (!targetRect) {
      // Center on screen
      return {
        position: 'fixed',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        zIndex: 100,
      };
    }

    const tooltipWidth = 360;
    const tooltipHeight = 200;
    const offset = 16;

    let top = 0;
    let left = 0;

    switch (currentStep.position) {
      case 'top':
        top = targetRect.top - tooltipHeight - offset;
        left = targetRect.left + targetRect.width / 2 - tooltipWidth / 2;
        break;
      case 'bottom':
        top = targetRect.bottom + offset;
        left = targetRect.left + targetRect.width / 2 - tooltipWidth / 2;
        break;
      case 'left':
        top = targetRect.top + targetRect.height / 2 - tooltipHeight / 2;
        left = targetRect.left - tooltipWidth - offset;
        break;
      case 'right':
        top = targetRect.top + targetRect.height / 2 - tooltipHeight / 2;
        left = targetRect.right + offset;
        break;
    }

    // Keep within viewport
    const padding = 16;
    top = Math.max(padding, Math.min(top, window.innerHeight - tooltipHeight - padding));
    left = Math.max(padding, Math.min(left, window.innerWidth - tooltipWidth - padding));

    return {
      position: 'fixed',
      top,
      left,
      width: tooltipWidth,
      zIndex: 100,
    };
  };

  return (
    <>
      {/* Overlay */}
      <div 
        className="fixed inset-0 bg-black/40 z-50 transition-opacity"
        onClick={handleSkip}
      />

      {/* Spotlight around target */}
      {targetRect && (
        <div
          className="fixed z-50 pointer-events-none"
          style={{
            top: targetRect.top - 4,
            left: targetRect.left - 4,
            width: targetRect.width + 8,
            height: targetRect.height + 8,
            boxShadow: '0 0 0 9999px rgba(0, 0, 0, 0.4)',
            borderRadius: '8px',
          }}
        />
      )}

      {/* Tooltip */}
      <div style={getTooltipStyle()}>
        <Card className="shadow-2xl border-2 border-primary/20">
          <CardHeader className="pb-3">
            <div className="flex items-start justify-between gap-4">
              <div className="flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-primary" />
                <CardTitle className="text-lg">{currentStep.title}</CardTitle>
              </div>
              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8 shrink-0"
                onClick={handleSkip}
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
            <CardDescription className="text-base mt-2">
              {currentStep.content}
            </CardDescription>
            {currentStep.actionRequired && (
              <p className="text-sm font-medium text-primary mt-2">
                👉 {currentStep.actionRequired}
              </p>
            )}
          </CardHeader>
          <CardFooter className="flex items-center justify-between pt-0">
            <div className="flex items-center gap-1">
              {steps.map((_, index) => (
                <div
                  key={index}
                  className={cn(
                    'h-1.5 rounded-full transition-all',
                    index === currentStepIndex 
                      ? 'w-4 bg-primary' 
                      : 'w-1.5 bg-muted-foreground/30'
                  )}
                />
              ))}
            </div>
            <div className="flex items-center gap-2">
              {!isFirstStep && (
                <Button variant="ghost" size="sm" onClick={handlePrevious}>
                  <ChevronLeft className="h-4 w-4 mr-1" />
                  Back
                </Button>
              )}
              <Button size="sm" onClick={handleNext}>
                {isLastStep ? 'Get Started' : 'Next'}
                {!isLastStep && <ChevronRight className="h-4 w-4 ml-1" />}
              </Button>
            </div>
          </CardFooter>
        </Card>
      </div>

      {/* Add highlight styles */}
      <style jsx global>{`
        .tour-highlight {
          position: relative;
          z-index: 51;
        }
      `}</style>
    </>
  );
}

// Hook to check if tour should be shown
export function useProjectTour() {
  const [showTour, setShowTour] = useState(false);
  const [hasCompleted, setHasCompleted] = useState(true);

  useEffect(() => {
    const completed = localStorage.getItem(TOUR_STORAGE_KEY);
    setHasCompleted(!!completed);
  }, []);

  const startTour = useCallback(() => {
    setShowTour(true);
  }, []);

  const completeTour = useCallback(() => {
    localStorage.setItem(TOUR_STORAGE_KEY, 'true');
    setShowTour(false);
    setHasCompleted(true);
  }, []);

  const resetTour = useCallback(() => {
    localStorage.removeItem(TOUR_STORAGE_KEY);
    setHasCompleted(false);
  }, []);

  return {
    showTour,
    hasCompleted,
    startTour,
    completeTour,
    resetTour,
    TourComponent: showTour ? (
      <ProjectTour 
        onComplete={completeTour}
        onSkip={completeTour}
      />
    ) : null,
  };
}

// Mini tour button for settings/help
export function TourButton({ onClick }: { onClick?: () => void }) {
  return (
    <Button 
      variant="outline" 
      size="sm" 
      className="gap-2"
      onClick={onClick}
    >
      <Sparkles className="h-4 w-4" />
      Take Tour
    </Button>
  );
}
