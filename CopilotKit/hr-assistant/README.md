# HR Assistant

An AI-powered HR Assistant built with Next.js, FastAPI, LangGraph, and CopilotKit. The application helps manage candidates, schedule interviews, and answer HR-related questions using Groq's Mixtral model.

## Features

- Chat interface for HR-related queries
- Candidate management
- Interview scheduling
- AI-powered responses using Groq's Mixtral model
- CopilotKit integration for enhanced AI capabilities

## Tech Stack

- Frontend:
  - Next.js 14
  - TypeScript
  - Tailwind CSS
  - CopilotKit
  - Axios

- Backend:
  - FastAPI
  - LangGraph
  - Groq
  - Python 3.9+

## Prerequisites

- Node.js 18+
- Python 3.9+
- Groq API key
- CopilotKit API key

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd hr-assistant
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Create a `.env` file in the backend directory:
```
GROQ_API_KEY=your_groq_api_key
```

5. Create a `.env.local` file in the frontend directory:
```
NEXT_PUBLIC_COPILOT_API_KEY=your_copilotkit_api_key
```

## Running the Application

1. Start the backend server:
```bash
cd backend
uvicorn main:app --reload
```

2. Start the frontend development server:
```bash
cd frontend
npm run dev
```

3. Open http://localhost:3000 in your browser

## API Endpoints

- `POST /chat`: Send a message to the HR Assistant
- `GET /candidates`: Get all candidates
- `POST /candidates`: Create a new candidate
- `GET /interviews`: Get all interviews
- `POST /interviews`: Schedule a new interview

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 