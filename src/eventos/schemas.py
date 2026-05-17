# É aqui que acontece a validação dos dados de entrada usando Pydantic.
# Esse código é meramente ilustrativo. Será necessário ajustar de acordo com o nosso projeto.

from datetime import datetime
from pydantic import BaseModel

class SchemaCriarEvento(BaseModel):
    # Dados de entrada: Define os campos necessários para criar um evento.

    titulo: str
    data_inicio: datetime
    data_fim: datetime

class SchemaRespostaEvento(BaseModel):
    # Dados de saída: Define os campos que serão retornados após criar um evento.

    id: int
    titulo: str
    data_inicio: datetime
    data_fim: datetime
    link_calendario: str

class Config:
    # Configuração para permitir a leitura direta dos modelos do SQLAlchemy.

    from_attributes = True
