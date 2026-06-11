import pytest

from src.drive.utils import (
    extrair_file_id,
    montar_url_proxy,
    converter_link_para_proxy,
)


class TestExtrairFileId:
    @pytest.mark.parametrize("link,esperado", [
        ("https://drive.google.com/file/d/ABC123_xyz/view", "ABC123_xyz"),
        ("https://drive.google.com/thumbnail?id=ABC123_xyz&sz=w1000", "ABC123_xyz"),
        ("https://drive.google.com/uc?id=ABC123_xyz", "ABC123_xyz"),
        ("https://drive.google.com/open?id=ABC123_xyz", "ABC123_xyz"),
        ("https://lh3.googleusercontent.com/d/ABC123_xyz", "ABC123_xyz"),
        ("ABC123_xyz0", "ABC123_xyz0"),
    ])
    def test_extrai_de_formatos_conhecidos(self, link, esperado):
        assert extrair_file_id(link) == esperado

    @pytest.mark.parametrize("link", [
        None,
        "",
        "https://exemplo.com/imagem.png",
    ])
    def test_retorna_none_quando_nao_e_drive(self, link):
        assert extrair_file_id(link) is None


class TestConverterLinkParaProxy:
    def test_converte_link_do_drive(self):
        resultado = converter_link_para_proxy(
            "https://drive.google.com/file/d/ABC123_xyz/view"
        )
        assert resultado == montar_url_proxy("ABC123_xyz")
        assert resultado.endswith("/drive/imagem/ABC123_xyz")

    def test_preserva_url_externa(self):
        externo = "https://exemplo.com/imagem.png"
        assert converter_link_para_proxy(externo) == externo

    def test_preserva_none(self):
        assert converter_link_para_proxy(None) is None
