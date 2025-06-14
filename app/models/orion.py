from datetime import date, datetime,timezone
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
import pytz

class Orion(BaseModel):
    company: str = None
    job_role: str = None
    elgible_cgpa: Optional[float]  
    backlogs_allowed: Optional[int]  
    skills: Optional[list]  
    batch: Optional[list]  
    dept: Optional[list]  
    posted_by: str
    posted_on: Optional[str]  
    desc: Optional[str]
    applyby: Optional[str]
    applylink: Optional[str]

def gettime():
    # Get IST timezone
    ist = pytz.timezone("Asia/Kolkata")

    # Get current time in IST
    current_time = datetime.now(timezone.utc).astimezone(ist)

    # Format: "DD-MM-YYYY HH:MM AM/PM"
    formatted_time = current_time.strftime("%d-%m-%Y %I:%M %p")
    return str(formatted_time)

def convertstr_list(skills):
    list_skill=[skill.strip() for skill in  skills.split(sep=',')]
    return list_skill



class JobCreate(BaseModel):
    company: str 
    role: str
    cgpa_operator: Optional[str] = None
    cgpa_value: Optional[float] = None
    Backlogs: int = 0
    department: List[str]
    batch: int
    skills: Optional[str]
    sems: Optional[int] = None
    apply_by: date 
    apply_link: Optional[HttpUrl] = None
    description: str

    posted_by:str = None
    posted_on:str = gettime()
  
