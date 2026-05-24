from fastapi import APIRouter, HTTPException, Query, Header, Depends

from src.drive.service import ServicoDrive
from src.drive.schema import RespostaDrive
from src.security import verificar_roles

router = APIRouter(prefix="/galeria", tags=["Galeria do Google Drive"])

@router.get("/fotos", response_model=list[RespostaDrive])
def listar_fotos(
    pasta: str = Query(..., min_length=1),
    google_autorizacao: str = Header(None, alias="X-Google-Authorization"),
    usuario_logado: dict = Depends(verificar_roles(["admin", "superadmin"])),
):
    """
    Lista as fotos armazenadas no Google Drive por nome de pasta.
    """

    if not google_autorizacao:
        raise HTTPException(
            status_code=401,
            detail="Token Google ausente"
        )

    servico = ServicoDrive(token_acesso=google_autorizacao)

    try:
        return servico.listar_fotos(pasta)

    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro)) from erro

    except RuntimeError as erro:
        raise HTTPException(status_code=502, detail=str(erro)) from erro