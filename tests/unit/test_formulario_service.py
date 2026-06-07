import pytest
from unittest.mock import MagicMock
from src.formulario.service import ServicoFormulario


class TestServicoFormulario:
    @pytest.fixture
    def mock_repositorio(self):
        return MagicMock()

    @pytest.fixture
    def servico(self, mock_repositorio):
        return ServicoFormulario(repositorio=mock_repositorio)

    def test_listar_inscricoes(self, servico, mock_repositorio):
        mock_db = MagicMock()
        mock_repositorio.listar_inscricoes.return_value = []

        resultado = servico.listar_inscricoes(mock_db, 1)

        mock_repositorio.listar_inscricoes.assert_called_once_with(mock_db, 1)
        assert resultado == []
