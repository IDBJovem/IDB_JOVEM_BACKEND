# É aqui que definimos a tabela física do banco de dados para Eventos.
# O código é meramente ilustrativo e deve ser ajustado de acordo com o nosso projeto.

from sqlalchemy import Column, Integer, String, DateTime, Text
from src.database import Base


class Evento(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    data_inicio = Column(DateTime, nullable=False)
    data_fim = Column(DateTime, nullable=False)
    link_calendario = Column(Text, nullable=True)
