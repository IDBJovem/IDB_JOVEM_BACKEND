"""Testes de integração para o módulo drive (Galeria Google Drive).

Estratégia: drive usa verificar_roles (Keycloak) + header X-Google-Authorization.
Mockamos obter_usuario_atual para bypassar o Keycloak e ServicoDrive
para não chamar o Google Drive real.
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

from src.drive.controller import router
from src.security import obter_usuario_atual


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

USUARIO_ADMIN = {"sub": "uuid-admin", "realm_access": {"roles": ["admin", "superadmin"]}}

TOKEN_GOOGLE = "Bearer token-google-valido"


@pytest.fixture
def mock_servico():
    return MagicMock()


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[obter_usuario_atual] = lambda: USUARIO_ADMIN
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Dados de teste
# ---------------------------------------------------------------------------

FOTO_RESPOSTA = {
    "id": "abc123",
    "nome": "foto_evento.jpg",
    "url_visualizacao": "https://drive.google.com/file/abc123",
}


# ---------------------------------------------------------------------------
# GET /galeria/fotos
# ---------------------------------------------------------------------------

class TestListarFotos:

    def test_listar_fotos_sucesso(self, client):
        """GET /galeria/fotos com token e pasta válidos deve retornar lista."""
        with patch("src.drive.controller.ServicoDrive") as MockServico:
            from src.drive.schema import RespostaDrive
            MockServico.return_value.listar_fotos.return_value = [FOTO_RESPOSTA]
            resposta = client.get(
                "/galeria/fotos?pasta=Retiro2025",
                headers={"X-Google-Authorization": TOKEN_GOOGLE}
            )
        assert resposta.status_code == 200
        assert isinstance(resposta.json(), list)

    def test_listar_fotos_lista_vazia(self, client):
        with patch("src.drive.controller.ServicoDrive") as MockServico:
            MockServico.return_value.listar_fotos.return_value = []
            resposta = client.get(
                "/galeria/fotos?pasta=PastaVazia",
                headers={"X-Google-Authorization": TOKEN_GOOGLE}
            )
        assert resposta.status_code == 200
        assert resposta.json() == []

    def test_listar_fotos_sem_token_google_retorna_401(self, client):
        """Sem o header X-Google-Authorization deve retornar 401."""
        resposta = client.get("/galeria/fotos?pasta=Retiro2025")
        assert resposta.status_code == 401
        assert "Token Google ausente" in resposta.json()["detail"]

    def test_listar_fotos_sem_pasta_retorna_422(self, client):
        """Parâmetro 'pasta' é obrigatório — sem ele retorna 422."""
        resposta = client.get(
            "/galeria/fotos",
            headers={"X-Google-Authorization": TOKEN_GOOGLE}
        )
        assert resposta.status_code == 422

    def test_listar_fotos_pasta_vazia_retorna_422(self, client):
        """Parâmetro 'pasta' com string vazia deve retornar 422 (min_length=1)."""
        resposta = client.get(
            "/galeria/fotos?pasta=",
            headers={"X-Google-Authorization": TOKEN_GOOGLE}
        )
        assert resposta.status_code == 422

    def test_listar_fotos_pasta_nao_encontrada_retorna_404(self, client):
        """ValueError do serviço deve ser convertido em 404."""
        with patch("src.drive.controller.ServicoDrive") as MockServico:
            MockServico.return_value.listar_fotos.side_effect = ValueError("Pasta não encontrada")
            resposta = client.get(
                "/galeria/fotos?pasta=PastaInexistente",
                headers={"X-Google-Authorization": TOKEN_GOOGLE}
            )
        assert resposta.status_code == 404
        assert "Pasta não encontrada" in resposta.json()["detail"]

    def test_listar_fotos_erro_google_retorna_502(self, client):
        """RuntimeError do serviço deve ser convertido em 502."""
        with patch("src.drive.controller.ServicoDrive") as MockServico:
            MockServico.return_value.listar_fotos.side_effect = RuntimeError("Falha ao acessar Drive")
            resposta = client.get(
                "/galeria/fotos?pasta=Retiro2025",
                headers={"X-Google-Authorization": TOKEN_GOOGLE}
            )
        assert resposta.status_code == 502
        assert "Falha ao acessar Drive" in resposta.json()["detail"]

    @pytest.mark.parametrize("pasta", [
        "Retiro2025",
        "Encontro Teen",
        "Fotos Voluntarios",
        "Galeria Geral",
    ])
    def test_listar_fotos_varias_pastas(self, client, pasta):
        """Listagem de fotos com diferentes nomes de pasta."""
        with patch("src.drive.controller.ServicoDrive") as MockServico:
            MockServico.return_value.listar_fotos.return_value = []
            resposta = client.get(
                f"/galeria/fotos?pasta={pasta}",
                headers={"X-Google-Authorization": TOKEN_GOOGLE}
            )
        assert resposta.status_code == 200

    @pytest.mark.parametrize("status_erro,excecao", [
        (404, ValueError("Pasta não encontrada")),
        (502, RuntimeError("Falha no Drive")),
    ])
    def test_listar_fotos_erros_mapeados(self, client, status_erro, excecao):
        """Verifica mapeamento correto de exceções para status HTTP."""
        with patch("src.drive.controller.ServicoDrive") as MockServico:
            MockServico.return_value.listar_fotos.side_effect = excecao
            resposta = client.get(
                "/galeria/fotos?pasta=Teste",
                headers={"X-Google-Authorization": TOKEN_GOOGLE}
            )
        assert resposta.status_code == status_erro