# fastapi_menu_restaurant

# Тестовое задание 

Написать проект на FastAPI с использованием PostgreSQL в качестве БД. В проекте следует реализовать REST API по работе с меню ресторана, все CRUD операции. Для проверки задания, к презентаций будет приложена Postman коллекция с тестами. Задание выполнено, если все тесты проходят успешно.
Даны 3 сущности: Меню, Подменю, Блюдо.

Зависимости:
- У меню есть подменю, которые к ней привязаны.
- У подменю есть блюда.

Условия:
- Блюдо не может быть привязано напрямую к меню, минуя подменю.
- Блюдо не может находиться в 2-х подменю одновременно.
- Подменю не может находиться в 2-х меню одновременно.
- Если удалить меню, должны удалиться все подменю и блюда этого меню.
- Если удалить подменю, должны удалиться все блюда этого подменю.
- Цены блюд выводить с округлением до 2 знаков после запятой.
- Во время выдачи списка меню, для каждого меню добавлять кол-во подменю и блюд в этом меню.
- Во время выдачи списка подменю, для каждого подменю добавлять кол-во блюд в этом подменю.


Запуск
1. клонировать проект https://github.com/ip-Wan-Kenobi/fastapi_menu_restaurant.git
2. Установить виртуальное окружение и зависимости
3. В корневой папке создать файл .env В нем указать 
```angular2html
DATABASE_URL=postgresql+asyncpg://user:password@postgresserver/db
```
4. Создать таблицы в базе данных (в консоле пишем)
```
 alembic revision --autogenerate -m "menu"
 alembic upgrade head
```
