"""
Testes de integração para o módulo de eventos.
Usa dependency_overrides do FastAPI para simular banco e autenticação,
testando apenas o comportamento das rotas HTTP.
"""
import pytest
from unittest.mock import MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.evento.controller import router as evento_router, get_servico
from src.security import obter_usuario_atual
from src.evento.schema import RespostaEvento


EVENTO_BASE = {
    "nome": "Retiro Teen 2025",
    "descricao": "Retiro anual",
    "local_latitude": -15.7801,
    "local_longitude": -47.9292,
    "data_inicio": "2025-07-10T08:00:00",
    "data_fim": "2025-07-12T18:00:00",
    "link_galeria": None,
    "formulario_link": None,
}

EVENTO_RESPOSTA = {
    **EVENTO_BASE,
    "evento_id": 1,
    "calendario_evento_id": None,
    "nome_local": None,
}

USUARIO_ADMIN = {"sub": "user-123", "realm_access": {"roles": ["admin", "superadmin"]}}


@pytest.fixture
def servico_mock():
    return MagicMock()


@pytest.fixture
def client_evento(servico_mock):
    app = FastAPI()
    app.include_router(evento_router)
    app.dependency_overrides[get_servico] = lambda: servico_mock
    app.dependency_overrides[obter_usuario_atual] = lambda: USUARIO_ADMIN
    with TestClient(app) as c:
        yield c, servico_mock
    app.dependency_overrides.clear()


class TestListarEventos:
    def test_retorna_200_com_lista_vazia(self, client_evento):
        client, servico = client_evento
        servico.listar_evento.return_value = []
        response = client.get("/evento/")
        assert response.status_code == 200
        assert response.json() == []

    def test_retorna_200_com_eventos(self, client_evento):
        client, servico = client_evento
        servico.listar_evento.return_value = [RespostaEvento(**EVENTO_RESPOSTA)]
        response = client.get("/evento/")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["nome"] == "Retiro Teen 2025"


class TestBuscarEventoPorId:
    def test_retorna_200_quando_existe(self, client_evento):
        client, servico = client_evento
        servico.buscar_evento.return_value = RespostaEvento(**EVENTO_RESPOSTA)
        response = client.get("/evento/1")
        assert response.status_code == 200
        assert response.json()["evento_id"] == 1

    def test_retorna_404_quando_nao_existe(self, client_evento):
        client, servico = client_evento
        servico.buscar_evento.side_effect = ValueError("Evento não encontrado")
        response = client.get("/evento/999")
        assert response.status_code == 404


PAYLOADS_EVENTO_VALIDOS = [
    pytest.param({**EVENTO_BASE}, id="payload_completo"),
    pytest.param(
        {**EVENTO_BASE, "descricao": None, "link_galeria": None},
        id="payload_sem_campos_opcionais",
    ),
    pytest.param(
        {**EVENTO_BASE, "nome": "Encontro Jovem",
         "formulario_link": "https://forms.google.com/123"},
        id="payload_com_formulario",
    ),
]


@pytest.mark.parametrize("payload", PAYLOADS_EVENTO_VALIDOS)
def test_criar_evento_payload_valido(client_evento, payload):
    client, servico = client_evento
    servico.criar_evento.return_value = RespostaEvento(
        **{**payload, "evento_id": 1, "calendario_evento_id": None, "nome_local": None}
    )
    response = client.post("/evento/", json=payload)
    assert response.status_code == 201
    assert response.json()["nome"] == payload["nome"]


PAYLOADS_EVENTO_INVALIDOS = [
    pytest.param({}, id="payload_vazio"),
    pytest.param({"nome": "Evento X"}, id="sem_coordenadas_e_datas"),
    pytest.param({**EVENTO_BASE, "local_latitude": "invalido"}, id="latitude_invalida"),
    pytest.param({**EVENTO_BASE, "data_inicio": "data-invalida"}, id="data_invalida"),
]


@pytest.mark.parametrize("payload", PAYLOADS_EVENTO_INVALIDOS)
def test_criar_evento_payload_invalido_retorna_422(client_evento, payload):
    client, _ = client_evento
    response = client.post("/evento/", json=payload)
    assert response.status_code == 422


class TestDeletarEvento:
    def test_retorna_204_quando_existe(self, client_evento):
        client, servico = client_evento
        servico.deletar_evento.return_value = None
        response = client.delete("/evento/1")
        assert response.status_code == 204

    def test_retorna_404_quando_nao_existe(self, client_evento):
        client, servico = client_evento
        servico.deletar_evento.side_effect = ValueError("Evento não encontrado")
        response = client.delete("/evento/999")
        assert response.status_code == 404