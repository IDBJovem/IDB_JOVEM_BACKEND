from sqlalchemy.orm import Session
from src.admin.model import Admin


class RepositorioAdmin:

    def __init__(self, db: Session):
        self.db = db

    def salvar(self, admin: Admin) -> Admin:
        if admin.admin_id:
            admin = self.db.merge(admin)
        else:
            self.db.add(admin)

        self.db.commit()
        return admin

    def buscar_todos(self) -> list[Admin]:
        return self.db.query(Admin).all()

    def buscar_por_id(self, admin_id: int) -> Admin | None:
        return self.db.query(Admin).filter(Admin.admin_id == admin_id).first()

    def buscar_por_email(self, email: str) -> Admin | None:
        return self.db.query(Admin).filter(Admin.email == email).first()

    def buscar_por_keycloak_id(self, keycloak_id: str) -> Admin | None:
        return self.db.query(Admin).filter(Admin.keycloak_id == keycloak_id).first()

    def deletar(self, admin: Admin) -> None:
        self.db.delete(admin)
        self.db.commit()
