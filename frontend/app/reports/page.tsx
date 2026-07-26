import { Download, FileText, Printer } from "lucide-react";

import { DataTable } from "@/components/dashboard/data-table";
import { SectionGrid } from "@/components/dashboard/section-grid";
import { AppShell } from "@/components/layout/app-shell";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function ReportsPage() {
  return (
    <AppShell title="Reports" subtitle="PDF generation, audit-stamped exports, and command-ready summaries.">
      <div className="grid gap-5 xl:grid-cols-[360px_1fr]">
        <Card>
          <CardHeader>
            <CardTitle>Generate Report</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <Button className="w-full">
              <FileText className="h-4 w-4" />
              Crime Summary
            </Button>
            <Button className="w-full" variant="secondary">
              <Printer className="h-4 w-4" />
              District Brief
            </Button>
            <Button className="w-full" variant="outline">
              <Download className="h-4 w-4" />
              Export Queue
            </Button>
          </CardContent>
        </Card>
        <DataTable title="Recent PDF Reports" />
      </div>
      <div className="mt-5">
        <SectionGrid
          items={[
            { title: "Watermarked", description: "Every PDF carries officer and timestamp metadata.", metric: "100%" },
            { title: "Approval Required", description: "Bulk exports require supervisor review.", metric: "Enabled" },
            { title: "Retention", description: "Export history retained for audit.", metric: "365d" },
          ]}
        />
      </div>
    </AppShell>
  );
}

