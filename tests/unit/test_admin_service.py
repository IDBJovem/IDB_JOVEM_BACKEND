import pytest
from unittest.mock import MagicMock
from src.admin.service import ServicoAdmin
from src.admin.model import Admin
from src.admin.schema import SolicitacaoAdmin

@pytest.fixture
def mock_repositorio():
    return MagicMock()

@pytest.fixture
def servico(mock_repositorio):
    return ServicoAdmin(repositorio=mock_repositorio)

def test_criar_admin_sucesso(servico, mock_repositorio):
    mock_repositorio.buscar_por_email.return_value = None
    mock_repositorio.buscar_por_keycloak_id.return_value = None
    
    dados = SolicitacaoAdmin(nome="Teste", email="t@t.com", keycloak_id="uuid")
    
    admin_retorno = Admin(admin_id=1, nome="Teste", email="t@t.com", keycloak_id="uuid")
    mock_repositorio.salvar.return_value = admin_retorno
    
    resultado = servico.criar_admin(dados)
    
    mock_repositorio.salvar.assert_called_once()
    assert resultado.admin_id == 1

def test_criar_admin_email_duplicado(servico, mock_repositorio):
    mock_repositorio.buscar_por_email.return_value = Admin()
    dados = SolicitacaoAdmin(nome="Teste", email="t@t.com", keycloak_id="uuid")
    
    with pytest.raises(ValueError, match="Já existe um administrador com esse e-mail."):
        servico.criar_admin(dados)

def test_criar_admin_keycloak_id_duplicado(servico, mock_repositorio):
    mock_repositorio.buscar_por_email.return_value = None
    mock_repositorio.buscar_por_keycloak_id.return_value = Admin()
    dados = SolicitacaoAdmin(nome="Teste", email="t@t.com", keycloak_id="uuid")
    
    with pytest.raises(ValueError, match="Já existe um administrador com esse Keycloak ID."):
        servico.criar_admin(dados)

def test_listar_admins(servico, mock_repositorio):
    servico.listar_admins()
    mock_repositorio.buscar_todos.assert_called_once()

def test_buscar_admin_sucesso(servico, mock_repositorio):
    mock_repositorio.buscar_por_id.return_value = Admin(admin_id=1)
    admin = servico.buscar_admin(1)
    assert admin.admin_id == 1

def test_buscar_admin_nao_encontrado(servico, mock_repositorio):
    mock_repositorio.buscar_por_id.return_value = None
    with pytest.raises(ValueError, match="Administrador não encontrado."):
        servico.buscar_admin(1)

def test_deletar_admin_sucesso(servico, mock_repositorio):
    admin = Admin(admin_id=1, keycloak_id="uuid-1")
    mock_repositorio.buscar_por_id.return_value = admin
    
    usuario_logado = {"sub": "uuid-outro"}
    servico.deletar_admin(1, usuario_logado)
    
    mock_repositorio.deletar.assert_called_once_with(admin)

def test_deletar_admin_proprio_usuario(servico, mock_repositorio):
    admin = Admin(admin_id=1, keycloak_id="uuid-1")
    mock_repositorio.buscar_por_id.return_value = admin
    
    usuario_logado = {"sub": "uuid-1"}
    with pytest.raises(ValueError, match="Não é permitido excluir o próprio usuário administrador."):
        servico.deletar_admin(1, usuario_logado)
