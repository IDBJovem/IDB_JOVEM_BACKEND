"""Modulo de seguranca e controle de papeis (roles) via Keycloak."""

from typing import Iterable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

autenticacao_bearer = HTTPBearer()


async def obter_usuario_atual(
    credenciais: HTTPAuthorizationCredentials = Depends(autenticacao_bearer)
):
    """Valida o token JWT e retorna os dados do usuario logado."""
    token = credenciais.credentials

    # MOCK: Simulando um login de Admin ou Superadmin nos Dias 1-5
    if token == "token-admin":
        return {"sub": "1", "nome": "Admin Joao", "roles": ["admin"]}
    if token == "token-super":
        return {"sub": "2", "nome": "Super Chefe", "roles": ["superadmin"]}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalido ou expirado"
    )


def verificar_roles(roles_exigidas: Iterable[str]):
    """Fabrica de dependencias para checar uma lista de papeis do Keycloak."""
    roles_exigidas = list(roles_exigidas)

    def dependencia(usuario: dict = Depends(obter_usuario_atual)):
        roles_usuario = usuario.get("roles", [])
        if not any(role in roles_usuario for role in roles_exigidas):
            roles_txt = ", ".join(roles_exigidas)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acesso negado. Exige a permissao de {roles_txt}."
            )
        return usuario

    return dependencia


def verificar_role(role_exigida: str):
    """Fabrica de dependencias para checar papeis especificos do Keycloak."""
    return verificar_roles([role_exigida])