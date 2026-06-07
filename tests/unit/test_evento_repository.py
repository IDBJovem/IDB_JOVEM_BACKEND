import pytest
from unittest.mock import MagicMock
from src.evento.repository import RepositorioEvento
from src.evento.model import Evento

@pytest.fixture
def mock_db_session():
    return MagicMock()

@pytest.fixture
def repositorio(mock_db_session):
    return RepositorioEvento(db=mock_db_session)

def test_salvar_novo_evento(repositorio, mock_db_session):
    evento = Evento(nome="Teste")
    evento.evento_id = None
    repositorio.salvar(evento)
    mock_db_session.add.assert_called_once_with(evento)
    mock_db_session.commit.assert_called_once()

def test_salvar_evento_existente(repositorio, mock_db_session):
    evento = Evento(evento_id=1, nome="Teste")
    repositorio.salvar(evento)
    mock_db_session.merge.assert_called_once_with(evento)
    mock_db_session.commit.assert_called_once()

def test_buscar_todos(repositorio, mock_db_session):
    repositorio.buscar_todos()
    mock_db_session.query.assert_called_with(Evento)

def test_buscar_por_id(repositorio, mock_db_session):
    repositorio.buscar_por_id(1)
    mock_db_session.query.assert_called_with(Evento)

def test_deletar(repositorio, mock_db_session):
    evento = Evento(evento_id=1)
    repositorio.deletar(evento)
    mock_db_session.delete.assert_called_once_with(evento)

def test_deletar_nulo(repositorio, mock_db_session):
    repositorio.deletar(None)
    mock_db_session.delete.assert_not_called()

def test_pesquisar_por_nome(repositorio, mock_db_session):
    repositorio.pesquisar_por_nome("teste")
    mock_db_session.query.assert_called_with(Evento)
    mock_db_session.query().from_statement().params().all.assert_called_once()
