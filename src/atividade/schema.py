from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SchemaCriarAtividade(BaseModel):
    nome: str
    descricao: Optional[str]
    horario_inicio: datetime
    horario_termino: datetime
    evento_id: int


class SchemaRespostaAtividade(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]
    horario_inicio: datetime
    horario_termino: datetime
    evento_id: int
