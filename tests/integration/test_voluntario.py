"""
Testes de integração para o módulo de voluntários.
Usa dependency_overrides do FastAPI para simular banco e autenticação.
"""
import pytest
from unittest.mock import MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.voluntario.controller import router as voluntario_router, get_servico
from src.security import obter_usuario_atual
from src.voluntario.schema import RespostaVoluntario


VOLUNTARIO_BASE = {
    "nome": "João Silva",
    "email": "joao@email.com",
    "resposta_id_formulario": None,
}

VOLUNTARIO_RESPOSTA = {**VOLUNTARIO_BASE, "voluntario_id": 1}
USUARIO_ADMIN = {"sub": "user-123", "realm_access": {"roles": ["admin", "superadmin"]}}


@pytest.fixture
def servico_mock():
    return MagicMock()


@pytest.fixture
def client_voluntario(servico_mock):
    app = FastAPI()
    app.include_router(voluntario_router)
    app.dependency_overrides[get_servico] = lambda: servico_mock
    app.dependency_overrides[obter_usuario_atual] = lambda: USUARIO_ADMIN
    with TestClient(app) as c:
        yield c, servico_mock
    app.dependency_overrides.clear()


class TestListarVoluntarios:
    def test_retorna_200_com_lista_vazia(self, client_voluntario):
        client, servico = client_voluntario
        servico.listar_voluntarios.return_value = []
        response = client.get("/voluntarios/")
        assert response.status_code == 200
        assert response.json() == []

    def test_retorna_200_com_voluntarios(self, client_voluntario):
        client, servico = client_voluntario
        servico.listar_voluntarios.return_value = [RespostaVoluntario(**VOLUNTARIO_RESPOSTA)]
        response = client.get("/voluntarios/")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["nome"] == "João Silva"


class TestBuscarVoluntarioPorId:
    def test_retorna_200_quando_existe(self, client_voluntario):
        client, servico = client_voluntario
        servico.buscar_voluntario.return_value = RespostaVoluntario(**VOLUNTARIO_RESPOSTA)
        response = client.get("/voluntarios/1")
        assert response.status_code == 200
        assert response.json()["voluntario_id"] == 1

    def test_retorna_404_quando_nao_existe(self, client_voluntario):
        client, servico = client_voluntario
        servico.buscar_voluntario.side_effect = ValueError("Voluntário não encontrado")
        response = client.get("/voluntarios/999")
        assert response.status_code == 404


PAYLOADS_VOLUNTARIO_VALIDOS = [
    pytest.param({"nome": "João Silva", "email": "joao@email.com"}, id="payload_minimo"),
    pytest.param(
        {"nome": "Maria Santos", "email": "maria@email.com",
         "resposta_id_formulario": "abc123"},
        id="payload_completo",
    ),
    pytest.param(
        {"nome": "Pedro Costa", "email": "pedro@email.com",
         "resposta_id_formulario": None},
        id="payload_com_formulario_nulo",
    ),
]


@pytest.mark.parametrize("payload", PAYLOADS_VOLUNTARIO_VALIDOS)
def test_criar_voluntario_payload_valido(client_voluntario, payload):
    client, servico = client_voluntario
    servico.criar_voluntario.return_value = RespostaVoluntario(
        **{**payload, "voluntario_id": 1}
    )
    response = client.post("/voluntarios/", json=payload)
    assert response.status_code == 201
    assert response.json()["nome"] == payload["nome"]


PAYLOADS_VOLUNTARIO_INVALIDOS = [
    pytest.param({}, id="payload_vazio"),
    pytest.param({"nome": "João Silva"}, id="sem_email"),
    pytest.param({"email": "joao@email.com"}, id="sem_nome"),
]


@pytest.mark.parametrize("payload", PAYLOADS_VOLUNTARIO_INVALIDOS)
def test_criar_voluntario_payload_invalido_retorna_422(client_voluntario, payload):
    client, _ = client_voluntario
    response = client.post("/voluntarios/", json=payload)
    assert response.status_code == 422


class TestDeletarVoluntario:
    def test_retorna_204_quando_existe(self, client_voluntario):
        client, servico = client_voluntario
        servico.deletar_voluntario.return_value = None
        response = client.delete("/voluntarios/1")
        assert response.status_code == 204

    def test_retorna_404_quando_nao_existe(self, client_voluntario):
        client, servico = client_voluntario
        servico.deletar_voluntario.side_effect = ValueError("Voluntário não encontrado")
        response = client.delete("/voluntarios/999")
        assert response.status_code == 404