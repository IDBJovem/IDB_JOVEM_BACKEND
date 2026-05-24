from sqlalchemy.orm import Session

from src.voluntario.models import Voluntario, Trabalha


class RepositorioVoluntario:

    def __init__(self, db: Session):
        self.db = db

    def salvar(self, voluntario: Voluntario) -> Voluntario:
        self.db.add(voluntario)
        self.db.commit()
        return voluntario

    def buscar_todos(self) -> list[Voluntario]:
        return self.db.query(Voluntario).all()

    def buscar_por_id(self, voluntario_id: int) -> Voluntario | None:
        return (
            self.db.query(Voluntario)
            .filter(Voluntario.voluntario_id == voluntario_id)
            .first()
        )

    def buscar_por_email(self, email: str) -> Voluntario | None:
        return (
            self.db.query(Voluntario)
            .filter(Voluntario.email == email)
            .first()
        )

    def deletar(self, voluntario: Voluntario) -> None:
        self.db.delete(voluntario)
        self.db.commit()

    def buscar_trabalho(self, voluntario_id: int, evento_id: int) -> Trabalha | None:
        return (
            self.db.query(Trabalha)
            .filter(
                Trabalha.voluntario_id == voluntario_id,
                Trabalha.evento_id == evento_id,
            )
            .first()
        )

    def listar_por_evento(self, evento_id: int) -> list[Trabalha]:
        return self.db.query(Trabalha).filter(Trabalha.evento_id == evento_id).all()

    def salvar_trabalho(self, trabalho: Trabalha) -> Trabalha:
        self.db.add(trabalho)
        self.db.commit()
        self.db.refresh(trabalho)
        return trabalho
