import pytest
from unittest.mock import MagicMock
from src.voluntario.repository import RepositorioVoluntario
from src.voluntario.models import Voluntario, Trabalha

@pytest.fixture
def mock_db_session():
    return MagicMock()

@pytest.fixture
def repositorio(mock_db_session):
    return RepositorioVoluntario(db=mock_db_session)

def test_salvar_voluntario(repositorio, mock_db_session):
    voluntario = Voluntario(nome="Teste")
    repositorio.salvar(voluntario)
    mock_db_session.add.assert_called_once_with(voluntario)
    mock_db_session.commit.assert_called_once()

def test_buscar_todos(repositorio, mock_db_session):
    repositorio.buscar_todos()
    mock_db_session.query.assert_called_with(Voluntario)

def test_buscar_por_id(repositorio, mock_db_session):
    repositorio.buscar_por_id(1)
    mock_db_session.query.assert_called_with(Voluntario)

def test_buscar_por_email(repositorio, mock_db_session):
    repositorio.buscar_por_email("t@t.com")
    mock_db_session.query.assert_called_with(Voluntario)

def test_deletar(repositorio, mock_db_session):
    voluntario = Voluntario(voluntario_id=1)
    repositorio.deletar(voluntario)
    mock_db_session.delete.assert_called_once_with(voluntario)

def test_buscar_trabalho(repositorio, mock_db_session):
    repositorio.buscar_trabalho(1, 2)
    mock_db_session.query.assert_called_with(Trabalha)

def test_listar_por_evento(repositorio, mock_db_session):
    repositorio.listar_por_evento(1)
    mock_db_session.query.assert_called_with(Trabalha)

def test_salvar_trabalho(repositorio, mock_db_session):
    trabalho = Trabalha(voluntario_id=1, evento_id=2)
    repositorio.salvar_trabalho(trabalho)
    mock_db_session.add.assert_called_once_with(trabalho)
    mock_db_session.refresh.assert_called_once_with(trabalho)
