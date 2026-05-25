from src.voluntario.models import Voluntario, Trabalha
from src.voluntario.repository import RepositorioVoluntario
from src.voluntario.schema import SolicitacaoVoluntario


STATUS_VALIDOS = ["pendente", "aprovado", "reprovado"]


class ServicoVoluntario:

    def __init__(self, repositorio: RepositorioVoluntario):
        self.repositorio = repositorio

    def criar_voluntario(self, dados: SolicitacaoVoluntario):
        existente = self.repositorio.buscar_por_email(dados.email)

        if existente:
            raise ValueError("Já existe um voluntário com esse e-mail.")

        voluntario = Voluntario(**dados.model_dump())
        return self.repositorio.salvar(voluntario)

    def listar_voluntarios(self):
        return self.repositorio.buscar_todos()

    def buscar_voluntario(self, voluntario_id: int):
        voluntario = self.repositorio.buscar_por_id(voluntario_id)

        if not voluntario:
            raise ValueError("Voluntário não encontrado.")

        return voluntario

    def deletar_voluntario(self, voluntario_id: int):
        voluntario = self.buscar_voluntario(voluntario_id)
        self.repositorio.deletar(voluntario)

    def listar_voluntarios_evento(self, evento_id: int):
        return self.repositorio.listar_por_evento(evento_id)

    def atualizar_status(self, voluntario_id: int, evento_id: int, status: str):
        if status not in STATUS_VALIDOS:
            raise ValueError("Status inválido. Use: pendente, aprovado ou reprovado.")

        voluntario = self.repositorio.buscar_por_id(voluntario_id)
        if not voluntario:
            raise ValueError("Voluntário não encontrado.")

        trabalho = self.repositorio.buscar_trabalho(voluntario_id, evento_id)

        if not trabalho:
            trabalho = Trabalha(
                voluntario_id=voluntario_id,
                evento_id=evento_id,
                status=status,
            )
        else:
            trabalho.status = status

        return self.repositorio.salvar_trabalho(trabalho)

    def contar_voluntarios_evento(self, evento_id: int):
        trabalhos = self.repositorio.listar_por_evento(evento_id)

        return {
            "evento_id": evento_id,
            "total": len(trabalhos),
            "pendentes": len([t for t in trabalhos if t.status == "pendente"]),
            "aprovados": len([t for t in trabalhos if t.status == "aprovado"]),
            "reprovados": len([t for t in trabalhos if t.status == "reprovado"]),
        }
