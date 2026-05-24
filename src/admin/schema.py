from pydantic import BaseModel, EmailStr


class BaseAdmin(BaseModel):
    nome: str
    email: EmailStr
    keycloak_id: str


class SolicitacaoAdmin(BaseAdmin):
    pass


class RespostaAdmin(BaseAdmin):
    admin_id: int

    class Config:
        from_attributes = True
