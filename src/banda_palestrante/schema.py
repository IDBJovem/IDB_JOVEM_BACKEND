from pydantic import BaseModel

class BaseBandaPalestrante(BaseModel):
    nome: str
    link_foto: str | None = None
    profissao: str | None = None


class SolicitacaoBandaPalestrante(BaseBandaPalestrante):
    pass


class RespostaBandaPalestrante(BaseBandaPalestrante):
    participante_id: int

    class Config:
        from_attributes = True
