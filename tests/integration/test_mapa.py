"""Testes de integração para o módulo mapa.

Estratégia: mapa usa ServicoMapa instanciado diretamente na rota
e validar_coordenadas do shared/utils. Mockamos ServicoMapa com
patch para não chamar a API de geocoding real.
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch

from src.mapa.controller import router


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


# ---------------------------------------------------------------------------
# GET /mapa/endereco
# ---------------------------------------------------------------------------

class TestBuscarEndereco:

    def test_buscar_endereco_sucesso(self, client):
        """Coordenadas válidas com resposta do serviço deve retornar 200."""
        with patch("src.mapa.controller.ServicoMapa") as MockServico:
            MockServico.return_value.buscar_endereco_por_coordenadas.return_value = (
                "Brasília, DF, Brasil"
            )
            resposta = client.get("/mapa/endereco?latitude=-15.7801&longitude=-47.9292")
        assert resposta.status_code == 200
        assert resposta.json()["nome_local"] == "Brasília, DF, Brasil"

    def test_buscar_endereco_nao_encontrado_retorna_404(self, client):
        """Quando o serviço retorna None, deve retornar 404."""
        with patch("src.mapa.controller.ServicoMapa") as MockServico:
            MockServico.return_value.buscar_endereco_por_coordenadas.return_value = None
            resposta = client.get("/mapa/endereco?latitude=-15.7801&longitude=-47.9292")
        assert resposta.status_code == 404
        assert "Endereço não encontrado" in resposta.json()["detail"]

    def test_buscar_endereco_sem_latitude_retorna_422(self, client):
        """Parâmetro latitude é obrigatório."""
        resposta = client.get("/mapa/endereco?longitude=-47.9292")
        assert resposta.status_code == 422

    def test_buscar_endereco_sem_longitude_retorna_422(self, client):
        """Parâmetro longitude é obrigatório."""
        resposta = client.get("/mapa/endereco?latitude=-15.7801")
        assert resposta.status_code == 422

    def test_buscar_endereco_sem_parametros_retorna_422(self, client):
        """Sem nenhum parâmetro deve retornar 422."""
        resposta = client.get("/mapa/endereco")
        assert resposta.status_code == 422

    def test_buscar_endereco_coordenadas_invalidas_retorna_400(self, client):
        """Coordenadas fora do range válido devem retornar 400."""
        with patch("src.mapa.controller.ServicoMapa"):
            resposta = client.get("/mapa/endereco?latitude=999&longitude=999")
        assert resposta.status_code == 400

    def test_buscar_endereco_latitude_texto_retorna_422(self, client):
        """Latitude não numérica deve retornar 422."""
        resposta = client.get("/mapa/endereco?latitude=abc&longitude=-47.9292")
        assert resposta.status_code == 422

    @pytest.mark.parametrize("latitude,longitude,nome_esperado", [
        (-15.7801, -47.9292, "Brasília, DF"),
        (-23.5505, -46.6333, "São Paulo, SP"),
        (-22.9068, -43.1729, "Rio de Janeiro, RJ"),
        (-3.7172, -38.5433, "Fortaleza, CE"),
    ])
    def test_buscar_endereco_varias_cidades(self, client, latitude, longitude, nome_esperado):
        """Busca de endereço para diferentes coordenadas brasileiras."""
        with patch("src.mapa.controller.ServicoMapa") as MockServico:
            MockServico.return_value.buscar_endereco_por_coordenadas.return_value = nome_esperado
            resposta = client.get(f"/mapa/endereco?latitude={latitude}&longitude={longitude}")
        assert resposta.status_code == 200
        assert resposta.json()["nome_local"] == nome_esperado

    @pytest.mark.parametrize("latitude,longitude", [
        (-15.7801, -47.9292),
        (-23.5505, -46.6333),
        (-22.9068, -43.1729),
    ])
    def test_buscar_endereco_retorna_nome_local(self, client, latitude, longitude):
        """Resposta deve sempre conter o campo nome_local."""
        with patch("src.mapa.controller.ServicoMapa") as MockServico:
            MockServico.return_value.buscar_endereco_por_coordenadas.return_value = "Local Teste"
            resposta = client.get(f"/mapa/endereco?latitude={latitude}&longitude={longitude}")
        assert resposta.status_code == 200
        assert "nome_local" in resposta.json()