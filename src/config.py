from pydantic_settings import BaseSettings, SettingsConfigDict

class ConfiguracoesAmbiente(BaseSettings):

    DATABASE_URL: str

    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = ""

    KEYCLOAK_URL: str = ""
    KEYCLOAK_REALM: str = ""
    KEYCLOAK_CLIENT_ID: str = ""
    KEYCLOAK_ISSUER: str = ""
    KEYCLOAK_JWKS_URL: str = ""
    KEYCLOAK_AUDIENCE: str = ""

    SECRET_KEY: str = "dev-secret"

    # URL publica deste backend, usada para montar os links do proxy de imagens
    # do Drive (ex.: http://localhost:8000/drive/imagem/{file_id}).
    # Em producao, defina o dominio real da API no .env.
    BASE_URL: str = "http://localhost:8000"

    # Origens (front-ends) autorizadas a consumir a API via navegador.
    # Lista separada por virgula. Em producao, defina o dominio real no .env.
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

configuracoes = ConfiguracoesAmbiente()
