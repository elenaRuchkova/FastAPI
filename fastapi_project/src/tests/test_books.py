# from unittest import TestCase
# import unittest

# Тестирование с помощью обычных функций и http-клиента
# def test_get_book():
#     response = requests.get("url")
#     assert response.status_code == 200, "Wrong code"  # asert = предупреждение
#     assert response.json() == {
#         "books": [
#             {"title": "Wrong Code", "author": "Robert Martin", "pages": 104, "year": 2007},
#         ]
#     }

# большой минус: приложение запускать вручную, отдельно от main, 
# много одинакового кода
# потом чистить базу данных от запросов
# на смену прошел Юниттест(встроен в Python)

# Пример написания теста с помощью Юниттеста 
# https://docs.python.org/3/library/unittest.html
# class TestBooks(TestCase):
#     def setUp(self):
#         # метод setUp выполняемый перед каждым тестом
#         # например, можно заполнить БД,
          # вызвать Book
#         pass

#     def tearDown(self):  
          # метод tearDown все удаляет 
#         pass

#     def test_get_book(self):
#         response = requests.get("url")
#         self.assertEqual(response.status_code, 200)  # система предупреждений
#         assert response.json() == {
#             "books": [
#                 {"title": "Wrong Code", "author": "Robert Martin", "pages": 104, "year": 2007},
#             ]
#         }

# из плюсов: используется в Jango,  Классы (но это не уникальная структура)
# из минусов: сложно задавать параметры теста, (в отличие PyTest)
# (например, не равно какому-то числу это отдельная функция)
# сложная система assert (предупреждений), на каждый случай свои правила

# if __name__ == '__main__':
#     unittest.main()