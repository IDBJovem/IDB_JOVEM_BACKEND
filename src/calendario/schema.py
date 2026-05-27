from datetime import date, datetime

from pydantic import BaseModel

class RespostaEvento(BaseModel):
    nome: str
    data: date
    local: str

    class Config:
        from_attributes = True

class SolicitacaoEvento(RespostaEvento):
    descricao: str | None = None
    data_inicio: datetime
    data_fim: datetime
