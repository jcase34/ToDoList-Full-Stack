from fastapi import FastAPI
from . import models
from .database import engine, get_db
from .routers import post, user, auth
from .config import Settings

# Command below instructs sqlAlchemy to create all tables when first starting application. 
# models.Base.metadata.create_all(bind=engine)

# Main applicatin
app = FastAPI()

# Routers for user, post, authentication
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Welcome"}






