import pytest
from unittest.mock import MagicMock
from src.produto.service import ServicoProduto
from src.produto.model import Produto
from src.produto.schema import SolicitacaoProduto


@pytest.fixture
def mock_repositorio():
    return MagicMock()


@pytest.fixture
def servico(mock_repositorio):
    return ServicoProduto(repositorio=mock_repositorio)


def test_criar_produto(servico, mock_repositorio):
    dados = SolicitacaoProduto(nome="Produto X", descricao="Desc", link_produto="http://link.com")
    produto = Produto(produto_id=1, **dados.model_dump())
    mock_repositorio.salvar.return_value = produto

    resultado = servico.criar_produto(dados)
    mock_repositorio.salvar.assert_called_once()
    assert resultado.produto_id == 1


def test_listar_produtos(servico, mock_repositorio):
    servico.listar_produtos()
    mock_repositorio.buscar_todos.assert_called_once()


def test_buscar_produto_sucesso(servico, mock_repositorio):
    mock_repositorio.buscar_por_id.return_value = Produto(produto_id=1)
    resultado = servico.buscar_produto(1)
    assert resultado.produto_id == 1


def test_buscar_produto_nao_encontrado(servico, mock_repositorio):
    mock_repositorio.buscar_por_id.return_value = None
    with pytest.raises(ValueError, match="Produto não encontrado."):
        servico.buscar_produto(1)


def test_atualizar_produto_sucesso(servico, mock_repositorio):
    produto = Produto(produto_id=1, nome="Antigo")
    mock_repositorio.buscar_por_id.return_value = produto
    mock_repositorio.salvar.return_value = produto

    dados = SolicitacaoProduto(nome="Novo", descricao="Nova desc")
    resultado = servico.atualizar_produto(1, dados)
    mock_repositorio.salvar.assert_called_once()


def test_atualizar_produto_nao_encontrado(servico, mock_repositorio):
    mock_repositorio.buscar_por_id.return_value = None
    dados = SolicitacaoProduto(nome="Novo")

    with pytest.raises(ValueError, match="Produto não encontrado."):
        servico.atualizar_produto(1, dados)


def test_deletar_produto_sucesso(servico, mock_repositorio):
    produto = Produto(produto_id=1)
    mock_repositorio.buscar_por_id.return_value = produto
    servico.deletar_produto(1)
    mock_repositorio.deletar.assert_called_once_with(produto)


def test_deletar_produto_nao_encontrado(servico, mock_repositorio):
    mock_repositorio.buscar_por_id.return_value = None
    with pytest.raises(ValueError, match="Produto não encontrado."):
        servico.deletar_produto(1)
