from datetime import date, datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from pydantic import BaseModel, HttpUrl, field_validator  # For password hashing

                                     #model
from models.sienna import Sienna
from models.zephyr import Zephyr
from models.orion import JobCreate
from schemas.zephyr_schema import get_admin_info,admins
from schemas.sienna_schema import users
from config import conn,conn2,conn3                                     #config db connection
from bson import ObjectId

Zephyr_router = APIRouter()

Zephyr_router.mount("/static", StaticFiles(directory="static"), name="static")              #frontend purpose
templates = Jinja2Templates(directory="templates")

import bcrypt 
from passlib.context import CryptContext  # For password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@Zephyr_router.post('/adminpost')
async def postadmins(new_admin: Zephyr):
    try:
        print(dict(new_admin)['password'])
        new_admin_dic=dict(new_admin)
        hashed_password = pwd_context.hash(new_admin_dic['password'])
        new_admin_dic.update({'password':hashed_password})
        resp = conn2.insert_one(new_admin_dic)
        return {"status_code":200, "id":str(resp.inserted_id),"message":"Admin Added successfully"}
    except Exception as e:
        return HTTPException(status_code=500)
    
@Zephyr_router.get('/admin_login',response_class=HTMLResponse)
async def zephyr(request:Request):
    return templates.TemplateResponse("sienna_login.html",{"request": request,"role":"Admin"})


