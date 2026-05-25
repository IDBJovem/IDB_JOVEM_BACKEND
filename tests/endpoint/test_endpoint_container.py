"""Testes de integração — apontam para o container real via HTTP com banco de dados."""

import pytest
import httpx

pytestmark = pytest.mark.endpoint

BASE_URL = "http://localhost:8000"


class TestInfrastrutura:

    def test_aplicacao_esta_no_ar(self):
        resposta = httpx.get(f"{BASE_URL}/health")
        assert resposta.status_code == 200
        assert resposta.json() == {"status": "ok"}

    def test_root_retorna_mensagem(self):
        resposta = httpx.get(f"{BASE_URL}/")
        assert resposta.status_code == 200
        assert "message" in resposta.json()

    @pytest.mark.parametrize("tentativa", [1, 2, 3])
    def test_health_estavel_em_multiplas_chamadas(self, tentativa):
        resposta = httpx.get(f"{BASE_URL}/health")
        assert resposta.status_code == 200
        assert resposta.json().get("status") == "ok"


class TestRotasPublicas:

    @pytest.mark.parametrize("rota", ["/banda-palestrante/", "/produto/"])
    def test_rotas_publicas_retornam_200(self, rota):
        resposta = httpx.get(f"{BASE_URL}{rota}")
        assert resposta.status_code == 200

    def test_banda_palestrante_retorna_lista(self):
        resposta = httpx.get(f"{BASE_URL}/banda-palestrante/")
        assert resposta.status_code == 200
        assert isinstance(resposta.json(), list)

    def test_produto_retorna_lista(self):
        resposta = httpx.get(f"{BASE_URL}/produto/")
        assert resposta.status_code == 200
        assert isinstance(resposta.json(), list)

    def test_banda_palestrante_content_type_json(self):
        resposta = httpx.get(f"{BASE_URL}/banda-palestrante/")
        assert "application/json" in resposta.headers["content-type"]

    def test_banda_palestrante_id_inexistente_retorna_404(self):
        resposta = httpx.get(f"{BASE_URL}/banda-palestrante/999999")
        assert resposta.status_code == 404

    def test_produto_id_inexistente_retorna_404(self):
        resposta = httpx.get(f"{BASE_URL}/produto/999999")
        assert resposta.status_code == 404


class TestRotasProtegidas:

    @pytest.mark.parametrize("rota,status_esperado", [
        ("/admin/", 403),
        ("/evento/", 401),
        ("/banda-palestrante/", 403),
        ("/produto/", 403),
    ], ids=["admin", "evento", "banda-post", "produto-post"])
    def test_post_protegido_sem_token(self, rota, status_esperado):
        """POST em rotas protegidas deve rejeitar sem token."""
        resposta = httpx.post(f"{BASE_URL}{rota}", json={"nome": "Teste"})
        assert resposta.status_code == status_esperado

    @pytest.mark.parametrize("rota", ["/admin/", "/evento/"])
    def test_get_protegido_nao_retorna_200_sem_token(self, rota):
        resposta = httpx.get(f"{BASE_URL}{rota}")
        assert resposta.status_code != 200

    def test_admin_get_sem_token_retorna_403(self):
        resposta = httpx.get(f"{BASE_URL}/admin/")
        assert resposta.status_code == 403

    def test_evento_get_sem_token_retorna_401(self):
        resposta = httpx.get(f"{BASE_URL}/evento/")
        assert resposta.status_code == 401

    @pytest.mark.parametrize("rota", [
        "/admin/",
        "/evento/",
        "/banda-palestrante/",
        "/produto/",
    ])
    def test_delete_protegido_sem_token(self, rota):
        """DELETE sem token nunca deve retornar 200 ou 204."""
        resposta = httpx.delete(f"{BASE_URL}{rota}1")
        assert resposta.status_code not in (200, 204)
