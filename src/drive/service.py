import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from src.drive.schema import RespostaDrive
from src.shared.utils import extrair_token_bearer

class ServicoDrive:

    def __init__(self, token_acesso: str | None = None):
        self.token_acesso = token_acesso

    def _montar_url_busca_pasta(self, nome_pasta: str) -> str:
        consulta = (
            "mimeType='application/vnd.google-apps.folder' "
            f"and name='{nome_pasta}' and trashed=false"
        )

        parametros = {
            "q": consulta,
            "fields": "files(id,name)",
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
        return f"https://drive.google.com/uc?export=view&id={id_arquivo}"

    def _buscar_pasta_id(self, token: str, nome_pasta: str) -> str | None:

        url = self._montar_url_busca_pasta(nome_pasta)

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

        token = extrair_token_bearer(self.token_acesso)

        if not token:
            return []

        id_pasta = self._buscar_pasta_id(token, nome_pasta)

        if not id_pasta:
            raise ValueError("Pasta do Google Drive não encontrada")

        return self._buscar_fotos_drive(token, id_pasta)
