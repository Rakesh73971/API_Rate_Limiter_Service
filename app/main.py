from fastapi import FastAPI
from app.routes import auth,user,rate_limit_rule,request_log
from . import models
from .database import engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(rate_limit_rule.router)
app.include_router(request_log.router)