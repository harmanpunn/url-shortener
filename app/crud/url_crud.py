import hashlib
from sqlalchemy.orm import Session
from app.models.url import URL
from datetime import datetime, timedelta, timezone
from app.schemas.url import URLCreate

# Function to create a short URL
def create_short_url(db: Session, url_data: URLCreate) -> URL:

    short_url = hashlib.md5(url_data.original_url.encode()).hexdigest()[:6]

    expiration = None
    if url_data.expiration_time:
        expiration = datetime.now(timezone.utc) + timedelta(hours=url_data.expiration_time)

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

    if db_url and (not db_url.expiration_time or db_url.expiration_time.replace(tzinfo=timezone.utc) > datetime.now(timezone.utc)):
        return db_url
    
    return None