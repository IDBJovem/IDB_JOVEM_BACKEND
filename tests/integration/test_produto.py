"""
Testes de integração para o módulo de produtos.
Usa dependency_overrides do FastAPI para simular banco e autenticação.
"""
import pytest
from unittest.mock import MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.produto.controller import router as produto_router, get_servico
from src.security import obter_usuario_atual
from src.produto.schema import RespostaProduto


PRODUTO_BASE = {
    "nome": "Camiseta IDB Teen",
    "descricao": "Camiseta oficial do evento",
    "link_produto": "https://loja.idb.com/camiseta",
}

PRODUTO_RESPOSTA = {**PRODUTO_BASE, "produto_id": 1}
USUARIO_ADMIN = {"sub": "user-123", "realm_access": {"roles": ["admin", "superadmin"]}}


@pytest.fixture
def servico_mock():
    return MagicMock()


@pytest.fixture
def client_produto(servico_mock):
    app = FastAPI()
    app.include_router(produto_router)
    app.dependency_overrides[get_servico] = lambda: servico_mock
    app.dependency_overrides[obter_usuario_atual] = lambda: USUARIO_ADMIN
    with TestClient(app) as c:
        yield c, servico_mock
    app.dependency_overrides.clear()


class TestListarProdutos:
    def test_retorna_200_com_lista_vazia(self, client_produto):
        client, servico = client_produto
        servico.listar_produtos.return_value = []
        response = client.get("/produto/")
        assert response.status_code == 200
        assert response.json() == []

    def test_retorna_200_com_produtos(self, client_produto):
        client, servico = client_produto
        servico.listar_produtos.return_value = [RespostaProduto(**PRODUTO_RESPOSTA)]
        response = client.get("/produto/")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["nome"] == "Camiseta IDB Teen"


class TestBuscarProdutoPorId:
    def test_retorna_200_quando_existe(self, client_produto):
        client, servico = client_produto
        servico.buscar_produto.return_value = RespostaProduto(**PRODUTO_RESPOSTA)
        response = client.get("/produto/1")
        assert response.status_code == 200
        assert response.json()["produto_id"] == 1

    def test_retorna_404_quando_nao_existe(self, client_produto):
        client, servico = client_produto
        servico.buscar_produto.side_effect = ValueError("Produto não encontrado")
        response = client.get("/produto/999")
        assert response.status_code == 404


PAYLOADS_PRODUTO_VALIDOS = [
    pytest.param({"nome": "Camiseta IDB Teen"}, id="payload_minimo"),
    pytest.param(
        {"nome": "E-book Liderança", "descricao": "E-book sobre liderança jovem",
         "link_produto": "https://hotmart.com/ebook"},
        id="payload_completo",
    ),
    pytest.param(
        {"nome": "Livro de Orações", "descricao": None, "link_produto": None},
        id="payload_com_opcionais_nulos",
    ),
]


@pytest.mark.parametrize("payload", PAYLOADS_PRODUTO_VALIDOS)
def test_criar_produto_payload_valido(client_produto, payload):
    client, servico = client_produto
    servico.criar_produto.return_value = RespostaProduto(
        **{**payload, "produto_id": 1,
           "descricao": payload.get("descricao"),
           "link_produto": payload.get("link_produto")}
    )
    response = client.post("/produto/", json=payload)
    assert response.status_code == 201
    assert response.json()["nome"] == payload["nome"]


PAYLOADS_PRODUTO_INVALIDOS = [
    pytest.param({}, id="payload_vazio"),
    pytest.param({"descricao": "Sem nome"}, id="sem_nome"),
]


@pytest.mark.parametrize("payload", PAYLOADS_PRODUTO_INVALIDOS)
def test_criar_produto_payload_invalido_retorna_422(client_produto, payload):
    client, _ = client_produto
    response = client.post("/produto/", json=payload)
    assert response.status_code == 422


class TestDeletarProduto:
    def test_retorna_204_quando_existe(self, client_produto):
        client, servico = client_produto
        servico.deletar_produto.return_value = None
        response = client.delete("/produto/1")
        assert response.status_code == 204

    def test_retorna_404_quando_nao_existe(self, client_produto):
        client, servico = client_produto
        servico.deletar_produto.side_effect = ValueError("Produto não encontrado")
        response = client.delete("/produto/999")
        assert response.status_code == 404