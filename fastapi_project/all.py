from pydantic import BaseModel, Field, field_validator
from pydantic import ValidationError
from typing import Optional

from pydantic_core import PydanticCustomError  # кастомная ошибка, которую задаем сами
import re

#__all__ = ["IncomingSeller", "ReturnedSeller", "ReturnedAllSeller"] #TODO

# Базовый класс "Sellers", содержащий поля, которые есть во всех классах-наследниках.
class BaseSeller(BaseModel):
    first_name: str
    last_name: Optional[str] # необязательный параметр #TODO
    mail: str = 'example@mail.com'
    #password: str = '###'
    books: list[ReturnedAllBooks]
   

# Класс для валидации входящих данных. Не содержит id так как его присваивает БД.
class IncomingSeller(BaseSeller):
    mail: str  # Пример присваивания дефолтного значения
    password: str
    books: list[ReturnedAllBooks]            
    
    
# Класс, валидирующий исходящие данные. Он уже содержит id
class ReturnedSeller(BaseSeller): #TODO
    id: int
    books: list[ReturnedAllBooks]


# Класс для возврата массива объектов "Книга"
class ReturnedAllSellers(BaseModel): #TODO
    sellers: list[ReturnedSeller]

# Базовый класс "Книги", содержащий поля, которые есть во всех классах-наследниках.
class BaseBook(BaseModel):
    title: str
    author: str
    year: int #= 2024 # необязательный параметр
    seller_id:int
    #seller

# Класс для валидации входящих данных. Не содержит id так как его присваивает БД.
class IncomingBook(BaseBook):
    year: int = 2024  # Пример присваивания дефолтного значения
    count_pages: int 

# Класс, валидирующий исходящие данные. Он уже содержит id
class ReturnedBook(BaseBook):
    id: int
    count_pages: int

# Класс для возврата массива объектов "Книга"
class ReturnedAllBooks(BaseModel):
    books: list[ReturnedBook]

class Book(BaseModel):
        __tablename__= "books_table"

        id: Mapped[int] = mapped_column(primary_key=True)
        title: Mapped[str] = mapped_column(String(50), nullable=False) # можно ничего не указывать
        author: Mapped[str] = mapped_column(String(100), nullable=False) # поле не мб = 0
        year: Mapped[int]        
        count_pages: Mapped[int]
        seller_id: Mapped[int] = mapped_column(ForeignKey("sellers_table.id"))
        seller: Mapped["Seller"]= relationship("Seller", back_populates="books")
        #seller_id: Mapped["Seller"] = relationship("Seller", back_populates="id") # 

class Seller(BaseModel):
        __tablename__= "sellers_table"

        id: Mapped[int] = mapped_column(primary_key=True)
        #id:Mapped[int]= relationship("Book", back_populates="seller_id")
        first_name: Mapped[str] = mapped_column(String(100), nullable=False) # можно ничего не указывать
        last_name: Mapped[str] = mapped_column(String(100), nullable=False) # поле не мб = 0
        mail: Mapped[str] = mapped_column(String(100), nullable=False)
        password: Mapped[str] = mapped_column(String(100), nullable=False)
        books: Mapped[list["Book"]] = relationship("Book", back_populates="seller") #"Book", back_populates="seller_id"

sellers_router = APIRouter(tags=["sellers"],prefix="/sellers")   

DBSession = Annotated[AsyncSession, Depends(get_async_session)]


# Ручка для создания записи о продавце в БД. Возвращает инфо о продавце.
@sellers_router.post("/", response_model=ReturnedSeller)  # Прописываем модель ответа)  # post - создаем
async def create_seller(seller: IncomingSeller, session: DBSession):
    

    # это - бизнес логика. Обрабатываем данные, сохраняем, преобразуем и т.д.
    # TODO запись в БД
    new_seller = Seller(
        first_name=seller.first_name,
        last_name=seller.last_name,
        mail=seller.mail,
        password=seller.password,
        books=seller.books
    )
    session.add(new_seller)
    await session.flush()
    
    return new_seller
    

# Ручка, возвращающая всеx продавцов
@sellers_router.get("/", response_model=ReturnedAllSellers)
async def get_all_sellers(session: DBSession):
    # Хотим видеть формат:
    # books: [{"id": 1, "title": "Blabla", ...}, {"id": 2, ...}]
    query = select(Seller)
    res = await session.execute(query)
    sellers = res.scalars().all()
    return {"sellers": sellers}  # для валидации создаем класс ReturnedAllBooks

# Ручка для получения продавца по его ИД
@sellers_router.get("/{seller_id}", response_model=ReturnedSeller)
async def get_seller(seller_id: int, session: DBSession):
    res = await session.get(Seller, seller_id)
    return res

        