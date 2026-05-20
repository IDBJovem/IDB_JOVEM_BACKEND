from datetime import date

from pydantic import BaseModel

# Esse schema define o que o seu frontend vai receber quando pedir os eventos
class EventoResponse(BaseModel):
    titulo: str
    data: date
    local: str

    # Isso permite que o Pydantic leia dados
    class Config:
        from_attributes = True
