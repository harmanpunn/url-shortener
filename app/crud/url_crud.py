import hashlib
from sqlalchemy.orm import Session
from app.models.url import URL
from datetime import datetime, timedelta, timezone
from app.schemas.url import URLCreate
from fastapi import HTTPException


# Function to create a short URL
def create_short_url(db: Session, url_data: URLCreate) -> URL:

    db_existing_url = db.query(URL).filter(URL.original_url == url_data.original_url).first()

    if db_existing_url:
        return db_existing_url
    
    # Generates a short URL by taking the MD5 hash of the original URL and truncating it to 6 characters
    short_url = hashlib.md5(url_data.original_url.encode()).hexdigest()[:6]

    expiration = None
    if url_data.expiration_time:
        expiration = datetime.now(timezone.utc) + timedelta(days=url_data.expiration_time)
    else:
        expiration = datetime.now(timezone.utc) + timedelta(days=365) # We are setting the default expiration time to 1 year

    # Creating URL model
    db_url = URL(
        short_url=short_url,
        original_url=url_data.original_url,
        expiration_time=expiration,
        created_at=datetime.now(timezone.utc)
    )

    # Save to db
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    return db_url


# Function to retrieve the original URL
def get_original_url(db: Session, short_url: str) -> URL:
    db_url = db.query(URL).filter(URL.short_url == short_url).first()

    if db_url:
        if db_url.expiration_time and db_url.expiration_time.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            # Delete expired URL from the database for DB cleanup
            db.delete(db_url)
            db.commit()
            raise HTTPException(status_code=410, detail="URL has expired and was deleted.")
        return db_url
    
    # Raise a 404 if the short URL doesn't exist
    raise HTTPException(status_code=404, detail="URL not found.")

# Delete the shortened URL
def delete_short_url(db: Session, short_url: str) -> URL:

    db_url = db.query(URL).filter(URL.short_url == short_url).first()

    if db_url:
        db.delete(db_url)
        db.commit()
        return True

    return False

# Retrieve all shortened URLs
def get_all_short_urls(db: Session) -> list:

    return db.query(URL).all()