import pytest
from fastapi.testclient import TestClient
from src.main import app  # Garantir que o import aponta para src.main

@pytest.fixture
def client():
    """
    Cria uma instância do TestClient do FastAPI para ser usada nos testes.
    """
    with TestClient(app) as c:
        yield c