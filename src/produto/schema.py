from pydantic import BaseModel


class BaseProduto(BaseModel):
    nome: str
    descricao: str | None = None
    link_produto: str | None = None


class SolicitacaoProduto(BaseProduto):
    pass


class RespostaProduto(BaseProduto):
    produto_id: int

    class Config:
        from_attributes = True
