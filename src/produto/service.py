from src.produto.model import Produto
from src.produto.repository import RepositorioProduto
from src.produto.schema import SolicitacaoProduto
from src.drive.service import ServicoDrive


# Pasta no Google Drive onde ficam as imagens dos produtos.
PASTA_PRODUTOS = "idbj/produtos"


class ServicoProduto:

    def __init__(self, repositorio: RepositorioProduto, drive: ServicoDrive | None = None):
        self.repositorio = repositorio
        self.drive = drive

    def _enriquecer(self, produto: Produto) -> Produto:
        """Resolve a URL de visualização da imagem a partir do nome do arquivo
        salvo. Sem o serviço do Drive (ex.: testes) o produto volta inalterado."""
        if self.drive and produto is not None:
            produto.imagem_url = self.drive.obter_url_por_nome(
                PASTA_PRODUTOS, produto.imagem_nome
            )

        return produto

    def criar_produto(self, dados: SolicitacaoProduto):
        produto = Produto(**dados.model_dump())
        produto = self.repositorio.salvar(produto)
        return self._enriquecer(produto)

    def listar_produtos(self):
        produtos = self.repositorio.buscar_todos()

        if not self.drive:
            return produtos

        mapa = self.drive.listar_mapa_nome_url(PASTA_PRODUTOS)

        for produto in produtos:
            produto.imagem_url = (
                mapa.get(produto.imagem_nome) if produto.imagem_nome else None
            )

        return produtos

    def buscar_produto(self, produto_id: int):
        produto = self.repositorio.buscar_por_id(produto_id)

        if not produto:
            raise ValueError("Produto não encontrado.")

        return self._enriquecer(produto)

    def atualizar_produto(self, produto_id: int, dados: SolicitacaoProduto):
        produto = self.repositorio.buscar_por_id(produto_id)

        if not produto:
            raise ValueError("Produto não encontrado.")

        mudancas = dados.model_dump(exclude_unset=True)

        for campo, valor in mudancas.items():
            setattr(produto, campo, valor)

        produto = self.repositorio.salvar(produto)
        return self._enriquecer(produto)

    def deletar_produto(self, produto_id: int):
        produto = self.repositorio.buscar_por_id(produto_id)

        if not produto:
            raise ValueError("Produto não encontrado.")

        self.repositorio.deletar(produto)
