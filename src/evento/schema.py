from datetime import datetime
from pydantic import BaseModel


class BaseEvento(BaseModel):
    nome: str
    descricao: str | None = None
    local_latitude: float
    local_longitude: float
    data_inicio: datetime
    data_fim: datetime
    link_galeria: str | None = None

class SolicitacaoEvento(BaseEvento):
    """"
    Modelo para a solicitação de criação ou atualização de um evento.
    Herda os campos básicos de Baseevento.
    """

class RespostaEvento(BaseEvento):
    evento_id: int
    calendario_evento_id: str | None = None
    nome_local: str

    class Config:
        from_attributes = True
