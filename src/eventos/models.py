# É aqui que definimos a tabela física do banco de dados para Eventos.
# O código é meramente ilustrativo e deve ser ajustado de acordo com o nosso projeto.

from sqlalchemy import Column, Integer, String, Text
from src.database import Base

class ModeloEvento(Base):
    # Modelo para a tabela de eventos no banco de dados.

    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    data_inicio = Column(String(255), nullable=False)
    data_fim = Column(String(255), nullable=False)
    link_calendario = Column(Text, nullable=True)
