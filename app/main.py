from fastapi import FastAPI
from app.routes import auth,user
from . import models
from .database import engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(user.router)