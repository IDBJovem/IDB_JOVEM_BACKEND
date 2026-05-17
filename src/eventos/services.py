# Aqui que orquestramos o fluxo de salvar um evento no banco e disparar APIs
# Código meramente ilustrativo, pode ser ajustado se necessário,
# mas a arquitetura geral deve ser mantida.
import uuid
from src.eventos.interfaces import IServicoCalendario
from src.eventos.models import ModeloEvento
from src.eventos.repository import RepositorioEvento
from src.eventos.schemas import SchemaCriarEvento

class ServicoEvento:
    def __init__(
            self, repositorio: RepositorioEvento, servico_calendario: IServicoCalendario
    ) -> None:
        self.repositorio = repositorio
        self.servico_calendario = servico_calendario

    def executar_criacao_evento(self, dados: SchemaCriarEvento) -> dict:
        if dados.data_fim <= dados.data_inicio:
            raise ValueError("A data de término deve ser maior à data de início.")
        novo_evento_model = ModeloEvento(
            id=uuid.uuid4().int,
            titulo=dados.titulo,
            data_inicio=dados.data_inicio,
            data_fim=dados.data_fim
        )

        if self.repositorio:
            self.repositorio.salvar_no_banco(novo_evento_model)

        link_calendario = self.servico_calendario.criar_evento_agenda(
            titulo=dados.titulo,
            inicio=dados.data_inicio,
            fim=dados.data_fim
        )

        resposta = {
            "id": novo_evento_model.id,
            "titulo": novo_evento_model.titulo,
            "data_inicio": novo_evento_model.data_inicio,
            "data_fim": novo_evento_model.data_fim,
            "link_calendario": link_calendario
        }

        return resposta
