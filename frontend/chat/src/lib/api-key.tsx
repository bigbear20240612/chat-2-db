// @ts-expect-error  MC8yOmFIVnBZMlhucUx2b2pZbmt1cm82Y2toR2FRPT06Yjc2NzdlZWE=

export function getApiKey(): string | null {
  try {
    if (typeof window === "undefined") return null;
    return window.localStorage.getItem("lg:chat:apiKey") ?? null;
  } catch {
    // no-op
  }

  return null;
}
// TODO  MS8yOmFIVnBZMlhucUx2b2pZbmt1cm82Y2toR2FRPT06Yjc2NzdlZWE=
