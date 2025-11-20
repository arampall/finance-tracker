import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

load_dotenv()

# Get the database URL from the environment variables
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/finance_tracker"
)

#Create the database engine
engine = create_async_engine(
    DATABASE_URL, 
    echo=True,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

async_session = async_sessionmaker(
    engine, 
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

#Create a Base class for the database models
Base = declarative_base()

# Dependency for FastAPI routes
async def get_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()