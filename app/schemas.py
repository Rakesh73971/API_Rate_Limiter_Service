from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role:Optional[str] = None
    
class UserResponse(BaseModel):
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

class LimitRuleBase(BaseModel):
    role: str
    requests_limit: int
    time_window: int

class LimitRuleResponse(LimitRuleBase):
    id: int

    class Config:
        from_attributes=True
class TokenData(BaseModel):
    id:Optional[int] = None


class RequestLogBase(BaseModel):
    endpoint: str
    status: str
    

class RequestLogResponse(RequestLogBase):
    id: int
    user_id: int
    timestamp: datetime

    class Config:
        from_attributes=True