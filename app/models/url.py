from sqlalchemy import Column, String, DateTime
from app.db.database import Base
from datetime import datetime

class URL(Base):
    __tablename__ = "urls"

    short_url = Column(String, primary_key=True, index=True)

    original_url = Column(String, index=True)

    expiration_time = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(datetime.timezone.utc))