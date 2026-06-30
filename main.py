from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq()

class ChatRequest(BaseModel):
    message: str
    history: list = []

@app.post("/chat")
def chat(req: ChatRequest):
    messages = req.history + [{"role": "user", "content": req.message}]
    
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages
    )
    
    reply = response.choices[0].message.content
    return {"reply": reply}

@app.get("/")
def root():
    return {"status": "Chatbot API is running!"}