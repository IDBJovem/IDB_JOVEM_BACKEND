# Coloque aqui funções utilitarias

def extrair_token_bearer(valor: str | None) -> str | None:
    if not valor:
        return None
    token = valor.strip()
    if token.lower().startswith("bearer "):
        return token[7:].strip()
    return token
