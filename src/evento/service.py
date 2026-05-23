from src.evento.schema import SolicitacaoEvento
from src.shared.utils import validar_datas, validar_coordenadas
from src.evento.model import Evento
from src.evento.repository import RepositorioEvento
from src.calendario.service import ServicoCalendario
from src.mapa.service import ServicoMapa


class ServicoEvento:

    def __init__(
        self, repositorio: RepositorioEvento,
        google_calendario: ServicoCalendario,
        mapa_servico: ServicoMapa
    ):
        self.repositorio = repositorio
        self.calendario = google_calendario
        self.mapa_servico = mapa_servico

    def criar_evento(self, dados: SolicitacaoEvento):
        validar_datas(dados.data_inicio, dados.data_fim)
        validar_coordenadas(dados.local_latitude, dados.local_longitude)
        evento = Evento(**dados.model_dump())
        evento = self.repositorio.salvar(evento)

        nome_local = self.mapa_servico.buscar_endereco_por_coordenadas(
            evento.local_latitude,
            evento.local_longitude
        )

        evento.nome_local = nome_local
        evento = self.repositorio.salvar(evento)

        try:
            calendario_id = self.calendario.criar_evento(evento, nome_local)
            evento.calendario_evento_id = calendario_id
            evento = self.repositorio.salvar(evento)

        except Exception as erro:
            print(f"Erro ao integrar com o Google Calendário: {erro}")
            raise

        return evento

    def listar_eventos(self):
        return self.repositorio.buscar_todos()

    def buscar_evento(self, evento_id: int):
        evento = self.repositorio.buscar_por_id(evento_id)

        if not evento:
            raise ValueError("Evento não encontrado.")

        return evento

    def atualizar_evento(self, evento_id: int, mudancas: SolicitacaoEvento):
        evento = self.buscar_evento(evento_id)

        dados_mudanca = mudancas.model_dump(exclude_unset=True)

        for campo, novo_valor in dados_mudanca.items():
            setattr(evento, campo, novo_valor)

        validar_datas(evento.data_inicio, evento.data_fim)
        validar_coordenadas(evento.local_latitude, evento.local_longitude)

        evento.nome_local = self.mapa_servico.buscar_endereco_por_coordenadas(
            evento.local_latitude,
            evento.local_longitude
        )

        if evento.calendario_evento_id:
            self.calendario.atualizar_evento(
                evento.calendario_evento_id,
                evento,
                evento.nome_local
            )

        return self.repositorio.salvar(evento)

    def deletar_evento(self, evento_id: int):
        evento = self.buscar_evento(evento_id)

        if evento.calendario_evento_id:
            self.calendario.deletar_evento(evento.calendario_evento_id)

        self.repositorio.deletar(evento)
