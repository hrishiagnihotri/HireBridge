from pydantic import BaseModel
from typing import Optional

class Zephyr(BaseModel):
    name: Optional[str] = None  # Optional field with default None
    password: Optional[str] = None  # Optional field with default None
    department: Optional[str] = None  # Optional field with default None
    phone: Optional[int] = None  # Optional field with default None
