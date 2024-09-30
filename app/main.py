from fastapi import FastAPI
from app.api.v1.endpoints.urls import router as url_router
from app.api.v1.endpoints.redirect import router as redirect_router
from app.db.database import Base, engine
from app.db.base import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):

    init_db()
    print("Application startup: Database initialized")
    
    yield  

    print("Application shutdown")

app = FastAPI(lifespan=lifespan)

app.include_router(url_router, prefix="/api/v1")
app.include_router(redirect_router)
