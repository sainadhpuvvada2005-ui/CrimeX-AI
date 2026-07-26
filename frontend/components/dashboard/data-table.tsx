import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const rows = [
  ["FIR-2026-01842", "Bengaluru City", "High", "Under Review"],
  ["FIR-2026-01809", "Mysuru", "Medium", "Assigned"],
  ["FIR-2026-01776", "Mangaluru", "Critical", "Escalated"],
  ["FIR-2026-01721", "Hubballi", "Low", "Closed"],
];

export function DataTable({ title = "Priority Case Queue" }: { title?: string }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[560px] text-left text-sm">
            <thead className="text-xs uppercase text-muted-foreground">
              <tr>
                <th className="pb-3">Case</th>
                <th className="pb-3">Unit</th>
                <th className="pb-3">Gravity</th>
                <th className="pb-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {rows.map((row) => (
                <tr key={row[0]}>
                  {row.map((cell, index) => (
                    <td key={cell} className="py-3">
                      {index === 2 ? <Badge>{cell}</Badge> : cell}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  );
}

