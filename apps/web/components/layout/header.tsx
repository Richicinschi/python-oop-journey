"use client";

import * as React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { BookOpen, Menu, X, FolderGit2, Code, Home, Clock } from "lucide-react";
import { Button } from "@/components/ui/button";
import { MobileSearchButton, SearchButton } from "@/components/search";
import { UserMenu } from "@/components/auth/user-menu";
import { cn } from "@/lib/utils";

interface HeaderProps {
  onSearchClick?: () => void;
}

const navLinks = [
  { href: "/", label: "Home" },
  { href: "/weeks", label: "Curriculum" },
  { href: "/projects", label: "Projects" },
  { href: "/problems", label: "Problems" },
  { href: "/recent", label: "Recent" },
];

export function Header({ onSearchClick }: HeaderProps) {
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);

  return (
    <header className="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto px-4 h-14 flex items-center">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 mr-8">
          <BookOpen className="h-6 w-6 text-primary" />
          <span className="font-bold text-lg hidden sm:inline">Python OOP</span>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center gap-6 flex-1">
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className={cn(
                "text-sm font-medium transition-colors hover:text-primary",
                pathname === link.href || (link.href !== '/' && pathname.startsWith(link.href))
                  ? "text-foreground"
                  : "text-muted-foreground"
              )}
            >
              {link.label}
            </Link>
          ))}
        </nav>

        {/* Search, User Menu, and Mobile Menu */}
        <div className="flex items-center gap-2 ml-auto">
          <div className="hidden sm:block w-[200px] lg:w-[280px]">
            <SearchButton onClick={onSearchClick || (() => {})} />
          </div>
          <MobileSearchButton onClick={onSearchClick || (() => {})} className="sm:hidden" />

          {/* User Menu */}
          <UserMenu />

          {/* Mobile Menu Toggle */}
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? (
              <X className="h-5 w-5" />
            ) : (
              <Menu className="h-5 w-5" />
            )}
          </Button>
        </div>
      </div>

      {/* Mobile Navigation */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t">
          <nav className="container mx-auto px-4 py-4 flex flex-col gap-2">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setMobileMenuOpen(false)}
                className={cn(
                  "px-4 py-2 rounded-md text-sm font-medium transition-colors",
                  pathname === link.href || (link.href !== '/' && pathname.startsWith(link.href))
                    ? "bg-accent text-foreground"
                    : "text-muted-foreground hover:bg-accent hover:text-foreground"
                )}
              >
                {link.label}
              </Link>
            ))}
          </nav>
        </div>
      )}
    </header>
  );
}
