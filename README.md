# Flight Price Assistant

A beginner-friendly full‑stack AI chatbot that answers airline ticket price questions using an LLM + FastAPI backend + simple HTML frontend.

This project demonstrates how a browser UI communicates with a Python API, how the API talks to an LLM, and how the LLM can call tools (functions) to retrieve structured data.

---

## Overview

This app simulates a travel assistant. The user asks about ticket prices, the AI decides whether it needs real data, and if so, it calls a Python function that returns the price.

The goal of this project is educational — to understand how real AI applications are wired together end‑to‑end.

You will learn:

* How frontend (HTML + JS) talks to backend (FastAPI)
* How FastAPI parses JSON automatically using Pydantic
* How an LLM uses tool/function calling
* How chat memory works in a backend server
* How HTTP request‑response cycle works
* How to connect UI → API → AI → Tools → UI

---

## Tech Stack

**Frontend**

* HTML
* CSS
* Vanilla JavaScript (fetch API)

**Backend**

* Python 3.x
* FastAPI
* Pydantic
* Uvicorn

**AI**

* OpenAI API (`gpt-4o-mini`)
* Function / Tool calling

---

## Project Structure

```
project/
│
├── .env
├── index.html
├── llm_logic.py
├── main.py
├── pyproject.toml
└── README.md
```

---

## How the App Works (End‑to‑End Flow)

1. User types a message in the browser
2. JavaScript sends POST request to FastAPI
3. FastAPI validates request using Pydantic
4. Backend sends message to LLM
5. LLM decides if it needs the `get_ticket_price` tool
6. Python function returns structured data
7. LLM converts it into natural language
8. FastAPI returns JSON response
9. Browser displays the reply

---

## Possible Improvements

* Streaming responses
* Database chat memory
* Multiple users (sessions)
* Real flight API integration
* Authentication
* Deployment to cloud

---

## Author Note

This project is designed as a learning bridge between:

> "I know Python" → "I can build real AI apps"

It focuses on understanding flow instead of complexity.

A Terminal version of this app was also included

## Screenhot

<img width="702" height="888" alt="Flight Price Assistant" src="https://github.com/user-attachments/assets/ccc99de3-50ae-47c6-b0b7-3984d4c389b8" />



