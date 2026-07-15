from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    environment: str = "development"
    database_url: str = "sqlite:///./bechad.db"
    jwt_secret: str = "dev-only-change-me"
    jwt_issuer: str = "bechad"
    openai_api_key: str | None = None
    openai_coach_enabled: bool = False
    class Config: env_file = ".env"
settings=Settings()
engine=create_engine(settings.database_url, future=True, pool_pre_ping=True, connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {})
SessionLocal=sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
class Base(DeclarativeBase): pass
def get_db() -> Generator:
    db=SessionLocal();
    try: yield db
    finally: db.close()
