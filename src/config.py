# Classe para o mapeamento seguro do arquivo .env
# Aqui q ficam as chaves de API, URLs de banco e credenciais de segurança

from pydantic_settings import BaseSettings, SettingsConfigDict

class ConfiguracoesAmbiente(BaseSettings):
    # Se for cadastrado um valor no .env, ele deve ser declarado aqui
    AMBIENTE: str = "desenvolvimento"
    PORTA: int = 8000

    # Banco de Dados
    DATABASE_URL: str

    # APIs do Google
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = ""

    # Autenticação
    KEYCLOAK_URL: str = ""
    KEYCLOAK_REALM: str = ""
    KEYCLOAK_CLIENT_ID: str = ""
    KEYCLOAK_ISSUER: str = ""
    KEYCLOAK_JWKS_URL: str = ""
    KEYCLOAK_AUDIENCE: str = ""

    SECRET_KEY: str = "dev-secret"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

configuracoes = ConfiguracoesAmbiente()
