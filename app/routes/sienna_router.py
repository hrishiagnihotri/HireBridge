import os
import re
from fastapi import APIRouter, File,UploadFile, Form,HTTPException, Request, Depends, status, Query

from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles                 #frontend purpose
from fastapi.templating import Jinja2Templates

from utils.utils import generateMatchingPercent as genmatch
from models.sienna import Sienna,resumedetails                            #model
from schemas.sienna_schema import users,profilesienna_params                     #schema
from schemas.orion_schema import alljobs                     #schema
from config import conn,conn3                                    #config db connection
from bson import ObjectId
import mimetypes

import bcrypt

sienna_router = APIRouter()

sienna_router.mount("/static", StaticFiles(directory="static"), name="static")              #frontend purpose
templates = Jinja2Templates(directory="templates")

#[testing] fetching user
@sienna_router.get('/show')
async def success():
    user_data=conn.find({"soft_delete":False}).sort([('department',1),('sem',-1),('name',1)])
    return users(user_data)

@sienna_router.get("/login",response_class=HTMLResponse)
async def sienna(request:Request):
    # #print(request)
    return templates.TemplateResponse("sienna_login.html",{"request": request})

from routes.auth_router import get_current_user
@sienna_router.get("/dashboard",response_class=HTMLResponse)
async def sienna_dashboard(request:Request,current_user: Sienna= Depends(get_current_user)):

    if not current_user:
        return RedirectResponse(url="/login")
    
    # check to see if user is able to successfully login
    # print(request,"User Logged:"+request.session["user"],current_user,sep="\t======")user

    return templates.TemplateResponse("sienna_dashboard.html",{"request": request,"user":current_user.title()})

@sienna_router.get('/getcurruser')
async def getcurruser(request: Request,cur_user:Sienna=Depends(get_current_user)):
    user = conn.find_one({"name": cur_user})
    return profilesienna_params(user)

@sienna_router.post("/logout")
async def logout(request: Request):
    """ Logs out the user by clearing the session and redirects to login """
    request.session.clear()  # Clear user session
    return RedirectResponse(url="/login")

@sienna_router.get('/fetchalljobs')
async def fetch_alljobs():
    jobs= conn3.find()
    return alljobs(jobs)

from schemas.sienna_schema import matchingparameters_sienna,multisienna_parameters
@sienna_router.get('/fetchfilteredjobs')
async def fetch_filteredjob(request:Request):
    # try:
    loggeduser=request.session["user"]
    # #print(loggeduser)
    if loggeduser:
        userbio=conn.find({'name':loggeduser})
        criterialist=matchingparameters_sienna(userbio[0])
        # criterialist=multisienna_parameters(userbio)[0]

        # print("criterialist",criterialist)

        matching_job = conn3.find({
            'cgpa_value':{'$lte': criterialist['cgpa']},
            'Backlogs':{'$gte': criterialist['backlogs_exists']},
            'department':criterialist['department'],
            'batch':criterialist['batch'],
            'sems':{'$lte':criterialist['sem']},
            })
        
        StudentSkill=criterialist['skills']
        matching_job_list=alljobs(matching_job)

        jobmap={}
        for i,matched_job in enumerate(matching_job_list):
            # i=(re.search(r'(\d+)$',matched_job['id']).group(1))
            # i=(matched_job['id'])
            jobmap[f"JobSkill{i}"]=matched_job['skills']
        # #print("StudentSkill",StudentSkill)
        # #print(jobmap)
        try:
        
            listofjobstemp=format_job_skills(StudentSkill,jobmap)
            matchpercentage =await genmatch(listofjobstemp)
            # #print(matchpercentage)
            hello = convert_to_dicts(matchpercentage,matching_job_list)
            # #print(hello)
            # skillMatchP=await generateMatchingPercent(alljobs(matching_job))
            # print(matching_job_list[2])
            matching_job_list,hello
            return {
                "filtered":matching_job_list,
                "match_percent_filtered":hello
            }
    
        except:
            fakemps = {}
            # print(matching_job_list)
            for item in matching_job_list:
                fakemps[item['id']]=999

            return {
                "filtered":matching_job_list,
                "match_percent_filtered":fakemps
            }

    else:
        print("user session empty somehow but loged log70")
        
    # except:
    #     return {"error":"no user logged-in log69"}

def format_job_skills(student_skills, job_skills_dict):
    formatted_string = f'StudentSkill=[{", ".join(student_skills)}]\n'  # Format StudentSkill
    for job, skills in job_skills_dict.items():
        formatted_string += f'{job}=[{", ".join(skills)}]\n'  # Format JobSkills
    return formatted_string.strip()  # Remove trailing newline

def convert_to_dicts(data,joblist):
    result = []
    
    # Splitting input into lines
    lines = data.split("\n")
    
    entry = {}
    for line in lines:

        # Extract match percentage and convert to float
        match = re.search(r"Match_Percentage: (\d+(\.\d+)?)%", line)
        if match:
            result.append(float(match.group(1)))  # Convert to float
        
    for i,item in enumerate(joblist):
        entry[item['id']]=result[i]
    

    return entry

