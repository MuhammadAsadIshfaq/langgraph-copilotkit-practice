# Automated Hiring System Backend

This is the backend service for the Automated Hiring System, built with FastAPI and LangGraph. It processes resumes, screens candidates, and automatically handles interview scheduling or rejection emails.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with:
```
GROQ_API_KEY=your_groq_api_key_here
```

## Running the Server

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The server will run on `http://localhost:8000`

## API Endpoints

### POST /process-resume

Process a candidate's resume and run it through the hiring workflow.

**Form Data:**
- `file`: Resume file (PDF, DOCX, or DOC)
- `name`: Candidate's name
- `email`: Candidate's email
- `position`: Position applied for
- `job_description`: Job description
- `company_name`: Company name
- `interviewer`: Interviewer's name
- `interviewer_email`: Interviewer's email
- `interview_location`: Interview location

**Response:**
Returns the final state of the hiring workflow, including:
- Screening results
- Interview scheduling details (if qualified)
- Rejection email details (if not qualified)
- Complete workflow history

## Project Structure

```
backend/
├── app/
│   ├── agents/
│   │   ├── resume_screener.py
│   │   ├── interview_scheduler.py
│   │   └── rejection_sender.py
│   ├── models/
│   │   └── hiring_state.py
│   ├── utils/
│   │   └── resume_parser.py
│   └── main.py
├── requirements.txt
└── README.md
```

## Integration with Next.js Frontend

The backend is configured to accept requests from `http://localhost:3000` (default Next.js development server). To integrate with your Next.js frontend:

1. Make sure CORS is properly configured in the backend (already set up in `main.py`)
2. Use the `/process-resume` endpoint from your frontend application
3. Handle the response appropriately in your frontend UI

## Error Handling

The API includes basic error handling for:
- Missing required fields
- Invalid file formats
- Missing GROQ API key
- Resume parsing errors

## Security Considerations

- The GROQ API key should be kept secure and never exposed to the frontend
- File uploads are validated for supported formats
- CORS is configured to only allow requests from trusted origins 