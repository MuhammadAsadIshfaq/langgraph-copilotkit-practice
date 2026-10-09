'use client';

import { CopilotKit } from '@copilotkit/react-core';

export function Providers({ children }) {
  return (
    <CopilotKit
      apiKey={process.env.NEXT_PUBLIC_COPILOT_API_KEY || 'your-api-key'}
      baseURL={process.env.NEXT_PUBLIC_COPILOT_BASE_URL || 'http://localhost:8000'}
      chatApiEndpoint="/api/chat"
      defaultSystemPrompt="You are an AI assistant helping with the hiring process."
    >
      {children}
    </CopilotKit>
  );
} 