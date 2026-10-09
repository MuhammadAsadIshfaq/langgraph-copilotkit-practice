import { Inter } from 'next/font/google';
import './globals.css';
import { CopilotKit } from '@copilotkit/react-core';
import { CopilotSidebar } from '@copilotkit/react-ui';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'Hiring Workflow System',
  description: 'AI-powered hiring workflow system',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <CopilotKit
          apiKey={process.env.NEXT_PUBLIC_GROQ_API_KEY}
          baseURL="http://localhost:8000"
        >
          <CopilotSidebar
            defaultOpen={true}
            className="w-96"
          />
          <main className="min-h-screen bg-gray-50">
            {children}
          </main>
        </CopilotKit>
      </body>
    </html>
  );
} 