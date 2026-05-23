from typing import Optional

from pydantic import BaseModel


class SchemaCriarVoluntario(BaseModel):
    nome: str
    email: str
    link_formulario: Optional[str]


class SchemaRespostaVoluntario(BaseModel):
    id: int
    nome: str
    email: str
    link_formulario: Optional[str]
