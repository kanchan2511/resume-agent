# 🚀 AI Resume Feedback Agent (LangGraph + FastAPI)

An intelligent career assistant that goes beyond simple parsing. This agent researches live market trends to provide data-driven resume feedback.

## 🧠 System Architecture
This project implements a **Research-then-Analyze** pattern:
1. **Agentic Search:** Uses a LangGraph agent equipped with the Tavily Search Tool to find current industry demands based on the resume's job title.
2. **Reasoning Engine:** Processes search results and resume content using Llama-3.1 (Groq).
3. **Structured Output:** Forces the final analysis into a strict Pydantic schema for reliable frontend rendering.
4. **Real-time Monitoring:** Uses Server-Sent Events (SSE) to stream backend "thought process" logs to the React UI.

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI, LangChain, LangGraph
- **AI:** Groq (Llama-3.1-8b), Tavily Search API
- **Frontend:** React, Axios, CSS3
- **DevOps:** Pydantic (Validation), Dotenv (Config)

## ⚡ Key Features
- **Live Market Context:** Doesn't just check grammar; it checks if your skills match 2024/2025 job trends.
- **Async Processing:** Built with `async/await` for high-performance I/O.
- **Streaming Logs:** Users see what the "agent" is doing (e.g., "Searching for trends...") in real-time.

## 🚦 Getting Started
1. Clone the repo.
2. Create a `.env` file with `GROQ_API_KEY` and `TAVILY_API_KEY`.
3. Run backend: `uvicorn main:app --reload`
4. Run frontend: `npm start`