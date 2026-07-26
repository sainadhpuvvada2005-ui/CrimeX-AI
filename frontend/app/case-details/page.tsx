"use client";

import { FileSearch, ShieldAlert, UserRound } from "lucide-react";

import { DataTable } from "@/components/dashboard/data-table";
import { SectionGrid } from "@/components/dashboard/section-grid";
import { StatCard } from "@/components/dashboard/stat-card";
import { AppShell } from "@/components/layout/app-shell";

export default function CaseDetailsPage() {
  return (
    <AppShell title="Case Details" subtitle="Role-aware FIR case lookup, related entities, and evidence references.">
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        <StatCard label="Case Files" value="18,420" trend="current authorized scope" icon={FileSearch} />
        <StatCard label="Accused Linked" value="32,816" trend="official records only" icon={UserRound} />
        <StatCard label="Sensitive Fields" value="Masked" trend="RBAC enforced" icon={ShieldAlert} />
      </div>
      <div className="mt-5 grid gap-5 xl:grid-cols-[1fr_360px]">
        <DataTable title="Case Search Results" />
        <SectionGrid
          items={[
            { title: "Victim Records", description: "Authorized related records.", metric: "4" },
            { title: "Act Sections", description: "Mapped legal provisions.", metric: "7" },
            { title: "Court Status", description: "Chargesheet and hearing status.", metric: "Active" },
          ]}
        />
      </div>
    </AppShell>
  );
}
