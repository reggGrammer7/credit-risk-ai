from fastapi import APIRouter, HTTPException
from schemas.schemas import ChatRequest, ChatResponse
from services import llm_service

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        answer = llm_service.chat(
            applicant=request.applicant,
            prediction=request.prediction,
            question=request.question,
            history=request.history or [],
        )
        return ChatResponse(answer=answer)
    except EnvironmentError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {e}")
