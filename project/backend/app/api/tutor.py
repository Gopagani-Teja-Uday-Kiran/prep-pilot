from fastapi import APIRouter, HTTPException

from app.schemas.tutor import TutorRequest, TutorResponse
from app.services.tutor_service import (TutorProviderError, answer_question)

router = APIRouter(prefix="/api/tutor", tags=["tutor"])


@router.post("/ask", response_model=TutorResponse)
def ask_tutor(request: TutorRequest) -> TutorResponse:
    try:
        return answer_question(request.question)
    except TutorProviderError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    