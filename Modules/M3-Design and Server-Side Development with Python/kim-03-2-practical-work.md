**Практическое занятие 3.2. Введение в FastAPI и основы REST API**

**1\. Назначение**

Сформировать у обучающихся практические навыки создания базового веб-приложения на FastAPI, проектирования REST-эндпоинтов с параметрами пути и запроса.

**2\. Проверяемые результаты обучения**

| Код | Индикатор | Уровень | Дескриптор освоения |
| --- | --- | --- | --- |
| PL-1.1 | Разрабатывает и отлаживает прикладные решения разной сложности с использованием Python, тестирует, испытывает и оценивает их качество | С   | Обучающийся способен создавать веб-приложения на FastAPI, проектировать REST-эндпоинты, использовать параметры пути и запроса |

**3\. Условия выполнения**

| Параметр | Значение |
| --- | --- |
| **Форма контроля** | Практическая работа |
| **Время выполнения** | 2 академических часа |
| **Формат сдачи** | Git-репозиторий с кодом |
| **Режим выполнения** | Индивидуальный/Парный |
| **Используемые инструменты** | Python 3.10+, FastAPI, Uvicorn, HTTP-клиент (curl/Postman) |

**4\. Задание**

**Этап 1. Настройка проекта**

1.  Создайте новый проект и виртуальное окружение:

bash

mkdir fastapi-practice-1

cd fastapi-practice-1

python -m venv .venv

source .venv/bin/activate _\# или .venv\\Scripts\\activate_

1.  Установите зависимости:

bash

pip install "fastapi\[standard\]"

1.  Создайте структуру проекта:

text

fastapi-practice-1/

├── main.py

├── requirements.txt

└── .gitignore

**Этап 2. Базовое приложение**

**Создайте файл** main.py**:**

from fastapi import FastAPI

app = FastAPI(

title="Мой первый FastAPI проект",

description="Практика по серверному программированию",

version="0.1.0"

)

@app.get("/")

async def root():

"""Корневой эндпоинт."""

return {"message": "Добро пожаловать в FastAPI!"}

@app.get("/hello/{name}")

async def hello(name: str):

"""Приветствие пользователя по имени."""

return {"message": f"Привет, {name}!"}

@app.get("/items/")

async def get_items(skip: int = 0, limit: int = 10):

"""Получение списка элементов с пагинацией."""

items = \[

{"id": i, "name": f"Item {i}"}

for i in range(skip, skip + limit)

\]

return {"total": len(items), "items": items}

**Запустите приложение:**

bash

fastapi dev main.py

**Проверьте в браузере:**

- http://localhost:8000/
- http://localhost:8000/hello/Вася
- http://localhost:8000/items/?skip=5&limit=3
- http://localhost:8000/docs — автоматическая документация

**Этап 3. Создание CRUD-эндпоинтов**

**Создайте эндпоинты для работы с постами (в памяти):**

from fastapi import FastAPI, HTTPException

from pydantic import BaseModel

from typing import List, Optional

app = FastAPI()

_\# Модель поста (схема)_

class PostCreate(BaseModel):

title: str

content: str

author: str

class PostRead(BaseModel):

id: int

title: str

content: str

author: str

_\# Хранилище в памяти_

posts_db = \[\]

post_id_counter = 1

@app.get("/posts/", response_model=List\[PostRead\])

async def get_all_posts():

"""Получение всех постов."""

return posts_db

@app.get("/posts/{post_id}", response_model=PostRead)

async def get_post(post_id: int):

"""Получение поста по ID."""

for post in posts_db:

if post\["id"\] == post_id:

return post

raise HTTPException(status_code=404, detail="Пост не найден")

@app.post("/posts/", response_model=PostRead, status_code=201)

async def create_post(post: PostCreate):

"""Создание нового поста."""

global post_id_counter

new_post = {

"id": post_id_counter,

"title": post.title,

"content": post.content,

"author": post.author

}

posts_db.append(new_post)

post_id_counter += 1

return new_post

@app.delete("/posts/{post_id}", status_code=204)

async def delete_post(post_id: int):

"""Удаление поста."""

global posts_db

for i, post in enumerate(posts_db):

if post\["id"\] == post_id:

posts_db.pop(i)

return

raise HTTPException(status_code=404, detail="Пост не найден")

**Этап 4. Задания для самостоятельного выполнения**

**Уровень Базовый:**

1.  Добавьте эндпоинт PUT /posts/{post_id} для полного обновления поста (замены всех полей).
2.  Добавьте эндпоинт PATCH /posts/{post_id} для частичного обновления (только переданные поля обновляются, остальные остаются без изменений).
3.  Добавьте параметр запроса ?author=Имя к эндпоинту GET /posts/, чтобы фильтровать посты по автору.

**Уровень Продвинутый:**

1.  Реализуйте валидацию: при создании поста проверяйте, что title не короче 3 символов и не длиннее 100 символов, а content не короче 10 символов (используйте Annotated + Field в Pydantic-схеме).
2.  Добавьте эндпоинт GET /posts/search/?q=текст, который ищет посты, содержащие переданный текст в title или content.

**Этап 5. Тестирование через curl/Postman**

**Примеры запросов для проверки:**

bash

_\# Создание поста_

curl -X POST http://localhost:8000/posts/ \\

\-H "Content-Type: application/json" \\

\-d '{"title": "Мой первый пост", "content": "Это содержание поста", "author": "Анна"}'

_\# Получение всех постов_

curl http://localhost:8000/posts/

_\# Получение поста по ID_

curl http://localhost:8000/posts/1

_\# Обновление поста_

curl -X PUT http://localhost:8000/posts/1 \\

\-H "Content-Type: application/json" \\

\-d '{"title": "Новый заголовок", "content": "Новое содержание", "author": "Иван"}'

_\# Удаление поста_

curl -X DELETE http://localhost:8000/posts/1

**5\. Формат сдачи**

1.  Код в Git-репозитории (файл main.py)
2.  Файл requirements.txt
3.  Скриншоты работающей документации /docs

**6\. Критерии оценивания**

| №   | Критерий | Вес | Описание |
| --- | --- | --- | --- |
| 1   | Базовое приложение | 20% | Все эндпоинты из части 2 работают корректно |
| 2   | CRUD-эндпоинты | 30% | GET (все/один), POST, DELETE реализованы |
| 3   | PUT и PATCH | 20% | Обновление реализовано корректно |
| 4   | Фильтрация | 15% | Фильтр по автору работает |
| 5   | Валидация | 15% | Валидация добавлена (для продвинутого уровня) |