from utils.descutil import getsummary
from utils.createword import makeresumeoutofit
from concurrent.futures import ThreadPoolExecutor
import asyncio
@sienna_router.post('/fsomewhere')
async def buildresume(request:Request, data:resumedetails):
    try:
        if request.session['user']==None:
            RedirectResponse('/login')
        #resume candidate info dictionary
        c_info=data.model_dump()
        # #print(c_info)
        #key descriptions which needs to AI summarized
        key_descriptions = ['c_intdes','c_projdes1', 'c_projdes2', 'c_certdes1', 'c_certdes2']
        tasks =[]
        tobeupdated =[] #storing description keys who values are to be replaced by AI results
        for key in key_descriptions:
            if c_info[key]!= '':
                tasks.append(getsummary(c_info[key]))
                tobeupdated.append(key)
        #result list contains ai summaries 
        results = await asyncio.gather(*tasks)
        for i in range(len(tobeupdated)):
            c_info[tobeupdated[i]]=results[i]

        #generate docx file out of final c_info dictionary
        download_path=makeresumeoutofit(c_info,request.session['user'])
        # #print(download_path)
        return download_path
    except Exception as e:
        return e
    
#method to download files
from starlette.responses import FileResponse
@sienna_router.get('/downloadresume')
async def downloadfile(filepath : str):
    if os.path.exists(filepath):
        filename = os.path.basename(filepath)
        return FileResponse(
            path=filepath,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    else:
        print('errorFile not found')

#upload to vault
MAX_FILE_SIZE = 10*1024*1024
@sienna_router.post('/uploadvault')
async def uploadFile(request:Request,file:UploadFile = File(...)):
    contents = await file.read()
    foldername=request.session['user']
    if len(contents)> MAX_FILE_SIZE:
        raise HTTPException(413,detail='File is too large ,10MB')
    
    os.makedirs(f'userdata/{foldername}',exist_ok=True)
    
    with open(f"userdata/{foldername}/{file.filename}",'wb') as f:
        f.write(contents)

    return {'filename':file.filename,"size":len(contents)}

@sienna_router.get('/getvaultfiles')
async def getvaultfiles(request:Request):
    username = request.session['user']
    ans = getfiles(username)
    print('backend fetched files:',ans)
    return ans

def getfiles(userbase):
    filedict = {}
    for root,dirs,files in os.walk(f'userdata\\{userbase}'):
        for file in files:
            relative_path = os.path.join(root,file)
            filedict[file]=relative_path

    return filedict

@sienna_router.get('/downloadanyfile')
async def downloadfile(filepath: str):
    if os.path.exists(filepath):
        # Get the file name from the path
        filename = os.path.basename(filepath)
        
        # Guess the MIME type (e.g., application/pdf, image/png, etc.)
        media_type, _ = mimetypes.guess_type(filepath)
        if media_type is None:
            media_type = "application/octet-stream"  # Default binary stream

        return FileResponse(
            path=filepath,
            filename=filename,
            media_type=media_type
        )
    else:
        print('Error: File not found')
        return {"error": "File not found"}
    
@sienna_router.get('/removeanyfile')
async def removefile(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
        return
    else:
        return {'status':"Error deleting file."}
    
@sienna_router.delete('/deletemsg')
async def deletemsg(request:Request,id:str,message:str):
    print(message)
    try:
        resp = conn.update_one({'usn':id.upper()},{"$pull":{f'messages':message}})
        print(resp.matched_count)
        if resp.modified_count==0:
            raise HTTPException(400,detail="couldnt delete..")
        return {"message":"Deletion success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    

@sienna_router.get('/testingMetrics')
async def gettopjobskills():
    resp = conn3.aggregate([
    {
        '$addFields': {
            'skillsArray': {
                '$split': ["$skills", ", "]
            }
        }
    },
    { 
        '$unwind': "$skillsArray" 
    },
    { 
        '$group': { 
            '_id': "$skillsArray", 
            'count': { '$sum': 1 } 
        } 
    },
    { 
        '$sort': { 'count': -1 } 
    },
    { 
        '$limit': 3 
    }])

    
    top_skills = list(resp)
    print(top_skills)

    top_ids = [item['_id'].lower() for item in top_skills]
    top_ids_count = [item['count'] for item in top_skills]

    resp2 = conn.aggregate([
        { 
            '$unwind': "$skills" 
        },
        {
            '$match': {
                '$expr': {
                '$in': [
                    { '$toLower': "$skills" },
                    top_ids
                ]
            }
            }
        },
        {
            '$group': {
                '_id': "$skills",
                'count': { '$sum': 1 }
            }
        },
        {
            '$sort': { 'count': -1 }
        }
    ])

    siennaCount=list(resp2)
    actual_dict = {item['_id']: item['count'] for item in siennaCount}

    print(siennaCount)

    parcel_dict ={}
    for item in top_skills:
        parcel_dict[item['_id']]=[item['count'],actual_dict.get(item['_id'],0)]

    print(parcel_dict)
    return parcel_dict

@sienna_router.get('/get2ndgraph')
async def get2ndgraph():
    try:
        # MongoDB aggregation pipeline
        pipeline = [
            { 
                "$match": { 
                    "sems": { "$in": [1,2,3,4,5,6, 7, 8] }  # Filtering for sems 6, 7, 8
                }
            },
            {
                "$group": { 
                    "_id": "$sems",  # Grouping by the sems field to count occurrences of each value
                    "count": { "$sum": 1 }  # Counting the number of records for each sems value
                }
            },
            { 
                "$sort": { "_id": 1 }  # Optional: Sort by sems in ascending order (6, 7, 8)
            }
        ]

        # Execute the aggregation pipeline
        result = list(conn3.aggregate(pipeline))
        actual={}
        if result: 
            c_data = {}
            c_sum = 0
            for data in result:
                c_sum+= data['count']
                c_data[data['_id']]= c_sum

            # for number in range(6,9):
            #     if number not in c_data:
            #         if number==6:
            #             c_data[]
            #         c_data[number]=c_data[number-1]

            return c_data
        else:
            raise HTTPException(status_code=404, detail="No data found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))