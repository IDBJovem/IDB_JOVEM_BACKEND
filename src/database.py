from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config import configuracoes

DATABASE_URL = configuracoes.DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def obter_banco() -> Generator:
    banco = SessionLocal()
    try:
        yield banco
    finally:
        banco.close()