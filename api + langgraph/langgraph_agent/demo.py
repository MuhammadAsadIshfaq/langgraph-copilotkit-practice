import os
from dotenv import load_dotenv
load_dotenv()

# pylint: disable=wrong-import-position
from fastapi import FastAPI
import uvicorn
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitRemoteEndpoint, LangGraphAgent
from agent import create_todo_api_graph  # adjust path as necessary



# Load environment variables
load_dotenv()

# Create FastAPI app
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create the LangGraph app instance
graph = create_todo_api_graph()

# Register agent with CopilotKit
sdk = CopilotKitRemoteEndpoint(
    agents=[
        LangGraphAgent(
            name="create_todo_api_graph",
            description="Manage tasks and users using natural language",
            graph=graph,
        )
    ]
)

# Attach CopilotKit endpoint
add_fastapi_endpoint(app, sdk, "/copilotkit")


@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "ok"}


def main():
    """Run the FastAPI server"""
    port = int(os.getenv("PORT", "8001"))   
    uvicorn.run(
        "demo:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        reload_dirs=(
            ["."]+
            (["../../../sdk-python/copilotkit"]
             if os.path.exists("../../../sdk-python/copilotkit")
             else []
             )
        )
    )


if __name__ == "__main__":
    main()