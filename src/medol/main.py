from fastapi import FastAPI

from src.medol.api.router import api_router
from src.medol.core.config import Settings

app = FastAPI()

app.include_router(api_router, prefix=Settings.app_config().get('api_version'))


@app.get("/")
async def read_root():
    return {"message": "Welcome to Telegram-Service!"}