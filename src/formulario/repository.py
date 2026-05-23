import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from sqlalchemy.orm import Session

from src.eventos.model import Evento
from src.formulario.schema import RespostaInscricaoFormulario
from src.shared.utils import extrair_token_bearer
from src.voluntario.models import Trabalha, Voluntario

STATUS_PENDENTE = "pendente"

class RepositorioFormulario:
    def __init__(self, token_acesso: str = None):
        self.token_acesso = token_acesso

    def _extrair_formulario_id_link(self, link: str) -> str | None:
        if "/forms/d/" not in link:
            return None
        parte = link.split("/forms/d/")[-1]
        return parte.split("/")[0] if parte else None

    def _definir_formulario_id(self, link_formulario: str) -> str:
        formulario_id = self._extrair_formulario_id_link(link_formulario)
        if not formulario_id:
            raise ValueError("Use o link completo do Forms para extrair o formulario_id")
        return formulario_id

    def _montar_link_resposta(self, formulario_id: str, resposta_id: str) -> str:
        return (
            f"https://docs.google.com/forms/d/{formulario_id}/edit#response={resposta_id}"
        )

    def _montar_requisicao(self, url: str, token: str) -> Request:
        requisicao = Request(url)
        requisicao.add_header("Authorization", f"Bearer {token}")
        requisicao.add_header("Accept", "application/json")
        return requisicao

    def _buscar_json(self, url: str, token: str, erro_mensagem: str) -> dict:
        requisicao = self._montar_requisicao(url, token)
        try:
            with urlopen(requisicao, timeout=10) as resposta:
                corpo = resposta.read().decode("utf-8")
        except (HTTPError, URLError) as erro:
            raise RuntimeError(erro_mensagem) from erro
        return json.loads(corpo)

    def _buscar_formulario(self, token: str, formulario_id: str) -> dict:
        url = f"https://forms.googleapis.com/v1/forms/{formulario_id}"
        return self._buscar_json(url, token, "Falha ao buscar formulario no Google Forms")

    def _buscar_respostas(self, token: str, formulario_id: str) -> list[dict]:
        url = f"https://forms.googleapis.com/v1/forms/{formulario_id}/responses"
        dados = self._buscar_json(url, token, "Falha ao buscar respostas no Google Forms")
        return dados.get("responses", [])

    def _mapear_perguntas(self, formulario: dict) -> dict[str, str]:
        mapa: dict[str, str] = {}
        for item in formulario.get("items", []):
            pergunta = item.get("questionItem", {}).get("question", {})
            pergunta_id = pergunta.get("questionId")
            if pergunta_id:
                mapa[pergunta_id] = item.get("title", "")
        return mapa

    def _localizar_id_pergunta(self, mapa: dict[str, str], titulo: str) -> str | None:
        titulo_normalizado = titulo.strip().lower()
        for pergunta_id, nome in mapa.items():
            if nome.strip().lower() == titulo_normalizado:
                return pergunta_id
        return None

    def _extrair_texto_resposta(self, respostas: dict, pergunta_id: str | None) -> str | None:
        if not pergunta_id:
            return None
        resposta = respostas.get(pergunta_id, {})
        textos = resposta.get("textAnswers", {}).get("answers", [])
        if textos:
            return textos[0].get("value")
        return None

    def _buscar_evento(self, db: Session, evento_id: int) -> Evento:
        evento = db.query(Evento).filter(Evento.evento_id == evento_id).first()
        if not evento:
            raise ValueError("Evento nao encontrado")
        return evento

    def _salvar_voluntario(
        self,
        db: Session,
        nome: str,
        email: str,
        resposta_id: str,
    ) -> Voluntario:
        voluntario = db.query(Voluntario).filter(Voluntario.email == email).first()
        if voluntario:
            voluntario.nome = nome
            voluntario.resposta_id_formulario = resposta_id
            db.add(voluntario)
            return voluntario
        voluntario = Voluntario(
            nome=nome,
            email=email,
            resposta_id_formulario=resposta_id,
        )
        db.add(voluntario)
        db.flush()
        return voluntario

    def _garantir_trabalho(
        self,
        db: Session,
        voluntario_id: int,
        evento_id: int,
    ) -> Trabalha:
        trabalho = (
            db.query(Trabalha)
            .filter(
                Trabalha.voluntario_id == voluntario_id,
                Trabalha.evento_id == evento_id,
            )
            .first()
        )
        if trabalho:
            return trabalho
        trabalho = Trabalha(
            voluntario_id=voluntario_id,
            evento_id=evento_id,
            status=STATUS_PENDENTE,
        )
        db.add(trabalho)
        return trabalho

    def _montar_inscricao(
        self,
        contexto: dict,
        resposta: dict,
    ) -> RespostaInscricaoFormulario | None:
        resposta_id = resposta.get("responseId", "")
        respostas_campos = resposta.get("answers", {})
        nome = self._extrair_texto_resposta(respostas_campos, contexto["id_nome"])
        email = self._extrair_texto_resposta(respostas_campos, contexto["id_email"])
        if not nome or not email or not resposta_id:
            return None
        voluntario = self._salvar_voluntario(contexto["db"], nome, email, resposta_id)
        trabalho = self._garantir_trabalho(
            contexto["db"],
            voluntario.voluntario_id,
            contexto["evento"].evento_id,
        )
        return RespostaInscricaoFormulario(
            evento_id=contexto["evento"].evento_id,
            voluntario_id=voluntario.voluntario_id,
            nome=voluntario.nome,
            email=voluntario.email,
            status=trabalho.status,
            resposta_id=resposta_id,
            link_resposta=self._montar_link_resposta(
                contexto["formulario_id"],
                resposta_id,
            ),
        )

    def listar_inscricoes(
        self,
        db: Session,
        evento_id: int,
    ) -> list[RespostaInscricaoFormulario]:
        token = extrair_token_bearer(self.token_acesso)
        if not token:
            raise RuntimeError("Token de acesso ausente")
        evento = self._buscar_evento(db, evento_id)
        if not evento.formulario_link:
            raise ValueError("Evento sem formulario configurado")

        formulario_id = self._definir_formulario_id(evento.formulario_link)

        formulario = self._buscar_formulario(token, formulario_id)
        respostas = self._buscar_respostas(token, formulario_id)
        mapa_perguntas = self._mapear_perguntas(formulario)
        id_nome = self._localizar_id_pergunta(mapa_perguntas, "Nome")
        id_email = self._localizar_id_pergunta(mapa_perguntas, "Email")

        contexto = {
            "db": db,
            "evento": evento,
            "formulario_id": formulario_id,
            "id_nome": id_nome,
            "id_email": id_email,
        }

        lista: list[RespostaInscricaoFormulario] = []
        for resposta in respostas:
            inscricao = self._montar_inscricao(contexto, resposta)
            if inscricao:
                lista.append(inscricao)
        db.commit()
        return lista
