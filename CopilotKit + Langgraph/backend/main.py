from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class Message(BaseModel):
    message: str

@app.post("/process-message")
async def process_message(data: Message):
    user_input = data.message
    # You can connect this to a LangGraph agent here
    response = f"Agent received: {user_input}"
    return {"response": response}
