# É aqui que acontece a validação dos dados de entrada usando Pydantic.
# Esse código é meramente ilustrativo. Será necessário ajustar de acordo com o nosso projeto.

from datetime import datetime
from pydantic import BaseModel


class BaseEvento(BaseModel):
    titulo: str
    data_inicio: datetime
    data_fim: datetime


class RespostaEvento(BaseModel):
    id: int
    titulo: str
    data_inicio: datetime
    data_fim: datetime
    link_calendario: str

    class Config:
        from_attributes = True

class SolicitacaoEvento(BaseEvento):
    pass

class ContagemRespostaEvento(BaseModel):
    pass
