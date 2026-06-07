import pytest
from unittest.mock import patch, MagicMock
from urllib.error import HTTPError, URLError
from src.mapa.service import ServicoMapa


class TestServicoMapa:
    def test_init(self):
        servico = ServicoMapa()
        assert servico.agente_usuario == "IDB-Jovem-Backend/1.0"

    @patch("src.mapa.service.urlopen")
    def test_buscar_endereco_sucesso(self, mock_urlopen):
        import json
        mock_resposta = MagicMock()
        mock_resposta.read.return_value = json.dumps({
            "display_name": "Rua Teste, 123, Brasília"
        }).encode("utf-8")
        mock_resposta.__enter__ = lambda s: s
        mock_resposta.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resposta

        servico = ServicoMapa()
        resultado = servico.buscar_endereco_por_coordenadas(-15.7942, -47.8822)
        assert resultado == "Rua Teste, 123, Brasília"

    @patch("src.mapa.service.urlopen")
    def test_buscar_endereco_http_error(self, mock_urlopen):
        mock_urlopen.side_effect = HTTPError(
            url="http://test.com", code=500, msg="Error", hdrs=None, fp=None
        )
        servico = ServicoMapa()
        resultado = servico.buscar_endereco_por_coordenadas(-15.7942, -47.8822)
        assert resultado is None

    @patch("src.mapa.service.urlopen")
    def test_buscar_endereco_url_error(self, mock_urlopen):
        mock_urlopen.side_effect = URLError("Connection error")
        servico = ServicoMapa()
        resultado = servico.buscar_endereco_por_coordenadas(-15.7942, -47.8822)
        assert resultado is None

    @patch("src.mapa.service.urlopen")
    def test_buscar_endereco_sem_display_name(self, mock_urlopen):
        import json
        mock_resposta = MagicMock()
        mock_resposta.read.return_value = json.dumps({}).encode("utf-8")
        mock_resposta.__enter__ = lambda s: s
        mock_resposta.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resposta

        servico = ServicoMapa()
        resultado = servico.buscar_endereco_por_coordenadas(0.0, 0.0)
        assert resultado is None
