"""FastAPI server for GenAI code review."""

from __future__ import annotations

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.providers import review_code

load_dotenv()

app = FastAPI(
    title="GenAI Code Reviewer",
    description="LLM-powered code review with OpenAI and Gemini",
    version="1.0.0",
)


class ReviewRequest(BaseModel):
    code: str = Field(..., min_length=1)
    language: str = "python"
    provider: str | None = None


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/review")
def review(req: ReviewRequest) -> dict:
    try:
        return review_code(req.code, req.language, req.provider)
    except Exception as exc:  # noqa: BLE001 — surface API errors to client
        raise HTTPException(status_code=500, detail=str(exc)) from exc
