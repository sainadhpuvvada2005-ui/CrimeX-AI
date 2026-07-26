"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  BarChart3,
  Bot,
  FileText,
  Fingerprint,
  Gauge,
  Map,
  Network,
  Settings,
  Shield,
  SlidersHorizontal,
  UserCog,
} from "lucide-react";

import { ThemeToggle } from "@/components/layout/theme-toggle";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const navigation = [
  { href: "/dashboard", label: "Dashboard", icon: Gauge },
  { href: "/analytics", label: "Analytics", icon: BarChart3 },
  { href: "/chatbot", label: "Chatbot", icon: Bot },
  { href: "/gis-map", label: "GIS Map", icon: Map },
  { href: "/criminal-network", label: "Network", icon: Network },
  { href: "/case-details", label: "Cases", icon: Fingerprint },
  { href: "/fir-management", label: "FIR Management", icon: FileText },
  { href: "/reports", label: "Reports", icon: FileText },
  { href: "/admin", label: "Admin", icon: UserCog },
  { href: "/settings", label: "Settings", icon: Settings },
];

export function AppShell({ children, title, subtitle }: { children: React.ReactNode; title: string; subtitle: string }) {
  const pathname = usePathname();

  return (
    <div className="min-h-screen">
      <aside className="fixed left-0 top-0 z-30 hidden h-screen w-72 border-r border-white/20 bg-white/72 p-4 backdrop-blur-2xl dark:border-white/10 dark:bg-slate-950/72 lg:block">
        <Link href="/dashboard" className="flex items-center gap-3 rounded-lg px-2 py-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-lg bg-blue-700 text-white shadow-lg shadow-blue-900/20">
            <Shield className="h-5 w-5" />
          </div>
          <div>
            <p className="text-sm font-bold tracking-normal">CrimeX AI</p>
            <p className="text-xs text-muted-foreground">KSP Intelligence Console</p>
          </div>
        </Link>
        <div className="mt-6 space-y-1">
          {navigation.map((item) => {
            const Icon = item.icon;
            const active = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex h-11 items-center gap-3 rounded-md px-3 text-sm font-medium transition",
                  active
                    ? "bg-blue-700 text-white shadow-lg shadow-blue-950/15"
                    : "text-muted-foreground hover:bg-blue-700/10 hover:text-foreground",
                )}
              >
                <Icon className="h-4 w-4" />
                {item.label}
              </Link>
            );
          })}
        </div>
      </aside>

      <div className="lg:pl-72">
        <header className="sticky top-0 z-20 border-b border-white/20 bg-white/68 backdrop-blur-2xl dark:border-white/10 dark:bg-slate-950/68">
          <div className="flex min-h-16 flex-wrap items-center justify-between gap-3 px-4 py-3 sm:px-6">
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-xl font-bold tracking-normal sm:text-2xl">{title}</h1>
                <Badge>Secure</Badge>
              </div>
              <p className="mt-1 text-sm text-muted-foreground">{subtitle}</p>
            </div>
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm">
                <SlidersHorizontal className="h-4 w-4" />
                Controls
              </Button>
              <ThemeToggle />
            </div>
          </div>
          <nav className="flex gap-2 overflow-x-auto px-4 pb-3 lg:hidden">
            {navigation.map((item) => {
              const Icon = item.icon;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    "flex h-10 shrink-0 items-center gap-2 rounded-md px-3 text-sm font-medium",
                    pathname === item.href ? "bg-blue-700 text-white" : "bg-white/50 dark:bg-slate-900/60",
                  )}
                >
                  <Icon className="h-4 w-4" />
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </header>
        <main className="px-4 py-5 sm:px-6">{children}</main>
      </div>
    </div>
  );
}

