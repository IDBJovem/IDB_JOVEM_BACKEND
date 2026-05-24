from sqlalchemy.orm import Session
from src.produto.model import Produto


class RepositorioProduto:

    def __init__(self, db: Session):
        self.db = db

    def salvar(self, produto: Produto) -> Produto:
        self.db.add(produto)
        self.db.commit()
        return produto

    def buscar_todos(self) -> list[Produto]:
        return self.db.query(Produto).all()

    def buscar_por_id(self, produto_id: int) -> Produto | None:
        return (
            self.db.query(Produto)
            .filter(Produto.produto_id == produto_id)
            .first()
        )

    def deletar(self, produto: Produto) -> None:
        self.db.delete(produto)
        self.db.commit()
