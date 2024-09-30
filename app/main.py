from fastapi import FastAPI
from app.api.v1.endpoints.urls import router as url_router
from app.db.database import Base, engine
from app.db.base import init_db



app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(url_router, prefix="/api/v1")