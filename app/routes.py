import os

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal
from .deps import get_current_client

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/news")
async def get_news(
    q: str = Query("technology", description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Results per page"),
    client=Depends(get_current_client),
):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": q,
        "page": page,
        "pageSize": page_size,
        "apiKey": NEWS_API_KEY,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()

    if response.status_code != 200:
        return {
            "error": data.get("message", "Failed to fetch news"),
            "status_code": response.status_code,
        }

    return {
        "total_results": data.get("totalResults"),
        "articles": data.get("articles"),
        "page": page,
        "page_size": page_size,
    }


@router.get("/posts", response_model=list[schemas.PostOut])
def list_posts(db: Session = Depends(get_db), client=Depends(get_current_client)):
    return db.query(models.Post).all()


@router.post("/news/save-latest")
async def save_latest_news(
    db: Session = Depends(get_db), client=Depends(get_current_client)
):
    url = "https://newsapi.org/v2/top-headlines"
    params = {"country": "us", "apiKey": NEWS_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()

    top_articles = data.get("articles", [])[:3]
    saved = []

    for article in top_articles:
        news = models.Post(
            title=article["title"],
            description=article.get("description"),
            url=article["url"],
            published_at=article["publishedAt"],
        )
        db.add(news)
        saved.append(news)

    db.commit()
    return {"message": "Top 3 news saved", "count": len(saved)}


@router.get("/news/headlines/country/{country_code}")
async def get_headlines_by_country(country_code: str):
    url = "https://newsapi.org/v2/top-headlines"
    params = {"country": country_code, "apiKey": NEWS_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    return response.json()


@router.get("/news/headlines/source/{source_id}")
async def get_headlines_by_source(source_id: str):
    url = "https://newsapi.org/v2/top-headlines"
    params = {"sources": source_id, "apiKey": NEWS_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    return response.json()


@router.get("/news/headlines/filter")
async def get_filtered_headlines(
    country: str = Query(None),
    source: str = Query(None),
    client=Depends(get_current_client),
):
    if country and source:
        raise HTTPException(
            status_code=400,
            detail="You cannot use both 'country' and 'source' together. Choose one.",
        )

    url = "https://newsapi.org/v2/top-headlines"
    params = {"apiKey": NEWS_API_KEY}

    if country:
        params["country"] = country
    elif source:
        params["sources"] = source
    else:
        raise HTTPException(
            status_code=400,
            detail="You must provide either 'country' or 'source'.",
        )

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()

    return data
