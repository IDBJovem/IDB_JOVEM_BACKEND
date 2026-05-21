"""Modulo de seguranca para integracao e validacao de tokens JWT do Keycloak."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

autenticacao_bearer = HTTPBearer()

# URL de configuracao do seu Keycloak local (substitua pelo seu realm)
URL_CONFIG_KEYCLOAK = "http://localhost:8080/admin/master/console/#/jovem"

# CHAVE_PUBLICA: chave publica do realm
CHAVE_PUBLICA_KEYCLOAK = (
    "-----BEGIN PUBLIC KEY-----\n"
    "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAucurtWzeEtsQRfsDdOmfeR5T6PM/6m2q+wmNHvPHO1mO/KQ+B59ksw49IksV313a3sD+y98SX0IZgTNSks+fZtpZLSd2dGFdMECbOh5GgUtZdLE8HhSxZAYGOup8A+oPEIJZCgMqMwXgnyBlamzoXH8F7zokwEHZQ0kjoh0JvamlYQ8Q3VKPn6dsCpdlIn8FYImF5ueNvkrLGuxqVW8qRqQfg40sZIJB6Ab7Sjw6BrVw4NoD0zSVsKRuKAhUVjLQQ8HKGpAJ+Lh0b+gRJKHqqfGIGBHkSgwXbXUOL84N3GdUNb9QJTapsxpAV0PCLcXkV49zpd0eE7A0qsb70TxfbQIDAQAB\n"
    "-----END PUBLIC KEY-----"
)


async def obter_usuario_atual(
    credenciais: HTTPAuthorizationCredentials = Depends(autenticacao_bearer)
):
    """Decodifica o token JWT enviado pelo front-end e valida as permissoes."""
    token = credenciais.credentials

    try:
        # Valida a assinatura, a expiracao e o cliente alvo (audience) do token
        payload_token = jwt.decode(
            token,
            CHAVE_PUBLICA_KEYCLOAK,
            algorithms=["RS256"],
            audience=["account", "jovem-backend"],
        )
        if payload_token.get("azp") != "jovem-backend":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalido para este cliente.",
            )
        return payload_token
    except jwt.ExpiredSignatureError as erro:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="O token de acesso expirou."
        ) from erro
    except jwt.InvalidTokenError as erro:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido ou assinatura incorreta."
        ) from erro


def verificar_role(role_exigida: str):
    """Fabrica de dependencias para verificar papeis do Keycloak no token."""
    def dependencia(usuario: dict = Depends(obter_usuario_atual)):
        # O Keycloak costuma injetar as roles dentro de 'realm_access'
        acesso_realm = usuario.get("realm_access", {})
        roles_usuario = acesso_realm.get("roles", [])

        if role_exigida not in roles_usuario:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acesso negado. Requer o papel de: {role_exigida}"
            )
        return usuario
    return dependencia


def verificar_roles(roles_exigidas: list[str]):
    """Fabrica de dependencias para verificar multiplos papeis."""
    def dependencia(usuario: dict = Depends(obter_usuario_atual)):
        acesso_realm = usuario.get("realm_access", {})
        roles_usuario = acesso_realm.get("roles", [])

        if not any(role in roles_usuario for role in roles_exigidas):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "Acesso negado. Requer um dos papeis: "
                    f"{', '.join(roles_exigidas)}"
                ),
            )
        return usuario

    return dependencia