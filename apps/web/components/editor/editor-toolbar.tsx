"use client";

import { useCallback } from "react";
import {
  RotateCcw,
  Save,
  Type,
  Sun,
  Moon,
  WrapText,
  Play,
  Settings,
} from "lucide-react";
import { useTheme } from "next-themes";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Separator } from "@/components/ui/separator";

export interface EditorToolbarProps {
  /** Whether code has unsaved changes */
  hasUnsavedChanges?: boolean;
  /** Current font size */
  fontSize?: number;
  /** Current word wrap state */
  wordWrap?: boolean;
  /** Called when reset is clicked */
  onReset?: () => void;
  /** Called when save is clicked */
  onSave?: () => void;
  /** Called when run is clicked */
  onRun?: () => void;
  /** Called when font size changes */
  onFontSizeChange?: (size: number) => void;
  /** Called when word wrap toggles */
  onWordWrapChange?: (enabled: boolean) => void;
  /** Custom class name */
  className?: string;
}

const FONT_SIZES = [12, 13, 14, 15, 16, 17, 18, 20, 22, 24];

export function EditorToolbar({
  hasUnsavedChanges = false,
  fontSize = 14,
  wordWrap = true,
  onReset,
  onSave,
  onRun,
  onFontSizeChange,
  onWordWrapChange,
  className,
}: EditorToolbarProps) {
  const { theme, setTheme, systemTheme } = useTheme();

  const effectiveTheme = theme === "system" ? systemTheme : theme;
  const isDark = effectiveTheme === "dark";

  const toggleTheme = useCallback(() => {
    setTheme(isDark ? "light" : "dark");
  }, [isDark, setTheme]);

  const handleFontSizeSelect = useCallback(
    (size: number) => {
      onFontSizeChange?.(size);
    },
    [onFontSizeChange]
  );

  return (
    <TooltipProvider delayDuration={100}>
      <div
        className={cn(
          "flex items-center gap-1 px-2 py-1.5",
          "bg-muted/50 border-b border-border",
          "rounded-t-md",
          className
        )}
      >
        {/* Action buttons */}
        <Tooltip>
          <TooltipTrigger asChild>
            <Button
              variant="ghost"
              size="sm"
              onClick={onReset}
              className="h-8 px-2"
            >
              <RotateCcw className="h-4 w-4" />
              <span className="sr-only">Reset to starter code</span>
            </Button>
          </TooltipTrigger>
          <TooltipContent>
            <p>Reset to starter code</p>
          </TooltipContent>
        </Tooltip>

        <Tooltip>
          <TooltipTrigger asChild>
            <Button
              variant="ghost"
              size="sm"
              onClick={onSave}
              disabled={!hasUnsavedChanges}
              className="h-8 px-2"
            >
              <Save
                className={cn(
                  "h-4 w-4",
                  hasUnsavedChanges && "text-yellow-500"
                )}
              />
              <span className="sr-only">Save draft</span>
            </Button>
          </TooltipTrigger>
          <TooltipContent>
            <p>Save draft {hasUnsavedChanges && "(unsaved changes)"}</p>
          </TooltipContent>
        </Tooltip>

        <Separator orientation="vertical" className="h-6 mx-1" />

        {/* Run button */}
        <Tooltip>
          <TooltipTrigger asChild>
            <Button
              variant="default"
              size="sm"
              onClick={onRun}
              className="h-8 px-3 gap-1.5"
            >
              <Play className="h-4 w-4" />
              <span className="hidden sm:inline text-xs">Run</span>
              <kbd className="hidden md:inline-flex h-5 items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground ml-1">
                <span className="text-xs">⌘</span>Enter
              </kbd>
            </Button>
          </TooltipTrigger>
          <TooltipContent>
            <p>Run code (Ctrl+Enter)</p>
          </TooltipContent>
        </Tooltip>

        <div className="flex-1" />

        {/* Settings dropdown */}
        <DropdownMenu>
          <Tooltip>
            <TooltipTrigger asChild>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="sm" className="h-8 px-2">
                  <Settings className="h-4 w-4" />
                  <span className="sr-only">Editor settings</span>
                </Button>
              </DropdownMenuTrigger>
            </TooltipTrigger>
            <TooltipContent>
              <p>Editor settings</p>
            </TooltipContent>
          </Tooltip>
          <DropdownMenuContent align="end" className="w-48">
            <DropdownMenuLabel>Editor Settings</DropdownMenuLabel>
            <DropdownMenuSeparator />

            {/* Font size submenu */}
            <DropdownMenuLabel className="text-xs font-normal text-muted-foreground">
              Font Size: {fontSize}px
            </DropdownMenuLabel>
            {FONT_SIZES.map((size) => (
              <DropdownMenuItem
                key={size}
                onClick={() => handleFontSizeSelect(size)}
                className={cn(fontSize === size && "bg-accent")}
              >
                <Type className="mr-2 h-4 w-4" />
                <span>{size}px</span>
                {fontSize === size && (
                  <span className="ml-auto text-xs text-muted-foreground">
                    Active
                  </span>
                )}
              </DropdownMenuItem>
            ))}

            <DropdownMenuSeparator />

            {/* Word wrap toggle */}
            <DropdownMenuItem onClick={() => onWordWrapChange?.(!wordWrap)}>
              <WrapText className="mr-2 h-4 w-4" />
              <span>Word Wrap</span>
              <span
                className={cn(
                  "ml-auto text-xs",
                  wordWrap ? "text-green-500" : "text-muted-foreground"
                )}
              >
                {wordWrap ? "On" : "Off"}
              </span>
            </DropdownMenuItem>

            <DropdownMenuSeparator />

            {/* Theme toggle */}
            <DropdownMenuItem onClick={toggleTheme}>
              {isDark ? (
                <Sun className="mr-2 h-4 w-4" />
              ) : (
                <Moon className="mr-2 h-4 w-4" />
              )}
              <span>{isDark ? "Light Theme" : "Dark Theme"}</span>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>

        {/* Quick theme toggle */}
        <Tooltip>
          <TooltipTrigger asChild>
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleTheme}
              className="h-8 px-2"
            >
              {isDark ? (
                <Sun className="h-4 w-4" />
              ) : (
                <Moon className="h-4 w-4" />
              )}
              <span className="sr-only">
                {isDark ? "Switch to light theme" : "Switch to dark theme"}
              </span>
            </Button>
          </TooltipTrigger>
          <TooltipContent>
            <p>{isDark ? "Switch to light theme" : "Switch to dark theme"}</p>
          </TooltipContent>
        </Tooltip>

        {/* Quick word wrap toggle */}
        <Tooltip>
          <TooltipTrigger asChild>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onWordWrapChange?.(!wordWrap)}
              className={cn(
                "h-8 px-2",
                wordWrap && "bg-accent text-accent-foreground"
              )}
            >
              <WrapText className="h-4 w-4" />
              <span className="sr-only">
                {wordWrap ? "Disable word wrap" : "Enable word wrap"}
              </span>
            </Button>
          </TooltipTrigger>
          <TooltipContent>
            <p>{wordWrap ? "Disable word wrap" : "Enable word wrap"}</p>
          </TooltipContent>
        </Tooltip>
      </div>
    </TooltipProvider>
  );
}
