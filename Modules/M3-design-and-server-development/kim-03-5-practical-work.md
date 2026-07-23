**Практическое занятие 3.5: Работа с базой данных из приложения**

**1\. Назначение**

Сформировать у обучающихся практические навыки работы с SQLAlchemy ORM: создания моделей, выполнения запросов, управления миграциями через Alembic, работы с транзакциями и пулом соединений, а также диагностики и устранения проблемы N+1 запросов.

**2\. Проверяемые результаты обучения**

| Код | Индикатор | Уровень | Дескриптор освоения |
| --- | --- | --- | --- |
| PL-1.1 | Разрабатывает и отлаживает прикладные решения разной сложности с использованием Python, тестирует, испытывает и оценивает их качество | С   | Обучающийся способен создавать модели SQLAlchemy, выполнять запросы к БД, настраивать миграции через Alembic, управлять транзакциями и пулом соединений, выявлять и устранять проблему N+1 запросов |

**3\. Условия выполнения**

| Параметр | Значение |
| --- | --- |
| **Форма контроля** | Практическая работа |
| **Время выполнения** | 2 академических часа |
| **Формат сдачи** | Git-репозиторий с кодом |
| **Режим выполнения** | Индивидуальный/Парный |
| **Используемые инструменты** | Python 3.10+, SQLAlchemy 2.x, Alembic, PostgreSQL/SQLite, FastAPI |

**4\. Задание**

**Этап 1. Настройка проекта и модели**

**Создайте структуру проекта:**

text

db_practice/

├── src/

│ ├── \__init_\_.py

│ ├── main.py

│ ├── database.py

│ ├── models.py

│ └── schemas.py

├── alembic/

│ └── ...

├── alembic.ini

├── requirements.txt

└── .env

**Установите зависимости:**

bash

pip install "fastapi\[standard\]" sqlalchemy alembic psycopg2-binary python-dotenv

**Создайте файл** src/database.py**:**

python

from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/mydb")

engine = create_engine(

DATABASE_URL,

pool_size=10, _\# размер пула соединений_

max_overflow=20, _\# дополнительные соединения при пиковой нагрузке_

pool_pre_ping=True, _\# проверка соединения перед использованием_

echo=True _\# логирование SQL-запросов (для отладки)_

)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():

"""Dependency для FastAPI."""

db = SessionLocal()

try:

yield db

finally:

db.close()

**Настройка пула соединений:** Параметры pool_size и max_overflow критически важны для production-приложений. Если приложение не возвращает соединения в пул или превышает лимит, возникает ошибка QueuePool limit of size &lt;x&gt; overflow &lt;y&gt; reached .

**Создайте файл** src/models.py**:**

python

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from src.database import Base

class User(Base):

\__tablename__ = "users"

id = Column(Integer, primary_key=True, index=True)

name = Column(String(50), nullable=False)

email = Column(String(50), unique=True, nullable=False, index=True)

_\# Связь: пользователь -> заказы_

orders = relationship("Order", back_populates="user", lazy="select")

class Product(Base):

\__tablename__ = "products"

id = Column(Integer, primary_key=True, index=True)

name = Column(String(100), nullable=False)

price = Column(Float, nullable=False)

stock = Column(Integer, nullable=False)

_\# Связь: товар -> позиции заказа_

order_items = relationship("OrderItem", back_populates="product")

class Order(Base):

\__tablename__ = "orders"

id = Column(Integer, primary_key=True, index=True)

user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

total_amount = Column(Float, nullable=False, default=0.0)

created_at = Column(DateTime(timezone=True), server_default=func.now())

_\# Связи_

user = relationship("User", back_populates="orders")

items = relationship("OrderItem", back_populates="order", lazy="select")

class OrderItem(Base):

\__tablename__ = "order_items"

id = Column(Integer, primary_key=True, index=True)

order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)

product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

quantity = Column(Integer, nullable=False)

unit_price = Column(Float, nullable=False)

_\# Связи_

order = relationship("Order", back_populates="items")

product = relationship("Product", back_populates="order_items")

**Этап 2. Миграции через Alembic**

**Инициализация Alembic:**

bash

alembic init alembic

**Настройка** alembic.ini**:**

ini

sqlalchemy.url = postgresql://user:password@localhost:5432/mydb

**Настройка** alembic/env.py **(импорт метаданных):**

python

_\# В файле alembic/env.py_

from src.models import Base _\# импорт всех моделей_

target_metadata = Base.metadata

**Создание и применение миграций:**

bash

_\# Генерация миграции_

alembic revision --autogenerate -m "Initial migration: users, products, orders, order_items"

_\# Применение миграции_

alembic upgrade head

**Структура файла миграции:**

python

def upgrade():

