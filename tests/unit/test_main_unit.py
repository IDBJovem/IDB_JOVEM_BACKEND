import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


class TestMainApp:
    @patch("src.main.configuracoes")
    def test_app_criada(self, mock_config):
        mock_config.CORS_ORIGINS = "http://localhost:3000,http://localhost:5173"
        mock_config.SECRET_KEY = "test-key"

        from src.main import app
        assert app.title == "IDB Jovem Backend"

    def test_read_root(self):
        from src.main import app
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["message"] == "IDB Jovem Backend está rodando!"

    def test_health_check(self):
        from src.main import app
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
