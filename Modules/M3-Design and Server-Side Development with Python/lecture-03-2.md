**Лекция 3.2: Серверное программирование на Python с FastAPI**

**1\. Введение в FastAPI**

**1.1. Что такое FastAPI?**

**FastAPI** — это современный, высокопроизводительный веб-фреймворк для построения API на Python, основанный на стандартных подсказках типов (type hints). Он был создан Себастьяном Рамиресом и с момента своего появления завоевал огромную популярность благодаря своей скорости, простоте и надёжности.

**Ключевые особенности FastAPI**:

| Характеристика | Описание |
| --- | --- |
| **Высокая производительность** | Один из самых быстрых Python-фреймворков, сравнимый с NodeJS и Go (благодаря Starlette и Pydantic) |
| **Быстрая разработка** | Увеличивает скорость разработки функций на 200–300% |
| **Меньше ошибок** | Сокращает количество ошибок разработчика примерно на 40% |
| **Интуитивность** | Отличная поддержка в редакторах кода, автодополнение везде, меньше времени на отладку |
| **Краткость** | Минимизация дублирования кода |
| **Надёжность** | Готовый к production код с автоматической интерактивной документацией |
| **Стандартизация** | Основан на открытых стандартах API: OpenAPI (Swagger) и JSON Schema |

FastAPI стоит на плечах гигантов: **Starlette** для веб-частей и **Pydantic** для работы с данными.

**1.2. Почему FastAPI?**

В отличие от других Python-фреймворков, FastAPI предлагает уникальное сочетание:

1.  Автоматическая валидация данных — благодаря интеграции с Pydantic
2.  Автоматическая документация — Swagger UI и ReDoc генерируются автоматически
3.  Асинхронность из коробки — поддержка async/await
4.  Встроенная инъекция зависимостей — через механизм Depends()

**2\. Первое приложение на FastAPI**

**2.1. Установка**

bash

pip install "fastapi\[standard\]"

Кавычки необходимы для корректной установки в некоторых терминалах.

**2.2. Создание приложения**

from fastapi import FastAPI

app = FastAPI()

@app.get("/")

async def read_root():

return {"Hello": "World"}

@app.get("/items/{item_id}")

async def read_item(item_id: int, q: str | None = None):

return {"item_id": item_id, "q": q}

Обратите внимание: **FastAPI понимает Python-аннотации типов** и автоматически преобразует item_id из строки в целое число.

**2.3. Запуск приложения**

bash

fastapi dev main.py

По умолчанию сервер запускается на http://127.0.0.1:8000 с автоматической перезагрузкой при изменениях кода.

Автоматическая интерактивная документация доступна по адресу /docs (Swagger UI).

**3\. Проектирование REST API**

**3.1. Основы REST**

**REST** (Representational State Transfer) — архитектурный стиль для построения распределённых систем. Ключевые принципы REST API:

| Принцип | Описание |
| --- | --- |
| **Ресурсы** | Всё, что может быть идентифицировано (пользователи, товары, заказы) |
| **HTTP-методы** | GET (чтение), POST (создание), PUT (замена), PATCH (частичное обновление), DELETE (удаление) |
| **Статус-коды** | 200 (OK), 201 (Created), 400 (Bad Request), 404 (Not Found), 422 (Unprocessable Entity) |
| **Без состояния** | Каждый запрос содержит всю необходимую информацию |

**3.2. Параметры запроса**

FastAPI поддерживает все типы параметров HTTP-запросов:

**Параметры пути (Path Parameters)**

Параметры, встроенные в URL:

@app.get("/users/{user_id}")

async def get_user(user_id: int):

return {"user_id": user_id}

FastAPI автоматически парсит и валидирует тип параметра.

**Параметры запроса (Query Parameters)**

Параметры после ? в URL:

@app.get("/items/")

async def read_items(skip: int = 0, limit: int = 100, q: str | None = None):

return {"skip": skip, "limit": limit, "q": q}

**Тело запроса (Request Body)**

Данные, передаваемые в теле POST/PUT/PATCH запросов — обычно в формате JSON.

**4\. Валидация данных с Pydantic**

**4.1. Что такое Pydantic?**

