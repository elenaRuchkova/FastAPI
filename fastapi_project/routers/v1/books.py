from typing import Annotated

from fastapi import Response, status, APIRouter, Depends
from fastapi.responses import ORJSONResponse
from icecream import ic
from schemas import IncomingBook, ReturnedAllBooks, ReturnedBook
from configurations.database import get_async_session

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.models import Book
# добавление файла __init__ в schemas позволило импортировать напрямую,
# без schemas.book

#from main import app тоже сработает


# чтобы не писать в app ("/books/", response_model=ReturnedBook)
# количество тегов: количество дублированных ручек , "v1", "v2"
books_router = APIRouter(tags=["books"],prefix="/books")   

# симулируем хранилище данных. Просто сохраняем объекты в память, в словаре.
#fake_storage ={}

DBSession = Annotated[AsyncSession, Depends(get_async_session)]

# Ручка для создания записи о книге в БД. Возвращает созданную книгу.
@books_router.post("/", response_model=ReturnedBook)  # Прописываем модель ответа)  # post - создаем
async def create_book(book: IncomingBook, session: DBSession):
    

    # это - бизнес логика. Обрабатываем данные, сохраняем, преобразуем и т.д.
    # TODO запись в БД
    new_book = Book(
        title=book.title,
        author=book.author,
        year=book.year,
        count_pages=book.count_pages,
        seller_id=book.seller_id
    )
    session.add(new_book)
    await session.flush()

    # return new_book  # Так можно просто вернуть объект
    return new_book # Возвращаем объект в формате Json с нужным нам статус-кодом, обработанный нужным сериализатором.


# Ручка, возвращающая все книги
@books_router.get("/", response_model=ReturnedAllBooks)
async def get_all_books(session: DBSession):
    # Хотим видеть формат:
    # books: [{"id": 1, "title": "Blabla", ...}, {"id": 2, ...}]
    query = select(Book)
    res = await session.execute(query)
    books = res.scalars().all()
    return {"books": books}  # для валидации создаем класс ReturnedAllBooks

# Ручка для получения книги по ее ИД
@books_router.get("/{book_id}", response_model=ReturnedBook)
async def get_book(book_id: int, session: DBSession):
    res = await session.get(Book, book_id)
    return res

# Ручка для удаления книги
@books_router.delete("/{book_id}")
async def delete_book(book_id:int, session: DBSession):
    deleted_book = await session.get(Book, book_id)
    # print("*****************", deleted_book)
    ic(deleted_book)  # Красивая и информативная замена для print. Полезна при отладке.
    if deleted_book:
        await session.delete(deleted_book)
    return Response(status_code=status.HTTP_204_NO_CONTENT)  # Response может вернуть текст и метаданные.

# Ручка для обновления данных о книге
@books_router.put("/{book_id}")
async def update_book(book_id: int, new_data: ReturnedBook, session: DBSession):
    # Оператор "морж", позволяющий одновременно и присвоить значение и проверить его.
    if updated_book := await session.get(Book, book_id):
        updated_book.author = new_data.author
        updated_book.title = new_data.title
        updated_book.year = new_data.year
        updated_book.count_pages = new_data.count_pages
        updated_book.seller_id = new_data.seller_id

        await session.flush()

        return updated_book

    return Response(status_code=status.HTTP_404_NOT_FOUND)