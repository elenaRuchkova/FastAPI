import pytest
#from starlette import status
from fastapi import status
from sqlalchemy import select
from src.models.all_models import Seller


result = {
    "sellers": [
        {"first_name": "fdhgdh", "last_name": "jdhdj", "mail": "gjhg@ma.ru"},
        {"first_name": "fdhgdfgfrh", "last_name": "jrrgdhdj", "mail": "gjhg@ma.ru"},
    ]
}


# Тест на ручку создающую продавца
@pytest.mark.asyncio
async def test_create_seller(async_client):
    data = {"first_name": "Devid", "last_name": "Oligvi",
        "mail": "do@mail.ru", "password": "GF$ghj98", "books": [] }
    response = await async_client.post("/api/v1/sellers/", json=data)

    assert response.status_code == status.HTTP_200_OK #status.HTTP_201_CREATED

    result_data = response.json()

    assert result_data == {
        "id": result_data["id"],
        "first_name": "Devid",
        "last_name": "Oligvi",
        "mail": "do@mail.ru",        
        "books": [] 
    }


# Тест на ручку получения списка продавцов
#pytest.mark.parametrize("result", [result])  # добавляем параметры для теста(мб несколько)
@pytest.mark.asyncio
async def test_get_sellers(db_session, async_client): # ,result    если используем параметры
    # Создаем продавцов вручную, а не через ручку
    seller = Seller(first_name="Eugeny", last_name="Onegin", mail="eo@pu.ru", password= "GF$ghj98", books=[])
    seller_2 = Seller(first_name="Mihail", last_name="Lermontov", mail="mu@pi.ru", password= "GF$ghj98", books=[])
    # добавляем в базу
    db_session.add_all([seller, seller_2])
    await db_session.flush()
    # вызываем из БД
    response = await async_client.get("/api/v1/sellers/")
    # проверяем статус код
    assert response.status_code == status.HTTP_200_OK
    # проверяем длину(знаем что 2 записи)
    assert len(response.json()["sellers"]) == 2  # Опасный паттерн! Если в БД есть данные, то тест упадет

    # Проверяем интерфейс ответа, (на который у нас есть контракт).
    assert response.json() == {  # == result, если используем параметры
        "sellers": [
            {"id": seller.id, "first_name": "Eugeny", "last_name": "Onegin", "mail": "eo@pu.ru"},
            {"id": seller_2.id, "first_name": "Mihail", "last_name": "Lermontov", "mail": "mu@pi.ru"},
        ]
    }


# # Тест на ручку получения одного продавца
# @pytest.mark.asyncio
# async def test_get_single_seller(db_session, async_client):
#     # Создаем книги вручную
#     seller = Seller(first_name="Eugeny", last_name="Onegin", mail="eo@pu.ru")
#     seller_2 = Seller(first_name="Mihail", last_name="Lermontov", mail="mu@pi.ru")

#     db_session.add_all([seller, seller_2])
#     await db_session.flush()

#     response = await async_client.get(f"/api/v1/seller/{seller.id}")

#     assert response.status_code == status.HTTP_200_OK

#     # Проверяем интерфейс ответа, на который у нас есть контракт.
#     assert response.json() == {
#         "title": "Eugeny Onegin",
#         "author": "Pushkin",
#         "year": 2001,
#         "count_pages": 104,
#         "id": book.id,
#     }


# # Тест на ручку удаления продавца
# @pytest.mark.asyncio
# async def test_delete_book(db_session, async_client):
#     # Создаем книги вручную, а не через ручку, чтобы нам не попасться на ошибку которая
#     # может случиться в POST ручке
#     seller = Seller(author="Pushkin", title="Eugeny Onegin", year=2001, count_pages=104)

#     db_session.add(seller)
#     await db_session.flush()

#     response = await async_client.delete(f"/api/v1/books/{book.id}")

#     assert response.status_code == status.HTTP_204_NO_CONTENT
#     await db_session.flush()

#     all_books = await db_session.execute(select(Book))
#     res = all_books.scalars().all()
#     assert len(res) == 0


# # Тест на ручку обновления книги
# @pytest.mark.asyncio
# async def test_update_book(db_session, async_client):
#     # Создаем книги вручную, а не через ручку, чтобы нам не попасться на ошибку которая
#     # может случиться в POST ручке
#     book = Book(author="Pushkin", title="Eugeny Onegin", year=2001, count_pages=104)

#     db_session.add(book)
#     await db_session.flush()

#     response = await async_client.put(
#         f"/api/v1/books/{book.id}",
#         json={"title": "Mziri", "author": "Lermontov", "count_pages": 100, "year": 2007, "id": book.id},
#     )

#     assert response.status_code == status.HTTP_200_OK
#     await db_session.flush()

#     # Проверяем, что обновились все поля
#     res = await db_session.get(Book, book.id)
#     assert res.title == "Mziri"
#     assert res.author == "Lermontov"
#     assert res.count_pages == 100
#     assert res.year == 2007
#     assert res.id == book.id