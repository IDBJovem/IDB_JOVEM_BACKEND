# Aqui que fica as rotas HTTP (Endpoints) usando FastAPI.
# Arquivo usado para comunicacao entre o front-end e o back-end.
# Arquivo e meramente ilustrativo e deve ser ajustado de acordo com o nosso projeto.
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from src.banda_palestrante.schema import (
    SchemaCriarBandaPalestrante,
    SchemaRespostaBandaPalestrante,
)
from src.security import verificar_roles

router = APIRouter(prefix="/banda-palestrante", tags=["banda_palestrante"])


BANCO_MOCK_BANDA_PALESTRANTE: List[SchemaRespostaBandaPalestrante] = [
    SchemaRespostaBandaPalestrante(
        id=1,
        nome="Maria Silva",
        link_foto=None,
        profissao="Palestrante",
    )
]


@router.get("/", response_model=List[SchemaRespostaBandaPalestrante])
def listar_banda_palestrante():
    """Retorna a lista de bandas e palestrantes cadastrados no sistema."""
    return BANCO_MOCK_BANDA_PALESTRANTE


@router.post(
    "/",
    response_model=SchemaRespostaBandaPalestrante,
    status_code=status.HTTP_201_CREATED,
)

def criar_banda_palestrante(
    payload: SchemaCriarBandaPalestrante,
    usuario_logado: dict = Depends(verificar_roles(["admin", "superadmin"])),
):
    """Cadastra um participante verificando as permissoes do usuario."""
    novo_participante = SchemaRespostaBandaPalestrante(
        id=len(BANCO_MOCK_BANDA_PALESTRANTE) + 1,
        **payload.model_dump(),
    )
    BANCO_MOCK_BANDA_PALESTRANTE.append(novo_participante)
    return novo_participante
