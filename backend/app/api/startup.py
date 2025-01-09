from app.core.assistant import AIAssistant
import os

async def init_ai_assistant(app):
    """Initialize AI Assistant instance during startup"""
    app.state.assistant = AIAssistant(os.getenv("OPENAI_API_KEY"))

def init_startup_handlers(app):
    """Register all startup handlers"""
    @app.on_event("startup")
    async def startup_event():
        await init_ai_assistant(app)
