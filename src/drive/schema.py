from pydantic import BaseModel

# Schema que define a estrutura de cada foto enviada para o frontend
class RespostaDrive(BaseModel):
    id: str
    nome: str
    url_visualizacao: str

    class Config:
        from_attributes = True