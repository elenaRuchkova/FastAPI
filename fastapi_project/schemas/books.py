from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError  # кастомная ошибка, которую задаем сами

__all__ = ["IncomingBook", "ReturnedBook", "ReturnedAllBooks"]

# Базовый класс "Книги", содержащий поля, которые есть во всех классах-наследниках.
class BaseBook(BaseModel):
    title: str
    author: str
    year: int #= 2024 # необязательный параметр
    seller_id:int
    

# Класс для валидации входящих данных. Не содержит id так как его присваивает БД.
class IncomingBook(BaseBook):
    year: int = 2024  # Пример присваивания дефолтного значения
    count_pages: int = Field(
        alias="pages",
        default=300,
    )  # Пример использования тонкой настройки полей. Передачи в них метаинформации.

    @field_validator("year")  # валидатор поля, from pydantic. внутри IncomingBook 
    #в скобках название поля которое проверяет
    # проверяет что дата не слишком древняя
    @staticmethod # питонячий декоратор classmethod/staticmethod
    def validate_year(val: int):
        if val < 1900:
            raise PydanticCustomError("Validation error", "Year is wrong!")
        return val

# Класс, валидирующий исходящие данные. Он уже содержит id
class ReturnedBook(BaseBook):
    id: int
    count_pages: int

# Класс для возврата массива объектов "Книга"
class ReturnedAllBooks(BaseModel):
    books: list[ReturnedBook]