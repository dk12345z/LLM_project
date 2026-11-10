from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="LLM Project")

SYSTEM_PROMPT = (
    "You are a helpful assistant. Keep answers concise, clear, and practical. "
    "If no external API service is configured, explain that the app is running in offline mode."
)
MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", "8"))

conversation_store: Dict[str, List[Dict[str, str]]] = {}


class ChatMessage(BaseModel):
    role: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)


class ChatRequest(BaseModel):
    conversation_id: str = "demo-session"
    message: str = Field(..., min_length=1)
    history: Optional[List[ChatMessage]] = None


def _default_history() -> List[Dict[str, str]]:
    return []


def _get_conversation_history(conversation_id: str, incoming_history: Optional[List[ChatMessage]]) -> List[Dict[str, str]]:
    if incoming_history is not None:
        return [msg.model_dump() for msg in incoming_history]

    return conversation_store.get(conversation_id, _default_history())


def _summarize(messages: List[Dict[str, str]]) -> str:
    if not messages:
        return "No prior context."

    parts: List[str] = []
    for item in messages[:6]:
        role = item.get("role", "user")
        content = item.get("content", "")
        parts.append(f"{role}: {content[:120]}".strip())

    summary = " ".join(parts)
    if len(summary) > 220:
        summary = summary[:217] + "..."
    return summary


def _trim_context(history: List[Dict[str, str]], max_messages: int) -> Tuple[List[Dict[str, str]], Optional[str]]:
    if len(history) <= max_messages:
        return history, None

    keep = history[-max_messages:]
    prior = history[:-max_messages]
    return keep, _summarize(prior)


def _prepare_model_messages(history: List[Dict[str, str]], new_message: str) -> List[Dict[str, str]]:
    messages: List[Dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]
    for item in history:
        role = item.get("role", "user")
        content = item.get("content", "")
        if role in {"user", "assistant"}:
            messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": new_message})
    return messages


def _call_openai(messages: List[Dict[str, str]]) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=messages,
        temperature=0.2,
    )
    return response.choices[0].message.content or "No response generated."


def _call_gemini(messages: List[Dict[str, str]]) -> str:
    import google.generativeai as genai

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"))

    prompt = "\n".join(f"{message['role']}: {message['content']}" for message in messages)
    response = model.generate_content(prompt)
    return getattr(response, "text", "No response generated.")


def _generate_reply(messages: List[Dict[str, str]]) -> str:
    provider = (os.getenv("LLM_PROVIDER") or "openai").lower()

    if provider == "gemini" and os.getenv("GEMINI_API_KEY"):
        return _call_gemini(messages)

    if os.getenv("OPENAI_API_KEY"):
        return _call_openai(messages)

    return (
        "Offline mode: no external API key is configured, so the app is returning a local fallback response. "
        "The backend is functioning correctly and ready to use once you add an API key."
    )


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/api/chat")
def chat(request: ChatRequest) -> Dict[str, Any]:
    history = _get_conversation_history(request.conversation_id, request.history)
    summary: Optional[str] = None

    if len(history) > MAX_HISTORY_MESSAGES:
        history, summary = _trim_context(history, MAX_HISTORY_MESSAGES)

    model_messages = _prepare_model_messages(history, request.message)

    try:
        reply = _generate_reply(model_messages)
    except Exception as exc:  # pragma: no cover - defensive against provider issues
        raise HTTPException(status_code=502, detail=f"LLM request failed: {exc}") from exc

    history.append({"role": "user", "content": request.message})
    history.append({"role": "assistant", "content": reply})
    conversation_store[request.conversation_id] = history

    return {
        "conversation_id": request.conversation_id,
        "reply": reply,
        "history": history,
        "summary": summary or "Earlier context summary not required.",
    }


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
