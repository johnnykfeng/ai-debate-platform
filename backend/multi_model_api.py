from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# You should set these environment variables with your actual keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


# Input data model
class PromptRequest(BaseModel):
    prompt: str

client = OpenAI(api_key=OPENAI_API_KEY)

claude_client = OpenAI(
    api_key=ANTHROPIC_API_KEY,  # Your Anthropic API key
    base_url="https://api.anthropic.com/v1/"  # Anthropic's API endpoint
)

# Endpoint for GPT (OpenAI)
@app.post("/gpt")
async def call_gpt(request: PromptRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": request.prompt}]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint for Gemini (Google)
@app.post("/gemini")
async def call_gemini(request: PromptRequest):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [{"parts": [{"text": request.prompt}]}]
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return {"response": response.json()["candidates"][0]["content"]["parts"][0]["text"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint for Claude (Anthropic)
@app.post("/claude")
async def call_claude(request: PromptRequest):
    try:
        response = claude_client.chat.completions.create(
            model="claude-3-7-sonnet-20250219", # Anthropic model name
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": request.prompt}
            ],
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        