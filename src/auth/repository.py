import os
from google_auth_oauthlib.flow import Flow
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

class RepositorioAuth:
    def __init__(self):
        # Credenciais configuradas no Google Cloud
        self.id_cliente = os.getenv("GOOGLE_CLIENT_ID")
        self.segredo_cliente = os.getenv("GOOGLE_CLIENT_SECRET")
        self.uri_redirecionamento = os.getenv("GOOGLE_REDIRECT_URI")

        # Formato que o Google exige
        self.config_cliente = {
            "web": {
                "client_id": self.id_cliente,
                "client_secret": self.segredo_cliente,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        }

        # Escopos unificados (Fluxo único para as 3 APIs do Google)
        self.escopos = [
            "https://www.googleapis.com/auth/calendar.readonly",
            "https://www.googleapis.com/auth/drive.readonly",
            "https://www.googleapis.com/auth/forms.responses.readonly"
        ]

    def _criar_fluxo_google(self, estado: str | None = None) -> Flow:
        """Método interno para inicializar a biblioteca do Google"""
        return Flow.from_client_config(
            self.config_cliente,
            scopes=self.escopos,
            redirect_uri=self.uri_redirecionamento,
            state=estado,
        )

    def gerar_url_login(self) -> tuple[str, str, str]:
        """Gera o link oficial do Google para o Admin clicar e autorizar"""
        fluxo = self._criar_fluxo_google()

        # offline = pede o Refresh Token / consent = força o envio dele nos testes
        url_autorizacao, estado = fluxo.authorization_url(
            access_type="offline",
            prompt="consent"
        )
        return url_autorizacao, estado, fluxo.code_verifier

    def trocar_codigo_por_tokens(self, codigo: str, estado: str, verificador_codigo: str) -> dict:
        """Recebe o código temporário do Google e troca pelas chaves reais"""
        fluxo = self._criar_fluxo_google(estado=estado)
        fluxo.code_verifier = verificador_codigo
        fluxo.fetch_token(code=codigo)

        credenciais = fluxo.credentials

        return {
            "access_token": credenciais.token,
            "refresh_token": credenciais.refresh_token,
        }
