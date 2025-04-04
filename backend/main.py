from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
import openai
from anthropic import Anthropic
import httpx

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize API clients
openai.api_key = os.getenv("OPENAI_API_KEY")
anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")


class DebateRequest(BaseModel):
    topic: str
    model1: str
    model2: str
    position1: str
    rounds: int


class DebateResponse(BaseModel):
    round: int
    model1: dict
    model2: dict


async def get_openai_response(prompt: str) -> str:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"OpenAI API error: {str(e)}")


async def get_claude_response(prompt: str) -> str:
    try:
        response = await anthropic.messages.create(
            model="claude-2",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Claude API error: {str(e)}")


async def get_deepseek_response(prompt: str) -> str:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 500
                }
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Deepseek API error: {str(e)}")


async def get_model_response(model: str, prompt: str) -> str:
    if model == "openai":
        return await get_openai_response(prompt)
    elif model == "claude":
        return await get_claude_response(prompt)
    elif model == "deepseek":
        return await get_deepseek_response(prompt)
    else:
        raise HTTPException(
            status_code=400, detail=f"Unsupported model: {model}")


@app.post("/api/debate", response_model=List[DebateResponse])
async def start_debate(request: DebateRequest):
    debate_history = []

    for round_num in range(1, request.rounds + 1):
        # Generate prompts for both models
        prompt1 = f"""You are participating in a debate about: {request.topic}
        You are taking the {request.position1} position.
        {f'Previous arguments: {debate_history[-1]["model2"]["argument"]}' if round_num > 1 else ''}
        Please provide a well-reasoned argument."""

        prompt2 = f"""You are participating in a debate about: {request.topic}
        You are taking the {'oppose' if request.position1 == 'support' else 'support'} position.
        {f'Previous arguments: {debate_history[-1]["model1"]["argument"]}' if round_num > 1 else ''}
        Please provide a well-reasoned counter-argument."""

        # Get responses from both models
        response1 = await get_model_response(request.model1, prompt1)
        response2 = await get_model_response(request.model2, prompt2)

        # Add round to history
        debate_history.append({
            "round": round_num,
            "model1": {
                "name": request.model1,
                "position": request.position1,
                "argument": response1
            },
            "model2": {
                "name": request.model2,
                "position": "oppose" if request.position1 == "support" else "support",
                "argument": response2
            }
        })

    return debate_history

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
