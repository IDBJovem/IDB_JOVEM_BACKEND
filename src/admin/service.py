from src.admin.model import Admin
from src.admin.repository import RepositorioAdmin
from src.admin.schema import SolicitacaoAdmin


class ServicoAdmin:

    def __init__(self, repositorio: RepositorioAdmin):
        self.repositorio = repositorio

    def criar_admin(self, dados: SolicitacaoAdmin):
        admin_email = self.repositorio.buscar_por_email(dados.email)

        if admin_email:
            raise ValueError("Já existe um administrador com esse e-mail.")

        admin_keycloak = self.repositorio.buscar_por_keycloak_id(dados.keycloak_id)

        if admin_keycloak:
            raise ValueError("Já existe um administrador com esse Keycloak ID.")

        admin = Admin(**dados.model_dump())
        return self.repositorio.salvar(admin)

    def listar_admins(self):
        return self.repositorio.buscar_todos()

    def buscar_admin(self, admin_id: int):
        admin = self.repositorio.buscar_por_id(admin_id)

        if not admin:
            raise ValueError("Administrador não encontrado.")

        return admin

    def deletar_admin(self, admin_id: int, usuario_logado: dict):
        admin = self.buscar_admin(admin_id)

        if str(usuario_logado.get("sub")) == str(admin.keycloak_id):
            raise ValueError("Não é permitido excluir o próprio usuário administrador.")

        self.repositorio.deletar(admin)