op.create_table('users',

sa.Column('id', sa.Integer(), nullable=False),

sa.Column('name', sa.String(50), nullable=False),

sa.Column('email', sa.String(50), nullable=False),

sa.PrimaryKeyConstraint('id')

)

op.create_index(op.f('ix_users_email'), 'users', \['email'\], unique=True)

_\# ... остальные таблицы_

def downgrade():

op.drop_table('order_items')

op.drop_table('orders')

op.drop_table('products')

op.drop_table('users')

**Этап 3. CRUD-операции с SQLAlchemy**

**Создайте файл** src/schemas.py **(Pydantic схемы):**

python

from pydantic import BaseModel

from datetime import datetime

from typing import List, Optional

class UserCreate(BaseModel):

name: str

email: str

class UserRead(BaseModel):

id: int

name: str

email: str

class OrderItemCreate(BaseModel):

product_id: int

quantity: int

class OrderCreate(BaseModel):

user_id: int

items: List\[OrderItemCreate\]

class OrderRead(BaseModel):

id: int

user_id: int

total_amount: float

created_at: datetime

**Создайте файл** src/main.py **с эндпоинтами:**

python

from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy.orm import Session

from typing import List

from src.database import get_db

from src import models, schemas

app = FastAPI(title="DB Practice", version="0.1.0")

@app.post("/users/", response_model=schemas.UserRead, status_code=201)

def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

"""Создание пользователя."""

db_user = models.User(name=user.name, email=user.email)

db.add(db_user)

db.commit()

db.refresh(db_user)

return db_user

@app.get("/users/", response_model=List\[schemas.UserRead\])

def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

"""Получение списка пользователей."""

users = db.query(models.User).offset(skip).limit(limit).all()

return users

@app.post("/orders/", response_model=schemas.OrderRead, status_code=201)

def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):

"""Создание заказа."""

_\# Проверка существования пользователя_

user = db.query(models.User).filter(models.User.id == order.user_id).first()

if not user:

raise HTTPException(status_code=404, detail="User not found")

_\# Создание заказа_

db_order = models.Order(user_id=order.user_id)

db.add(db_order)

db.flush() _\# получаем id заказа_

total = 0.0

for item_data in order.items:

product = db.query(models.Product).filter(

models.Product.id == item_data.product_id

).first()

if not product:

raise HTTPException(status_code=404, detail=f"Product {item_data.product_id} not found")

db_item = models.OrderItem(

order_id=db_order.id,

product_id=item_data.product_id,

quantity=item_data.quantity,

unit_price=product.price

)

db.add(db_item)

total += product.price \* item_data.quantity

db_order.total_amount = total

db.commit()

db.refresh(db_order)

return db_order

**Этап 4. Проблема N+1 запросов и её устранение**

**Задача:** Написать эндпоинт, который возвращает всех пользователей с их заказами. **НЕПРАВИЛЬНО (N+1 проблема):**

python

@app.get("/users-with-orders-naive/")

def get_users_with_orders_naive(db: Session = Depends(get_db)):

"""⚠️ Плохой пример: N+1 запросов."""

users = db.query(models.User).all() _\# 1 запрос_

result = \[\]

for user in users:

_\# Для КАЖДОГО пользователя выполняется отдельный запрос_

orders = user.orders _\# N запросов!_

result.append({

"id": user.id,

"name": user.name,

"orders_count": len(orders),

"orders": \[{"id": o.id, "total": o.total_amount} for o in orders\]

})

return result

**Проблема:** При 100 пользователях выполняется 101 запрос .

**ПРАВИЛЬНО (Eager Loading):**

python

from sqlalchemy.orm import selectinload

@app.get("/users-with-orders/")

def get_users_with_orders(db: Session = Depends(get_db)):

"""✅ Правильный пример: один запрос через selectinload."""

users = db.query(models.User).options(

selectinload(models.User.orders) _\# Жадная загрузка заказов_

).all() _\# 1-2 запроса вместо N+1_

result = \[\]

for user in users:

_\# orders уже загружены, дополнительных запросов нет_

result.append({

"id": user.id,

"name": user.name,

"orders_count": len(user.orders),

"orders": \[{"id": o.id, "total": o.total_amount} for o in user.orders\]

})

return result

**Сравнение стратегий загрузки :**

| Стратегия | Запросы | Когда использовать |
| --- | --- | --- |
| joinedload | 1 (LEFT JOIN) | Для one-to-one, когда нужно фильтровать по связанной таблице |
| selectinload | 2 (с IN) | Для one-to-many, многие-ко-многим — **рекомендуется** для коллекций |
| lazy="select" (по умолчанию) | N+1 | Только если связь используется редко |

