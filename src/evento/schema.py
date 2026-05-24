# É aqui que acontece a validação dos dados de entrada usando Pydantic.
# Esse código é meramente ilustrativo. Será necessário ajustar de acordo com o nosso projeto.

from datetime import datetime
from pydantic import BaseModel


class BaseEvento(BaseModel):
    nome: str
    descricao: str | None = None
    local_latitude: float | None = None
    local_longitude: float | None = None
    data_inicio: datetime
    data_fim: datetime
    link_galeria: str | None = None
    formulario_link: str | None = None


class RespostaEvento(BaseModel):
    evento_id: int
    nome: str
    descricao: str | None = None
    local_latitude: float | None = None
    local_longitude: float | None = None
    data_inicio: datetime
    data_fim: datetime
    link_galeria: str | None = None
    formulario_link: str | None = None

    class Config:
        from_attributes = True

class SolicitacaoEvento(BaseEvento):
    pass

class ContagemRespostaEvento(BaseModel):
    pass
