import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


class ServicoMapa:
    BASE_URL = "https://nominatim.openstreetmap.org"

    def __init__(self):
        self.agente_usuario = "IDB-Jovem-Backend/1.0"

    def buscar_endereco_por_coordenadas(self, latitude: float, longitude: float) -> str | None:
        parametros = {
            "format": "jsonv2",
            "latitude": latitude,
            "longitude": longitude,
            "endereco": 1,
        }

        url = f"{self.BASE_URL}/reverse?{urlencode(parametros)}"

        requisicao = Request(url)
        requisicao.add_header("User-Agent", self.agente_usuario)
        requisicao.add_header("Accept", "application/json")

        try:
            with urlopen(requisicao, timeout=10) as resposta:
                corpo = resposta.read().decode("utf-8")

        except (HTTPError, URLError):
            return None

        dados = json.loads(corpo)

        return dados.get("display_name")
