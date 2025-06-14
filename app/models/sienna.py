from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional

class Sienna(BaseModel):
    sno: str = None
    name: Optional[str] = None  # Optional field with default None
    password: Optional[str] = None  # Optional field with default None
    email: Optional[str] = None
    gender:Optional[str] = None
    usn: Optional[str] = None  # Optional field with default None
    sem: Optional[int] = None  # Optional field with default None
    department: Optional[str] = None  # Optional field with default None
    phone: Optional[int] = None  # Optional field with default None
    passout: Optional[int] = None  # Optional field with default None
    cgpa: Optional[float] = None  # Optional field with default None
    backlog: Optional[int] = None  # Optional field with default None
    skills:list[str] = []             #to validate use List[str] from typing
    user_tour: bool = False
    soft_delete: bool = False
    admin_remark: str = "good"

    # model_config = ConfigDict(extra='ignore')
    


# class SiennaLogin(BaseModel):
#     name:str

# class Sienna_hsh(SiennaLogin):
#     hsh_password:str

# class TokenData(BaseModel):
#     name: Optional[str] = None

class resumedetails(BaseModel):
    c_name:Optional[str]
    c_phone:Optional[str]
    c_email:Optional[str]
    c_skills:Optional[str]
    c_deg:Optional[str]
    c_degmarks:Optional[str]
    c_degbatch:Optional[str]
    c_coll:Optional[str]
    c_collmarks:Optional[str]
    c_collbatch:Optional[str]
    c_school:Optional[str]
    c_schoolmarks:Optional[str]
    c_schoolbatch:Optional[str]
    c_int:Optional[str]
    c_intdes:Optional[str]
    c_proj1:Optional[str]
    c_projdes1:Optional[str]
    c_proj2:Optional[str]
    c_projdes2:Optional[str]
    c_cert1:Optional[str]
    c_certdes1:Optional[str]
    c_cert2:Optional[str]
    c_certdes2:Optional[str]
    
