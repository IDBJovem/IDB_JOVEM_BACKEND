def test_read_root(client):
    """
    Testa se a rota inicial responde com status 200.
    """
    response = client.get("/")
    assert response.status_code == 200