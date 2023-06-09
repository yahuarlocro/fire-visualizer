from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@127.0.0.1/hotspots"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.postgres_user}:{settings.postgres_pw}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
