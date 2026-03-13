"use client";

import * as React from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, BookOpen } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import searchIndex from "@/data/search-index.json";

export default function WeekPage() {
  const params = useParams();
  const weekId = parseInt(params.weekId as string, 10);

  const weekData = searchIndex.find(
    (item) => item.type === "week" && item.week === weekId
  );

  const days = searchIndex.filter(
    (item) => item.type === "day" && item.week === weekId
  );

  const problems = searchIndex.filter(
    (item) => item.type === "problem" && item.week === weekId
  );

  if (!weekData) {
    return (
      <div className="container mx-auto px-4 py-12">
        <h1 className="text-2xl font-bold">Week not found</h1>
        <Button asChild className="mt-4">
          <Link href="/weeks">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Weeks
          </Link>
        </Button>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl">
      <Button asChild variant="ghost" className="mb-6">
        <Link href="/weeks">
          <ArrowLeft className="mr-2 h-4 w-4" />
          All Weeks
        </Link>
      </Button>

      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">{weekData.title}</h1>
        <p className="text-muted-foreground">{weekData.description}</p>
      </div>

      <div className="grid md:grid-cols-2 gap-4 mb-8">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Days</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{days.length}</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Problems</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{problems.length}</p>
          </CardContent>
        </Card>
      </div>

      <h2 className="text-2xl font-bold mb-4">Days</h2>
      <div className="space-y-3">
        {days.map((day) => (
          <Link key={day.id} href={day.url}>
            <Card className="hover:shadow-sm transition-shadow">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium">{day.title}</h3>
                    <p className="text-sm text-muted-foreground">
                      {day.description}
                    </p>
                  </div>
                  <BookOpen className="h-5 w-5 text-muted-foreground" />
                </div>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
