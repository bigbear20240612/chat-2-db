// @ts-expect-error  MC8yOmFIVnBZMlhucUx2b2pZbmt1cm82ZDNSdFNBPT06N2FkZGQ5MDA=

import { useEffect, useState } from "react";

export function useMediaQuery(query: string) {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const media = window.matchMedia(query);
    setMatches(media.matches);

    const listener = (e: MediaQueryListEvent) => setMatches(e.matches);
    media.addEventListener("change", listener);
    return () => media.removeEventListener("change", listener);
  }, [query]);

  return matches;
}
// NOTE  MS8yOmFIVnBZMlhucUx2b2pZbmt1cm82ZDNSdFNBPT06N2FkZGQ5MDA=
