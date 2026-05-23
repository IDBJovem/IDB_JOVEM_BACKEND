# Aqui que fica as rotas HTTP (Endpoints) usando FastAPI.
# Arquivo usado para comunicacao entre o front-end e o back-end.
# Arquivo e meramente ilustrativo e deve ser ajustado de acordo com o nosso projeto.
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from src.atividade.schema import SchemaCriarAtividade, SchemaRespostaAtividade
from src.security import verificar_roles

router = APIRouter(prefix="/atividades", tags=["atividades"])


BANCO_MOCK_ATIVIDADES: List[SchemaRespostaAtividade] = [
    SchemaRespostaAtividade(
        id=1,
        nome="Abertura",
        descricao="Boas-vindas e apresentacao.",
        horario_inicio=datetime(2026, 5, 20, 9, 0, 0),
        horario_termino=datetime(2026, 5, 20, 10, 0, 0),
        evento_id=1,
    )
]


@router.get("/", response_model=List[SchemaRespostaAtividade])
def listar_atividades():
    """Retorna a lista de atividades cadastradas no sistema."""
    return BANCO_MOCK_ATIVIDADES


@router.post(
    "/",
    response_model=SchemaRespostaAtividade,
    status_code=status.HTTP_201_CREATED,
)

def criar_atividade(
    payload: SchemaCriarAtividade,
    usuario_logado: dict = Depends(verificar_roles(["admin", "superadmin"])),
):
    """Cadastra uma atividade verificando as permissoes do usuario."""
    if payload.horario_termino <= payload.horario_inicio:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O horario de termino deve ser maior que o de inicio.",
        )
    nova_atividade = SchemaRespostaAtividade(
        id=len(BANCO_MOCK_ATIVIDADES) + 1,
        **payload.model_dump(),
    )
    BANCO_MOCK_ATIVIDADES.append(nova_atividade)
    return nova_atividade
