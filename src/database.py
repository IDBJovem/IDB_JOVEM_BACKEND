from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config import configuracoes

DATABASE_URL = (
    f"postgresql://{configuracoes.POSTGRES_USER}:{configuracoes.POSTGRES_PASSWORD}"
    f"@{configuracoes.DATABASE_HOST}:{configuracoes.PORT}/{configuracoes.POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def obter_banco() -> Generator:
    banco = SessionLocal()
    try:
        yield banco
    finally:
        banco.close()
