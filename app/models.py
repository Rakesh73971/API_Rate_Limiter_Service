from .database import Base
from sqlalchemy import Column,Integer,String,TIMESTAMP,text


class User(Base):
    __tablename__="users"

    id = Column(Integer,primary_key=True,nullable=False)
    full_name = Column(String,nullable=False)
    email = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    