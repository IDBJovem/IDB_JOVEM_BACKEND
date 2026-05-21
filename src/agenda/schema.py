from datetime import date, datetime

from pydantic import BaseModel

# Esse schema define o que o seu frontend vai receber quando pedir os eventos
class EventoResponse(BaseModel):
    id_google: str | None = None
    link_calendario: str | None = None
    titulo: str
    data: date
    local: str

    # Isso permite que o Pydantic leia dados
    class Config:
        from_attributes = True


class SolicitacaoEventoAgenda(BaseModel):
    titulo: str
    data_inicio: datetime
    data_fim: datetime
    local: str | None = None
    descricao: str | None = None


class RespostaEventoAgenda(BaseModel):
    id_google: str
    link_calendario: str
    titulo: str
    data_inicio: datetime
    data_fim: datetime
    local: str | None = None

    class Config:
        from_attributes = True
