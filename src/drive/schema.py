from pydantic import BaseModel

class RespostaDrive(BaseModel):
    id: str
    nome: str
    url_visualizacao: str

    class Config:
        from_attributes = True