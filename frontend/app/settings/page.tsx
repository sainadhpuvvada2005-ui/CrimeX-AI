import { Bell, Database, Moon, Shield } from "lucide-react";

import { SectionGrid } from "@/components/dashboard/section-grid";
import { AppShell } from "@/components/layout/app-shell";
import { ThemeToggle } from "@/components/layout/theme-toggle";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function SettingsPage() {
  return (
    <AppShell title="Settings" subtitle="Workspace preferences, security defaults, data connectors, and appearance.">
      <div className="grid gap-5 xl:grid-cols-[360px_1fr]">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Moon className="h-5 w-5 text-blue-700 dark:text-blue-200" />
              Appearance
            </CardTitle>
          </CardHeader>
          <CardContent className="flex items-center justify-between">
            <span className="text-sm text-muted-foreground">Dark mode</span>
            <ThemeToggle />
          </CardContent>
        </Card>
        <SectionGrid
          items={[
            { title: "Security", description: "Session timeout and MFA policy.", metric: "Strict" },
            { title: "Data Source", description: "Official FIR database connectivity.", metric: "PostgreSQL" },
            { title: "Notifications", description: "Alerts and escalation channels.", metric: "Active" },
          ]}
        />
      </div>
      <div className="mt-5 grid gap-4 md:grid-cols-3">
        {[Shield, Database, Bell].map((Icon, index) => (
          <Card key={index}>
            <CardContent className="flex items-center gap-3 p-5">
              <Icon className="h-5 w-5 text-blue-700 dark:text-blue-200" />
              <span className="text-sm font-medium">Configuration group {index + 1}</span>
            </CardContent>
          </Card>
        ))}
      </div>
    </AppShell>
  );
}

