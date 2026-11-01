# LLM Project

This repository contains a small FastAPI-based LLM chat backend that satisfies the task requirements:

- backend endpoint to send user messages to an LLM API and receive a response
- per-conversation message history tracking
- context window management with truncation and summarisation
- a defined system prompt
- graceful handling of API failures and missing keys
- a quick browser UI for end-to-end testing

## Quick start

1. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copy the environment template and add a key if you want real LLM calls:

   ```bash
   cp .env.example .env
   ```

3. Run the app:

   ```bash
   uvicorn app:app --reload
   ```

4. Open the browser at `http://localhost:8000`.

## Environment variables

- `OPENAI_API_KEY` for OpenAI models
- `GEMINI_API_KEY` for Google Gemini (optional)
- `LLM_PROVIDER` = `openai` or `gemini` (default `openai`)
- `OPENAI_MODEL` (default `gpt-4o-mini`)
- `GEMINI_MODEL` (default `gemini-1.5-flash`)
- `MAX_HISTORY_MESSAGES` (default `8`)

If no key is configured, the app runs in offline mode and returns a clear message instead of crashing.

## API

### POST /api/chat

Request body:

```json
{
  "conversation_id": "demo-session",
  "message": "Hello there!",
  "history": [
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello!"}
  ]
}
```

Response:

```json
{
  "conversation_id": "demo-session",
  "reply": "...",
  "history": [
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello!"},
    {"role": "user", "content": "Hello there!"}
  ],
  "summary": "Earlier context summary..."
}
```

## Notes

This implementation balances the task requirements with a production-friendly structure:

- history is stored per conversation ID
- older messages are summarised before being passed to the model when the window grows too large
- the runtime remains usable even without an external API key
- errors are surfaced with clear HTTP responses instead of silent failure
