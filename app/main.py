from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import posts, user, auth, vote
from pydantic import BaseSettings
from .config import settings

#models.Base.metadata.create_all(bind=engine) #tells sql alchemy to create tables , replaced by alembic

app = FastAPI()

origins = ["*"] # all can access it

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router) 
app.include_router(user.router) 
app.include_router(auth.router) 
app.include_router(vote.router) 

@app.get("/")
def root():
    return {"Hello": "World"}

