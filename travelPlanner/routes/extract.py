from fastapi import HTTPException
from pydantic import BaseModel, HttpUrl
from travelPlanner.azure_client import call_extract_agent
from main import app


class ExtractRequest(BaseModel):
    imageUrl: HttpUrl


class ExtractResponse(BaseModel):
    placeName: str
    city: str
    category: str
    notes: str
    aiDescription: str


@app.post("/api/extract", response_model=ExtractResponse)
async def extract_memory(req: ExtractRequest):
    try:
        result = call_extract_agent(str(req.imageUrl))
        # result should already be a dict with correct keys
        return ExtractResponse(**result)
    except Exception as e:
        # You can log e here
        raise HTTPException(status_code=500, detail=f"Failed to extract details: {e}")
