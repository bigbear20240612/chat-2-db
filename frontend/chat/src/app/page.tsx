"use client";
// TODO  MC8yOmFIVnBZMlhucUx2b2pZbmt1cm82VTA5Q1lnPT06NDgzZTZkNTg=

import { Thread } from "@/components/thread";
import { StreamProvider } from "@/providers/Stream";
import { ThreadProvider } from "@/providers/Thread";
import { ArtifactProvider } from "@/components/thread/artifact";
import { Toaster } from "@/components/ui/sonner";
import React from "react";
// eslint-disable  MS8yOmFIVnBZMlhucUx2b2pZbmt1cm82VTA5Q1lnPT06NDgzZTZkNTg=

export default function DemoPage(): React.ReactNode {
  return (
    <React.Suspense fallback={<div>加载中...</div>}>
      <Toaster />
      <ThreadProvider>
        <StreamProvider>
          <ArtifactProvider>
            <Thread />
          </ArtifactProvider>
        </StreamProvider>
      </ThreadProvider>
    </React.Suspense>
  );
}
