import pytest
from unittest.mock import patch, MagicMock
from urllib.error import HTTPError, URLError
from src.drive.service import ServicoDrive


class TestServicoDrive:
    @patch.dict("os.environ", {"GOOGLE_REFRESH_TOKEN": ""})
    @patch("src.drive.service.ServicoAuth")
    def test_obter_token_sem_refresh(self, mock_auth_class):
        servico = ServicoDrive()
        servico.refresh_token = None
        with pytest.raises(RuntimeError, match="GOOGLE_REFRESH_TOKEN nao configurado"):
            servico._obter_token_valido()

    @patch.dict("os.environ", {"GOOGLE_REFRESH_TOKEN": "token-123"})
    @patch("src.drive.service.ServicoAuth")
    def test_obter_token_sucesso(self, mock_auth_class):
        mock_auth = MagicMock()
        mock_creds = MagicMock()
        mock_creds.token = "access-token"
        mock_auth.obter_credenciais_validas.return_value = mock_creds
        mock_auth_class.return_value = mock_auth

        servico = ServicoDrive()
        resultado = servico._obter_token_valido()
        assert resultado == "access-token"

    @patch.dict("os.environ", {"GOOGLE_REFRESH_TOKEN": "token-123"})
    @patch("src.drive.service.ServicoAuth")
    def test_obter_token_falha(self, mock_auth_class):
        mock_auth = MagicMock()
        mock_auth.obter_credenciais_validas.side_effect = Exception("Erro")
        mock_auth_class.return_value = mock_auth

        servico = ServicoDrive()
        with pytest.raises(RuntimeError, match="Falha automatica ao renovar credenciais"):
            servico._obter_token_valido()

    @patch("src.drive.service.ServicoAuth")
    def test_montar_url_busca_pasta(self, mock_auth_class):
        servico = ServicoDrive()
        url = servico._montar_url_busca_pasta("MinhasPastas")
        assert "googleapis.com/drive/v3/files" in url
        assert "MinhasPastas" in url

    @patch("src.drive.service.ServicoAuth")
    def test_montar_url_busca_fotos(self, mock_auth_class):
        servico = ServicoDrive()
        url = servico._montar_url_busca_fotos("folder-id-123")
        assert "googleapis.com/drive/v3/files" in url
        assert "folder-id-123" in url

    @patch("src.drive.service.ServicoAuth")
    def test_montar_url_visualizacao(self, mock_auth_class):
        servico = ServicoDrive()
        url = servico._montar_url_visualizacao("file-id-123")
        assert "file-id-123" in url
        assert "drive.google.com" in url

    @patch("src.drive.service.urlopen")
    @patch("src.drive.service.ServicoAuth")
    def test_buscar_pasta_id_sucesso(self, mock_auth_class, mock_urlopen):
        import json
        mock_resposta = MagicMock()
        mock_resposta.read.return_value = json.dumps({
            "files": [{"id": "folder-id-123", "name": "Pasta"}]
        }).encode("utf-8")
        mock_resposta.__enter__ = lambda s: s
        mock_resposta.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resposta

        servico = ServicoDrive()
        resultado = servico._buscar_pasta_id("token", "Pasta")
        assert resultado == "folder-id-123"

    @patch("src.drive.service.urlopen")
    @patch("src.drive.service.ServicoAuth")
    def test_buscar_pasta_id_nao_encontrada(self, mock_auth_class, mock_urlopen):
        import json
        mock_resposta = MagicMock()
        mock_resposta.read.return_value = json.dumps({"files": []}).encode("utf-8")
        mock_resposta.__enter__ = lambda s: s
        mock_resposta.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resposta

        servico = ServicoDrive()
        resultado = servico._buscar_pasta_id("token", "Inexistente")
        assert resultado is None

    @patch("src.drive.service.urlopen")
    @patch("src.drive.service.ServicoAuth")
    def test_buscar_pasta_id_http_error(self, mock_auth_class, mock_urlopen):
        mock_urlopen.side_effect = HTTPError(
            url="http://test.com", code=500, msg="Error", hdrs=None, fp=None
        )
        servico = ServicoDrive()
        with pytest.raises(RuntimeError, match="Falha ao buscar pasta"):
            servico._buscar_pasta_id("token", "Pasta")

    @patch("src.drive.service.urlopen")
    @patch("src.drive.service.ServicoAuth")
    def test_buscar_fotos_drive_sucesso(self, mock_auth_class, mock_urlopen):
        import json
        mock_resposta = MagicMock()
        mock_resposta.read.return_value = json.dumps({
            "files": [
                {"id": "file-1", "name": "foto1.jpg", "mimeType": "image/jpeg"},
                {"id": "file-2", "name": "foto2.png", "mimeType": "image/png"},
            ]
        }).encode("utf-8")
        mock_resposta.__enter__ = lambda s: s
        mock_resposta.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resposta

        servico = ServicoDrive()
        resultado = servico._buscar_fotos_drive("token", "folder-id")
        assert len(resultado) == 2
        assert resultado[0].nome == "foto1.jpg"

    @patch("src.drive.service.urlopen")
    @patch("src.drive.service.ServicoAuth")
    def test_buscar_fotos_drive_sem_id(self, mock_auth_class, mock_urlopen):
        import json
        mock_resposta = MagicMock()
        mock_resposta.read.return_value = json.dumps({
            "files": [{"name": "foto1.jpg", "mimeType": "image/jpeg"}]
        }).encode("utf-8")
        mock_resposta.__enter__ = lambda s: s
        mock_resposta.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resposta

        servico = ServicoDrive()
        resultado = servico._buscar_fotos_drive("token", "folder-id")
        assert len(resultado) == 0

    @patch("src.drive.service.urlopen")
    @patch("src.drive.service.ServicoAuth")
    def test_buscar_fotos_drive_http_error(self, mock_auth_class, mock_urlopen):
        mock_urlopen.side_effect = HTTPError(
            url="http://test.com", code=500, msg="Error", hdrs=None, fp=None
        )
        servico = ServicoDrive()
        with pytest.raises(RuntimeError, match="Falha ao buscar fotos"):
            servico._buscar_fotos_drive("token", "folder-id")

    @patch("src.drive.service.ServicoAuth")
    def test_listar_fotos_sucesso(self, mock_auth_class):
        servico = ServicoDrive()
        servico._obter_token_valido = MagicMock(return_value="token")
        servico._buscar_pasta_id = MagicMock(return_value="folder-id")
        servico._buscar_fotos_drive = MagicMock(return_value=[])

        resultado = servico.listar_fotos("Pasta")
        servico._buscar_fotos_drive.assert_called_once_with("token", "folder-id")

    @patch("src.drive.service.ServicoAuth")
    def test_listar_fotos_pasta_nao_encontrada(self, mock_auth_class):
        servico = ServicoDrive()
        servico._obter_token_valido = MagicMock(return_value="token")
        servico._buscar_pasta_id = MagicMock(return_value=None)

        with pytest.raises(ValueError, match="Pasta do Google Drive não encontrada"):
            servico.listar_fotos("Inexistente")
