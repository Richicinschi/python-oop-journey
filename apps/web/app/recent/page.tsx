"use client";

import * as React from "react";
import Link from "next/link";
import { Clock, Trash2, ArrowRight, Calendar } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { useVisitedItems } from "@/hooks/use-visited-items";
import { groupByDate, formatRelativeTime, cn } from "@/lib/utils";
import type { VisitedItem } from "@repo/types";

export default function RecentPage() {
  const { visitedItems, removeVisitedItem, clearVisitedItems } = useVisitedItems();

  const grouped = groupByDate(visitedItems);

  const groupLabels: Record<string, string> = {
    today: "Today",
    yesterday: "Yesterday",
    thisWeek: "This Week",
    older: "Earlier",
  };

  const groupOrder = ["today", "yesterday", "thisWeek", "older"];

  if (visitedItems.length === 0) {
    return (
      <div className="container mx-auto px-4 py-12 max-w-4xl">
        <div className="text-center">
          <Clock className="h-12 w-12 mx-auto text-muted-foreground/50 mb-4" />
          <h1 className="text-2xl font-bold mb-2">No Recent Activity</h1>
          <p className="text-muted-foreground mb-6">
            Start exploring the curriculum to see your recently visited content here.
          </p>
          <Button asChild>
            <Link href="/weeks">Browse Curriculum</Link>
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold mb-2">Recently Visited</h1>
          <p className="text-muted-foreground">
            {visitedItems.length} items in your history
          </p>
        </div>
        <Button variant="destructive" size="sm" onClick={clearVisitedItems}>
          <Trash2 className="h-4 w-4 mr-2" />
          Clear History
        </Button>
      </div>

      {/* Grouped Items */}
      <div className="space-y-8">
        {groupOrder.map((groupKey) => {
          const items = grouped[groupKey];
          if (!items || items.length === 0) return null;

          return (
            <section key={groupKey}>
              <h2 className="text-sm font-semibold text-muted-foreground uppercase tracking-wide mb-4">
                {groupLabels[groupKey]}
              </h2>
              <div className="space-y-2">
                {items.map((item) => (
                  <RecentItemCard
                    key={item.id}
                    item={item}
                    onRemove={() => removeVisitedItem(item.id)}
                  />
                ))}
              </div>
            </section>
          );
        })}
      </div>
    </div>
  );
}

function RecentItemCard({
  item,
  onRemove,
}: {
  item: VisitedItem;
  onRemove: () => void;
}) {
  const getTypeIcon = (type: VisitedItem["type"]) => {
    switch (type) {
      case "week":
        return <Calendar className="h-4 w-4" />;
      case "day":
        return <Calendar className="h-4 w-4" />;
      case "problem":
        return <ArrowRight className="h-4 w-4" />;
      case "theory":
        return <ArrowRight className="h-4 w-4" />;
      default:
        return <ArrowRight className="h-4 w-4" />;
    }
  };

  const getTypeLabel = (type: VisitedItem["type"]) => {
    return type.charAt(0).toUpperCase() + type.slice(1);
  };

  return (
    <Card className="group hover:shadow-sm transition-shadow">
      <CardContent className="p-4">
        <div className="flex items-center gap-4">
          <div className="p-2 rounded-lg bg-muted text-muted-foreground">
            {getTypeIcon(item.type)}
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <h3 className="font-medium truncate">{item.title}</h3>
              <span className="text-xs text-muted-foreground uppercase">
                {getTypeLabel(item.type)}
              </span>
            </div>
            <div className="flex items-center gap-3 mt-1 text-sm text-muted-foreground">
              <span>{formatRelativeTime(item.visitedAt)}</span>
              {item.week !== undefined && (
                <>
                  <span>·</span>
                  <span>Week {item.week}</span>
                  {item.day && <span>· Day {item.day}</span>}
                </>
              )}
            </div>
          </div>
          <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
            <Button variant="ghost" size="sm" onClick={onRemove}>
              <Trash2 className="h-4 w-4" />
            </Button>
            <Button asChild size="sm">
              <Link href={item.url}>
                View
                <ArrowRight className="ml-1 h-4 w-4" />
              </Link>
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
