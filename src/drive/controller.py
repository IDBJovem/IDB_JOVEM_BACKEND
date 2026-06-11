from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import StreamingResponse

from src.drive.service import ServicoDrive
from src.drive.schema import RespostaDrive
from src.security import verificar_roles

router = APIRouter(prefix="/galeria", tags=["Galeria do Google Drive"])

router_imagem = APIRouter(prefix="/drive", tags=["Imagens do Google Drive"])


@router_imagem.get("/imagem/{file_id}")
def proxy_imagem(file_id: str):
    """
    Proxy publico de imagens do Google Drive. Baixa o arquivo usando as
    credenciais do servidor e devolve os bytes com o Content-Type correto e
    cache de 24h, evitando o hotlink direto ao Drive (que falha em rajadas).
    """
    servico = ServicoDrive()

    try:
        content_type, conteudo = servico.baixar_imagem(file_id)

    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro)) from erro

    except RuntimeError as erro:
        raise HTTPException(status_code=502, detail=str(erro)) from erro

    return StreamingResponse(
        conteudo,
        media_type=content_type,
        headers={"Cache-Control": "public, max-age=86400"},
    )

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
