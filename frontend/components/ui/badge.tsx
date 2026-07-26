import * as React from "react";

import { cn } from "@/lib/utils";

export function Badge({ className, ...props }: React.HTMLAttributes<HTMLSpanElement>) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-md border border-blue-500/20 bg-blue-600/10 px-2 py-1 text-xs font-semibold text-blue-700 dark:text-blue-200",
        className,
      )}
      {...props}
    />
  );
}

