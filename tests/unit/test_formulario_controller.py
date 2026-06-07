import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from src.formulario.controller import listar_inscricoes, get_servico


class TestFormularioController:
    def test_get_servico(self):
        servico = get_servico()
        from src.formulario.service import ServicoFormulario
        assert isinstance(servico, ServicoFormulario)

    def test_listar_inscricoes_sucesso(self):
        mock_servico = MagicMock()
        mock_servico.listar_inscricoes.return_value = []
        mock_db = MagicMock()

        resultado = listar_inscricoes(evento_id=1, db=mock_db, servico=mock_servico)
        mock_servico.listar_inscricoes.assert_called_once_with(mock_db, 1)
        assert resultado == []

    def test_listar_inscricoes_value_error(self):
        mock_servico = MagicMock()
        mock_servico.listar_inscricoes.side_effect = ValueError("Evento não encontrado")
        mock_db = MagicMock()

        with pytest.raises(HTTPException) as exc:
            listar_inscricoes(evento_id=1, db=mock_db, servico=mock_servico)
        assert exc.value.status_code == 404

    def test_listar_inscricoes_runtime_error(self):
        mock_servico = MagicMock()
        mock_servico.listar_inscricoes.side_effect = RuntimeError("Erro API")
        mock_db = MagicMock()

        with pytest.raises(HTTPException) as exc:
            listar_inscricoes(evento_id=1, db=mock_db, servico=mock_servico)
        assert exc.value.status_code == 502
