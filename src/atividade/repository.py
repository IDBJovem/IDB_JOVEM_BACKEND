from sqlalchemy.orm import Session
from src.atividade.model import Atividade

class RepositorioAtividade:
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, atividade: Atividade) -> Atividade:
        if atividade.atividade_id:
            self.db.merge(atividade)
        else:
            self.db.add(atividade)
        self.db.commit()
        return atividade

    def buscar_por_evento(self, evento_id) -> list[Atividade]:
        return self.db.query(Atividade).filter(Atividade.evento_id == evento_id).all

    def buscar_por_id(self, atividade_id: int) -> Atividade:
        return self.db.query(Atividade).filter(Atividade.atividade_id == atividade_id).first()

    def deletar(self, atividade) -> None:
        if atividade is not None:
            self.db.delete(atividade)
            self.db.commit()
