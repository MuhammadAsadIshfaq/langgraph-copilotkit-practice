# Hiring Workflow Backend

This is a FastAPI-based backend for an automated hiring workflow system that uses LangGraph and Groq LLM for resume screening and interview scheduling.

## Features

- Resume screening using AI
- Automatic interview scheduling
- Rejection handling
- Support for PDF, DOC, and DOCX resume formats
- RESTful API endpoints

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

## Running the Application

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /process-resume
Process a candidate's resume and determine next steps.

**Request:**
- `resume`: Resume file (PDF, DOC, or DOCX)
- `job_description`: Job description text
- `candidate_info`: JSON object with candidate details (optional)

**Response:**
- Screening results
- Interview scheduling (if qualified)
- Rejection email (if not qualified)

### GET /health
Health check endpoint.

## Project Structure

```
backend/
├── app/
│   ├── agents/
│   │   ├── resume_screener.py
│   │   ├── interview_scheduler.py
│   │   └── rejection_handler.py
│   ├── utils/
│   │   └── file_utils.py
│   └── main.py
├── requirements.txt
└── README.md
```

## Workflow

1. Resume is uploaded and processed
2. AI screens the resume against job requirements
3. If qualified:
   - Interview is scheduled
   - Confirmation emails are sent
4. If not qualified:
   - Rejection email is sent 