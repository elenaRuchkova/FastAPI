import pytest
import pytest_asyncio
from main import app
import httpx


@pytest_asynco.fixture(scope="function")  # определяем для функции
async def async_client(app): # чтобы не стартовать вручную
    async with httpx.AsyncClient(app=app, base_url="http://127.0.0.1") as test_client:
        yield test_client

def test_create_book(async_client):
    data = {"title": "Clean Code",
  "author": "Robert Martin",
  "year": 2010,
  "count_pages": 300
    }
   response = async_client.post("/api/v1/books", json=data)
   assert response.status_code == 200