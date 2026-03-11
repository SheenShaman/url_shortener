## Cервис сокращения ссылок на FastAPI
Небольшой сервис для сокращения ссылок с HTTP API.
Проект реализует базовую функциональность сервиса сокращения ссылок с минимальным и прозрачным стеком.

### Возможности:
- Создание короткой ссылки
- Редирект по короткому коду
- Хранение данных в SQLite
- Тесты на pytest
- Логирование

### Технологии

- Python 3.12
- FastAPI
- SQLite
- pytest
- docker-compose


## Установка и запуск
- git clone https://github.com/SheenShaman/boto-education.git
- cd boto-education
- python -m venv .venv
- source .venv/bin/activate
- pip install poetry
- poetry install
- uvicorn app.main:app --reload
- pytest (для тестирования)

## Запуск через Docker
- docker compose up --build


## Идеи для развития
- Проверка уникальности короткого кода
- Валидация URL (схема, домен, длина)
- Поддержка PostgreSQL
- Асинхронная работа с БД

## Плюсы проекта
- Простая архитектура
- Использование типизации
- Логирование

## Минусы проект
- Синхронная работа с БД
- Отсутствие сервисного слоя
- Требуется замена БД