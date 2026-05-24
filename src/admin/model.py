from sqlalchemy import Column, Integer, Text
from src.database import Base


class Admin(Base):
    __tablename__ = "admin"

    admin_id    = Column(Integer, primary_key=True, autoincrement=True)
    nome        = Column(Text, nullable=False)
    email       = Column(Text, unique=True, nullable=False)
    keycloak_id = Column(Text, unique=True, nullable=False)
