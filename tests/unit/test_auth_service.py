import pytest
from unittest.mock import patch, MagicMock
from src.auth.service import ServicoAuth


class TestServicoAuth:
    @patch.dict("os.environ", {
        "GOOGLE_CLIENT_ID": "test-client-id",
        "GOOGLE_CLIENT_SECRET": "test-secret",
        "GOOGLE_REDIRECT_URI": "http://localhost/callback",
    })
    def test_init(self):
        servico = ServicoAuth()
        assert servico.id_cliente == "test-client-id"
        assert servico.segredo_cliente == "test-secret"
        assert servico.uri_redirecionamento == "http://localhost/callback"
        assert len(servico.escopos) == 3

    @patch.dict("os.environ", {
        "GOOGLE_CLIENT_ID": "test-client-id",
        "GOOGLE_CLIENT_SECRET": "test-secret",
        "GOOGLE_REDIRECT_URI": "http://localhost/callback",
    })
    @patch("src.auth.service.Flow.from_client_config")
    def test_criar_fluxo_google(self, mock_flow):
        mock_fluxo = MagicMock()
        mock_flow.return_value = mock_fluxo

        servico = ServicoAuth()
        resultado = servico._criar_fluxo_google(estado="test-state")

        mock_flow.assert_called_once()
        assert resultado == mock_fluxo

    @patch.dict("os.environ", {
        "GOOGLE_CLIENT_ID": "test-client-id",
        "GOOGLE_CLIENT_SECRET": "test-secret",
        "GOOGLE_REDIRECT_URI": "http://localhost/callback",
    })
    @patch("src.auth.service.Flow.from_client_config")
    def test_gerar_url_login(self, mock_flow):
        mock_fluxo = MagicMock()
        mock_fluxo.authorization_url.return_value = ("http://google.com/auth", "state-123")
        mock_fluxo.code_verifier = "verifier-123"
        mock_flow.return_value = mock_fluxo

        servico = ServicoAuth()
        url, estado, verificador = servico.gerar_url_login()

        assert url == "http://google.com/auth"
        assert estado == "state-123"
        assert verificador == "verifier-123"

    @patch.dict("os.environ", {
        "GOOGLE_CLIENT_ID": "test-client-id",
        "GOOGLE_CLIENT_SECRET": "test-secret",
        "GOOGLE_REDIRECT_URI": "http://localhost/callback",
    })
    @patch("src.auth.service.Flow.from_client_config")
    def test_trocar_codigo_por_tokens(self, mock_flow):
        mock_credenciais = MagicMock()
        mock_credenciais.token = "access-token-123"
        mock_credenciais.refresh_token = "refresh-token-456"

        mock_fluxo = MagicMock()
        mock_fluxo.credentials = mock_credenciais
        mock_flow.return_value = mock_fluxo

        servico = ServicoAuth()
        tokens = servico.trocar_codigo_por_tokens("code-123", "state-123", "verifier-123")

        assert tokens["access_token"] == "access-token-123"
        assert tokens["refresh_token"] == "refresh-token-456"

    @patch.dict("os.environ", {
        "GOOGLE_CLIENT_ID": "test-client-id",
        "GOOGLE_CLIENT_SECRET": "test-secret",
        "GOOGLE_REDIRECT_URI": "http://localhost/callback",
    })
    @patch("src.auth.service.Request")
    @patch("src.auth.service.Credentials")
    def test_obter_credenciais_validas_renova(self, mock_creds_class, mock_request):
        mock_creds = MagicMock()
        mock_creds.valid = False
        mock_creds_class.return_value = mock_creds

        servico = ServicoAuth()
        resultado = servico.obter_credenciais_validas("refresh-token")

        mock_creds.refresh.assert_called_once()
        assert resultado == mock_creds

    @patch.dict("os.environ", {
        "GOOGLE_CLIENT_ID": "test-client-id",
        "GOOGLE_CLIENT_SECRET": "test-secret",
        "GOOGLE_REDIRECT_URI": "http://localhost/callback",
    })
    @patch("src.auth.service.Request")
    @patch("src.auth.service.Credentials")
    def test_obter_credenciais_validas_ja_valida(self, mock_creds_class, mock_request):
        mock_creds = MagicMock()
        mock_creds.valid = True
        mock_creds_class.return_value = mock_creds

        servico = ServicoAuth()
        resultado = servico.obter_credenciais_validas("refresh-token")

        mock_creds.refresh.assert_not_called()
        assert resultado == mock_creds
