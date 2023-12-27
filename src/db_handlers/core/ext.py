from src.db_handlers.db_manage import AsyncSessionLocal, engine
from sqlalchemy import text
from models import Base


async def check_connection():
    async with AsyncSessionLocal() as ss:
        async with ss.begin():
            version = await ss.execute(text("SELECT VERSION()"))
            return version.scalar()


async def db_init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
