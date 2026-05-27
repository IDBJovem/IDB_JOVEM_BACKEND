import pytest
from datetime import date, datetime, timezone
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

from src.agenda.router import router


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)



EVENTO_RESPONSE = {
    "id_google": "abc123",
    "link_calendario": "https://calendar.google.com/event/abc123",
    "titulo": "Retiro Teen 2025",
    "data": "2025-07-10",
    "local": "Auditório Principal",
}

SOLICITACAO_EVENTO = {
    "titulo": "Retiro Teen 2025",
    "data_inicio": "2025-07-10T08:00:00",
    "data_fim": "2025-07-12T18:00:00",
    "local": "Auditório Principal",
    "descricao": "Evento anual",
}

RESPOSTA_EVENTO_CRIADO = {
    "id_google": "abc123",
    "link_calendario": "https://calendar.google.com/event/abc123",
    "titulo": "Retiro Teen 2025",
    "data_inicio": "2025-07-10T08:00:00+00:00",
    "data_fim": "2025-07-12T18:00:00+00:00",
    "local": "Auditório Principal",
}

TOKEN_VALIDO = "Bearer token-google-valido"



class TestListarEvento:

    def test_listar_sem_token_retorna_mocks(self, client):
        with patch("src.agenda.router.RepositorioAgenda") as MockRepo:
            from src.agenda.schema import EventoResponse
            MockRepo.return_value.listar_evento.return_value = [
                EventoResponse(**EVENTO_RESPONSE)
            ]
            resposta = client.get("/agenda/evento")
        assert resposta.status_code == 200
        assert isinstance(resposta.json(), list)

    def test_listar_com_token_retorna_lista(self, client):
        with patch("src.agenda.router.RepositorioAgenda") as MockRepo:
            from src.agenda.schema import EventoResponse
            MockRepo.return_value.listar_evento.return_value = [
                EventoResponse(**EVENTO_RESPONSE)
            ]
            resposta = client.get(
                "/agenda/evento",
                headers={"Authorization": TOKEN_VALIDO}
            )
        assert resposta.status_code == 200
        assert len(resposta.json()) == 1
        assert resposta.json()[0]["titulo"] == EVENTO_RESPONSE["titulo"]

    def test_listar_retorna_lista_vazia(self, client):
        with patch("src.agenda.router.RepositorioAgenda") as MockRepo:
            MockRepo.return_value.listar_evento.return_value = []
            resposta = client.get("/agenda/evento")
        assert resposta.status_code == 200
        assert resposta.json() == []

    def test_listar_repassa_token_ao_repositorio(self, client):
        with patch("src.agenda.router.RepositorioAgenda") as MockRepo:
            MockRepo.return_value.listar_evento.return_value = []
            client.get(
                "/agenda/evento",
                headers={"Authorization": TOKEN_VALIDO}
            )
            MockRepo.assert_called_once_with(token_acesso=TOKEN_VALIDO)

    @pytest.mark.parametrize("meses", [1, 3, 6, 12, 24])
    def test_listar_parametro_meses_valido(self, client, meses):
        with patch("src.agenda.router.RepositorioAgenda") as MockRepo:
            MockRepo.return_value.listar_evento.return_value = []
            resposta = client.get(f"/agenda/evento?meses={meses}")
        assert resposta.status_code == 200

    @pytest.mark.parametrize("meses_invalido", [0, 25, -1])
    def test_listar_parametro_meses_invalido_retorna_422(self, client, meses_invalido):
        resposta = client.get(f"/agenda/evento?meses={meses_invalido}")
        assert resposta.status_code == 422

    def test_listar_multiplos_eventos(self, client):
        from src.agenda.schema import EventoResponse
        eventos = [
            EventoResponse(**{**EVENTO_RESPONSE, "id_google": f"id-{i}", "titulo": f"Evento {i}"})
            for i in range(1, 4)
        ]
        with patch("src.agenda.router.RepositorioAgenda") as MockRepo:
            MockRepo.return_value.listar_evento.return_value = eventos
            resposta = client.get("/agenda/evento")
        assert resposta.status_code == 200
        assert len(resposta.json()) == 3



