from contextlib import asynccontextmanager
from fastapi import FastAPI
from typing_extensions import AsyncGenerator

from app.configuration.database.database import get_db
from app.routers.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    db = get_db()
    db.connect()
    yield
    await db.close()

app = FastAPI(lifespan=lifespan)


app.include_router(auth_router, prefix="/api/auth", tags=["auth"])