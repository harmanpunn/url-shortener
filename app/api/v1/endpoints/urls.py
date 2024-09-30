from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.url import URLCreate, URLResponse
from app.crud.url_crud import create_short_url, get_original_url
from app.db.database import get_db

router = APIRouter()

@router.post("/shorten", response_model=URLResponse)
def shorten_url(url_data: URLCreate, db: Session = Depends(get_db)):
    db_url = create_short_url(db, url_data)
    return URLResponse(
        short_url = f"http://localhost:8000/{db_url.short_url}",
        original_url = db_url.original_url,
        expiration_time = db_url.expiration_time
    )

@router.get("/{short_url}", response_model=URLResponse)
def redirect_to_original_url(short_url: str, db: Session = Depends(get_db)):
    db_url = get_original_url(db, short_url)
    
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found or expired")
    
    return URLResponse(
        short_url = f"http://localhost:8000/{db_url.short_url}",
        original_url = db_url.original_url,
        expiration_time = db_url.expiration_time
    )
