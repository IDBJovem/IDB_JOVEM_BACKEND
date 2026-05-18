from sqlalchemy import Column, Integer, Text, ForeignKey
from src.database import Base


class BandaPalestrante(Base):
    __tablename__ = "banda_palestrante"

    participante_id = Column(Integer, primary_key=True, autoincrement=True)
    nome            = Column(Text, nullable=False)
    link_foto       = Column(Text, nullable=True)
    profissao       = Column(Text, nullable=True)


class Participa(Base):
    __tablename__ = "participa"

    evento_id       = Column(Integer, ForeignKey("evento.evento_id"), primary_key=True)
    participante_id = Column(Integer, ForeignKey("banda_palestrante.participante_id"), primary_key=True)
