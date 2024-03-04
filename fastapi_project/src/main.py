from contextlib import asynccontextmanager

from fastapi import FastAPI 
from fastapi.responses import ORJSONResponse
from src.routers import v1_router
from src.configurations.database import global_init, create_db_and_tables, delete_db_and_tables  # связь с БД

# добавление файла __init__ в schemas позволило импортировать напрямую,
# без schemas.book
#from schemas import IncomingBook, ReturnedAllBooks, ReturnedBook

@asynccontextmanager
async def lifespan(app: FastAPI):  # Рекомендуется теперь вместо @app.on_event()
    # Запускается при старте приложения
    global_init()
    await create_db_and_tables()
    yield
    # Запускается при остановке приложения
    await delete_db_and_tables()

# Само приложение fastApi. именно оно запускается сервером и служит точкой входа
# в нем можно указать разные параметры для сваггера и для ручек (эндпоинтов).

# Само приложение fastApi. именно оно запускается сервером и служит точкой входа
# в нем можно указать разные параметры для сваггера и для ручек (эндпоинтов).
    

def create_application():
    return FastAPI(
        title="Book Library App",
        description="Учебное приложение для группы MTS Shad",
        version="0.0.1",
        responses={404: {"description": "Not Found!"}},
        default_response_class=ORJSONResponse,  # Подключаем быстрый сериализатор,
        lifespan=lifespan        
                  ) 


app = create_application()


def _configure():
    app.include_router(v1_router)

# # Просто пример ручки и того, как ее можно исключить из схемы сваггера ручка == endpoint
# @app.get("/", include_in_schema=False)   # get - получаем
# async def main():
#     return "Hello World!"

# @app.on_event("startup")
# async def startup_event():
#     global_init()
#     await create_db_and_tables()


_configure()