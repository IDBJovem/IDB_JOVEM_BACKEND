from pydantic import BaseModel


class RespostaInscricaoFormulario(BaseModel):
    evento_id: int
    voluntario_id: int
    nome: str
    email: str
    status: str
    resposta_id: str
    link_resposta: str

    class Config:
        from_attributes = True
