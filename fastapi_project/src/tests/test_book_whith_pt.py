# import pytest_asyncio  #poetry add pytest-asyncio --group dev
# from src.main import app
# import httpx  # стучится по ручкам, умеет и ассинхронно и синхронно


# @pytest_asynco.fixture(scope="function")  # определяем для функции
# async def async_client(app): # чтобы не стартовать вручную
#     async with httpx.AsyncClient(app=app, base_url="http://127.0.0.1") as test_client:
#         yield test_client

# def test_create_book(async_client):
#     data = {"title": "Clean Code",
#   "author": "Robert Martin",
#   "year": 2010,
#   "count_pages": 300
#     }
#    response = async_client.post("/api/v1/books", json=data)
#    assert response.status_code == 200
# запуск в командной строке: pytest tests (tests указание пакета)


import pytest
from fastapi import status
#from starlette import status
from sqlalchemy import select
#from src.models.all_models import Book
from src.models import all_models


result = {
    "books": [
        {"author": "fdhgdh", "title": "jdhdj", "year": 1997, "seller_id":1},
        {"author": "fdhgdfgfrh", "title": "jrrgdhdj", "year": 2001, "seller_id":1},
    ]
}

# Тест на ручку создающую книгу
@pytest.mark.asyncio
async def test_create_book(db_session, async_client):
    # seller = all_models.Seller(first_name="Eugeny", last_name="Onegin", mail="eo@pu.ru", password="gl#Jg67", books=[])
    # db_session.add(seller) 

    #await db_session.flush()

    # data_sell = {"first_name": "Devid", "last_name": "Oligvi",
    #     "mail": "do@mail.ru", "password": "GF$ghj98", "books": [] }
    
    # sell_response = await async_client.post("/api/v1/sellers/", json=data_sell)

    # seller = sell_response.json()

    data = {"title": "Wrong Code", "author": "Robert Martin", "pages": 104, "year": 2007, "seller_id": seller["id"]}
    
    response = await async_client.post("/api/v1/books/", json=data)

    assert response.status_code == 422 #status.HTTP_201_CREATED  # 422  HTTP_201_CREATED

    result_data = response.json()
    
    assert result_data == {
        "id": 1,
        "title": "Wrong Code",
        "author": "Robert Martin",
        "count_pages": 104,
        "year": 2007,
        "seller_id": seller["id"]
    }


# Тест на ручку получения списка книг
@pytest.mark.asyncio
async def test_get_books(db_session, async_client):
    # Создаем книги вручную, а не через ручку, чтобы нам не попасться на ошибку которая
    # может случиться в POST ручке
    seller = all_models.Seller(first_name="Eugeny", last_name="Onegin", mail="eo@pu.ru", password="gl#Jg67", books=[])
    book = all_models.Book(author="Pushkin", title="Eugeny Onegin", year=2001, count_pages=104, seller_id=seller.id)
    book_2 = all_models.Book(author="Lermontov", title="Mziri", year=1997, count_pages=104, seller_id=seller.id)

    db_session.add_all([book, book_2])
    await db_session.flush()

    response = await async_client.get("/api/v1/books/")

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()["books"]) == 2  # Опасный паттерн! Если в БД есть данные, то тест упадет

    # Проверяем интерфейс ответа, на который у нас есть контракт.
    assert response.json() == {
        "books": [
            {"title": "Eugeny Onegin", "author": "Pushkin", "year": 2001, "id": book.id, "count_pages": 104, "seller_id":seller.id},
            {"title": "Mziri", "author": "Lermontov", "year": 1997, "id": book_2.id, "count_pages": 104, "seller_id":seller.id}
        ]
    }


# # Тест на ручку получения одной книги
# @pytest.mark.asyncio
# async def test_get_single_book(db_session, async_client):
#     # Создаем книги вручную, а не через ручку, чтобы нам не попасться на ошибку которая
#     # может случиться в POST ручке
#     book = all_models.Book(author="Pushkin", title="Eugeny Onegin", year=2001, count_pages=104)
#     book_2 = all_models.Book(author="Lermontov", title="Mziri", year=1997, count_pages=104)

#     db_session.add_all([book, book_2])
#     await db_session.flush()

#     response = await async_client.get(f"/api/v1/books/{book.id}")

#     assert response.status_code == status.HTTP_200_OK

#     # Проверяем интерфейс ответа, на который у нас есть контракт.
#     assert response.json() == {
#         "title": "Eugeny Onegin",
#         "author": "Pushkin",
#         "year": 2001,
#         "count_pages": 104,
#         "id": book.id,
#     }


# # Тест на ручку удаления книги
# @pytest.mark.asyncio
# async def test_delete_book(db_session, async_client):
#     # Создаем книги вручную, а не через ручку, чтобы нам не попасться на ошибку которая
#     # может случиться в POST ручке
#     book = all_models.Book(author="Pushkin", title="Eugeny Onegin", year=2001, count_pages=104)

#     db_session.add(book)
#     await db_session.flush()

#     response = await async_client.delete(f"/api/v1/books/{book.id}")

#     assert response.status_code == status.HTTP_204_NO_CONTENT
#     await db_session.flush()

#     all_books = await db_session.execute(select(all_models.Book))
#     res = all_books.scalars().all()
#     assert len(res) == 0


# # Тест на ручку обновления книги
# @pytest.mark.asyncio
# async def test_update_book(db_session, async_client):
#     # Создаем книги вручную, а не через ручку, чтобы нам не попасться на ошибку которая
#     # может случиться в POST ручке
#     book = all_models.Book(author="Pushkin", title="Eugeny Onegin", year=2001, count_pages=104)

#     db_session.add(book)
#     await db_session.flush()

#     response = await async_client.put(
#         f"/api/v1/books/{book.id}",
#         json={"title": "Mziri", "author": "Lermontov", "count_pages": 100, "year": 2007, "id": book.id},
#     )

#     assert response.status_code == status.HTTP_200_OK
#     await db_session.flush()

#     # Проверяем, что обновились все поля
#     res = await db_session.get(all_models.Book, book.id)
#     assert res.title == "Mziri"
#     assert res.author == "Lermontov"
#     assert res.count_pages == 100
#     assert res.year == 2007
#     assert res.id == book.id