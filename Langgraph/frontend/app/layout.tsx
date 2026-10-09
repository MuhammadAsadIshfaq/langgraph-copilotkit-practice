import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { CopilotKitProvider } from "@copilotkit/nextjs";
import { GroqProvider } from "@groq/groq-js";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "LangGraph Hiring System",
  description: "Automated hiring workflow system",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <CopilotKitProvider
          apiKey={process.env.NEXT_PUBLIC_COPILOTKIT_API_KEY}
          model="llama-3.3-70b-versatile"
        >
          <GroqProvider apiKey={process.env.NEXT_PUBLIC_GROQ_API_KEY}>
            {children}
          </GroqProvider>
        </CopilotKitProvider>
      </body>
    </html>
  );
}
