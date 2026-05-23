# Aqui que fica as rotas HTTP (Endpoints) usando FastAPI.
# Arquivo usado para comunicacao entre o front-end e o back-end.
# Arquivo e meramente ilustrativo e deve ser ajustado de acordo com o nosso projeto.
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from src.voluntario.schema import SchemaCriarVoluntario, SchemaRespostaVoluntario
from src.security import verificar_roles

router = APIRouter(prefix="/voluntarios", tags=["voluntarios"])


BANCO_MOCK_VOLUNTARIOS: List[SchemaRespostaVoluntario] = [
    SchemaRespostaVoluntario(
        id=1,
        nome="Ana Lima",
        email="ana@exemplo.com",
        link_formulario=None,
    )
]


@router.get("/", response_model=List[SchemaRespostaVoluntario])
def listar_voluntarios():
    """Retorna a lista de voluntarios cadastrados no sistema."""
    return BANCO_MOCK_VOLUNTARIOS


@router.post(
    "/",
    response_model=SchemaRespostaVoluntario,
    status_code=status.HTTP_201_CREATED,
)

def criar_voluntario(
    payload: SchemaCriarVoluntario,
    usuario_logado: dict = Depends(verificar_roles(["admin", "superadmin"])),
):
    """Cadastra um voluntario verificando as permissoes do usuario."""
    novo_voluntario = SchemaRespostaVoluntario(
        id=len(BANCO_MOCK_VOLUNTARIOS) + 1,
        **payload.model_dump(),
    )
    BANCO_MOCK_VOLUNTARIOS.append(novo_voluntario)
    return novo_voluntario
