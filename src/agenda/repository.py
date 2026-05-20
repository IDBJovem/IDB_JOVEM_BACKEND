from datetime import date, datetime, timezone
import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from src.agenda.schema import EventoResponse

class RepositorioAgenda:
    def __init__(self, token_acesso: str = None):
        self.token_acesso = token_acesso

    def _extrair_token(self) -> str | None:
        if not self.token_acesso:
            return None
        token = self.token_acesso.strip()
        if token.lower().startswith("bearer "):
            return token[7:].strip()
        return token

    def _montar_url_eventos(self) -> str:
        parametros = {
            "timeMin": datetime.now(timezone.utc).isoformat(),
            "maxResults": 10,
            "singleEvents": "true",
            "orderBy": "startTime",
        }
        return (
            "https://www.googleapis.com/calendar/v3/calendars/primary/events?"
            f"{urlencode(parametros)}"
        )

    def _parsear_data(self, registro: dict) -> date | None:
        inicio = registro.get("start", {})
        data_texto = inicio.get("date") or inicio.get("dateTime")
        if not data_texto:
            return None
        if "T" in data_texto:
            data_texto = data_texto.replace("Z", "+00:00")
            return datetime.fromisoformat(data_texto).date()
        return date.fromisoformat(data_texto)

    def _converter_evento(self, registro: dict) -> EventoResponse | None:
        data_evento = self._parsear_data(registro)
        if not data_evento:
            return None
        return EventoResponse(
            titulo=registro.get("summary", "(Sem titulo)"),
            data=data_evento,
            local=registro.get("location", ""),
        )

    def _buscar_eventos_google(self, token: str) -> list[EventoResponse]:
        url = self._montar_url_eventos()
        requisicao = Request(url)
        requisicao.add_header("Authorization", f"Bearer {token}")
        requisicao.add_header("Accept", "application/json")
        try:
            with urlopen(requisicao, timeout=10) as resposta:
                corpo = resposta.read().decode("utf-8")
        except (HTTPError, URLError) as erro:
            raise RuntimeError("Falha ao acessar Google Calendar") from erro

        dados = json.loads(corpo)
        itens = dados.get("items", [])
        eventos: list[EventoResponse] = []
        for registro in itens:
            evento = self._converter_evento(registro)
            if evento:
                eventos.append(evento)
        return eventos

    def listar_eventos(self) -> list[EventoResponse]:
        """
        Busca os eventos. Por enquanto, simula a resposta do Google Calendar.
        """
        token = self._extrair_token()

        # Se não houver token (cliente não logou), manda dados simulados de teste
        if not token:
            return [
                EventoResponse(
                    titulo="[MOCK] Boas-vindas aos Novos Voluntarios",
                    data=date(2026, 6, 5),
                    local="Auditório Principal"
                ),
                EventoResponse(
                    titulo="[MOCK] Alinhamento do Projeto com Cliente",
                    data=date(2026, 6, 12),
                    local="Sala de Reuniões 02"
                ),
                EventoResponse(
                    titulo="[MOCK] Mutirao de Cadastro",
                    data=date(2026, 6, 20),
                    local="Comunidade Solar"
                )
            ]

        return self._buscar_eventos_google(token)