**Pydantic** — библиотека для валидации данных с использованием Python-аннотаций типов. FastAPI использует её для автоматической проверки входящих и исходящих данных.

Вместо ручного извлечения и валидации каждого поля, мы определяем **схему** — класс, наследующий от BaseModel:

from pydantic import BaseModel

class Post(BaseModel):

title: str

content: str

published: bool = True

rating: int | None = None

**4.2. Использование Pydantic в эндпоинтах**

from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):

title: str

content: str

published: bool = True

rating: int | None = None

@app.post("/posts/")

async def create_post(post: Post):

_\# post уже валидирован_

print(post.dict()) _\# преобразование в словарь_

return {"data": post.dict()}

FastAPI автоматически проверяет, что в теле запроса присутствуют все обязательные поля и они имеют правильные типы. При несоответствии возвращается ошибка 422 Unprocessable Entity с детальным описанием проблемы.

**4.3. Расширенная валидация полей**

Для более сложной валидации используются Annotated + Query, Path, Body и др.:

from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")

async def read_items(

q: Annotated\[str | None, Query(max_length=50, min_length=3)\] = None

):

results = {"items": \[{"item_id": "Foo"}, {"item_id": "Bar"}\]}

if q:

results.update({"q": q})

return results

**Параметры валидации:**

| Параметр | Описание |
| --- | --- |
| min_length / max_length | Длина строки |
| pattern | Регулярное выражение |
| gt / ge / lt / le | Числовые границы |
| default | Значение по умолчанию |
| examples | Примеры для OpenAPI документации |

Можно также добавлять собственные валидаторы с помощью @field_validator и @model_validator.

**4.4. Схемы для разных операций**

В больших проектах принято создавать отдельные схемы для разных операций:

from pydantic import BaseModel, EmailStr, Field

_\# Базовые поля_

class UserBase(BaseModel):

name: Annotated\[str, Field(min_length=2, max_length=30)\]

email: EmailStr

_\# Для создания_

class UserCreate(UserBase):

password: Annotated\[str, Field(min_length=8)\]

_\# Для чтения (без пароля!)_

class UserRead(BaseModel):

id: int

name: str

email: EmailStr

is_active: bool = True

_\# Для обновления (все поля опциональны)_

class UserUpdate(BaseModel):

name: Annotated\[str | None, Field(min_length=2, max_length=30)\] = None

email: EmailStr | None = None

Практика разделения схем по ролям (Create, Read, Update) позволяет контролировать, какие данные принимает API и что возвращает клиенту, обеспечивая безопасность (например, не возвращая хэш пароля).

**5\. Инъекция зависимостей**

**5.1. Основы Depends()**

FastAPI имеет встроенную систему **инъекции зависимостей** через Depends(). Это позволяет изолировать логику и упрощает тестирование.

**Базовый пример:**

from fastapi import Depends, FastAPI

app = FastAPI()

def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):

return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")

async def read_items(commons: dict = Depends(common_parameters)):

return commons

@app.get("/users/")

async def read_users(commons: dict = Depends(common_parameters)):

return commons

**5.2. Dependency Injection в чистой архитектуре**

При использовании слоистой архитектуры зависимости организуются в виде цепочки:

Запрос → Роутер → Сервис → Репозиторий → База данных

**Организация провайдеров зависимостей** (deps.py):

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.repositories.user_repository import UserRepository

from app.services.user_service import UserService

def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:

return UserRepository(db)

def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:

return UserService(repo)

**Использование в роутере:**

from fastapi import APIRouter, Depends

from app.services.user_service import UserService

from app.routers.deps import get_user_service

router = APIRouter(prefix="/users", tags=\["users"\])

@router.get("/{user_id}")

async def get_user(user_id: int, service: UserService = Depends(get_user_service)):

return await service.get_user(user_id)

**5.3. Что НЕЛЬЗЯ делать**

**Плохие практики** (которые нарушают принципы DI и делают код труднотестируемым):

1.  **Прямое создание экземпляра в хендлере**:

@router.get("/{user_id}")

async def get_user(user_id: int):

service = UserService() _\# ❌ НЕПРАВИЛЬНО_

1.  **Глобальный экземпляр**:

user_service = UserService() _\# ❌ Глобальное состояние — плохо_

1.  **Отсутствие Depends()**:

