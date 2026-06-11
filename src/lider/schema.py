from pydantic import BaseModel
from typing import Optional

class BaseLider(BaseModel):
    nome: str
    cargo: str
    imagem_url: Optional[str] = None
    is_antigo: bool = False
    ordem: int = 0

class SolicitacaoLider(BaseLider):
    pass

class RespostaLider(BaseLider):
    lider_id: int

    class Config:
        from_attributes = True
