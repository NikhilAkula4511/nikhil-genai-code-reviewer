"""LLM providers for code review."""

from __future__ import annotations

import json
import os
import re

from src.prompts import REVIEW_SYSTEM, REVIEW_USER_TEMPLATE


def _extract_json(text: str) -> dict:
    text = text.strip()
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("Model did not return JSON")
    return json.loads(match.group())


def review_with_openai(code: str, language: str) -> dict:
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    user = REVIEW_USER_TEMPLATE.format(language=language, code=code)
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": REVIEW_SYSTEM},
            {"role": "user", "content": user},
        ],
        temperature=0.2,
    )
    return _extract_json(resp.choices[0].message.content or "{}")


def review_with_gemini(code: str, language: str) -> dict:
    import google.generativeai as genai

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
    user = REVIEW_USER_TEMPLATE.format(language=language, code=code)
    resp = model.generate_content([REVIEW_SYSTEM, user])
    return _extract_json(resp.text or "{}")


def review_code(code: str, language: str = "python", provider: str | None = None) -> dict:
    provider = (provider or os.getenv("DEFAULT_PROVIDER", "openai")).lower()
    if provider == "gemini":
        if not os.getenv("GEMINI_API_KEY"):
            raise RuntimeError("GEMINI_API_KEY not set")
        return review_with_gemini(code, language)
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY not set")
    return review_with_openai(code, language)
