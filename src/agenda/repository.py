import calendar
from datetime import date, datetime, timezone
import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from src.agenda.schema import EventoResponse, RespostaEventoAgenda, SolicitacaoEventoAgenda
from src.shared.utils import extrair_token_bearer

class RepositorioAgenda:
    def __init__(self, token_acesso: str = None):
        self.token_acesso = token_acesso

    def _adicionar_meses(self, data_base: datetime, meses: int) -> datetime:
        if meses <= 0:
            return data_base
        mes_final = data_base.month - 1 + meses
        ano = data_base.year + mes_final // 12
        mes = mes_final % 12 + 1
        ultimo_dia = calendar.monthrange(ano, mes)[1]
        dia = min(data_base.day, ultimo_dia)
        return data_base.replace(year=ano, month=mes, day=dia)

    def _montar_url_evento(self, data_inicio: datetime, data_fim: datetime) -> str:
        parametros = {
            "timeMin": data_inicio.isoformat(),
            "timeMax": data_fim.isoformat(),
            "maxResults": 250,
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

    def _parsear_data_hora(self, registro: dict, chave: str) -> datetime | None:
        bloco = registro.get(chave, {})
        data_texto = bloco.get("dateTime") or bloco.get("date")
        if not data_texto:
            return None
        if "T" in data_texto:
            data_texto = data_texto.replace("Z", "+00:00")
            return datetime.fromisoformat(data_texto)
        return datetime.fromisoformat(f"{data_texto}T00:00:00+00:00")

    def _normalizar_data_hora(self, valor: datetime) -> datetime:
        if valor.tzinfo is None:
            return valor.replace(tzinfo=timezone.utc)
        return valor

    def _converter_evento(self, registro: dict) -> EventoResponse | None:
        data_evento = self._parsear_data(registro)
        if not data_evento:
            return None
        return EventoResponse(
            id_google=registro.get("id"),
            link_calendario=registro.get("htmlLink"),
            titulo=registro.get("summary", "(Sem titulo)"),
            data=data_evento,
            local=registro.get("location", ""),
        )

    def _converter_evento_criado(self, registro: dict) -> RespostaEventoAgenda | None:
        data_inicio = self._parsear_data_hora(registro, "start")
        data_fim = self._parsear_data_hora(registro, "end")
        if not data_inicio or not data_fim:
            return None
        return RespostaEventoAgenda(
            id_google=registro.get("id", ""),
            link_calendario=registro.get("htmlLink", ""),
            titulo=registro.get("summary", "(Sem titulo)"),
            data_inicio=data_inicio,
            data_fim=data_fim,
            local=registro.get("location", ""),
        )

    def _buscar_evento_google(self, token: str, meses: int) -> list[EventoResponse]:
        agora = datetime.now(timezone.utc)
        data_fim = self._adicionar_meses(agora, meses)
        url = self._montar_url_evento(agora, data_fim)
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
        evento: list[EventoResponse] = []
        for registro in itens:
            evento = self._converter_evento(registro)
            if evento:
                evento.append(evento)
        return evento

    def _montar_corpo_evento(self, solicitacao: SolicitacaoEventoAgenda) -> dict:
        inicio = self._normalizar_data_hora(solicitacao.data_inicio)
        fim = self._normalizar_data_hora(solicitacao.data_fim)
        corpo = {
            "summary": solicitacao.titulo,
            "location": solicitacao.local,
            "description": solicitacao.descricao,
            "start": {"dateTime": inicio.isoformat()},
            "end": {"dateTime": fim.isoformat()},
        }
        return {chave: valor for chave, valor in corpo.items() if valor}

    def _criar_evento_google(
        self,
        token: str,
        solicitacao: SolicitacaoEventoAgenda,
    ) -> RespostaEventoAgenda:
        url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
        corpo = json.dumps(self._montar_corpo_evento(solicitacao)).encode("utf-8")
        requisicao = Request(url, data=corpo, method="POST")
        requisicao.add_header("Authorization", f"Bearer {token}")
        requisicao.add_header("Accept", "application/json")
        requisicao.add_header("Content-Type", "application/json")
        try:
            with urlopen(requisicao, timeout=10) as resposta:
                retorno = resposta.read().decode("utf-8")
        except (HTTPError, URLError) as erro:
            raise RuntimeError("Falha ao criar evento no Google Calendar") from erro

        dados = json.loads(retorno)
        evento = self._converter_evento_criado(dados)
        if not evento:
            raise RuntimeError("Resposta invalida ao criar evento no Google Calendar")
        return evento

    def listar_evento(self, meses: int = 6) -> list[EventoResponse]:
        """
        Busca evento no Google Calendar quando ha token; sem token retorna mock.
        """
        token = extrair_token_bearer(self.token_acesso)

        # Se não houver token (cliente não logou), manda dados simulados de teste
        if not token:
            return [
                EventoResponse(
                    id_google="mock-1",
                    titulo="[MOCK] Boas-vindas aos Novos Voluntarios",
                    data=date(2026, 6, 5),
                    local="Auditório Principal"
                ),
                EventoResponse(
                    id_google="mock-2",
                    titulo="[MOCK] Alinhamento do Projeto com Cliente",
                    data=date(2026, 6, 12),
                    local="Sala de Reuniões 02"
                ),
                EventoResponse(
                    id_google="mock-3",
                    titulo="[MOCK] Mutirao de Cadastro",
                    data=date(2026, 6, 20),
                    local="Comunidade Solar"
                )
            ]

        return self._buscar_evento_google(token, meses)

    def criar_evento(self, solicitacao: SolicitacaoEventoAgenda) -> RespostaEventoAgenda:
        token = extrair_token_bearer(self.token_acesso)
        if not token:
            raise RuntimeError("Token de acesso ausente")
        return self._criar_evento_google(token, solicitacao)

    def _excluir_evento_google(self, token: str, id_google: str) -> None:
        url = f"https://www.googleapis.com/calendar/v3/calendars/primary/events/{id_google}"
        requisicao = Request(url, method="DELETE")
        requisicao.add_header("Authorization", f"Bearer {token}")
        requisicao.add_header("Accept", "application/json")
        try:
            with urlopen(requisicao, timeout=10) as resposta:
                resposta.read()
        except (HTTPError, URLError) as erro:
            raise RuntimeError("Falha ao excluir evento no Google Calendar") from erro

    def excluir_evento(self, id_google: str) -> None:
        token = extrair_token_bearer(self.token_acesso)
        if not token:
            raise RuntimeError("Token de acesso ausente")
        self._excluir_evento_google(token, id_google)
