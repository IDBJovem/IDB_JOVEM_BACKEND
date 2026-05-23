from datetime import datetime
from pydantic import BaseModel


class BaseAtividade(BaseModel):
    nome: str
    descricao: str | None = None
    horario_inicio: datetime
    horario_termino: datetime

class SolicitacaoAtividade(BaseAtividade):
    """"
    Modelo para a solicitação de criação ou atualização de uma atividade.
    Herda os campos básicos de BaseAtividade.
    """

class RespostaAtividade(BaseAtividade):
    atividade_id: int
    evento_id: int

    class Config:
        from_attributes = True
