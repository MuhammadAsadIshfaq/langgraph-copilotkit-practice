# Todo App with LangGraph and CopilotKit

A simple todo application built with Next.js, FastAPI, LangGraph, and CopilotKit.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file in the root directory and add your OpenAI API key:
```
NEXT_PUBLIC_OPENAI_API_KEY=your_openai_api_key_here
```

3. Start the FastAPI backend:
```bash
cd backend
uvicorn main:app --reload
```

4. In a new terminal, start the Next.js frontend:
```bash
npm run dev
```

## Features

- Add and manage todos
- AI-powered todo management through CopilotKit
- LangGraph agent integration for intelligent todo handling
- FastAPI backend for data persistence

## Project Structure

- `src/app/page.tsx` - Main Next.js page with todo list and CopilotKit integration
- `backend/main.py` - FastAPI backend with todo endpoints
- `backend/agent.py` - LangGraph agent for todo management

## Usage

1. Open http://localhost:3000 in your browser
2. Use the input field to add new todos
3. Click the checkbox to mark todos as complete
4. Use the CopilotKit sidebar (right side) to interact with the AI assistant

This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
