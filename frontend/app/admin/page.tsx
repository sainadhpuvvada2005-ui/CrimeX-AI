"use client";

import { KeyRound, ShieldCheck, UserCog } from "lucide-react";

import { DataTable } from "@/components/dashboard/data-table";
import { StatCard } from "@/components/dashboard/stat-card";
import { AppShell } from "@/components/layout/app-shell";

export default function AdminPage() {
  return (
    <AppShell title="Admin" subtitle="Users, roles, jurisdiction policies, and system governance.">
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        <StatCard label="Active Users" value="2,184" trend="MFA enabled" icon={UserCog} />
        <StatCard label="RBAC Policies" value="48" trend="department approved" icon={ShieldCheck} />
        <StatCard label="API Keys" value="12" trend="rotated on schedule" icon={KeyRound} />
      </div>
      <div className="mt-5">
        <DataTable title="Administrative Review Queue" />
      </div>
    </AppShell>
  );
}
