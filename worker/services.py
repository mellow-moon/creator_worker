import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

load_dotenv()

engine = create_async_engine(os.getenv("DATABASE_URL"), future=True, echo=True)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def fib(n: int) -> int:
    if n <= 1:
        return n
    else:
        return await fib(n - 1) + await fib(n - 2)
