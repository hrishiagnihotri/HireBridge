from fastapi import HTTPException
import httpx
openrouter_key='----'
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


async def generateMatchingPercent(listofjobs):
    # listofjobs="""StudentSkill=[C++,Python,Data Structures, Algorithms, Distributed Systems, Cloud Computing]
    # JobSkill1=[Python, Java, C++, Data Structures, Algorithms, Distributed Systems, Cloud Computing]
    # JobSkill2=[Swift, Objective-C, iOS Development, Xcode, UI/UX Design]
    # JobSkill3=[C++,Python]
    # JobSkill4=[Web]
    # JobSkill100=[java]
    # JobSkill50=[C++,java,web]"""
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
    try:

        headers = {
        "Authorization": f"Bearer {openrouter_key}",
        "Content-Type": "application/json"
    }
        payload = {
            "model": "mistralai/mistral-7b-instruct:free",  # Latest model
            # "model": "google/gemini-2.5-pro-exp-03-25:free",  # Latest model
            # "model": "google/gemini-2.0-pro-exp-02-05:free",  # Change to desired model
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
        print(data)
        print(data["choices"][0]["message"]["content"])
        return data["choices"][0]["message"]["content"]
    except:
        return 1
    

