from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from .base import BaseModel


class Book(BaseModel):
        __tablename__= "books_table"

        id: Mapped[int] = mapped_column(primary_key=True)
        title: Mapped[str] = mapped_column(String(50), nullable=False) # можно ничего не указывать
        author: Mapped[str] = mapped_column(String(100), nullable=False) # поле не мб = 0
        year: Mapped[int]        
        count_pages: Mapped[int]
        seller_id: Mapped[int] = mapped_column(ForeignKey("sellers_table.id"))
        seller: Mapped["Seller"]= relationship(back_populates="books")
        

class Seller(BaseModel):
        __tablename__= "sellers_table"

        id: Mapped[int] = mapped_column(primary_key=True)
        first_name: Mapped[str] = mapped_column(String(100), nullable=False) # можно ничего не указывать
        last_name: Mapped[str] = mapped_column(String(100), nullable=False) # поле не мб = 0
        mail: Mapped[str] = mapped_column(String(100), nullable=False)
        password: Mapped[str] = mapped_column(String(100), nullable=False)
        books: Mapped[list["Book"]] = relationship(back_populates="seller") # 
