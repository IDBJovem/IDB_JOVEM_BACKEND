import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from src.voluntario.controller import (
    criar_voluntario, listar_voluntarios, buscar_voluntario,
    deletar_voluntario, listar_voluntarios_evento,
    atualizar_status_voluntario, contar_voluntarios_evento,
    get_servico,
)


class TestVoluntarioController:
    def test_get_servico(self):
        mock_db = MagicMock()
        servico = get_servico(db=mock_db)
        from src.voluntario.service import ServicoVoluntario
        assert isinstance(servico, ServicoVoluntario)

    def test_criar_voluntario_sucesso(self):
        mock_servico = MagicMock()
        mock_servico.criar_voluntario.return_value = MagicMock()
        resultado = criar_voluntario(solicitacao=MagicMock(), servico=mock_servico, _={})
        mock_servico.criar_voluntario.assert_called_once()

    def test_criar_voluntario_erro(self):
        mock_servico = MagicMock()
        mock_servico.criar_voluntario.side_effect = ValueError("E-mail duplicado")
        with pytest.raises(HTTPException) as exc:
            criar_voluntario(solicitacao=MagicMock(), servico=mock_servico, _={})
        assert exc.value.status_code == 400

    def test_listar_voluntarios(self):
        mock_servico = MagicMock()
        mock_servico.listar_voluntarios.return_value = []
        resultado = listar_voluntarios(servico=mock_servico, _={})
        mock_servico.listar_voluntarios.assert_called_once()

    def test_buscar_voluntario_sucesso(self):
        mock_servico = MagicMock()
        mock_servico.buscar_voluntario.return_value = MagicMock()
        resultado = buscar_voluntario(voluntario_id=1, servico=mock_servico, _={})
        mock_servico.buscar_voluntario.assert_called_once_with(1)

    def test_buscar_voluntario_nao_encontrado(self):
        mock_servico = MagicMock()
        mock_servico.buscar_voluntario.side_effect = ValueError("Não encontrado")
        with pytest.raises(HTTPException) as exc:
            buscar_voluntario(voluntario_id=1, servico=mock_servico, _={})
        assert exc.value.status_code == 404

    def test_deletar_voluntario_sucesso(self):
        mock_servico = MagicMock()
        deletar_voluntario(voluntario_id=1, servico=mock_servico, _={})
        mock_servico.deletar_voluntario.assert_called_once_with(1)

    def test_deletar_voluntario_erro(self):
        mock_servico = MagicMock()
        mock_servico.deletar_voluntario.side_effect = ValueError("Não encontrado")
        with pytest.raises(HTTPException) as exc:
            deletar_voluntario(voluntario_id=1, servico=mock_servico, _={})
        assert exc.value.status_code == 404

    def test_listar_voluntarios_evento(self):
        mock_servico = MagicMock()
        mock_servico.listar_voluntarios_evento.return_value = []
        resultado = listar_voluntarios_evento(evento_id=1, servico=mock_servico, _={})
        mock_servico.listar_voluntarios_evento.assert_called_once_with(1)

    def test_atualizar_status_sucesso(self):
        mock_servico = MagicMock()
        mock_servico.atualizar_status.return_value = MagicMock()
        resultado = atualizar_status_voluntario(
            voluntario_id=1, evento_id=2, novo_status="aprovado",
            servico=mock_servico, _={}
        )
        mock_servico.atualizar_status.assert_called_once_with(1, 2, "aprovado")

    def test_atualizar_status_erro(self):
        mock_servico = MagicMock()
        mock_servico.atualizar_status.side_effect = ValueError("Status inválido")
        with pytest.raises(HTTPException) as exc:
            atualizar_status_voluntario(
                voluntario_id=1, evento_id=2, novo_status="invalido",
                servico=mock_servico, _={}
            )
        assert exc.value.status_code == 400

    def test_contar_voluntarios_evento(self):
        mock_servico = MagicMock()
        mock_servico.contar_voluntarios_evento.return_value = {"total": 0}
        resultado = contar_voluntarios_evento(evento_id=1, servico=mock_servico, _={})
        mock_servico.contar_voluntarios_evento.assert_called_once_with(1)
