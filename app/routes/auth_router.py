from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext  # For password hashing

from models.sienna import Sienna                            #model
from schemas.sienna_schema import users,user_info                     #schema
from config import conn                                     #config db connection
from bson import ObjectId

auth_router=APIRouter()
templates = Jinja2Templates(directory="templates")

# Password context for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        return None
    return user

@auth_router.post("/login", response_class=HTMLResponse)
async def login(request: Request,username: str = Form(...),password: str = Form(...)):
    # Get user from database
    user = conn.find_one({"usn": username.upper(),"soft_delete":False})
    # print(user_info(user))

    # print(user)
    
    # Verify user exists and password matches
    if  not user or not pwd_context.verify(password,user['password']):
        return templates.TemplateResponse(
            "sienna_login.html",
            {"request": request, "error": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    # Set session
    request.session["user"] = user['name']
    print(user['name'])
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)