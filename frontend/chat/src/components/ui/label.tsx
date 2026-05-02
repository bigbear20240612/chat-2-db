import * as React from "react";
import * as LabelPrimitive from "@radix-ui/react-label";
// TODO  MC8yOmFIVnBZMlhucUx2b2pZbmt1cm82Tm1FNFpnPT06MTk4OWY0OWI=

import { cn } from "@/lib/utils";
// NOTE  MS8yOmFIVnBZMlhucUx2b2pZbmt1cm82Tm1FNFpnPT06MTk4OWY0OWI=

function Label({
  className,
  ...props
}: React.ComponentProps<typeof LabelPrimitive.Root>) {
  return (
    <LabelPrimitive.Root
      data-slot="label"
      className={cn(
        "flex items-center gap-2 text-sm leading-none font-medium select-none group-data-[disabled=true]:pointer-events-none group-data-[disabled=true]:opacity-50 peer-disabled:cursor-not-allowed peer-disabled:opacity-50",
        className,
      )}
      {...props}
    />
  );
}

export { Label };
