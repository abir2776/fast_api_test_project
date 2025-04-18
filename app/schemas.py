from datetime import datetime

from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    description: str
    url: str
    published_at: datetime


class PostOut(PostCreate):
    id: int

    class Config:
        orm_mode = True


class TokenRequest(BaseModel):
    client_id: str
    client_secret: str
