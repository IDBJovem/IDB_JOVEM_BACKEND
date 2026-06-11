from src.produto.model import Produto
from src.produto.repository import RepositorioProduto
from src.produto.schema import SolicitacaoProduto


class ServicoProduto:

    def __init__(self, repositorio: RepositorioProduto):
        self.repositorio = repositorio

    def criar_produto(self, dados: SolicitacaoProduto):
        produto = Produto(**dados.model_dump())
        return self.repositorio.salvar(produto)

    def listar_produtos(self):
        return self.repositorio.buscar_todos()

    def buscar_produto(self, produto_id: int):
        produto = self.repositorio.buscar_por_id(produto_id)

        if not produto:
            raise ValueError("Produto não encontrado.")

        return produto

    def atualizar_produto(self, produto_id: int, dados: SolicitacaoProduto):
        produto = self.buscar_produto(produto_id)

        mudancas = dados.model_dump(exclude_unset=True)

        for campo, valor in mudancas.items():
            setattr(produto, campo, valor)

        return self.repositorio.salvar(produto)

    def deletar_produto(self, produto_id: int):
        produto = self.buscar_produto(produto_id)
        self.repositorio.deletar(produto)
