from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from src.database import Base


class Atividade(Base):
    __tablename__ = "atividade"

    atividade_id     = Column(Integer, primary_key=True, autoincrement=True)
    nome             = Column(Text, nullable=False)
    descricao        = Column(Text, nullable=True)
    horario_inicio   = Column(DateTime(timezone=True), nullable=False)
    horario_termino  = Column(DateTime(timezone=True), nullable=False)
    evento_id        = Column(Integer, ForeignKey("evento.evento_id"), nullable=False)
