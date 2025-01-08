from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.core.assistant import AIAssistant

app = FastAPI(title="AI Assistant API")

class Query(BaseModel):
    text: str

class Response(BaseModel):
    answer: str
    source: Optional[str]
    confidence: str

@app.post("/api/query", response_model=Response)
async def query_assistant(query: Query):
    try:
        response = await app.state.assistant.get_response(query.text)
        return Response(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 