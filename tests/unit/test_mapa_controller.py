import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from src.mapa.controller import buscar_endereco


class TestMapaController:
    @patch("src.mapa.controller.ServicoMapa")
    @patch("src.mapa.controller.validar_coordenadas")
    def test_buscar_endereco_sucesso(self, mock_validar, mock_mapa_class):
        mock_mapa = MagicMock()
        mock_mapa.buscar_endereco_por_coordenadas.return_value = "Rua Teste, 123"
        mock_mapa_class.return_value = mock_mapa

        resultado = buscar_endereco(latitude=-15.7942, longitude=-47.8822)
        assert resultado["nome_local"] == "Rua Teste, 123"

    @patch("src.mapa.controller.ServicoMapa")
    @patch("src.mapa.controller.validar_coordenadas")
    def test_buscar_endereco_nao_encontrado(self, mock_validar, mock_mapa_class):
        mock_mapa = MagicMock()
        mock_mapa.buscar_endereco_por_coordenadas.return_value = None
        mock_mapa_class.return_value = mock_mapa

        with pytest.raises(HTTPException) as exc:
            buscar_endereco(latitude=0.0, longitude=0.0)
        assert exc.value.status_code == 404

    @patch("src.mapa.controller.validar_coordenadas")
    def test_buscar_endereco_coordenadas_invalidas(self, mock_validar):
        mock_validar.side_effect = ValueError("Latitude inválida.")
        with pytest.raises(HTTPException) as exc:
            buscar_endereco(latitude=200.0, longitude=0.0)
        assert exc.value.status_code == 400
