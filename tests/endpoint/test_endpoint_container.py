"""Testes de endpoint — apontam para o container real via HTTP."""

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

    @pytest.mark.parametrize("tentativa", [1, 2, 3])
    def test_root_consistente_em_multiplas_chamadas(self, tentativa):
        resposta = httpx.get(f"{BASE_URL}/")
        assert resposta.status_code == 200
        assert "message" in resposta.json()


class TestRotasProtegidas:

    @pytest.mark.parametrize("rota", ["/admin/", "/evento/", "/banda-palestrante/", "/produto/"])
    def test_post_sem_token_nao_retorna_200(self, rota):
        resposta = httpx.post(f"{BASE_URL}{rota}", json={"nome": "Teste"})
        assert resposta.status_code != 200

    @pytest.mark.parametrize("rota", ["/admin/", "/evento/", "/banda-palestrante/", "/produto/"])
    def test_delete_sem_token_nao_retorna_204(self, rota):
        resposta = httpx.delete(f"{BASE_URL}{rota}1")
        assert resposta.status_code != 204
