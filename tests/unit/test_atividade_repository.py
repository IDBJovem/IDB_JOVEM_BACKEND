import pytest
from unittest.mock import MagicMock
from src.atividade.repository import RepositorioAtividade
from src.atividade.model import Atividade


@pytest.fixture
def mock_db_session():
    return MagicMock()


@pytest.fixture
def repositorio(mock_db_session):
    return RepositorioAtividade(db=mock_db_session)


def test_salvar_nova_atividade(repositorio, mock_db_session):
    atividade = Atividade(nome="Teste")
    atividade.atividade_id = None
    repositorio.salvar(atividade)
    mock_db_session.add.assert_called_once_with(atividade)
    mock_db_session.commit.assert_called_once()


def test_salvar_atividade_existente(repositorio, mock_db_session):
    atividade = Atividade(atividade_id=1, nome="Teste")
    repositorio.salvar(atividade)
    mock_db_session.merge.assert_called_once_with(atividade)
    mock_db_session.commit.assert_called_once()


def test_buscar_por_evento(repositorio, mock_db_session):
    repositorio.buscar_por_evento(1)
    mock_db_session.query.assert_called_with(Atividade)
    mock_db_session.query().filter().all.assert_called_once()


def test_buscar_por_id(repositorio, mock_db_session):
    repositorio.buscar_por_id(1)
    mock_db_session.query.assert_called_with(Atividade)
    mock_db_session.query().filter().first.assert_called_once()


def test_deletar_atividade(repositorio, mock_db_session):
    atividade = Atividade(atividade_id=1)
    repositorio.deletar(atividade)
    mock_db_session.delete.assert_called_once_with(atividade)
    mock_db_session.commit.assert_called_once()


def test_deletar_atividade_nula(repositorio, mock_db_session):
    repositorio.deletar(None)
    mock_db_session.delete.assert_not_called()
