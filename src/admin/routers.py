# Aqui que fica as rotas HTTP (Endpoints) usando FastAPI.
# Arquivo usado para comunicacao entre o front-end e o back-end.
# Arquivo e meramente ilustrativo e deve ser ajustado de acordo com o nosso projeto.
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from src.security import verificar_roles

router = APIRouter(prefix="/admin", tags=["admin"])


class SchemaCriarAdmin(BaseModel):
    nome: str
    email: str
    keycloak_id: str
    roles: List[str] = ["admin"]


class SchemaRespostaAdmin(BaseModel):
    id: int
    nome: str
    email: str
    keycloak_id: str
    roles: List[str]


class SchemaAtualizarPermissoes(BaseModel):
    roles: List[str]


BANCO_MOCK_ADMINS: List[SchemaRespostaAdmin] = [
    SchemaRespostaAdmin(
        id=1,
        nome="Admin Joao",
        email="admin@idb.com",
        keycloak_id="kc-1",
        roles=["admin"],
    )
]


@router.get("/", response_model=List[SchemaRespostaAdmin])
def listar_admins():
    """Retorna a lista de administradores cadastrados no sistema."""
    return BANCO_MOCK_ADMINS


@router.post(
    "/",
    response_model=SchemaRespostaAdmin,
    status_code=status.HTTP_201_CREATED,
)

def criar_admin(
    payload: SchemaCriarAdmin,
    usuario_logado: dict = Depends(verificar_roles(["admin", "superadmin"])),
):
    """Cadastra um administrador verificando as permissoes do usuario."""
    novo_admin = SchemaRespostaAdmin(id=len(BANCO_MOCK_ADMINS) + 1, **payload.model_dump())
    BANCO_MOCK_ADMINS.append(novo_admin)
    return novo_admin


@router.put(
    "/{admin_id}/permissoes",
    response_model=SchemaRespostaAdmin,
)
def atualizar_permissoes_admin(
    admin_id: int,
    payload: SchemaAtualizarPermissoes,
    usuario_logado: dict = Depends(verificar_roles(["superadmin"])),
):
    """Atualiza as permissoes de um administrador (apenas superadmin)."""
    if str(usuario_logado.get("sub")) == str(admin_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nao e permitido alterar as proprias permissoes.",
        )
    admin_encontrado = next(
        (admin for admin in BANCO_MOCK_ADMINS if admin.id == admin_id),
        None,
    )
    if not admin_encontrado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Administrador nao encontrado.",
        )
    admin_encontrado.roles = payload.roles
    return admin_encontrado
