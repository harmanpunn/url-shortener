from app.db.database import Base, engine
from app.models.url import URL

def init_db():
    Base.metadata.create_all(bind=engine)