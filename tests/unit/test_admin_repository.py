import pytest
from unittest.mock import MagicMock
from src.admin.repository import RepositorioAdmin
from src.admin.model import Admin

@pytest.fixture
def mock_db_session():
    return MagicMock()

@pytest.fixture
def repositorio(mock_db_session):
    return RepositorioAdmin(db=mock_db_session)

def test_salvar_novo_admin(repositorio, mock_db_session):
    admin = Admin(email="teste@teste.com", keycloak_id="uuid", nome="Teste")
    admin.admin_id = None 
    resultado = repositorio.salvar(admin)
    mock_db_session.add.assert_called_once_with(admin)
    mock_db_session.commit.assert_called_once()
    assert resultado == admin

def test_salvar_admin_existente(repositorio, mock_db_session):
    admin = Admin(admin_id=1, email="teste@teste.com", keycloak_id="uuid", nome="Teste")
    mock_db_session.merge.return_value = admin
    resultado = repositorio.salvar(admin)
    mock_db_session.merge.assert_called_once_with(admin)
    mock_db_session.commit.assert_called_once()
    assert resultado == admin

def test_buscar_todos(repositorio, mock_db_session):
    repositorio.buscar_todos()
    mock_db_session.query.assert_called_with(Admin)
    mock_db_session.query().all.assert_called_once()

def test_buscar_por_id(repositorio, mock_db_session):
    repositorio.buscar_por_id(1)
    mock_db_session.query.assert_called_with(Admin)
    mock_db_session.query().filter().first.assert_called_once()

def test_buscar_por_email(repositorio, mock_db_session):
    repositorio.buscar_por_email("teste@teste.com")
    mock_db_session.query.assert_called_with(Admin)
    mock_db_session.query().filter().first.assert_called_once()

def test_buscar_por_keycloak_id(repositorio, mock_db_session):
    repositorio.buscar_por_keycloak_id("uuid")
    mock_db_session.query.assert_called_with(Admin)
    mock_db_session.query().filter().first.assert_called_once()

def test_deletar(repositorio, mock_db_session):
    admin = Admin(admin_id=1)
    repositorio.deletar(admin)
    mock_db_session.delete.assert_called_once_with(admin)
    mock_db_session.commit.assert_called_once()
