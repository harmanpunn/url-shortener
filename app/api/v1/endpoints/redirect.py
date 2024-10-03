from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from app.crud.url_crud import get_original_url
from app.db.database import get_db
from datetime import datetime, timezone

router = APIRouter()

@router.get("/{short_url}")
def redirect_to_original_url(short_url: str, db: Session = Depends(get_db)):
    db_url = get_original_url(db, short_url)
    
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found or expired")
    
    if db_url.expiration_time and db_url.expiration_time.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=404, detail="URL expired")

    return RedirectResponse(url=db_url.original_url)
