# Modifique de acordo com que for necessário.
from sqlalchemy.orm import Session
from src.eventos.model import Evento


class RepositorioEvento:
    # Coloque todas as funções de banco aqui.
    @staticmethod
    def save(db: Session, evento: Evento) -> Evento:
        """Função para salvar evento no banco de dados."""

        db.merge(evento)
        db.add(evento)
        db.commit()

        return evento
