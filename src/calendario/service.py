from datetime import date, datetime, timezone
import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from src.calendario.schema import RespostaEvento, SolicitacaoEvento

class ServicoCalendario:
    def __init__(self, token_acesso: str = None):
        self.token_acesso = token_acesso

    def _extrair_token(self) -> str | None:
        if not self.token_acesso:
            return None
        token = self.token_acesso.strip()
        if token.lower().startswith("bearer "):
            return token[7:].strip()
        return token

    def _montar_url_evento(self) -> str:
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

    def _converter_evento(self, registro: dict) -> RespostaEvento | None:
        data_evento = self._parsear_data(registro)
        if not data_evento:
            return None
        return RespostaEvento(
            nome=registro.get("summary", "(Sem nome)"),
            data=data_evento,
            local=registro.get("location", ""),
        )

    def _buscar_evento_google(self, token: str) -> list[RespostaEvento]:
        url = self._montar_url_evento()
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
        evento: list[RespostaEvento] = []
        for registro in itens:
            evento = self._converter_evento(registro)
            if evento:
                evento.append(evento)
        return evento

    def listar_evento(self) -> list[RespostaEvento]:
        """
        Busca os evento. Por enquanto, simula a resposta do Google Calendar.
        """
        token = self._extrair_token()

        # Se não houver token (cliente não logou), manda dados simulados de teste
        if not token:
            return [
                RespostaEvento(
                    nome="[MOCK] Boas-vindas aos Novos Voluntarios",
                    data=date(2026, 6, 5),
                    local="Auditório Principal"
                ),
                RespostaEvento(
                    nome="[MOCK] Alinhamento do Projeto com Cliente",
                    data=date(2026, 6, 12),
                    local="Sala de Reuniões 02"
                ),
                RespostaEvento(
                    nome="[MOCK] Mutirao de Cadastro",
                    data=date(2026, 6, 20),
                    local="Comunidade Solar"
                )
            ]

        return self._buscar_evento_google(token)

    def criar_evento(self, evento: SolicitacaoEvento, nome_local: str) -> str:
        token = self._extrair_token()

        if not token:
            return None

        url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"

        corpo = {
            "summary": evento.nome,
            "location": nome_local,
            "description": evento.descricao,
            "start": {"dateTime": (evento.data_inicio.isoformat())},
            "end": {"dateTime": (evento.data_fim.isoformat())}
        }

        requisicao = Request(url, data=json.dumps(corpo).encode("utf-8"), method="POST")
        requisicao.add_header("Authorization", f"Bearer {token}")
        requisicao.add_header("Content-Type", "application/json")

        with urlopen(requisicao, timeout=10) as resposta:

            corpo_resposta = (resposta.read().decode("utf-8"))

        dados = json.loads(corpo_resposta)

        return dados.get("id")

    def atualizar_evento(self, calendario_event_id, evento: SolicitacaoEvento, nome_local: str) -> str:
        token = self._extrair_token()

        if not token:
            return

        url = (
        "https://www.googleapis.com/calendar/v3/"
        f"calendars/primary/events/{calendario_event_id}"
    )

        corpo = {
            "summary": evento.nome,
            "location": nome_local,
            "description": evento.descricao,
            "start": {"dateTime": evento.data_inicio.isoformat()},
            "end": {"dateTime": evento.data_fim.isoformat()}
        }

        requisicao = Request(url, data=json.dumps(corpo).encode("utf-8"), method="PUT")
        requisicao.add_header("Authorization", f"Bearer {token}")
        requisicao.add_header("Content-Type", "application/json")
        urlopen(requisicao, timeout=10)

    def deletar_evento(self, calendario_event_id):
        token = self._extrair_token()

        if not token:
            return

        url = (
        "https://www.googleapis.com/calendar/v3/"
        f"calendars/primary/events/{calendario_event_id}"
    )

        requisicao = Request(url, method="DELETE")
        requisicao.add_header("Authorization", f"Bearer {token}")
        urlopen(requisicao, timeout=10)