**Дополнительная оптимизация:** Используйте lazy="raise" в модели, чтобы при случайном обращении к не загруженной связи выбрасывалось исключение :

python

class User(Base):

_\# ..._

orders = relationship("Order", back_populates="user", lazy="raise")

**Этап 5. Транзакции и пакетные операции**

**Пример транзакции с откатом:**

python

@app.post("/orders-with-transaction/", status_code=201)

def create_order_with_transaction(

order: schemas.OrderCreate,

db: Session = Depends(get_db)

):

"""Создание заказа с транзакцией."""

try:

with db.begin_nested(): _\# savepoint_

_\# Проверка пользователя_

user = db.query(models.User).filter(

models.User.id == order.user_id

).first()

if not user:

raise HTTPException(404, "User not found")

_\# Создание заказа_

db_order = models.Order(user_id=order.user_id)

db.add(db_order)

db.flush()

total = 0.0

for item_data in order.items:

product = db.query(models.Product).filter(

models.Product.id == item_data.product_id

).with_for_update().first() _\# блокировка строки_

if not product:

raise HTTPException(404, f"Product {item_data.product_id} not found")

if product.stock < item_data.quantity:

raise HTTPException(400, f"Insufficient stock for {product.name}")

product.stock -= item_data.quantity

db.add(product)

db_item = models.OrderItem(

order_id=db_order.id,

product_id=item_data.product_id,

quantity=item_data.quantity,

unit_price=product.price

)

db.add(db_item)

total += product.price \* item_data.quantity

db_order.total_amount = total

db.commit()

except HTTPException:

db.rollback() _\# откат всех изменений_

raise

db.refresh(db_order)

return db_order

**Пакетные операции вместо цикла с commit :**

python

_\# ❌ Плохо: 1000 запросов_

for i in range(1000):

product = models.Product(name=f"Product {i}", price=i\*10, stock=100)

db.add(product)

db.commit()

_\# ✅ Хорошо: 1 запрос_

products = \[models.Product(name=f"Product {i}", price=i\*10, stock=100) for i in range(1000)\]

db.bulk_save_objects(products) _\# или bulk_insert_mappings для словарей_

db.commit()

**Этап 6. Задания для самостоятельного выполнения**

**Уровень Базовый:**

1.  Добавьте эндпоинт GET /users/{user_id}/orders для получения всех заказов пользователя с использованием selectinload для загрузки позиций заказа.
2.  Добавьте в модель Product поле created_at через миграцию.
3.  Реализуйте эндпоинт PATCH /products/{product_id} для частичного обновления товара.

**Уровень Продвинутый:**

1.  Добавьте эндпоинт GET /users/with-orders-and-items с загрузкой пользователей, заказов и позиций заказа в одном запросе (используйте selectinload с вложенными опциями).
2.  Реализуйте эндпоинт для массового обновления цен товаров с использованием bulk_update_mappings().
3.  Добавьте в модель Order поле status (Enum: pending, paid, shipped, delivered) через миграцию.

**5\. Формат сдачи**

1.  Git-репозиторий с полной структурой проекта
2.  Файл requirements.txt
3.  Файл .env с настройками подключения к БД
4.  Скриншот успешно выполненной миграции alembic upgrade head
5.  Скриншот документации /docs с новыми эндпоинтами

**6\. Критерии оценивания**

| №   | Критерий | Вес | Описание |
| --- | --- | --- | --- |
| 1   | Модели и база данных | 20% | Корректно созданы модели, настроен движок с пулом соединений |
| 2   | Миграции Alembic | 15% | Настроен Alembic, выполнена миграция |
| 3   | CRUD-эндпоинты | 20% | Все основные эндпоинты работают корректно |
| 4   | Устранение N+1 | 20% | Реализован эндпоинт с selectinload, проблема N+1 устранена |
| 5   | Транзакции | 15% | Реализован эндпоинт с транзакциями и обработкой ошибок |
| 6   | Документация | 10% | Код документирован, эндпоинты описаны |

**7\. Методические рекомендации**

**Для студентов**

1.  **Включите** echo=True в create_engine для просмотра SQL-запросов — это поможет диагностировать N+1.
2.  **Используйте** with db.begin_nested() для вложенных транзакций при работе с несколькими таблицами.
3.  **Не забывайте про** db.refresh() после commit() для получения сгенерированных полей (id, created_at).
4.  **Для пакетных операций** используйте bulk_insert_mappings или bulk_save_objects вместо цикла.

**Для преподавателей**

1.  Обратите внимание на echo=True — студенты должны видеть количество запросов и осознанно применять eager loading.
2.  Проверьте, что в эндпоинтах с N+1 проблема устранена с использованием selectinload или joinedload.
3.  Убедитесь, что транзакции корректно обрабатывают ошибки с откатом.