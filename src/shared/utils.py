def validar_datas(valor_inicio, valor_fim):
    """
    Valida datas ou horários.
    """

    if valor_inicio >= valor_fim:
        raise ValueError(
            "O valor final deve ser maior que o valor inicial."
        )

def validar_coordenadas(local_latitude, local_longitude):
    if not -90 <= local_latitude <= 90:
        raise ValueError("Latitude inválida.")

    if not -180 <= local_longitude <= 180:
        raise ValueError("Longitude inválida.")

def extrair_token_bearer(valor: str | None) -> str | None:
    if not valor:
        return None
    token = valor.strip()
    if token.lower().startswith("bearer "):
        return token[7:].strip()
    return token
