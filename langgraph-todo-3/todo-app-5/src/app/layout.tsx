import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ModelSelectorProvider } from "@/lib/model-selector-provider";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Todo Management",
  description: "AI-powered todo management application",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <ModelSelectorProvider>{children}</ModelSelectorProvider>
      </body>
    </html>
  );
} 