from src.atividade.repository import RepositorioAtividade
from src.evento.repository import RepositorioEvento
from src.atividade.schema import SolicitacaoAtividade
from src.shared.utils import validar_datas
from src.atividade.model import Atividade

class ServicoAtividade:
    def __init__(
        self,
        repositorio_atividade: RepositorioAtividade,
        repositorio_evento: RepositorioEvento
    ):

        self.repositorio_atividade = repositorio_atividade
        self.repositorio_evento = repositorio_evento

    def criar_atividade(self, evento_id, dados: SolicitacaoAtividade):
        evento = self.repositorio_evento.buscar_por_id(evento_id)

        if not evento:
            raise ValueError("Evento não encontrado.")

        validar_datas(dados.horario_inicio, dados.horario_termino)

        atividade = Atividade(evento_id = evento_id, **dados.model_dump())

        return self.repositorio_atividade.salvar(atividade)

    def listar_atividades(self, evento_id: int):
        return self.repositorio_atividade.buscar_por_evento(evento_id)

    def buscar_atividade(self, atividade_id: int):
        atividade = self.repositorio_atividade.buscar_por_id(atividade_id)

        if not atividade:
            raise ValueError("Atividade não encontrada.")

        return atividade

    def atualizar_atividade(self, atividade_id: int, mudancas: SolicitacaoAtividade):
        atividade = self.buscar_atividade(atividade_id)

        dados_mudanca = mudancas.model_dump(exclude_unset=True)

        for campo, novo_valor in dados_mudanca.items():
            setattr(atividade, campo, novo_valor)

        validar_datas(atividade.horario_inicio, atividade.horario_termino)

        return self.repositorio_atividade.salvar(atividade)

    def deletar_atividade(self, atividade_id: int):
        atividade = self.buscar_atividade(atividade_id)
        self.repositorio_atividade.deletar(atividade)
