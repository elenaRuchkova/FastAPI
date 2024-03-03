from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError  # кастомная ошибка, которую задаем сами
import re

#__all__ = ["IncomingSeller", "ReturnedSeller", "ReturnedAllSellers"] #TODO

# Базовый класс "Sellers", содержащий поля, которые есть во всех классах-наследниках.
class BaseSeller(BaseModel):
    first_name: str
    last_name: str = Field(None, description="Optional last name") # необязательный параметр #TODO
    mail: str = Field(description="Email address", default='example@mail.com')
    #password: str = '###'
    books: list = Field([], description="List of books")   

# Класс для валидации входящих данных. Не содержит id так как его присваивает БД.
class IncomingSeller(BaseSeller):
    mail: str  
    password: str
    
    # проверяет e-mail введен корректно
    @field_validator("mail")  

    @staticmethod 
    def validate_mail(val: str):  #TODO использовать спец библиотеку       
        pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
   
        if not re.match(pat,val): 
            raise PydanticCustomError("Validation error","e-mail is wrong!") 
        return val
            
    # проверяет password введен корректно
    @field_validator("password")

    @staticmethod
    def validate_password(val: str):
        SpecialSym =['$', '@', '#', '%']

        if len(val) < 6 or len(val) > 20:
            raise ValueError("The password must be between 6 and 20 characters long")
        
        if not any(char.isupper() for char in val) or not any(char.islower() for char in val):
           raise ValueError('Password should have at least one uppercase or one lowercase letter')
        
        if not any(char.isdigit() for char in val):
           raise ValueError('Password should have at least one numeral')
        
        if not any(char in SpecialSym for char in val):
           raise ValueError(f'Password should have at least one of the symbols {SpecialSym}')
     
        return val  
    
# Класс, валидирующий исходящие данные. Он уже содержит id
class ReturnedSeller(BaseSeller): #TODO
    id: int
    #books: list 

class UpdateSeller(BaseModel):
    first_name: str
    last_name: str
    mail: str

# Класс для возврата массива объектов "Продавцы"
class ReturnedAllSellers(BaseSeller): #TODO
    sellers: list[ReturnedSeller]
    #books: list



