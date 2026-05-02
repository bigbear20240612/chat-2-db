// NOTE  MC8yOmFIVnBZMlhucUx2b2pZbmt1cm82UjFSRVV3PT06NWZjOGVhNWE=

import type { Metadata } from "next";
import "./globals.css";
import { Inter } from "next/font/google";
import React from "react";
import { NuqsAdapter } from "nuqs/adapters/next/app";

const inter = Inter({
  subsets: ["latin"],
  preload: true,
  display: "swap",
});

export const metadata: Metadata = {
  title: "智能问数平台",
  description: "Agent Chat UX",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN" suppressHydrationWarning>
      <body className={inter.className}>
        <NuqsAdapter>{children}</NuqsAdapter>
      </body>
    </html>
  );
}
// NOTE  MS8yOmFIVnBZMlhucUx2b2pZbmt1cm82UjFSRVV3PT06NWZjOGVhNWE=
