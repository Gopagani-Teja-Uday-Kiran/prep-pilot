from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.tutor import router
import app.services.tutor_service as tutor_service

app = FastAPI()
app.include_router(router)
client = TestClient(app)


def test_tutor_returns_answer_and_citation(monkeypatch) -> None:
    monkeypatch.setattr(
        tutor_service,
        "retrieve",
        lambda question: [{
            "text": "Python groups statments using indentation.",
            "title": "Python Tutorial",
            "url": "https://docs.python.org/3.14/tutorial/introduction.html",
            "section": "Using Python as a Calculator",
            "score": 1.0,
        }],
    )
    monkeypatch.setattr(
        tutor_service,
        "generate_grounded_answer",
        lambda question, evidence: "Python uses indentation to group statements.[s1].",
    )
    response = client.post(
        "/api/tutor/ask",
        json={"question": "How does Python group statements?"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["insufficient_evidence"] is False
    assert body["citations"][0]["url"].startswith("https://docs.python.org/3.14/")
    assert "indentation" in body["answer"]


def test_tutor_reports_insufficient_evidence(monkeypatch) -> None:
    monkeypatch.setattr(tutor_service, "retrieve", lambda question: [])

    response = client.post(
        "/api/tutor/ask",
        json={"question": "Explain the lifecycle of a black hole."},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["insufficient_evidence"] is True
    assert body["citations"] == []
def test_gemini_is_used_when_groq_is_unavailable(monkeypatch) -> None:
    def fail_groq(question: str, evidence: str) -> str:
        raise tutor_service.ProviderUnavailableError("Groq unavailable")

    monkeypatch.setattr(tutor_service, "_generate_with_groq", fail_groq)
    monkeypatch.setattr(
        tutor_service,
        "_generate_with_gemini",
        lambda question, evidence: "Answer from Gemini [S1].",
    )

    assert tutor_service.generate_grounded_answer("Question?", "Evidence") == (
        "Answer from Gemini [S1]."
    )


def test_error_when_both_providers_are_unavailable(monkeypatch) -> None:
    def fail_provider(question: str, evidence: str) -> str:
        raise tutor_service.ProviderUnavailableError("Provider unavailable")

    monkeypatch.setattr(tutor_service, "_generate_with_groq", fail_provider)
    monkeypatch.setattr(tutor_service, "_generate_with_gemini", fail_provider)

    try:
        tutor_service.generate_grounded_answer("Question?", "Evidence")
    except tutor_service.TutorProviderError:
        pass
    else:
        raise AssertionError("Expected both-provider failure")