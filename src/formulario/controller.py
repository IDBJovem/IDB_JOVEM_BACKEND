from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from src.database import obter_banco
from src.formulario.repository import RepositorioFormulario
from src.formulario.service import ServicoFormulario
from src.formulario.schema import RespostaInscricaoFormulario


router = APIRouter(prefix="/formulario", tags=["Formulario"])


def get_servico(
    google_autorizacao: str = Header(None, alias="X-Google-Authorization"),
):
    if not google_autorizacao:
        raise HTTPException(status_code=401, detail="Token de acesso ausente")

    repositorio = RepositorioFormulario(token_acesso=google_autorizacao)
    return ServicoFormulario(repositorio)


@router.get(
    "/eventos/{evento_id}/inscricoes",
    response_model=list[RespostaInscricaoFormulario],
)
def listar_inscricoes(
    evento_id: int,
    db: Session = Depends(obter_banco),
    servico: ServicoFormulario = Depends(get_servico),
):
    try:
        return servico.listar_inscricoes(db, evento_id)

    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro)) from erro

    except RuntimeError as erro:
        raise HTTPException(status_code=502, detail=str(erro)) from erro
