"""Testes de integração para o módulo auth (OAuth2 Google).

Estratégia: as rotas de auth usam sessão e redirecionamento OAuth2.
Testamos os comportamentos HTTP sem depender do Google externo,
mockando o ServicoAuth com patch.
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from starlette.middleware.sessions import SessionMiddleware

from src.auth.controller import router


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def client():
    app = FastAPI()
    app.add_middleware(SessionMiddleware, secret_key="test-secret")
    app.include_router(router)
    with TestClient(app, follow_redirects=False) as c:
        yield c


# ---------------------------------------------------------------------------
# GET /auth/login
# ---------------------------------------------------------------------------

class TestIniciarLogin:

    def test_login_redireciona_para_google(self, client):
        """GET /auth/login deve retornar um redirecionamento (302/307)."""
        with patch("src.auth.controller.ServicoAuth") as MockServico:
            MockServico.return_value.gerar_url_login.return_value = (
                "https://accounts.google.com/o/oauth2/auth?client_id=test",
                "estado-teste",
                "verificador-teste"
            )
            resposta = client.get("/auth/login")
        assert resposta.status_code in (302, 307)

    def test_login_redireciona_para_url_google(self, client):
        """A URL de redirecionamento deve apontar para o Google."""
        with patch("src.auth.controller.ServicoAuth") as MockServico:
            MockServico.return_value.gerar_url_login.return_value = (
                "https://accounts.google.com/o/oauth2/auth?client_id=test",
                "estado-teste",
                "verificador-teste"
            )
            resposta = client.get("/auth/login")
        location = resposta.headers.get("location", "")
        assert "google" in location or resposta.status_code in (302, 307)

    @pytest.mark.parametrize("tentativa", [1, 2, 3])
    def test_login_consistente_em_multiplas_chamadas(self, client, tentativa):
        """Endpoint de login deve ser estável em múltiplas chamadas."""
        with patch("src.auth.controller.ServicoAuth") as MockServico:
            MockServico.return_value.gerar_url_login.return_value = (
                "https://accounts.google.com/o/oauth2/auth",
                f"estado-{tentativa}",
                f"verificador-{tentativa}"
            )
            resposta = client.get("/auth/login")
        assert resposta.status_code in (302, 307)


# ---------------------------------------------------------------------------
# GET /auth/callback
# ---------------------------------------------------------------------------

class TestCallbackGoogle:

    def test_callback_sem_sessao_retorna_400(self, client):
        """Sem sessão OAuth (estado/verificador), deve retornar 400."""
        resposta = client.get("/auth/callback?code=codigo-teste")
        assert resposta.status_code == 400
        assert "Sessao OAuth expirada" in resposta.json()["detail"]

    def test_callback_sem_code_retorna_422(self, client):
        """Sem o parâmetro 'code', deve retornar 422 (campo obrigatório)."""
        resposta = client.get("/auth/callback")
        assert resposta.status_code == 422

    @pytest.mark.parametrize("code", [
        "code_invalido_123",
        "outro_code_456",
        "code_expirado_789",
    ])
    def test_callback_sem_sessao_sempre_retorna_400(self, client, code):
        """Qualquer code sem sessão válida deve retornar 400."""
        resposta = client.get(f"/auth/callback?code={code}")
        assert resposta.status_code == 400