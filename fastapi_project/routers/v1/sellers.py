from typing import Annotated
from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from fastapi import Response, status, APIRouter, Depends

from icecream import ic
from schemas.sellers import IncomingSeller, ReturnedAllSellers, ReturnedSeller
from configurations.database import get_async_session

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.models import Seller



# чтобы не писать в app ("/books/", response_model=ReturnedBook)
# количество тегов: количество дублированных ручек , "v1", "v2"
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

# Ручка, возвращающая всеx продавцов #TODO
@sellers_router.get("/")# ,, response_model=list[ReturnedSeller] response_model=ReturnedAllSellers
async def get_all_sellers(session: DBSession):
    
    query = select(Seller)
    res = await session.execute(query)
    sellers = res.scalars().all()
 
    return {"sellers":[Seller(id=seller.id, 
                   first_name=seller.first_name, 
                   last_name=seller.last_name,
                   mail=seller.mail) for seller in sellers]}


# Ручка для получения продавца по его ИД
@sellers_router.get("/{seller_id}", response_model=ReturnedSeller)  
async def get_seller(seller_id: int, session: DBSession):
    query = (select(Seller).
              options(joinedload(Seller.books)).
              filter_by(id=seller_id))

    res = await session.execute(query)
    seller = res.scalars().first()
    
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")         
    
    return {"id": seller.id, 
            "first_name": seller.first_name,
            "last_name": seller.last_name, 
            "mail": seller.mail,      
            "books": [{"id": book.id, 
                   "title": book.title,
                   "author": book.author,
                   "count_pages":book.count_pages,
                   "year":book.year
                   } for book in seller.books]
    }


# Ручка для удаления записи о продавце
@sellers_router.delete("/{seller_id}")
async def delete_seller(seller_id:int, session: DBSession):
    query = (select(Seller).
              options(joinedload(Seller.books)).
              filter_by(id=seller_id))

    res = await session.execute(query)
    deleted_seller = res.scalars().first()    
    
    if deleted_seller:
        await session.delete(deleted_seller)

        # Удаляем все книги продавца        
        for book in deleted_seller.books:
            await session.delete(book)
        return {"message": f"Seller with id {seller_id} and associated books have been deleted successfully"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)  # Response может вернуть текст и метаданные.


# Ручка для обновления продавца по его ИД
@sellers_router.put("/{seller_id}")
async def update_seller(seller_id: int, seller_data: ReturnedSeller, session: DBSession): # 
    # # Получаем продавца по ID
    updated_seller = await session.get(Seller, seller_id)
    # query = select(Seller).filter_by(id=seller_id)
    # res = await session.execute(query)
    # updated_seller = res.scalars().first()
    
    if not updated_seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    
    # Обновляем все поля, кроме пароля
    updated_seller.first_name = seller_data.first_name
    updated_seller.last_name = seller_data.last_name
    updated_seller.mail = seller_data.mail
    
    # Сохраняем изменения в базе данных
    session.add(updated_seller)
    await session.flush()

    return {"message": f"Seller with id {seller_id} updated successfully"}

            
        

