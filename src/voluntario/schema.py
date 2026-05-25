from pydantic import BaseModel


class BaseVoluntario(BaseModel):
    nome: str
    email: str


class SolicitacaoVoluntario(BaseVoluntario):
    pass


class RespostaVoluntario(BaseVoluntario):
    voluntario_id: int

    class Config:
        from_attributes = True


class RespostaTrabalhoVoluntario(BaseModel):
    voluntario_id: int
    evento_id: int
    status: str
    resposta_id: str | None = None

    class Config:
        from_attributes = True
