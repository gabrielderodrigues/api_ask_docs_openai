from fastapi import APIRouter, HTTPException
from app.models.chat import PromptRequest, ChatResponse
from app.services.openai_service import get_chat_response

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: PromptRequest):
    try:
        content = get_chat_response(request.prompt)
        return ChatResponse(response=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))