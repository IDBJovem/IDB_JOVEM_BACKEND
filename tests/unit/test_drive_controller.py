import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from src.drive.controller import listar_fotos


class TestDriveController:
    @patch("src.drive.controller.ServicoDrive")
    def test_listar_fotos_sucesso(self, mock_drive_class):
        mock_drive = MagicMock()
        mock_drive.listar_fotos.return_value = []
        mock_drive_class.return_value = mock_drive

        resultado = listar_fotos(pasta="MinhasPastas", usuario_logado={})
        mock_drive.listar_fotos.assert_called_once_with("MinhasPastas")

    @patch("src.drive.controller.ServicoDrive")
    def test_listar_fotos_pasta_nao_encontrada(self, mock_drive_class):
        mock_drive = MagicMock()
        mock_drive.listar_fotos.side_effect = ValueError("Pasta não encontrada")
        mock_drive_class.return_value = mock_drive

        with pytest.raises(HTTPException) as exc:
            listar_fotos(pasta="Inexistente", usuario_logado={})
        assert exc.value.status_code == 404

    @patch("src.drive.controller.ServicoDrive")
    def test_listar_fotos_runtime_error(self, mock_drive_class):
        mock_drive = MagicMock()
        mock_drive.listar_fotos.side_effect = RuntimeError("Erro API Google")
        mock_drive_class.return_value = mock_drive

        with pytest.raises(HTTPException) as exc:
            listar_fotos(pasta="Pasta", usuario_logado={})
        assert exc.value.status_code == 502
