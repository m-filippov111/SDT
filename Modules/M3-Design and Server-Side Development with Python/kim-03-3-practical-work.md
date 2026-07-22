**Практическое занятие 2. Валидация данных и продвинутая работа с FastAPI**

**1\. Назначение**

Сформировать практические навыки глубокой валидации данных с использованием Pydantic, работы с Pydantic-схемами разных типов, валидации параметров через Annotated и обработки ошибок.

**2\. Проверяемые результаты обучения**

| Код | Индикатор | Уровень | Дескриптор освоения |
| --- | --- | --- | --- |
| PL-1.1 | Разрабатывает и отлаживает прикладные решения разной сложности с использованием Python, тестирует, испытывает и оценивает их качество | С   | Обучающийся способен использовать Pydantic для валидации данных, создавать сложные схемы с пользовательскими валидаторами, обрабатывать ошибки валидации |

**3\. Условия выполнения**

| Параметр | Значение |
| --- | --- |
| **Форма контроля** | Практическая работа |
| **Время выполнения** | 2 академических часа |
| **Формат сдачи** | Git-репозиторий с кодом |
| **Режим выполнения** | Индивидуальный |
| **Используемые инструменты** | Python 3.10+, FastAPI, Pydantic v2 |

**4\. Задание**

**Этап 1. Схемы разных типов (Create, Read, Update)**

Создайте модель пользователя с тремя типами схем:

from typing import Optional

from pydantic import BaseModel, Field, EmailStr

from typing_extensions import Annotated

class UserBase(BaseModel):

"""Базовые поля пользователя."""

username: str

email: EmailStr

class UserCreate(UserBase):

"""Схема для создания пользователя."""

password: Annotated\[str, Field(min_length=8, max_length=128)\]

confirm_password: str

class UserRead(BaseModel):

"""Схема для чтения пользователя (без пароля)."""

id: int

username: str

email: EmailStr

is_active: bool = True

class UserUpdate(BaseModel):

"""Схема для обновления пользователя (все поля опциональны)."""

username: Annotated\[Optional\[str\], Field(min_length=3, max_length=30)\] = None

email: Optional\[EmailStr\] = None

password: Annotated\[Optional\[str\], Field(min_length=8)\] = None

**Этап 2. Пользовательские валидаторы**

Добавьте валидацию, которая проверяет, что password и confirm_password совпадают:

from pydantic import BaseModel, field_validator, ValidationError

class UserCreateWithValidation(UserCreate):

@field_validator('confirm_password')

@classmethod

def validate_passwords_match(cls, v: str, info) -> str:

password = info.data.get('password')

if password is not None and v != password:

raise ValueError('Пароли не совпадают')

return v

**Добавьте валидацию для** username**:**

- Только буквы, цифры и подчёркивания
- Не может содержать пробелы

import re

class UserCreateWithValidation(UserCreate):

@field_validator('username')

@classmethod

def validate_username(cls, v: str) -> str:

if not re.match(r'^\[a-zA-Z0-9_\]+$', v):

raise ValueError('Имя пользователя может содержать только буквы, цифры и подчёркивания')

return v

**Этап 3. Работа с параметрами запроса через Annotated**

Вместо стандартного подхода с параметрами запроса изучите использование Annotated для валидации:

from fastapi import FastAPI, Query

from typing import Annotated

app = FastAPI()

@app.get("/search/")

async def search_items(

q: Annotated\[

Optional\[str\],

Query(

title="Поисковый запрос",

description="Строка для поиска по названию и описанию",

min_length=2,

max_length=50,

pattern=r'^\[a-zA-Z0-9\\s\]+$'

)

\] = None,

page: Annotated\[

int,

Query(

title="Номер страницы",

description="Номер страницы для пагинации",

ge=1,

le=100,

default=1

)

\] = 1,

per_page: Annotated\[

int,

Query(

title="Количество на странице",

description="Максимальное количество результатов на странице",

gt=0,

le=100,

default=10

)

\] = 10

):

"""Поиск с валидацией параметров."""

return {

"query": q,

"page": page,

"per_page": per_page,

"results": \[

{"id": i, "name": f"Result {i}"}

for i in range((page - 1) \* per_page, page \* per_page)

\]

}

Попробуйте отправить запросы с некорректными параметрами и посмотрите на возвращаемые ошибки:

bash

curl "http://localhost:8000/search/?q=a&page=0"

_\# Ошибка: page должно быть >= 1_

**Этап 4. Вложенные схемы**

Создайте схему для товара с вложенным объектом Category:

from typing import List

class CategoryBase(BaseModel):

name: str

description: Optional\[str\] = None

class CategoryRead(CategoryBase):

id: int

class ProductCreate(BaseModel):

name: Annotated\[str, Field(min_length=3, max_length=100)\]

price: Annotated\[float, Field(gt=0)\]

category: CategoryBase

tags: List\[str\] = \[\]

class ProductRead(ProductCreate):

id: int

category: CategoryRead

**Создайте эндпоинт для добавления товара с вложенной категорией:**

@app.post("/products/", response_model=ProductRead, status_code=201)

async def create_product(product: ProductCreate):

"""Создание товара с категорией."""

_\# Imitation of product creation_

return {

"id": 1,

"name": product.name,

"price": product.price,

"category": {

"id": 1,

"name": product.category.name,

"description": product.category.description

},

"tags": product.tags

}

**Этап 5. Обработка ошибок и кастомные исключения (15 минут)**

Создайте кастомное исключение для бизнес-ошибок и глобальный обработчик:

from fastapi import FastAPI, HTTPException, Request

from fastapi.responses import JSONResponse

class BusinessException(Exception):

def \__init_\_(self, detail: str, status_code: int = 400):

self.detail = detail

self.status_code = status_code

@app.exception_handler(BusinessException)

async def business_exception_handler(request: Request, exc: BusinessException):

return JSONResponse(

status_code=exc.status_code,

content={"detail": exc.detail, "type": "BusinessError"}

)

@app.post("/validate-user/")

async def validate_user(username: str):

if len(username) < 3:

raise BusinessException(

detail="Имя пользователя должно содержать минимум 3 символа",

status_code=400

)

return {"status": "valid", "username": username}

**5\. Формат сдачи**

1.  Код в Git-репозитории с файлами:

- main.py — все эндпоинты
- schemas.py — все Pydantic-схемы
- exceptions.py — кастомные исключения

**6\. Критерии оценивания**

| №   | Критерий | Вес | Описание |
| --- | --- | --- | --- |
| 1   | Схемы Create/Read/Update | 20% | Правильно разделены схемы для разных операций |
| 2   | Пользовательские валидаторы | 25% | Реализованы валидаторы пароля и username |
| 3   | Annotated-параметры | 20% | Валидация параметров запроса через Annotated |
| 4   | Вложенные схемы | 20% | Корректно созданы вложенные схемы |
| 5   | Обработка ошибок | 15% | Реализован кастомный обработчик исключений |