import pytest
from unittest.mock import MagicMock
from src.banda_palestrante.repository import RepositorioBandaPalestrante
from src.banda_palestrante.model import BandaPalestrante


@pytest.fixture
def mock_db_session():
    return MagicMock()


@pytest.fixture
def repositorio(mock_db_session):
    return RepositorioBandaPalestrante(db=mock_db_session)


def test_salvar(repositorio, mock_db_session):
    participante = BandaPalestrante(nome="Banda Teste")
    resultado = repositorio.salvar(participante)
    mock_db_session.add.assert_called_once_with(participante)
    mock_db_session.commit.assert_called_once()
    assert resultado == participante


def test_buscar_todos(repositorio, mock_db_session):
    repositorio.buscar_todos()
    mock_db_session.query.assert_called_with(BandaPalestrante)
    mock_db_session.query().all.assert_called_once()


def test_buscar_por_id(repositorio, mock_db_session):
    repositorio.buscar_por_id(1)
    mock_db_session.query.assert_called_with(BandaPalestrante)
    mock_db_session.query().filter().first.assert_called_once()


def test_deletar(repositorio, mock_db_session):
    participante = BandaPalestrante(participante_id=1)
    repositorio.deletar(participante)
    mock_db_session.delete.assert_called_once_with(participante)
    mock_db_session.commit.assert_called_once()
