# Future LLM Mentor Readiness

Status: **prepared, disabled**. The reviewed `TALK WITH ZACH` conversations remain the production mentor.

The future endpoint is `POST /api/mentor-question` with `{question, task}`. When disabled it returns a scripted-fallback response and makes no provider request. Provider keys exist only in the server environment; never expose them to the game HTML, Lovable public variables, recordings, or saves.

## Provider options

- **OpenRouter free router:** simplest prototype setting (`openrouter/free`), but free availability varies and low-volume limits make it unsuitable as a production dependency.
- **Groq:** OpenAI-compatible base URL and fast inference; choose a currently supported model and verify account limits before staging.
- **Hugging Face Inference Providers:** OpenAI-compatible router with small monthly experimentation credits, useful for evaluation rather than assuming unlimited free production service.

All providers use the same server adapter through `LLM_API_BASE`, `LLM_API_KEY`, and `LLM_MODEL`.

## Safety architecture

- Answers are grounded in the committed Zach conversations, Shop Class curriculum, and approved audio dialogue.
- Questions are capped at 400 characters; requests are capped per IP and time out after 20 seconds.
- Answers cannot change game state, spend coins, run equipment, or replace visible objectives.
- The system prompt prohibits invented machining values and bypassing PPE, guards, interlocks, lockout/tagout, inspections, or machine manuals.
- Provider failure returns the deterministic scripted mentor.
- No conversation history is stored by this endpoint. Provider retention and data-use terms still require review before enabling.

Run `pnpm llm:check`. Enabling requires every gate in `data/llm-mentor-options.json`, a staging-only key, red-team questions, and explicit release approval.
