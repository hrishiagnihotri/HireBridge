import asyncio
from fastapi import HTTPException
import httpx
from openai import OpenAI
# using miranda api key

base_url="https://openrouter.ai/api/v1",
api_key="----3"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

async def getsummary(userDesc):
    sysprompt = '''You are an assistant that helps refine and enhance user-written text for resumes or professional profiles.
Given the following raw input (project, internship, or certification description), rewrite it in a polished, professional, and natural tone
suitable for a resume.Try using ATS compliant words to standout the resume
Return only a 2-3 sentence response.Do not include any explanation, greeting, or additional comments outside the format.'''
    try:
        headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
        payload = {
            "model": "mistralai/mistral-7b-instruct:free",  # Change to desired model
            "messages": [
                {"role": "system","content" : sysprompt},
                {"role": "user", "content": userDesc},
                ]
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(OPENROUTER_URL, json=payload, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data=response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return e
