from fastapi import FastAPI

from . import models
from .auth import router as auth_router
from .database import engine
from .routes import router as post_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(post_router)
