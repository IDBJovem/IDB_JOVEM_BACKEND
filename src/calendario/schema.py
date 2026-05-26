from datetime import date, datetime

from pydantic import BaseModel

# Esse schema define o que o seu frontend vai receber quando pedir os evento
class RespostaEvento(BaseModel):
    nome: str
    data: date
    local: str

    # Isso permite que o Pydantic leia dados
    class Config:
        from_attributes = True

class SolicitacaoEvento(RespostaEvento):
    descricao: str | None = None
    data_inicio: datetime
    data_fim: datetime
