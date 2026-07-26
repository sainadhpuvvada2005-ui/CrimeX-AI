"use client";

import { BarChart3, Clock, Scale, TrendingUp } from "lucide-react";

import { ChartPanel } from "@/components/dashboard/chart-panel";
import { SectionGrid } from "@/components/dashboard/section-grid";
import { StatCard } from "@/components/dashboard/stat-card";
import { AppShell } from "@/components/layout/app-shell";

export default function AnalyticsPage() {
  return (
    <AppShell title="Crime Analytics" subtitle="District, unit, crime head, gravity, and time-series analysis.">
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Detection Rate" value="72.4%" trend="+2.8% vs last quarter" icon={TrendingUp} />
        <StatCard label="Avg Case Age" value="41d" trend="down by 6 days" icon={Clock} />
        <StatCard label="Gravity Index" value="8.1" trend="critical band monitored" icon={Scale} />
        <StatCard label="Analytics Jobs" value="36" trend="all completed" icon={BarChart3} />
      </div>
      <div className="mt-5">
        <ChartPanel title="Crime Head Distribution" description="Aggregated view from official FIR records." />
      </div>
      <div className="mt-5">
        <SectionGrid
          items={[
            { title: "District Comparison", description: "Normalized FIR load by district.", metric: "31 units" },
            { title: "Crime Sub Head Drilldown", description: "Granular category movement.", metric: "214 groups" },
            { title: "Case Gravity Mix", description: "Severity and priority distribution.", metric: "4 bands" },
          ]}
        />
      </div>
    </AppShell>
  );
}
