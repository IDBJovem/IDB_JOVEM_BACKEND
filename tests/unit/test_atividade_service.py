import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from src.atividade.service import ServicoAtividade
from src.atividade.model import Atividade
from src.atividade.schema import SolicitacaoAtividade


@pytest.fixture
def mock_repositorio_atividade():
    return MagicMock()


@pytest.fixture
def mock_repositorio_evento():
    return MagicMock()


@pytest.fixture
def servico(mock_repositorio_atividade, mock_repositorio_evento):
    return ServicoAtividade(
        repositorio_atividade=mock_repositorio_atividade,
        repositorio_evento=mock_repositorio_evento,
    )


def _dados_atividade():
    return SolicitacaoAtividade(
        nome="Palestra",
        descricao="Descrição",
        horario_inicio=datetime.now() + timedelta(hours=1),
        horario_termino=datetime.now() + timedelta(hours=2),
    )


def test_criar_atividade_sucesso(servico, mock_repositorio_atividade, mock_repositorio_evento):
    mock_repositorio_evento.buscar_por_id.return_value = MagicMock()
    atividade_mock = Atividade(atividade_id=1, nome="Palestra", evento_id=1)
    mock_repositorio_atividade.salvar.return_value = atividade_mock

    resultado = servico.criar_atividade(1, _dados_atividade())

    mock_repositorio_evento.buscar_por_id.assert_called_once_with(1)
    mock_repositorio_atividade.salvar.assert_called_once()
    assert resultado.atividade_id == 1


def test_criar_atividade_evento_nao_encontrado(servico, mock_repositorio_evento):
    mock_repositorio_evento.buscar_por_id.return_value = None

    with pytest.raises(ValueError, match="Evento não encontrado."):
        servico.criar_atividade(1, _dados_atividade())


def test_criar_atividade_horario_invalido(servico, mock_repositorio_evento):
    mock_repositorio_evento.buscar_por_id.return_value = MagicMock()
    dados = SolicitacaoAtividade(
        nome="Palestra",
        horario_inicio=datetime.now() + timedelta(hours=2),
        horario_termino=datetime.now() + timedelta(hours=1),
    )

    with pytest.raises(ValueError):
        servico.criar_atividade(1, dados)


def test_listar_atividades(servico, mock_repositorio_atividade):
    servico.listar_atividades(1)
    mock_repositorio_atividade.buscar_por_evento.assert_called_once_with(1)


def test_buscar_atividade_sucesso(servico, mock_repositorio_atividade):
    mock_repositorio_atividade.buscar_por_id.return_value = Atividade(atividade_id=1)
    resultado = servico.buscar_atividade(1)
    assert resultado.atividade_id == 1


def test_buscar_atividade_nao_encontrada(servico, mock_repositorio_atividade):
    mock_repositorio_atividade.buscar_por_id.return_value = None
    with pytest.raises(ValueError, match="Atividade não encontrada."):
        servico.buscar_atividade(1)


def test_atualizar_atividade_sucesso(servico, mock_repositorio_atividade):
    atividade = Atividade(
        atividade_id=1,
        nome="Antiga",
        horario_inicio=datetime.now() + timedelta(hours=1),
        horario_termino=datetime.now() + timedelta(hours=2),
    )
    mock_repositorio_atividade.buscar_por_id.return_value = atividade
    mock_repositorio_atividade.salvar.return_value = atividade

    resultado = servico.atualizar_atividade(1, _dados_atividade())
    mock_repositorio_atividade.salvar.assert_called_once()


def test_atualizar_atividade_nao_encontrada(servico, mock_repositorio_atividade):
    mock_repositorio_atividade.buscar_por_id.return_value = None
    with pytest.raises(ValueError, match="Atividade não encontrada."):
        servico.atualizar_atividade(1, _dados_atividade())


def test_deletar_atividade_sucesso(servico, mock_repositorio_atividade):
    atividade = Atividade(atividade_id=1)
    mock_repositorio_atividade.buscar_por_id.return_value = atividade
    servico.deletar_atividade(1)
    mock_repositorio_atividade.deletar.assert_called_once_with(atividade)


def test_deletar_atividade_nao_encontrada(servico, mock_repositorio_atividade):
    mock_repositorio_atividade.buscar_por_id.return_value = None
    with pytest.raises(ValueError, match="Atividade não encontrada."):
        servico.deletar_atividade(1)
