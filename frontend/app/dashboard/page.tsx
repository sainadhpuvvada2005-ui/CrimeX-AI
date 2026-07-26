"use client";

import { AlertTriangle, Database, MapPinned, ShieldCheck } from "lucide-react";

import { ChartPanel } from "@/components/dashboard/chart-panel";
import { DataTable } from "@/components/dashboard/data-table";
import { StatCard } from "@/components/dashboard/stat-card";
import { AppShell } from "@/components/layout/app-shell";

export default function DashboardPage() {
  return (
    <AppShell title="Command Dashboard" subtitle="Statewide operational summary and active intelligence posture.">
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Active FIR Records" value="1.28M" trend="+4.2% this month" icon={Database} />
        <StatCard label="Critical Cases" value="284" trend="37 escalated today" icon={AlertTriangle} />
        <StatCard label="Mapped Hotspots" value="126" trend="14 require review" icon={MapPinned} />
        <StatCard label="Audit Compliance" value="99.2%" trend="healthy access controls" icon={ShieldCheck} />
      </div>
      <div className="mt-5 grid gap-5 xl:grid-cols-[1.3fr_1fr]">
        <ChartPanel title="Crime Trend Index" description="Monthly FIR movement by registered crime categories." />
        <DataTable />
      </div>
    </AppShell>
  );
}