class TestCriarEvento:

    def test_criar_evento_sucesso(self, client):
        with patch("src.agenda.router.RepositorioAgenda") as MockRepo:
            from src.agenda.schema import RespostaEventoAgenda
            MockRepo.return_value.criar_evento.return_value = RespostaEventoAgenda(
                **RESPOSTA_EVENTO_CRIADO
            )
            resposta = client.post(
                "/agenda/evento",
                json=SOLICITACAO_EVENTO,
                headers={"Authorization": TOKEN_VALIDO},
            )
        assert resposta.status_code == 201
        assert resposta.json()["id_google"] == RESPOSTA_EVENTO_CRIADO["id_google"]
        assert resposta.json()["titulo"] == RESPOSTA_EVENTO_CRIADO["titulo"]

    def test_criar_evento_sem_token_retorna_401(self, client):
        resposta = client.post("/agenda/evento", json=SOLICITACAO_EVENTO)
        assert resposta.status_code == 401
        assert "Token de acesso ausente" in resposta.json()["detail"]

    def test_criar_evento_erro_google_retorna_502(self, client):
        with patch("src.agenda.router.RepositorioAgenda") as MockRepo:
            MockRepo.return_value.criar_evento.side_effect = RuntimeError(
                "Falha ao criar evento no Google Calendar"
            )
            resposta = client.post(
                "/agenda/evento",
                json=SOLICITACAO_EVENTO,
                headers={"Authorization": TOKEN_VALIDO},
            )
        assert resposta.status_code == 502
        assert "Falha ao criar evento" in resposta.json()["detail"]

    def test_criar_evento_sem_titulo_retorna_422(self, client):
        payload = {k: v for k, v in SOLICITACAO_EVENTO.items() if k != "titulo"}
        resposta = client.post(
            "/agenda/evento",
            json=payload,
            headers={"Authorization": TOKEN_VALIDO},
        )
        assert resposta.status_code == 422

    @pytest.mark.parametrize("campo_ausente", ["titulo", "data_inicio", "data_fim"])
    def test_criar_evento_campo_obrigatorio_ausente(self, client, campo_ausente):
        payload = {k: v for k, v in SOLICITACAO_EVENTO.items() if k != campo_ausente}
        resposta = client.post(
            "/agenda/evento",
            json=payload,
            headers={"Authorization": TOKEN_VALIDO},
        )
        assert resposta.status_code == 422

    def test_criar_evento_repassa_token_ao_repositorio(self, client):
        with patch("src.agenda.router.RepositorioAgenda") as MockRepo:
            from src.agenda.schema import RespostaEventoAgenda
            MockRepo.return_value.criar_evento.return_value = RespostaEventoAgenda(
                **RESPOSTA_EVENTO_CRIADO
            )
            client.post(
                "/agenda/evento",
                json=SOLICITACAO_EVENTO,
                headers={"Authorization": TOKEN_VALIDO},
            )
            MockRepo.assert_called_once_with(token_acesso=TOKEN_VALIDO)



class TestExcluirEvento:

    def test_excluir_evento_sucesso(self, client):
        with patch("src.agenda.router.RepositorioAgenda") as MockRepo:
            MockRepo.return_value.excluir_evento.return_value = None
            resposta = client.delete(
                "/agenda/evento/abc123",
                headers={"Authorization": TOKEN_VALIDO},
            )
        assert resposta.status_code == 204
        MockRepo.return_value.excluir_evento.assert_called_once_with("abc123")

    def test_excluir_evento_sem_token_retorna_401(self, client):
        resposta = client.delete("/agenda/evento/abc123")
        assert resposta.status_code == 401
        assert "Token de acesso ausente" in resposta.json()["detail"]

    def test_excluir_evento_erro_google_retorna_502(self, client):
        with patch("src.agenda.router.RepositorioAgenda") as MockRepo:
            MockRepo.return_value.excluir_evento.side_effect = RuntimeError(
                "Falha ao excluir evento no Google Calendar"
            )
            resposta = client.delete(
                "/agenda/evento/abc123",
                headers={"Authorization": TOKEN_VALIDO},
            )
        assert resposta.status_code == 502
        assert "Falha ao excluir evento" in resposta.json()["detail"]

    @pytest.mark.parametrize("id_google", ["abc123", "xyz-event-456", "google_id_789"])
    def test_excluir_varios_ids(self, client, id_google):
        with patch("src.agenda.router.RepositorioAgenda") as MockRepo:
            MockRepo.return_value.excluir_evento.return_value = None
            resposta = client.delete(
                f"/agenda/evento/{id_google}",
                headers={"Authorization": TOKEN_VALIDO},
            )
        assert resposta.status_code == 204