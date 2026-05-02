// TODO  MC8yOmFIVnBZMlhucUx2b2pZbmt1cm82VEhOVE1BPT06NjBmOGVmZjA=

import { cn } from "@/lib/utils";

function Skeleton({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="skeleton"
      className={cn("bg-primary/10 animate-pulse rounded-md", className)}
      {...props}
    />
  );
}

export { Skeleton };
// TODO  MS8yOmFIVnBZMlhucUx2b2pZbmt1cm82VEhOVE1BPT06NjBmOGVmZjA=
