from sqlalchemy import Column, Integer, Text, CheckConstraint, ForeignKey
from src.database import Base


class Voluntario(Base):
    __tablename__ = "voluntario"

    voluntario_id   = Column(Integer, primary_key=True, autoincrement=True)
    nome            = Column(Text, nullable=False)
    email           = Column(Text, unique=True, nullable=False)
    resposta_id_formulario = Column(Text, nullable=True)


class Trabalha(Base):
    __tablename__ = "trabalha"

    voluntario_id = Column(Integer, ForeignKey("voluntario.voluntario_id"), primary_key=True)
    evento_id     = Column(Integer, ForeignKey("evento.evento_id"), primary_key=True)
    status        = Column(
        Text,
        CheckConstraint("status IN ('pendente', 'aprovado', 'reprovado')"),
        nullable=False,
    )
