from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import RedirectResponse
from src.auth.service import ServicoAuth

router = APIRouter(prefix="/auth", tags=["Autenticação (OAuth2 Google)"])

@router.get("/login")
def iniciar_login(request: Request):
    """
    Chame esta rota no navegador para iniciar o login do Admin.
    Ela redirecionará você direto para o Google.
    """
    servico = ServicoAuth()
    url_google, estado, verificador_codigo = servico.gerar_url_login()
    request.session["google_estado"] = estado
    request.session["google_verificador_codigo"] = verificador_codigo
    return RedirectResponse(url=url_google)


@router.get("/callback")
def callback_google(request: Request, codigo: str = Query(..., alias="code")):
    """
    O Google redireciona para cá automaticamente enviando o '?code=...'
    """
    estado = request.session.get("google_estado")
    verificador_codigo = request.session.get("google_verificador_codigo")
    if not estado or not verificador_codigo:
        raise HTTPException(status_code=400, detail="Sessao OAuth expirada. Refaça o login.")

    repositorio = ServicoAuth()
    tokens_google = repositorio.trocar_codigo_por_tokens(codigo, estado, verificador_codigo)

    request.session.pop("google_estado", None)
    request.session.pop("google_verificador_codigo", None)

    # IMPORTANTE: No futuro vai salvar o 'refresh_token' num banco de dados.
    # Por enquanto, vamos printar no terminal.
    print("\n" + "="*40)
    print("SUCESSO! SEU REFRESH TOKEN É:")
    print(tokens_google.get("refresh_token"))
    print("="*40 + "\n")

    return {
        "mensagem": "Admin autenticado com sucesso no Google!",
        "instrucoes": "Copie o refresh_token do terminal/tela para usarmos nas APIs reais.",
        "dados": tokens_google
    }
