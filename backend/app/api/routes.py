from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.api.startup import init_startup_handlers

app = FastAPI(title="AI Assistant API")

init_startup_handlers(app)

class Query(BaseModel):
    text: str

class Response(BaseModel):
    answer: str
    
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