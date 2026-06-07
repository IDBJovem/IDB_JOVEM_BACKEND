import pytest
from unittest.mock import MagicMock
from src.voluntario.service import ServicoVoluntario
from src.voluntario.models import Voluntario, Trabalha
from src.voluntario.schema import SolicitacaoVoluntario

@pytest.fixture
def mock_repositorio():
    return MagicMock()

@pytest.fixture
def servico(mock_repositorio):
    return ServicoVoluntario(repositorio=mock_repositorio)

def test_criar_voluntario_sucesso(servico, mock_repositorio):
    mock_repositorio.buscar_por_email.return_value = None
    dados = SolicitacaoVoluntario(nome="Teste", email="t@t.com", telefone="123", keycloak_id="uuid")
    voluntario = Voluntario(**dados.model_dump())
    voluntario.voluntario_id = 1
    mock_repositorio.salvar.return_value = voluntario
    
    resultado = servico.criar_voluntario(dados)
    mock_repositorio.salvar.assert_called_once()
    assert resultado.voluntario_id == 1

def test_criar_voluntario_email_duplicado(servico, mock_repositorio):
    mock_repositorio.buscar_por_email.return_value = Voluntario()
    dados = SolicitacaoVoluntario(nome="Teste", email="t@t.com", telefone="123", keycloak_id="uuid")
    
    with pytest.raises(ValueError, match="Já existe um voluntário com esse e-mail."):
        servico.criar_voluntario(dados)

def test_buscar_voluntario_nao_encontrado(servico, mock_repositorio):
    mock_repositorio.buscar_por_id.return_value = None
    with pytest.raises(ValueError, match="Voluntário não encontrado."):
        servico.buscar_voluntario(1)

def test_deletar_voluntario(servico, mock_repositorio):
    voluntario = Voluntario(voluntario_id=1)
    mock_repositorio.buscar_por_id.return_value = voluntario
    servico.deletar_voluntario(1)
    mock_repositorio.deletar.assert_called_once_with(voluntario)

def test_listar_voluntarios(servico, mock_repositorio):
    servico.listar_voluntarios()
    mock_repositorio.buscar_todos.assert_called_once()

def test_listar_voluntarios_evento(servico, mock_repositorio):
    servico.listar_voluntarios_evento(1)
    mock_repositorio.listar_por_evento.assert_called_once_with(1)

def test_atualizar_status_invalido(servico):
    with pytest.raises(ValueError, match="Status inválido."):
        servico.atualizar_status(1, 1, "invalido")

def test_atualizar_status_voluntario_nao_encontrado(servico, mock_repositorio):
    mock_repositorio.buscar_por_id.return_value = None
    with pytest.raises(ValueError, match="Voluntário não encontrado."):
        servico.atualizar_status(1, 1, "aprovado")

def test_atualizar_status_novo_trabalho(servico, mock_repositorio):
    mock_repositorio.buscar_por_id.return_value = Voluntario()
    mock_repositorio.buscar_trabalho.return_value = None
    
    servico.atualizar_status(1, 2, "aprovado")
    mock_repositorio.salvar_trabalho.assert_called_once()
    args = mock_repositorio.salvar_trabalho.call_args[0][0]
    assert args.status == "aprovado"

def test_atualizar_status_trabalho_existente(servico, mock_repositorio):
    mock_repositorio.buscar_por_id.return_value = Voluntario()
    trabalho = Trabalha(voluntario_id=1, evento_id=2, status="pendente")
    mock_repositorio.buscar_trabalho.return_value = trabalho
    
    servico.atualizar_status(1, 2, "aprovado")
    mock_repositorio.salvar_trabalho.assert_called_once()
    assert trabalho.status == "aprovado"

def test_contar_voluntarios_evento(servico, mock_repositorio):
    mock_repositorio.listar_por_evento.return_value = [
        Trabalha(status="pendente"), Trabalha(status="aprovado"), Trabalha(status="reprovado"), Trabalha(status="aprovado")
    ]
    resultado = servico.contar_voluntarios_evento(1)
    assert resultado["total"] == 4
    assert resultado["pendentes"] == 1
    assert resultado["aprovados"] == 2
    assert resultado["reprovados"] == 1
