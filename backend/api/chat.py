from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from api.auth import get_current_user
from rag.pipeline import query_rag, astream_rag
from rag.guardrails import apply_guardrails

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    stream: bool = False

@router.post("/")
async def chat_endpoint(request: ChatRequest, current_user: dict = Depends(get_current_user)):
    if request.stream:
        async def generator():
            async for chunk in astream_rag(request.message):
                yield f"data: {chunk}\n\n"
        return StreamingResponse(generator(), media_type="text/event-stream")
    else:
        response = query_rag(request.message)
        return {"response": apply_guardrails(response)}
