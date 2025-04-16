from pydantic import BaseModel
from datetime import datetime


class PostCreate(BaseModel):
    title: str
    description: str
    url: str
    published_at: datetime


class PostOut(PostCreate):
    id: int

    class Config:
        orm_mode = True
