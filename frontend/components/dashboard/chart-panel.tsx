"use client";

import { motion } from "framer-motion";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

const bars = [42, 64, 51, 78, 66, 84, 72, 58, 91, 73, 69, 88];

export function ChartPanel({ title, description }: { title: string; description: string }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex h-56 items-end gap-2">
          {bars.map((height, index) => (
            <motion.div
              key={index}
              initial={{ height: 0 }}
              animate={{ height: `${height}%` }}
              transition={{ delay: index * 0.035, duration: 0.45 }}
              className="min-w-0 flex-1 rounded-t-md bg-gradient-to-t from-blue-800 to-sky-400"
            />
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

