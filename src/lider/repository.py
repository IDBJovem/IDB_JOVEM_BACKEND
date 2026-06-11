from sqlalchemy.orm import Session
from src.lider.model import Lider


class RepositorioLider:

    def __init__(self, db: Session):
        self.db = db

    def salvar(self, lider: Lider) -> Lider:
        self.db.add(lider)
        self.db.commit()
        return lider

    def buscar_todos(self) -> list[Lider]:
        return self.db.query(Lider).order_by(Lider.ordem).all()

    def buscar_por_id(self, lider_id: int) -> Lider | None:
        return (
            self.db.query(Lider)
            .filter(Lider.lider_id == lider_id)
            .first()
        )

    def deletar(self, lider: Lider) -> None:
        self.db.delete(lider)
        self.db.commit()
