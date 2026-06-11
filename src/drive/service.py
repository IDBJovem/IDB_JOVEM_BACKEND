import os
import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from src.drive.schema import RespostaDrive
from src.auth.service import ServicoAuth

class ServicoDrive:

    def __init__(self):
        self.refresh_token = os.getenv("GOOGLE_REFRESH_TOKEN")
        self.servico_auth = ServicoAuth()

    def _obter_token_valido(self) -> str:
        """Busca o refresh_token do .env, renova no Google e retorna o access_token ativo."""
        if not self.refresh_token:
            raise RuntimeError("GOOGLE_REFRESH_TOKEN nao configurado no arquivo .env")
        try:
            credenciais = self.servico_auth.obter_credenciais_validas(self.refresh_token)
            return credenciais.token
        except Exception as erro:
            raise RuntimeError("Falha automatica ao renovar credenciais do Google para o Drive") from erro

    @staticmethod
    def _escapar_valor_consulta(valor: str) -> str:
        """Escapa barra invertida e aspa simples para uso seguro na query da Drive API."""
        return valor.replace("\\", "\\\\").replace("'", "\\'")

    def _montar_url_busca_pasta(self, nome_pasta: str, id_pai: str | None = None) -> str:
        nome_pasta = self._escapar_valor_consulta(nome_pasta)
        consulta = (
            "mimeType='application/vnd.google-apps.folder' "
            f"and name='{nome_pasta}' and trashed=false"
        )

        if id_pai:
            consulta += f" and '{id_pai}' in parents"

        parametros = {
            "q": consulta,
            "fields": "files(id,name)",
            "pageSize": 1,
        }

        return f"https://www.googleapis.com/drive/v3/files?{urlencode(parametros)}"

    def _montar_url_busca_arquivo(self, id_pasta: str, nome_arquivo: str) -> str:
        nome_arquivo = self._escapar_valor_consulta(nome_arquivo)
        consulta = (
            f"'{id_pasta}' in parents "
            f"and name='{nome_arquivo}' "
            "and mimeType contains 'image/' "
            "and trashed=false"
        )

        parametros = {
            "q": consulta,
            "fields": "files(id,name,mimeType)",
            "pageSize": 1,
        }

        return f"https://www.googleapis.com/drive/v3/files?{urlencode(parametros)}"

    def _montar_url_busca_fotos(self, id_pasta: str) -> str:
        consulta = (
            f"'{id_pasta}' in parents "
            "and mimeType contains 'image/' "
            "and trashed=false"
        )

        parametros = {
            "q": consulta,
            "fields": "files(id,name,mimeType)",
            "pageSize": 200,
        }

        return f"https://www.googleapis.com/drive/v3/files?{urlencode(parametros)}"

    def _montar_url_visualizacao(self, id_arquivo: str) -> str:
        return f"https://drive.google.com/thumbnail?id={id_arquivo}&sz=w1000"

    def _buscar_pasta_id(
        self,
        token: str,
        nome_pasta: str,
        id_pai: str | None = None,
    ) -> str | None:

        url = self._montar_url_busca_pasta(nome_pasta, id_pai)

        requisicao = Request(url)
        requisicao.add_header("Authorization", f"Bearer {token}")
        requisicao.add_header("Accept", "application/json")

        try:
            with urlopen(requisicao, timeout=10) as resposta:
                corpo = resposta.read().decode("utf-8")

        except (HTTPError, URLError) as erro:
            raise RuntimeError(
                "Falha ao buscar pasta no Google Drive"
            ) from erro

        dados = json.loads(corpo)
        arquivos = dados.get("files", [])

        if not arquivos:
            return None

        return arquivos[0].get("id")

    def _resolver_pasta(self, token: str, caminho_pasta: str) -> str | None:
        """Resolve um caminho de pastas separado por '/' (ex.: 'idbj/produtos')
        descendo nível a nível e retorna o id da pasta final."""
        id_atual = None

        for parte in caminho_pasta.split("/"):
            parte = parte.strip()

            if not parte:
                continue

            id_atual = self._buscar_pasta_id(token, parte, id_atual)

            if not id_atual:
                return None

        return id_atual

    def _buscar_arquivo_id(
        self,
        token: str,
        id_pasta: str,
        nome_arquivo: str,
    ) -> str | None:

        url = self._montar_url_busca_arquivo(id_pasta, nome_arquivo)

        requisicao = Request(url)
        requisicao.add_header("Authorization", f"Bearer {token}")
        requisicao.add_header("Accept", "application/json")

        try:
            with urlopen(requisicao, timeout=10) as resposta:
                corpo = resposta.read().decode("utf-8")

        except (HTTPError, URLError) as erro:
            raise RuntimeError(
                "Falha ao buscar arquivo no Google Drive"
            ) from erro

        dados = json.loads(corpo)
        arquivos = dados.get("files", [])

        if not arquivos:
            return None

        return arquivos[0].get("id")

    def _buscar_fotos_drive(
        self,
        token: str,
        id_pasta: str
    ) -> list[RespostaDrive]:

        url = self._montar_url_busca_fotos(id_pasta)

        requisicao = Request(url)
        requisicao.add_header("Authorization", f"Bearer {token}")
        requisicao.add_header("Accept", "application/json")

        try:
            with urlopen(requisicao, timeout=10) as resposta:
                corpo = resposta.read().decode("utf-8")

        except (HTTPError, URLError) as erro:
            raise RuntimeError(
                "Falha ao buscar fotos no Google Drive"
            ) from erro

        dados = json.loads(corpo)
        arquivos = dados.get("files", [])

        fotos = []

        for arquivo in arquivos:
            id_arquivo = arquivo.get("id")

            if not id_arquivo:
                continue

            fotos.append(
                RespostaDrive(
                    id=id_arquivo,
                    nome=arquivo.get("name", ""),
                    url_visualizacao=(
                        self._montar_url_visualizacao(id_arquivo)
                    ),
                )
            )

        return fotos

    def listar_fotos(self, nome_pasta: str) -> list[RespostaDrive]:
        token = self._obter_token_valido()

        id_pasta = self._buscar_pasta_id(token, nome_pasta)

        if not id_pasta:
            raise ValueError("Pasta do Google Drive não encontrada")

        return self._buscar_fotos_drive(token, id_pasta)

    def obter_url_por_nome(
        self,
        caminho_pasta: str,
        nome_arquivo: str | None,
    ) -> str | None:
        """Resolve a URL de visualização de um único arquivo pelo nome dentro de
        uma pasta. Retorna None se o nome for vazio, se a pasta/arquivo não for
        encontrado ou se o Drive estiver indisponível (degradação suave)."""
        if not nome_arquivo:
            return None

        try:
            token = self._obter_token_valido()
            id_pasta = self._resolver_pasta(token, caminho_pasta)

            if not id_pasta:
                return None

            id_arquivo = self._buscar_arquivo_id(token, id_pasta, nome_arquivo)

        except (RuntimeError, ValueError):
            return None

        if not id_arquivo:
            return None

        return self._montar_url_visualizacao(id_arquivo)

    def listar_mapa_nome_url(self, caminho_pasta: str) -> dict[str, str]:
        """Lista as imagens de uma pasta e devolve {nome_arquivo: url_visualizacao}.
        Retorna {} se a pasta não existir ou o Drive estiver indisponível, para
        que listagens que dependem disso não quebrem (degradação suave)."""
        try:
            token = self._obter_token_valido()
            id_pasta = self._resolver_pasta(token, caminho_pasta)

            if not id_pasta:
                return {}

            fotos = self._buscar_fotos_drive(token, id_pasta)

        except (RuntimeError, ValueError):
            return {}

        return {foto.nome: foto.url_visualizacao for foto in fotos}
