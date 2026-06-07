import pytest
from unittest.mock import patch, MagicMock
from src.database import obter_banco


class TestObterBanco:
    @patch("src.database.SessionLocal")
    def test_obter_banco_yield_e_fecha(self, mock_session_local):
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session

        gen = obter_banco()
        banco = next(gen)

        assert banco == mock_session

        # Finaliza o generator para testar o finally
        with pytest.raises(StopIteration):
            next(gen)

        mock_session.close.assert_called_once()

    @patch("src.database.SessionLocal")
    def test_obter_banco_fecha_mesmo_com_erro(self, mock_session_local):
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session

        gen = obter_banco()
        banco = next(gen)

        # Simula erro lançado pelo consumer
        try:
            gen.throw(Exception("Erro simulado"))
        except Exception:
            pass

        mock_session.close.assert_called_once()
