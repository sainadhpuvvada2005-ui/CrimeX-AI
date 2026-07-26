import { GitBranch, Network, Search } from "lucide-react";

import { SectionGrid } from "@/components/dashboard/section-grid";
import { AppShell } from "@/components/layout/app-shell";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

export default function CriminalNetworkPage() {
  return (
    <AppShell title="Criminal Network" subtitle="Neo4j relationship exploration for accused, cases, vehicles, places, and associates.">
      <div className="grid gap-5 xl:grid-cols-[1fr_340px]">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Network className="h-5 w-5 text-blue-700 dark:text-blue-200" />
              Entity Graph
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="mb-4 flex gap-2">
              <Input placeholder="Search accused, FIR, phone, vehicle, or location" />
              <Button size="icon" aria-label="Search network">
                <Search className="h-4 w-4" />
              </Button>
            </div>
            <div className="relative h-[56vh] min-h-[420px] rounded-lg border border-white/20 bg-slate-950 text-white">
              {["FIR", "Accused", "Vehicle", "Location", "Associate"].map((label, index) => (
                <div
                  key={label}
                  className="absolute flex h-20 w-20 items-center justify-center rounded-full border border-sky-300/50 bg-blue-700/80 text-xs font-semibold shadow-lg shadow-blue-950/40"
                  style={{ left: `${18 + index * 15}%`, top: `${26 + (index % 2) * 24}%` }}
                >
                  {label}
                </div>
              ))}
              <GitBranch className="absolute left-1/2 top-1/2 h-24 w-24 -translate-x-1/2 -translate-y-1/2 text-sky-200/40" />
            </div>
          </CardContent>
        </Card>
        <SectionGrid
          items={[
            { title: "Connected Entities", description: "Nodes in current query scope.", metric: "1,842" },
            { title: "Strong Links", description: "Repeated co-occurrence signals.", metric: "318" },
            { title: "Paths Reviewed", description: "Audited investigative graph paths.", metric: "64" },
          ]}
        />
      </div>
    </AppShell>
  );
}

