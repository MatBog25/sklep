from beanie import init_beanie
from pymongo import AsyncMongoClient

from app.core.config import settings
from app.models import document_models

client: AsyncMongoClient | None = None


async def init_database() -> None:
    global client

    client = AsyncMongoClient(settings.mongodb_uri)
    await init_beanie(
        database=client[settings.mongodb_db_name],
        document_models=document_models,
    )


async def close_database() -> None:
    global client

    if client is not None:
        await client.close()
        client = None

