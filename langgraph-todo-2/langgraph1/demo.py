import os
from dotenv import load_dotenv

# Import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitRemoteEndpoint, LangGraphAgent
from agent import create_todo_agent  # adjust path as necessary


# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI()

# --- ADD CORS MIDDLEWARE HERE ---
# Define the origins that are allowed to make requests to your backend
# This should include the URL where your React frontend is running
origins = [
    "http://localhost",       # For direct access to localhost
    "http://localhost:3000",  # Your React app's development server
    # Add other origins if your frontend is deployed elsewhere, e.g.:
    # "https://your-production-frontend-domain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # List of allowed origins
    allow_credentials=True,         # Allow cookies to be sent with requests
    allow_methods=["*"],            # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],            # Allow all headers
)
# --- END CORS MIDDLEWARE ADDITION ---


# Create the LangGraph app instance
graph = create_todo_agent()

# Register agent with CopilotKit
sdk = CopilotKitRemoteEndpoint(
    agents=[
        LangGraphAgent(
            name="todo_agent",
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
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "demo:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        reload_dirs=["."]
    )


if __name__ == "__main__":
    main()



# import os
# from dotenv import load_dotenv

# # pylint: disable=wrong-import-position
# from fastapi import FastAPI
# import uvicorn
# from copilotkit.integrations.fastapi import add_fastapi_endpoint
# from copilotkit import CopilotKitRemoteEndpoint, LangGraphAgent
# from agent import create_todo_agent  # adjust path as necessary



# # Load environment variables
# load_dotenv()

# # Create FastAPI app
# app = FastAPI()

# # Create the LangGraph app instance
# graph = create_todo_agent()

# # Register agent with CopilotKit
# sdk = CopilotKitRemoteEndpoint(
#     agents=[
#         LangGraphAgent(
#             name="todo_agent",
#             description="Manage tasks and users using natural language",
#             graph=graph,
#         )
#     ]
# )

# # Attach CopilotKit endpoint
# add_fastapi_endpoint(app, sdk, "/copilotkit")


# @app.get("/health")
# def health():
#     """Health check endpoint"""
#     return {"status": "ok"}


# def main():
#     """Run the FastAPI server"""
#     port = int(os.getenv("PORT", "8000"))
#     uvicorn.run(
#         "demo:app",
#         host="0.0.0.0",
#         port=port,
#         reload=True,
#         reload_dirs=["."]
#     )


# if __name__ == "__main__":
#     main()