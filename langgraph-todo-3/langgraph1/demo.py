import os
from dotenv import load_dotenv
load_dotenv()

# pylint: disable=wrong-import-position
from fastapi import FastAPI, HTTPException
import uvicorn
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitRemoteEndpoint, LangGraphAgent
from agent import create_todo_agent
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Verify required environment variables
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY environment variable is not set")

# Create FastAPI app
app = FastAPI()

# Add CORS middleware
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request logging middleware
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"Response status: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise

# Create the agent
try:
    logger.info("Initializing LangGraph agent...")
    graph = create_todo_agent()
    
    # Create SDK with the graph
    sdk = CopilotKitRemoteEndpoint(
        agents=[
            LangGraphAgent(
                name="todo_agent",
                description="Todo management agent.",
                graph=graph,
            ),
        ],
    )
    
    # Add the CopilotKit FastAPI endpoint
    logger.info("Adding CopilotKit endpoint...")
    add_fastapi_endpoint(app, sdk, "/copilotkit")
except Exception as e:
    logger.error(f"Error initializing agent: {str(e)}")
    raise

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "ok"}

def main():
    """Run the FastAPI server"""
    port = int(os.getenv("PORT", "8000"))
    logger.info(f"Starting server on port {port}")
    uvicorn.run(
        "demo:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        reload_dirs=["."]
    )

if __name__ == "__main__":
    main()