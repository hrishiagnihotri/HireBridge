from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from config import conn                                              #db,currently pointing to sienna  
from routes.sienna_router import sienna_router                       #sienna routes
from routes.auth_router import auth_router                           #login routes
from routes.zephyr_router import Zephyr_router                          #login routes
from models.sienna import Sienna
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.sessions import SessionMiddleware
import requests

app=FastAPI()
app.include_router(sienna_router)
app.include_router(auth_router)
app.include_router(Zephyr_router)

# ✅ Correctly mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Add this middleware configuration
app.add_middleware(
    SessionMiddleware,
    secret_key="----",  # Replace with a strong secret key
    session_cookie="session_cookie",
    max_age=10000  # Session expiration time in seconds (optional)
)

from fastapi.middleware.cors import CORSMiddleware

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (Not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.get('/')
async def root():
    return {"message":"head to /login"}

#[testing] posting users
import bcrypt 
from passlib.context import CryptContext  # For password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
@app.post('/')
async def rootadd(new_user:Sienna):
    try:
        print(dict(new_user)['password'])
        new_user_dic=dict(new_user)
        hashed_password = pwd_context.hash(new_user_dic['password'])
        new_user_dic.update({'password':hashed_password})
        resp = conn.insert_one(new_user_dic)
        return {"status_code":200, "id":str(resp.inserted_id),"message":"User Added successfully"}
    except Exception as e:
        return HTTPException(status_code=500)
    

# =====================================================
    
from pydantic import BaseModel
from openai import OpenAI
# Connect to LM Studio's local server
client = OpenAI(
    base_url="http://localhost:1234/v1",  # LM Studio's default API URL
    api_key="lm-studio"  # Dummy key required by LM Studio
)

class PromptRequest(BaseModel):
    prompt: str
    max_tokens: int = 200
    temperature: float = 0.7

@app.post("/generate")
async def generate_text(request: PromptRequest):
    """
    Endpoint to generate text using DeepSeek model via LM Studio
    """
    try:
        completion = client.chat.completions.create(
            model="local-model",  # Not used by LM Studio, but required
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": request.prompt}
            ],
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        return {
            "response": completion.choices[0].message.content,
            "usage": completion.usage
        }
    except Exception as e:
        return {"error": str(e)}

# ===================================================== 

import httpx
openrouter_key='----'
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

class PromptRequest(BaseModel):
    prompt:str
@app.post('/gen2')
async def chat_with_router(prompt:PromptRequest):
    headers = {
    "Authorization": f"Bearer {openrouter_key}",
    "Content-Type": "application/json"
}

    payload = {
        "model": "mistralai/mistral-7b-instruct:free",  # Latest model
        # "model": "google/gemini-2.5-pro-exp-03-25:free",  # Latest model
        # "model": "google/gemini-2.0-pro-exp-02-05:free",  # Change to desired model
        "messages": [{"role": "system","content" : "You are an AI assistant that provides clear, concise, and well-structured responses. Your goal is to deliver just the right amount of information—neither too brief nor excessively detailed. Tailor your responses to be informative, contextually relevant, and efficient in communication. When answering, ensure completeness without unnecessary elaboration."},
            {"role": "user", "content": prompt.prompt}]
    }

    async with httpx.AsyncClient() as client:

        response = await client.post(OPENROUTER_URL, json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()


#blocked dono for purpose
# @app.post('/dono')
async def generateMatchingPercent(listofjobs):
    listofjobs="""StudentSkill=[C++,Python,Data Structures, Algorithms, Distributed Systems, Cloud Computing]
    JobSkill1=[Python, Java, C++, Data Structures, Algorithms, Distributed Systems, Cloud Computing]
    JobSkill2=[Swift, Objective-C, iOS Development, Xcode, UI/UX Design]
    JobSkill3=[C++,Python]
    JobSkill4=[Web]
    JobSkill100=[java]
    JobSkill50=[C++,java,web]"""
    sys_msg="""Given a list of student skills and a job's required skills, calculate the match percentage based on direct and contextual relevance. The match percentage is determined as follows:

If a student has a skill that exactly matches a required job skill, count it as a match.

If a student has a related skill (e.g., Python → NumPy = 50%, C++ → CUDA = 50%), count it as a partial match.

The match percentage is calculated as:

(Number of Matched Skills / Total Job Skills) × 100

Response Format Strictly:
Match_Percentage: [percentage]%, JobSkill[number]: [Comma-separated job skills]"*

Example Input:
StudentSkill = [Python, Java]
Job1Skill = [Python, C++]

Expected Output:
Match_Percentage: 50%, JobSkill: Python, C++
Note that response should adhere to Response Format and not give breakdown and explaination"""
    headers = {
    "Authorization": f"Bearer {openrouter_key}",
    "Content-Type": "application/json"
}
    payload = {
        "model": "google/gemini-2.0-pro-exp-02-05:free",  # Change to desired model
        "messages": [
            {"role": "system","content" : sys_msg},
            {"role": "user", "content": listofjobs},
            ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(OPENROUTER_URL, json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data=response.json()
    print(data["choices"][0]["message"]["content"])
    return data["choices"][0]["message"]["content"]