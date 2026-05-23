from typing import List

from pydantic import BaseModel


class SchemaCriarAdmin(BaseModel):
    nome: str
    email: str
    keycloak_id: str
    roles: List[str] = ["admin"]


class SchemaRespostaAdmin(BaseModel):
    id: int
    nome: str
    email: str
    keycloak_id: str
    roles: List[str]


class SchemaAtualizarPermissoes(BaseModel):
    roles: List[str]
