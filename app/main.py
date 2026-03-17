from fastapi import FastAPI
from app.routes import auth,user,rate_limit_rule,request_log
from . import models
from .database import engine
from .middleware.request_logger import RequestLoggerMiddleware

app = FastAPI()



app.add_middleware(RequestLoggerMiddleware)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(rate_limit_rule.router)
app.include_router(request_log.router)