import pytest
from unittest.mock import MagicMock
from src.produto.repository import RepositorioProduto
from src.produto.model import Produto


@pytest.fixture
def mock_db_session():
    return MagicMock()


@pytest.fixture
def repositorio(mock_db_session):
    return RepositorioProduto(db=mock_db_session)


def test_salvar(repositorio, mock_db_session):
    produto = Produto(nome="Produto Teste")
    resultado = repositorio.salvar(produto)
    mock_db_session.add.assert_called_once_with(produto)
    mock_db_session.commit.assert_called_once()
    assert resultado == produto


def test_buscar_todos(repositorio, mock_db_session):
    repositorio.buscar_todos()
    mock_db_session.query.assert_called_with(Produto)
    mock_db_session.query().all.assert_called_once()


def test_buscar_por_id(repositorio, mock_db_session):
    repositorio.buscar_por_id(1)
    mock_db_session.query.assert_called_with(Produto)
    mock_db_session.query().filter().first.assert_called_once()


def test_deletar(repositorio, mock_db_session):
    produto = Produto(produto_id=1)
    repositorio.deletar(produto)
    mock_db_session.delete.assert_called_once_with(produto)
    mock_db_session.commit.assert_called_once()
