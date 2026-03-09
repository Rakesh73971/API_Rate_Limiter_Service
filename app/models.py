from .database import Base
from sqlalchemy import Column,Integer,String,TIMESTAMP,text


class User(Base):
    __tablename__="users"

    id = Column(Integer,primary_key=True,nullable=False)
    full_name = Column(String,nullable=False)
    email = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)
    role = Column(String,default='free')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    

class RateLimitRule(Base):
    __tablename__="rate_limit_rules"
    id = Column(Integer,primary_key=True,nullable=False)
    role = Column(String,nullable=False)
    requests_limit = Column(Integer,nullable=False)
    time_window = Column(Integer,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class RequestLog(Base):
    __tablename__="request_logs"

    id = Column(Integer,primary_key=True,nullable=False)
    user_id = Column(Integer,nullable=False)
    endpoint = Column(String,nullable=False)
    status = Column(String,nullable=False)
    method = Column(String)
    timestamp = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
