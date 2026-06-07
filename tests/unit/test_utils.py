import pytest
from src.shared.utils import validar_datas, validar_coordenadas, extrair_token_bearer
from datetime import datetime, timedelta


class TestValidarDatas:
    def test_datas_validas(self):
        inicio = datetime.now()
        fim = datetime.now() + timedelta(hours=1)
        # Não deve levantar exceção
        validar_datas(inicio, fim)

    def test_data_inicio_igual_fim(self):
        agora = datetime.now()
        with pytest.raises(ValueError, match="O valor final deve ser maior que o valor inicial."):
            validar_datas(agora, agora)

    def test_data_inicio_maior_que_fim(self):
        inicio = datetime.now() + timedelta(hours=1)
        fim = datetime.now()
        with pytest.raises(ValueError, match="O valor final deve ser maior que o valor inicial."):
            validar_datas(inicio, fim)


class TestValidarCoordenadas:
    def test_coordenadas_validas(self):
        validar_coordenadas(-15.7942, -47.8822)

    def test_latitude_invalida_acima(self):
        with pytest.raises(ValueError, match="Latitude inválida."):
            validar_coordenadas(91.0, 0.0)

    def test_latitude_invalida_abaixo(self):
        with pytest.raises(ValueError, match="Latitude inválida."):
            validar_coordenadas(-91.0, 0.0)

    def test_longitude_invalida_acima(self):
        with pytest.raises(ValueError, match="Longitude inválida."):
            validar_coordenadas(0.0, 181.0)

    def test_longitude_invalida_abaixo(self):
        with pytest.raises(ValueError, match="Longitude inválida."):
            validar_coordenadas(0.0, -181.0)

    def test_limites_validos(self):
        validar_coordenadas(90.0, 180.0)
        validar_coordenadas(-90.0, -180.0)


class TestExtrairTokenBearer:
    def test_token_com_bearer(self):
        resultado = extrair_token_bearer("Bearer abc123")
        assert resultado == "abc123"

    def test_token_com_bearer_minusculo(self):
        resultado = extrair_token_bearer("bearer abc123")
        assert resultado == "abc123"

    def test_token_sem_bearer(self):
        resultado = extrair_token_bearer("abc123")
        assert resultado == "abc123"

    def test_valor_none(self):
        resultado = extrair_token_bearer(None)
        assert resultado is None

    def test_valor_vazio(self):
        resultado = extrair_token_bearer("")
        assert resultado is None

    def test_token_com_espacos(self):
        resultado = extrair_token_bearer("  Bearer   token123  ")
        assert resultado == "token123"
