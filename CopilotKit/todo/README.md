# AI-Powered Todo App

A modern todo application built with Next.js, TypeScript, FastAPI, and LangGraph, featuring AI-powered task management capabilities using Groq's Mixtral model.

## Features

- Add, complete, and delete todos
- AI-powered task suggestions and management using Groq's Mixtral model
- Automatic task enhancement and prioritization
- Time estimation for tasks
- Subtask suggestions for complex tasks
- Modern, responsive UI with Tailwind CSS
- Real-time updates
- Copilot sidebar for AI assistance

## Project Structure

```
todo/
├── ui/                 # Frontend Next.js application
│   ├── src/
│   │   ├── app/       # Next.js app directory
│   │   └── components/# React components
│   └── ...
└── agent/             # Backend FastAPI application
    ├── main.py        # FastAPI application
    ├── todo_workflow.py # LangGraph workflow
    └── ...
```

## Getting Started

### Prerequisites

- Node.js 18+ installed
- Python 3.9+ installed
- pnpm package manager
- Poetry for Python dependency management
- Groq API key

### Backend Setup

1. Navigate to the agent directory:
```bash
cd agent
```

2. Install Python dependencies:
```bash
poetry install --no-root
```

3. Create a `.env` file in the `agent` directory:
```
GROQ_API_KEY=your_groq_api_key_here
PORT=8000
HOST=0.0.0.0
```

4. Start the backend server:
```bash
poetry run python main.py
```

The backend will be available at http://localhost:8000

### Frontend Setup

1. Navigate to the UI directory:
```bash
cd ui
```

2. Install dependencies:
```bash
pnpm install
```

3. Create a `.env` file in the `ui` directory:
```
GROQ_API_KEY=your_groq_api_key_here
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. Start the development server:
```bash
pnpm dev
```

5. Open [http://localhost:3000](http://localhost:3000) in your browser.

## API Endpoints

### Backend API

- `GET /todos` - Get all todos
- `POST /todos` - Create a new todo
- `PUT /todos/{todo_id}` - Update a todo's completion status
- `DELETE /todos/{todo_id}` - Delete a todo

## AI Features

The application uses LangGraph with Groq's Mixtral model to provide the following AI-powered features:

1. **Task Enhancement**: Automatically improves task descriptions to be more specific and actionable
2. **Priority Suggestion**: Suggests priority levels for tasks
3. **Time Estimation**: Estimates completion time for tasks
4. **Subtask Generation**: Breaks down complex tasks into subtasks

## Technologies Used

### Frontend
- Next.js 14
- TypeScript
- Tailwind CSS
- CopilotKit
- Groq API

### Backend
- FastAPI
- LangGraph
- LangChain
- Groq API (Mixtral model)
- Poetry for dependency management 