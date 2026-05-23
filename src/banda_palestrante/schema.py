from typing import Optional

from pydantic import BaseModel


class SchemaCriarBandaPalestrante(BaseModel):
    nome: str
    link_foto: Optional[str]
    profissao: Optional[str]


class SchemaRespostaBandaPalestrante(BaseModel):
    id: int
    nome: str
    link_foto: Optional[str]
    profissao: Optional[str]
