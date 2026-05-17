# Modifique de acordo com que for necessário.

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Substitua a string abaixo pela string de conexão real
URL_BANCO_FICIOSA = "sqlite:///./idb_jovem_temporario.db"

# Inicializa o motor de conexão
engine = create_engine(URL_BANCO_FICIOSA, connect_args={"check_same_thread": False})

# Configura a fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base que todos os 'models.py' do sistema devem herdar para serem mapeados
Base = declarative_base()


def obter_banco() -> Generator:

    banco = SessionLocal()
    try:
        yield banco
    finally:
        banco.close()
