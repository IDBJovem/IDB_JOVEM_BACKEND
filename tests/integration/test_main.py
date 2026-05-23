"""
Testes de integração para as rotas da aplicação.
Cobre: rota raiz, health check e criação de evento (POST /events).
"""
import pytest


class TestRotaRaiz:
    def test_retorna_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_retorna_mensagem_correta(self, client):
        response = client.get("/")
        assert response.json() == {"message": "IDB Jovem Backend está rodando!"}


class TestHealthCheck:
    def test_retorna_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_retorna_status_ok(self, client):
        response = client.get("/health")
        assert response.json() == {"status": "ok"}


PAYLOADS_VALIDOS = [
    pytest.param(
        {"title": "Retiro Teen", "date": "2025-07-10", "location": "Sede IDB"},
        {"id": 1, "title": "Retiro Teen", "date": "2025-07-10",
         "location": "Sede IDB", "description": None, "capacity": None},
        id="payload_minimo",
    ),
    pytest.param(
        {"title": "Encontro Jovem", "date": "2025-08-15", "location": "Auditório Central",
         "description": "Encontro anual", "capacity": 200},
        {"id": 1, "title": "Encontro Jovem", "date": "2025-08-15",
         "location": "Auditório Central", "description": "Encontro anual", "capacity": 200},
        id="payload_completo",
    ),
    pytest.param(
        {"title": "Workshop", "date": "2025-09-01", "location": "Sala 3",
         "description": None, "capacity": 50},
        {"id": 1, "title": "Workshop", "date": "2025-09-01",
         "location": "Sala 3", "description": None, "capacity": 50},
        id="payload_com_capacity_sem_description",
    ),
]


@pytest.mark.parametrize("payload,esperado", PAYLOADS_VALIDOS)
def test_criar_evento_payload_valido(client, payload, esperado):
    """Garante que POST /events retorna 201 e o corpo correto para payloads válidos."""
    response = client.post("/events", json=payload)
    assert response.status_code == 201
    assert response.json() == esperado


PAYLOADS_INVALIDOS = [
    pytest.param({}, id="payload_vazio"),
    pytest.param({"date": "2025-07-10", "location": "Sede IDB"}, id="sem_title"),
    pytest.param({"title": "Evento X", "location": "Sede IDB"}, id="sem_date"),
    pytest.param({"title": "Evento X", "date": "2025-07-10"}, id="sem_location"),
]


@pytest.mark.parametrize("payload", PAYLOADS_INVALIDOS)
def test_criar_evento_payload_invalido_retorna_422(client, payload):
    """Garante que o FastAPI rejeita payloads incompletos com 422."""
    response = client.post("/events", json=payload)
    assert response.status_code == 422