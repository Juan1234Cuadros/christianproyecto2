from app import app


def test_root_status_code():
    """
    Simula una petición GET a la ruta principal ('/') de la API,
    ANTES del despliegue, y valida que el código de estado HTTP
    devuelto sea estrictamente 200 OK.
    """
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
