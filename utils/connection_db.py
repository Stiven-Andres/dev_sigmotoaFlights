'''Este es el archivo con la conexión a la DB.'''
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

load_dotenv()
CLEVER_DB=(
    f"postgresql+asyncpg://{os.getenv('CLEVER_USER')}:"
    f"{os.getenv('CLEVER_PASSWORD')}@"
    f"{os.getenv('CLEVER_HOST')}:"
    f"{os.getenv('CLEVER_PORT')}/"
    f"{os.getenv('CLEVER_DATABASE')}"
)
DATABASE_URL= "postgresql://db_parcial_3_mxra_user:IdRpSqWtoGmofyjuzGTiWJ4HBvSZIiwl@dpg-d15h8vuuk2gs73c7diag-a.oregon-postgres.render.com/db_parcial_3_mxra"

engine : AsyncEngine = create_async_engine(CLEVER_DB, echo=True)
async_session =sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async with async_session() as session:
        yield session