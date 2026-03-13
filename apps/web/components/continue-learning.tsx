"use client";

import * as React from "react";
import Link from "next/link";
import { Play, Clock, ChevronRight } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useVisitedItems } from "@/hooks/use-visited-items";
import { formatRelativeTime, cn } from "@/lib/utils";

interface ContinueLearningWidgetProps {
  className?: string;
}

export function ContinueLearningWidget({ className }: ContinueLearningWidgetProps) {
  const { visitedItems } = useVisitedItems();
  const lastVisited = visitedItems[0];

  if (!lastVisited) {
    return null;
  }

  const getTypeLabel = (type: string) => {
    switch (type) {
      case "week":
        return "Week";
      case "day":
        return "Day";
      case "problem":
        return "Problem";
      case "theory":
        return "Theory";
      default:
        return "Content";
    }
  };

  return (
    <Card className={cn("overflow-hidden", className)}>
      <CardHeader className="bg-gradient-to-r from-primary/10 to-primary/5 pb-4">
        <CardTitle className="text-base flex items-center gap-2">
          <Play className="h-4 w-4 text-primary" />
          Continue Learning
        </CardTitle>
      </CardHeader>
      <CardContent className="pt-4">
        <div className="space-y-3">
          <div>
            <p className="text-xs text-muted-foreground uppercase tracking-wide">
              {getTypeLabel(lastVisited.type)}
            </p>
            <h3 className="font-semibold text-lg mt-0.5">{lastVisited.title}</h3>
          </div>

          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Clock className="h-4 w-4" />
            <span>Visited {formatRelativeTime(lastVisited.visitedAt)}</span>
          </div>

          <Button asChild className="w-full">
            <Link href={lastVisited.url}>
              Resume
              <ChevronRight className="ml-1 h-4 w-4" />
            </Link>
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
