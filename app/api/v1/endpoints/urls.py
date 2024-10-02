import logging

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.schemas.url import URLCreate, URLResponse
from app.crud.url_crud import create_short_url, get_original_url, delete_short_url, get_all_short_urls
from app.db.database import get_db
from datetime import datetime, timezone

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/shorten", response_model=URLResponse)
def shorten_url(url_data: URLCreate, db: Session = Depends(get_db)):
    db_url = create_short_url(db, url_data)
    return URLResponse(
        short_url = f"http://localhost:8000/{db_url.short_url}",
        original_url = db_url.original_url,
        expiration_time = db_url.expiration_time
    )

# Retrieve all shortened URLs
@router.get("/urls", response_model=list[URLResponse])
def list_all_urls(db: Session = Depends(get_db)):
    db_urls = get_all_short_urls(db)
    
    if not db_urls:
        raise HTTPException(status_code=404, detail="No URLs found")
    
    return [
        URLResponse(
            short_url=f"http://localhost:8000/{db_url.short_url}",
            original_url=db_url.original_url,
            expiration_time=db_url.expiration_time,
            short_url_key = db_url.short_url
        ) for db_url in db_urls
    ]


# Accessing details (metadata) about a specific URL
@router.get("/urls/{short_url}", response_model=URLResponse)
def get_url_metadata(short_url: str, db: Session = Depends(get_db)):
    try:
        db_url = get_original_url(db, short_url)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    return URLResponse(
        short_url = f"http://localhost:8000/{db_url.short_url}",
        original_url = db_url.original_url,
        expiration_time = db_url.expiration_time
    )

# Delete a short URL
@router.delete("/{short_url}")
def delete_shortened_url(short_url: str, db: Session = Depends(get_db)):
    if not delete_short_url(db, short_url):
        raise HTTPException(status_code=404, message="URL not found")
    
    return {"message": "URL deleted successfully"}


