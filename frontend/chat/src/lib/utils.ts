// @ts-expect-error  MC8yOmFIVnBZMlhucUx2b2pZbmt1cm82VFV4VWVBPT06M2JkNDIwYWM=

import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
// FIXME  MS8yOmFIVnBZMlhucUx2b2pZbmt1cm82VFV4VWVBPT06M2JkNDIwYWM=

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