@Zephyr_router.post('/admin_login', response_class=HTMLResponse)
async def zephyr_login(request: Request,username: str = Form(...),password: str = Form(...)):
    user = conn2.find_one({"name": username})

    # Verify user exists and password matches
    if  not user or not pwd_context.verify(password,user['password']):
        return templates.TemplateResponse(
            "sienna_login.html",
            {"request": request, "error": "Invalid credentials",'role':'Admin'},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    # Set session
    request.session["admin"] = username
    return RedirectResponse(url="/admin_dashboard", status_code=status.HTTP_302_FOUND)

async def get_current_admin(request: Request):
    user = request.session.get("admin")
    if not user:
        return None
    return user

@Zephyr_router.get('/admin_dashboard',response_class=HTMLResponse)
async def zephyr_dashboard(request:Request,current_admin: Zephyr = Depends(get_current_admin)):
    if not current_admin:
        return RedirectResponse(url='/admin_login')
    
    return templates.TemplateResponse("zephyr_dashboard.html",{'request':request,'admin':current_admin.capitalize()})

@Zephyr_router.post("/admin_logout")
async def logout(request: Request):
    """ Logs out the user by clearing the session and redirects to login """
    request.session.clear()  # Clear user session
    return RedirectResponse(url="/admin_login")
from twilio.rest import Client
async def send_text(company,applyby,postedby):
    message = f"Hey HireBridge Alert, a job opportunity at {company} that fits your profile is posted on Hirebridge. Apply by {applyby}. -{postedby}."
   

    # Initialize the client
    client = Client(account_sid, auth_token)

    # Send a message
    message = client.messages.create(
        body=message,
        from_=twilio_number,
        to=destination_number
    )

    print(f"Message SID: {message.sid}")
    return

@Zephyr_router.post("/create-job/")
async def create_job(request:Request,det:JobCreate):
    try:
        job_det=det.model_dump()
        job_det["_id"] = ObjectId()
        job_det["apply_by"] = datetime.combine(job_det["apply_by"], datetime.min.time())
        job_det["apply_link"] = str(job_det["apply_link"])  # Convert HttpUrl to string
        job_det["posted_by"] = request.session["admin"]
        conn3.insert_one(job_det)
        resp = conn.find({
            'department':{ '$in': job_det['department'] },
            'cgpa':{'$gte': job_det['cgpa_value']},
            'backlog':{'$lte': job_det['Backlogs']},
            'sem':{'$gte': job_det['sems']}
                   })
        try:
            for user in users(resp):
                if user['phone'] == --:
                    # print('hello')
                    await send_text(job_det['company'],job_det['apply_by'],job_det['posted_by'])
                    break
        except:
            pass    
        # for x in resp:
        #     print(x)
        return {'message':'Job created successfully!'}
    except PyMongoError as e:
        return {'message':e}

# adding user backend
class AddSienna(BaseModel):
    sno: str = None
    name: Optional[str] = None  # Optional field with default None
    password: Optional[str] = None  # Optional field with default None
    reenter:str = None
    email: Optional[str] = None
    gender:Optional[str] = None
    usn: Optional[str] = None  # Optional field with default None
    sem: Optional[int] = None  # Optional field with default None
    department: Optional[str] = None  # Optional field with default None
    phone: Optional[int] = None  # Optional field with default None
    passout: Optional[int] = None  # Optional field with default None
    cgpa: Optional[float] = None  # Optional field with default None
    backlog: Optional[int] = None  # Optional field with default None
    skills:list = []             #to validate use List[str] from typing
    user_tour: bool = False
    soft_delete: bool = False
    admin_remark: str = "good"
    

    # model_config = ConfigDict(extra='ignore')

    @field_validator("skills", mode="before")
    @classmethod
    def convert_skills(cls, value):
        if isinstance(value, str):
            return [s.strip() for s in value.split(",") if s.strip()]
        return value

from pymongo.errors import DuplicateKeyError,PyMongoError
@Zephyr_router.post("/add-user")
async def add_user(rdata:AddSienna):
    data =  rdata.model_dump()
    if (data['password'] != data['reenter']):
        raise HTTPException(400,detail="Passwords dont match")
    
    abstract_data = Sienna(**data).model_dump()
    try:
        abstract_data["usn"] = abstract_data['usn'].upper()
        abstract_data["password"] = pwd_context.hash(abstract_data['password'])
        resp = conn.insert_one(abstract_data)
        return {"status_code":200, "id":str(resp.inserted_id),"message":"User Added successfully"}
    except DuplicateKeyError:
        return {"status_code":400, "message":"USN already exists in Server"}

from schemas.orion_schema import alljobs,job_info   
#fetching all jobs posted by session admin
@Zephyr_router.get('/getpostedjobs')
async def getprofilejaabs(request:Request):
    profile_name = request.session['admin']
    data = conn3.find({'posted_by':profile_name})
    return alljobs(data)

# delete operations
@Zephyr_router.post('/softdeleteuser')
async def softdeleteUser(userid):
    try:
        # conn.delete_many({"_id":ObjectId(userid)})
        conn.update_one({"_id":ObjectId(userid)},{"$set":{"soft_delete":True}})
        return
    
    except PyMongoError as e:
        raise HTTPException(400,"error deleting user")
    
@Zephyr_router.post('/deletejob')
async def deleteJob(jobid):
    try:
        conn3.delete_many({"_id":ObjectId(jobid)})
        return
    
    except PyMongoError as e:
        raise HTTPException(400,"error deleting Job")

# update operations
@Zephyr_router.put('/updateuser/{userid}')
async def update_user(userid:str,rdata:AddSienna):
    data = rdata.model_dump()
    if (data['password'] != '' and data['password'] != data['reenter']):
        raise HTTPException(400,detail="Passwords dont match")
    
    abstract_data = Sienna(**data).model_dump()
    try:
        abstract_data["usn"] = abstract_data['usn'].upper()
        if abstract_data["password"] != '':
            abstract_data["password"] = pwd_context.hash(abstract_data['password'])
        else:
            abstract_data.pop('password',None)
        print(abstract_data)
        resp = conn.update_many({'_id':ObjectId(userid)},{"$set":abstract_data})
        if resp.matched_count == 0:
            return {"status_code":400, "message":"No such profile exists."}
        return {"status_code":200, "id":str(resp.upserted_id),"message":"User Updated successfully."}
    except PyMongoError as e:
        return {"status_code":400, "message":"Updation failed."+e}

@Zephyr_router.put('/updatejob/{jobid}')
async def update_job(jobid:str,det:JobCreate,request:Request):
    try:
        job_det=det.model_dump()
        job_det["apply_by"] = datetime.combine(job_det["apply_by"], datetime.min.time())
        job_det["apply_link"] = str(job_det["apply_link"])  # Convert HttpUrl to string
        job_det["posted_by"] = request.session["admin"]
        conn3.update_one({'_id':ObjectId(jobid)},{"$set":job_det})
        return {'message':'Job updated successfully!'}
    
    except PyMongoError as e:
        return {'message':e}

class MsgModel(BaseModel):
    options: Optional[str] = None
    mode1: Optional[str] = None
    mode2: Optional[str] = None
    usnlist: Optional[str] = None

    orsem1: Optional[int] = None
    orsem2: Optional[int] = None
    ordept1: Optional[str] = None
    ordept2: Optional[str] = None
    orgender1: Optional[str] = None
    orgender2: Optional[str] = None

    andsem1: Optional[int] = None
    andsem2: Optional[int] = None
    anddept1: Optional[str] = None
    anddept2: Optional[str] = None
    andgender1: Optional[str] = None
    andgender2: Optional[str] = None
    message_area: Optional[str] = None

    class Config:
        extra = "allow"

@Zephyr_router.post('/sendnotification')
async def getmessage(request:Request,data:MsgModel):
    realdata =data.model_dump()
    print(realdata)
    try:
        mode = realdata['options']
        mode1_list = ['orsem1','ordept1','orgender1','andsem1','anddept1', 'andgender1']
        mode2_list = ['orsem2','ordept2','orgender2','andsem2','anddept2', 'andgender2']
        if mode== 'msg' and realdata['usnlist']:
            failed_usns = []
            realdata['usnlist']=[usn.strip() for usn in data.usnlist.split(",")]
            print(realdata["usnlist"])
            for usn in realdata["usnlist"]:
                resp=conn.update_one({'usn':usn.upper()},{'$push':{'messages':realdata['message_area']}})
                if resp.matched_count == 0:
                    failed_usns.append(usn.upper())
            print(failed_usns)
            fmessage=''
            if failed_usns:
                fmessage+=f"But failed to send messages to USN's {failed_usns}."
            return {'message':f"Message sent Successfully."+fmessage}
        else:
            if realdata['mode1'] is not None:
                if (realdata['mode1'] == '--'):
                    cond1='sem'
                    cond_val1='options'
                else:
                    cond1 = realdata['mode1']
                    cond_val1 = mode+realdata['mode1']+'1'
            if realdata['mode2'] is not None:
                if (realdata['mode2'] == '--'):
                    cond2='sem'
                    cond_val2='options'
                else:
                    cond2 = realdata['mode2']
                    cond_val2 = mode+realdata['mode2']+'2'
            # print(f'{cond1}:{realdata[cond_val1]} ${mode} {cond2}:{realdata[cond_val2]}')
        if cond1=='dept':
            cond1='department'
        if cond2=='dept':
            cond2='department'
        print('mode:',mode)
        print('cond1:',cond1)
        print('cond1val:',realdata[cond_val1])
        print('cond2:',cond2)
        print('cond2val:',realdata[cond_val2])

        resp = conn.update_many(
            {f'${mode}': [{cond1:realdata[cond_val1]},{cond2:realdata[cond_val2]}] },
            {'$push':{'messages':realdata['message_area']}})
        print(resp)
        message = "Message sent succesfully"
        return {'message':message}
    except PyMongoError as e:
        return {'message':e}
    except Exception as e:
        return {'message':"some error occured sending messages."+e}
    
# @zephyr
