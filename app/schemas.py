from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role:Optional[str] = None
    
class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name:Optional[str] = None
    email:Optional[EmailStr] = None
    role:Optional[str] = None

class LimitRuleCreate(BaseModel):
    role: str
    requests_limit: int
    time_window: int

class LimitRuleOut(LimitRuleCreate):
    id: int

    class Config:
        from_attributes=True
class TokenData(BaseModel):
    id:Optional[int] = None


class RequestLogCreate(BaseModel):
    endpoint: str
    status: str
    

class RequestLogOut(RequestLogCreate):
    id: int
    user_id: int
    timestamp: datetime

    class Config:
        from_attributes=True