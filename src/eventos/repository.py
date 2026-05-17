# Aqui que executamos os comandos de banco de dados.
# Nenhum outro arquivo deve executar comandos de banco de dados diretamente.
# O acesso ao banco deve ser feito exclusivamente por meio deste arquivo.

from sqlalchemy.orm import Session
from src.eventos.models import ModeloEvento

class RepositorioEvento:
    # Coloque todas as funções de banco aqui.

    def __init__(self,  db: Session) -> None:
        self.db = db

    def salvar_no_banco(self, evento_dados: ModeloEvento) -> ModeloEvento:
        # Depois substitua pelo código real do banco de dados.

        print(f"[MOCK] Salvando evento no banco: {evento_dados.titulo}")
        return evento_dados
