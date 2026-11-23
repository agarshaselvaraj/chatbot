# Neon_bot 🤖

A command-line AI chatbot built in Python using the OpenAI SDK connected to **Groq's high-speed inference API**. Neon_bot supports real-time streaming responses, conversation memory management (sliding window trimming and periodic summarization), token inspection with `tiktoken`, and session cost estimation.

## ✨ Features

- **Real-Time Streaming:** Prints LLM responses token-by-token in the terminal with smooth pacing.
- **Memory Management:**
  - **Sliding Window (`trim_messages`):** Retains system instructions alongside the most recent conversation turns to stay within context limits.
  - **Conversation Summarization (`summarize_messages`):** Periodically condenses older messages into a concise summary to preserve key facts and decisions.
- **Token Inspection & Cost Tracking:**
  - Uses `tiktoken` (`cl100k_base`) to display input token counts and token IDs before sending prompts.
  - Tracks total prompt and completion tokens across the session and calculates estimated API cost upon exit.

## 🛠️ Tech Stack

- **Python 3.10+**
- **OpenAI Python SDK** (configured with Groq's base URL)
- **Groq API** (`openai/gpt-oss-120b`)
- **tiktoken** (token encoding & counting)
- **python-dotenv** (environment variable management)