python

@router.get("/users")

async def get_users(db: AsyncSession): _\# ❌ db не будет передан_

...

**6\. Командные соглашения**

**6.1. Структура проекта**

Для серверного приложения на FastAPI рекомендуется следующая структура:

project/

├── src/

│ ├── api/

│ │ ├── routes/ # Маршруты (эндпоинты)

│ │ └── schemas/ # Pydantic схемы

│ ├── core/

│ │ ├── entities/ # Доменные сущности

│ │ ├── services/ # Бизнес-логика

│ │ └── interfaces/ # Абстракции (репозитории)

│ ├── infrastructure/

│ │ ├── database/ # Модели БД, репозитории

│ │ └── external/ # Внешние API

│ ├── routers/

│ │ └── deps.py # Провайдеры зависимостей

│ └── main.py # Точка входа

└── tests/

**6.2. Рекомендации по проектированию API**

1.  Используйте осмысленные имена ресурсов во множественном числе: /users, /products
2.  Возвращайте правильные HTTP-статусы: 201 для создания, 204 для удаления
3.  Используйте ответные модели (response_model), чтобы гарантировать структуру ответа
4.  Документируйте эндпоинты через docstrings — они попадают в Swagger
5.  Держите эндпоинты небольшими и делегируйте логику сервисам
6.  Используйте ConfigDict(extra="forbid") на схемах для создания и обновления, чтобы клиент не мог передать лишние поля

**6.3. Тестирование**

FastAPI предоставляет TestClient для удобного тестирования:

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_create_item():

response = client.post(

"/items/",

json={"name": "Test Item", "price": 10.99}

)

assert response.status_code == 201

assert response.json()\["name"\] == "Test Item"

Для тестирования с Dependency Injection можно использовать app.dependency_overrides для подмены зависимостей моками:

app.dependency_overrides\[get_user_service\] = lambda: mock_service

1.  **Итоги**

На этой лекции мы рассмотрели:

| Тема | Ключевые выводы |
| --- | --- |
| **FastAPI** | Современный высокопроизводительный фреймворк с автоматической документацией и валидацией |
| **REST API** | Ресурсы, HTTP-методы, параметры пути и запроса |
| **Pydantic** | Автоматическая валидация данных через схемы с аннотациями типов |
| **Валидация** | Использование Annotated, Query, Field для расширенной проверки |
| **Инъекция зависимостей** | Depends() для чистой архитектуры и тестируемости |

FastAPI позволяет разработчикам сосредоточиться на бизнес-логике, беря на себя рутинные задачи валидации, документации и маршрутизации. В следующем занятии мы перейдём к работе с базами данных через SQLAlchemy и Alembic.

1.  **Ссылки на материалы**

Документация

- [Git Book](https://git-scm.com/book/ru/v2)
- [GitHub Actions](https://docs.github.com/actions)
- [pytest](https://docs.pytest.org/)
- [ruff](https://docs.astral.sh/ruff/)
- [pre-commit](https://pre-commit.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)

1.  **Примеры**

- [Примеры .gitignore](https://github.com/github/gitignore)
- [GitHub Actions для Python](https://github.com/actions/starter-workflows/tree/main/ci)

**10\. Вопросы для самопроверки**

1.  В чём ключевые преимущества FastAPI перед другими веб-фреймворками?
2.  Какая команда используется для запуска FastAPI-приложения в режиме разработки?
3.  Как FastAPI преобразует параметр пути item_id: int из строки в число? Что произойдёт, если передать нечисловое значение?
4.  Какие основные HTTP-методы используются в REST API и для каких операций они предназначены?
5.  В чём разница между параметрами пути (path) и параметрами запроса (query)?
6.  Какую роль выполняет Pydantic в FastAPI и как создать схему для валидации тела запроса?
7.  Какие статус-коды возвращает FastAPI при успешной валидации и при ошибке валидации?
8.  Как задать дополнительные ограничения на поле (например, минимальную длину строки или числовой диапазон) при помощи Annotated и Field?
9.  Для чего используется механизм Depends() в FastAPI? Приведите пример использования.
10. Почему в чистой архитектуре **не рекомендуется** создавать экземпляры сервисов напрямую внутри хендлера (service = UserService())?