from pydantic import BaseModel, Field


class TutorRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)


class TutorCitation(BaseModel):
    title: str
    url: str
    section: str


class TutorResponse(BaseModel):
    answer: str
    citations: list[TutorCitation]
    insufficient_evidence: bool