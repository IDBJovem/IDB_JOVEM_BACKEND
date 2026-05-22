from sqlalchemy.orm import Session
from src.evento.model import Evento


class RepositorioEvento:

    def __init__(self, db: Session):
        self.db = db

    def salvar(self, evento: Evento) -> Evento:
        if evento.evento_id:
            self.db.merge(evento)
        else:
            self.db.add(evento)
        self.db.commit()
        return evento

    def buscar_todos(self) -> list[Evento]:
        return self.db.query(Evento).all()

    def buscar_por_id(self, evento_id: int) -> Evento:
        return self.db.query(Evento).filter(Evento.evento_id == evento_id).first()

    def deletar(self, evento) -> None:
        if evento is not None:
            self.db.delete(evento)
            self.db.commit()
