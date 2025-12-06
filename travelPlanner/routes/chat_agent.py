from typing import List, Any, Dict
from pydantic import BaseModel
from fastapi import HTTPException
from azure_client import call_chat_agent
from main import app

class Memory(BaseModel):
    id: str
    placeName: str
    city: str
    category: str
    notes: str
    aiDescription: str
    createdAt: str  # or datetime

class ChatRequest(BaseModel):
    memories: List[Memory]
    question: str

@app.post("/api/chat")
async def chat_with_memories(req: ChatRequest):
    try:
        result = call_chat_agent(
            memories=[m.model_dump() for m in req.memories],
            question=req.question,
        )
        return result  # already { responseText, matches }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {e}")
