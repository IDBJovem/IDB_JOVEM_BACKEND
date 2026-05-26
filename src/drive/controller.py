from fastapi import APIRouter, HTTPException, Query, Depends

from src.drive.service import ServicoDrive
from src.drive.schema import RespostaDrive
from src.security import verificar_roles

router = APIRouter(prefix="/galeria", tags=["Galeria do Google Drive"])

@router.get("/fotos", response_model=list[RespostaDrive])
def listar_fotos(
    pasta: str = Query(..., min_length=1),
    usuario_logado: dict = Depends(verificar_roles(["admin", "superadmin"])),
):
    """
    Lista as fotos armazenadas no Google Drive por nome de pasta.
    Autenticação com o Google feita de forma automatizada pelo servidor.
    """
    servico = ServicoDrive()

    try:
        return servico.listar_fotos(pasta)

    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro)) from erro

    except RuntimeError as erro:
        raise HTTPException(status_code=502, detail=str(erro)) from erro
