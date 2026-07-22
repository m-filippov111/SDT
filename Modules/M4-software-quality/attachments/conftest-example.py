# Пример фикстур pytest для FastAPI-приложения
#
# Скопируйте идеи в tests/conftest.py командного проекта.
# Адаптируйте импорты под вашу структуру (src.api.main и т.п.).

import pytest
from fastapi.testclient import TestClient

# from src.api.main import app


@pytest.fixture
def client():
    """HTTP-клиент для интеграционных тестов API."""
    # return TestClient(app)
    raise NotImplementedError("Подключите FastAPI app проекта")


@pytest.fixture
def sample_payload():
    """Минимально валидное тело запроса предметной области."""
    return {
        "name": "example",
        # дополните полями вашего API
    }


# Пример использования в tests/test_api_example.py:
#
# def test_create_ok(client, sample_payload):
#     response = client.post("/items/", json=sample_payload)
#     assert response.status_code == 201
#     assert "id" in response.json()
#
# def test_create_invalid(client):
#     response = client.post("/items/", json={})
#     assert response.status_code == 422
