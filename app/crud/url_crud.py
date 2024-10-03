import hashlib
from sqlalchemy.orm import Session
from app.models.url import URL
from datetime import datetime, timedelta, timezone
from app.schemas.url import URLCreate
from fastapi import HTTPException

from app.utils import normalize_url
import string
import random

# Base62 character set
BASE62_ALPHABET = string.ascii_letters + string.digits

# Function to create a Base62 encoded string from a hash
def base62_encode(number: int) -> str:
    if number == 0:
        return BASE62_ALPHABET[0]
    encoded_string = []
    base = len(BASE62_ALPHABET)
    while number:
        remainder = number % base
        number = number // base
        encoded_string.append(BASE62_ALPHABET[remainder])
    return ''.join(reversed(encoded_string))

# Function to create a short URL
def create_short_url(db: Session, url_data: URLCreate) -> URL:

    normalized_url = normalize_url(url_data.original_url) 

    db_existing_url = db.query(URL).filter(URL.original_url == normalized_url).first()

    if db_existing_url:
        return db_existing_url
    
    # Generate MD5 hash of the normalized URL
    md5_hash = hashlib.md5(normalized_url.encode()).hexdigest()

    # Convert the first part of the hash to a Base62 string (first 10 characters of MD5 converted to a number)
    hash_number = int(md5_hash[:10], 16)
    short_url = base62_encode(hash_number)[:6]

    # Check for key collision and regenerate if necessary
    while db.query(URL).filter(URL.short_url == short_url).first() is not None:
        # Generate a random Base62 string if there's a collision
        short_url = base62_encode(random.randint(0, 62**6))

    #  Generates a short URL by taking the MD5 hash of the original URL and truncating it to 6 characters
    # short_url = hashlib.md5(normalized_url.encode()).hexdigest()[:6] # Old way of generating short URL

    # expiration = datetime.now(timezone.utc) + timedelta(days=url_data.expiration_time or 365) # We are setting the default expiration time to 1 year
    
    # Expiration is in datetime format
    expiration = url_data.expiration_time or (datetime.now(timezone.utc) + timedelta(days=365))


    # Creating URL model
    db_url = URL(
        short_url=short_url,
        original_url=normalized_url,
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