from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llm_logic import run_chat

app = FastAPI()

# This allows our HTML file to talk to our Python code
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# This "History" stores the chat in memory (resets if you restart the server)
chat_history = [{"role": "system", "content": "You are a flight assistant."}]

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    bot_response = run_chat(request.message, chat_history)
    
    # Update history so the bot remembers the conversation
    chat_history.append({"role": "user", "content": request.message})
    chat_history.append({"role": "assistant", "content": bot_response})
    
    return {"reply": bot_response}

if __name__ == "__main__":

    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000)