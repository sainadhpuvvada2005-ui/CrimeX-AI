import { Layers, LocateFixed, MapPin } from "lucide-react";

import { SectionGrid } from "@/components/dashboard/section-grid";
import { AppShell } from "@/components/layout/app-shell";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

export default function GisMapPage() {
  return (
    <AppShell title="GIS Map" subtitle="Spatial crime intelligence, hotspots, and station-level overlays.">
      <div className="grid gap-5 xl:grid-cols-[1fr_340px]">
        <Card>
          <CardContent className="p-0">
            <div className="relative h-[68vh] min-h-[460px] overflow-hidden rounded-lg bg-[linear-gradient(135deg,rgba(219,234,254,0.85),rgba(15,23,42,0.15)),url('https://images.unsplash.com/photo-1524661135-423995f22d0b?auto=format&fit=crop&w=1600&q=80')] bg-cover bg-center dark:bg-[linear-gradient(135deg,rgba(15,23,42,0.92),rgba(37,99,235,0.22)),url('https://images.unsplash.com/photo-1524661135-423995f22d0b?auto=format&fit=crop&w=1600&q=80')]">
              <div className="absolute left-[28%] top-[36%] flex h-12 w-12 items-center justify-center rounded-full bg-red-600 text-white shadow-lg">
                <MapPin className="h-5 w-5" />
              </div>
              <div className="absolute left-[54%] top-[52%] flex h-10 w-10 items-center justify-center rounded-full bg-blue-700 text-white shadow-lg">
                <MapPin className="h-4 w-4" />
              </div>
              <div className="absolute bottom-4 left-4 flex gap-2">
                <Button variant="secondary">
                  <Layers className="h-4 w-4" />
                  Layers
                </Button>
                <Button>
                  <LocateFixed className="h-4 w-4" />
                  Focus
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
        <SectionGrid
          items={[
            { title: "Hotspots", description: "Density clusters under review.", metric: "126" },
            { title: "Geo Confidence", description: "Records with usable location quality.", metric: "91%" },
            { title: "Station Boundaries", description: "Operational overlay layers.", metric: "482" },
          ]}
        />
      </div>
    </AppShell>
  );
}

