**Самостоятельная работа по модулю 3 (12 часов)**

**Реализация серверной части командного проекта (спринт 1): API, модели данных, подключение хранилища**

**1\. Назначение**

Закрепить и применить на практике знания, полученные в модуле 3 «Проектирование и серверная разработка на Python». В рамках самостоятельной работы студенты реализуют серверную часть командного проекта — от проектирования архитектуры и моделей данных до создания полноценного REST API с подключением к базе данных и миграциями.

**Общая трудоёмкость:** 12 академических часов.

**2\. Проверяемые результаты обучения**

| Код | Индикатор | Уровень | Дескриптор освоения |
| --- | --- | --- | --- |
| PL-1.1 | Разрабатывает и отлаживает прикладные решения разной сложности с использованием Python, тестирует, испытывает и оценивает их качество | С   | Обучающийся способен самостоятельно спроектировать архитектуру серверного приложения, создать модели данных, реализовать REST API на FastAPI с подключением к базе данных и миграциями |

**3\. Условия выполнения**

| Параметр | Значение |
| --- | --- |
| **Форма контроля** | Промежуточная (спринт) |
| **Время выполнения** | 12 академических часов |
| **Формат сдачи** | Git-репозиторий команды |
| **Режим выполнения** | Командный (3–5 человек) |
| **Используемые инструменты** | Python 3.10+, FastAPI, SQLAlchemy 2.x, Alembic, PostgreSQL, Pydantic, Uvicorn |
| **Допустимые источники** | Документация FastAPI, SQLAlchemy, материалы лекций, консультации с преподавателем |
| **Правила использования ИИ** | Разрешено для помощи в написании кода. **Обязательно документируется** в ai-usage-log.md |

**4\. Общее описание проекта**

**Тема проекта:** Командный проект выбирается самостоятельно или предлагается преподавателем. Примеры тем:

- **Система управления задачами** (Trello-подобный сервис)
- **Платформа для онлайн-обучения** (курсы, студенты, преподаватели)
- **Система бронирования** (отелей, билетов, встреч)
- **Сервис доставки еды** (заказы, рестораны, курьеры)
- **Блог-платформа** (посты, комментарии, лайки)

**Требования к проекту:**

1.  Минимум **5 сущностей**, связанных между собой (один-ко-многим, многие-ко-многим)
2.  Полноценное REST API с CRUD-операциями для всех сущностей
3.  Валидация данных через Pydantic
4.  Подключение к PostgreSQL через SQLAlchemy с пулом соединений
5.  Миграции через Alembic
6.  Решение проблемы N+1 запросов

**5\. Задание (по этапам)**

**Этап 1. Анализ и проектирование**

**5.1. Формулировка требований**

1.  **Определите предметную область** вашего проекта (1-2 абзаца текста).
2.  **Опишите пользовательские сценарии** (4–5 ключевых сценариев использования):
    - Кто пользователь?
    - Что он хочет сделать?
    - Какой результат ожидает?

**Результат:** Файл docs/requirements.md

**5.2. Проектирование архитектуры**

1.  **Определите сущности проекта** (минимум 5). Для каждой сущности опишите:
    - Название и назначение
    - Атрибуты (поле, тип, обязательность, уникальность)
    - Связи с другими сущностями (один-ко-многим, многие-ко-многим)
    - Бизнес-правила и ограничения
2.  **Создайте ER-диаграмму** (схему базы данных) в любом удобном формате.

**Пример описания сущности:**

markdown

\### Сущность "Заказ" (Order)

\- **\*\*Назначение:\*\*** Хранит информацию о заказе пользователя.

\- **\*\*Атрибуты:\*\***

\- \`id\` (Integer, PK) — уникальный идентификатор

\- \`user_id\` (Integer, FK) — ссылка на пользователя

\- \`status\` (Enum) — статус заказа (created, paid, shipped, delivered)

\- \`total_amount\` (Float) — общая сумма заказа

\- \`created_at\` (DateTime) — дата и время создания

\- **\*\*Связи:\*\***

\- Многие-к-одному с \`User\` (у пользователя много заказов)

\- Один-ко-многим с \`OrderItem\` (заказ содержит много позиций)

\- **\*\*Бизнес-правила:\*\***

\- Статус может меняться в строго определённой последовательности

\- \`total_amount\` вычисляется на основе позиций заказа

**Результат:** Файл docs/data-model.md + ER-диаграмма (изображение или код).

**5.3. Проектирование API**

1.  **Составьте список эндпоинтов** для каждой сущности:
    - CRUD-операции (GET список, GET один, POST, PUT/PATCH, DELETE)
    - Дополнительные бизнес-эндпоинты (например, /orders/{id}/confirm, /products/search)
2.  **Для каждого эндпоинта опишите:**
    - HTTP-метод и путь
    - Параметры запроса (path, query, body)
    - Ожидаемый ответ (структура, статус-код)
    - Возможные ошибки

**Пример:**

markdown

\### POST /orders/

\- **\*\*Описание:\*\*** Создание нового заказа

\- **\*\*Тело запроса:\*\***

\`\`\`json

{

"user_id": 1,

"items": \[

{"product_id": 5, "quantity": 2},

{"product_id": 12, "quantity": 1}

\]

}

- **Ответ (201 Created):**

json

{

"id": 1,

"user_id": 1,

"total_amount": 7500.00,

"status": "created",

"created_at": "2024-11-15T10:30:00Z"

}

- **Возможные ошибки:**
    - 404 — пользователь не найден
    - 404 — товар не найден
    - 400 — недостаточно товара на складе

text

\*\*Результат:\*\* Файл \`docs/api-design.md\` с подробным описанием всех эндпоинтов.

\---

**Этап 2. Реализация моделей и базы данных**

**5.4. Настройка проекта и структуры**

1\. \*\*Создайте структуру проекта:\*\*

team-XX-project/  
├── .github/  
│ └── workflows/  
├── src/  
│ ├── **init**.py  
│ ├── main.py  
│ ├── config.py  
│ ├── database.py  
│ ├── models/  
│ │ ├── **init**.py  
│ │ ├── user.py  
│ │ ├── product.py  
│ │ └── ... (по числу сущностей)  
│ ├── schemas/  
│ │ ├── **init**.py  
│ │ ├── user.py  
│ │ └── ... (по числу сущностей)  
│ ├── api/  
│ │ ├── **init**.py  
│ │ └── routes/  
│ │ ├── **init**.py  
│ │ ├── users.py  
│ │ ├── products.py  
│ │ └── ... (по числу сущностей)  
│ ├── core/  
│ │ ├── **init**.py  
│ │ ├── services/  
│ │ │ ├── **init**.py  
│ │ │ └── ... (бизнес-логика)  
│ │ └── interfaces/  
│ │ ├── **init**.py  
│ │ └── repositories.py  
│ └── routers/  
│ ├── **init**.py  
│ └── deps.py  
├── alembic/  
│ └── versions/  
├── alembic.ini  
├── tests/  
│ ├── **init**.py  
│ ├── test_models.py  
│ └── test_api.py  
├── requirements.txt  
├── .env  
├── .gitignore  
└── README.md

text

2\. \*\*Настройте переменные окружения\*\* в файле \`.env\`:

DATABASE_URL=postgresql://user:password@localhost:5432/project_db  
DATABASE_POOL_SIZE=20  
DATABASE_MAX_OVERFLOW=10

text

3\. \*\*Настройте пул соединений\*\* с параметрами из \`.env\`:

\`\`\`python

\# src/database.py

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from src.config import settings

engine = create_engine(

settings.DATABASE_URL,

pool_size=settings.POOL_SIZE,

max_overflow=settings.MAX_OVERFLOW,

pool_pre_ping=True,

echo=settings.DEBUG

)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():

db = SessionLocal()

try:

yield db

finally:

db.close()

**Результат:** Настроенный проект с файлами конфигурации.

**5.5. Реализация моделей SQLAlchemy**

1.  **Создайте модели** для всех сущностей (минимум 5).
2.  **Определите все связи** между моделями (ForeignKey, relationship).
3.  **Добавьте индексы** на часто используемые поля.
4.  **Используйте Enum-типы** для полей с ограниченным набором значений (статусы, роли).

**Пример модели (Enum + индексы):**

python

_\# src/models/order.py_

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime, Index

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from src.database import Base

import enum

class OrderStatus(enum.Enum):

CREATED = "created"

PAID = "paid"

SHIPPED = "shipped"

DELIVERED = "delivered"

CANCELLED = "cancelled"

class Order(Base):

\__tablename__ = "orders"

id = Column(Integer, primary_key=True, index=True)

user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

status = Column(Enum(OrderStatus), default=OrderStatus.CREATED, nullable=False)

total_amount = Column(Float, nullable=False, default=0.0)

created_at = Column(DateTime(timezone=True), server_default=func.now())

_\# Связи_

user = relationship("User", back_populates="orders")

items = relationship("OrderItem", back_populates="order", lazy="select")

_\# ... остальные связи_

\__table_args__ = (

Index("ix_orders_user_status", "user_id", "status"),

)

def can_transition_to(self, new_status: OrderStatus) -> bool:

"""Проверка возможности смены статуса."""

allowed_transitions = {

OrderStatus.CREATED: \[OrderStatus.PAID, OrderStatus.CANCELLED\],

OrderStatus.PAID: \[OrderStatus.SHIPPED\],

OrderStatus.SHIPPED: \[OrderStatus.DELIVERED\],

OrderStatus.DELIVERED: \[\],

OrderStatus.CANCELLED: \[\],

}

return new_status in allowed_transitions.get(self.status, \[\])

**Рекомендации:**

- Используйте lazy="selectin" для связей, которые часто загружаются .
- Добавляйте бизнес-методы в модели для инкапсуляции логики (как can_transition_to()).
- Используйте композитные индексы для часто фильтруемых комбинаций полей.

**Результат:** Файлы с моделями в директории src/models/.

**5.6. Настройка Alembic и миграции**

1.  **Инициализируйте Alembic:**

bash

alembic init alembic

1.  **Настройте** alembic.ini — укажите URL вашей БД.
2.  **Настройте** env.py — импортируйте Base.metadata из ваших моделей:

python

_\# alembic/env.py_

from src.models import Base

target_metadata = Base.metadata

1.  **Создайте первую миграцию:**

bash

alembic revision --autogenerate -m "Initial migration"

1.  **Примените миграцию:**

bash

alembic upgrade head

1.  **Проверьте структуру** в базе данных (через psql или pgAdmin).
2.  **Проверьте обратное применение** (откат):

bash

alembic downgrade -1

alembic upgrade head

**Результат:** Файлы миграций в alembic/versions/, база данных создана.

**Этап 3. Реализация бизнес-логики и сервисов**

**5.7. Реализация бизнес-логики (сервисы)**

**Создайте сервисы для основных бизнес-операций:**

python

_\# src/core/services/order_service.py_

from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.order import Order, OrderStatus

from src.models.user import User

from src.models.product import Product

from src.models.order_item import OrderItem

from src.schemas.order import OrderCreate

class OrderService:

def \__init_\_(self, db: Session):

self.db = db

def create_order(self, order_data: OrderCreate) -> Order:

"""Создание заказа с проверками."""

_\# Проверка пользователя_

user = self.db.query(User).filter(User.id == order_data.user_id).first()

if not user:

raise ValueError("User not found")

_\# Создание заказа_

order = Order(user_id=order_data.user_id)

self.db.add(order)

self.db.flush()

total = 0.0

for item in order_data.items:

_\# Блокировка строки для избежания гонок_

product = self.db.query(Product).filter(

Product.id == item.product_id

).with_for_update().first()

if not product:

raise ValueError(f"Product {item.product_id} not found")

if product.stock < item.quantity:

raise ValueError(f"Insufficient stock for {product.name}")

_\# Обновление остатка_

product.stock -= item.quantity

self.db.add(product)

_\# Создание позиции заказа_

order_item = OrderItem(

order_id=order.id,

product_id=item.product_id,

quantity=item.quantity,

unit_price=product.price

)

self.db.add(order_item)

total += product.price \* item.quantity

order.total_amount = total

self.db.commit()

self.db.refresh(order)

return order

def update_order_status(self, order_id: int, new_status: OrderStatus) -> Order:

"""Обновление статуса заказа с проверкой переходов."""

order = self.db.query(Order).filter(Order.id == order_id).first()

if not order:

raise ValueError("Order not found")

if not order.can_transition_to(new_status):

raise ValueError(

f"Cannot transition from {order.status} to {new_status}"

)

order.status = new_status

self.db.commit()

self.db.refresh(order)

return order

def get_user_orders(self, user_id: int) -> List\[Order\]:

"""Получение заказов пользователя."""

return self.db.query(Order).filter(Order.user_id == user_id).all()

**5.8. Реализация Pydantic схем**

**Создайте схемы для всех сущностей (Create, Read, Update):**

python

_\# src/schemas/order.py_

from pydantic import BaseModel, Field

from datetime import datetime

from typing import List, Optional

from src.models.order import OrderStatus

class OrderItemCreate(BaseModel):

product_id: int

quantity: int = Field(gt=0)

class OrderCreate(BaseModel):

user_id: int

items: List\[OrderItemCreate\]

class OrderRead(BaseModel):

id: int

user_id: int

status: OrderStatus

total_amount: float

created_at: datetime

model_config = {"from_attributes": True}

class OrderUpdate(BaseModel):

status: OrderStatus

**Рекомендации:**

- Используйте model_config = {"from_attributes": True} для поддержки ORM-объектов.
- Для длинных схем используйте @field_validator для дополнительной валидации.
- Разделяйте схемы по ролям (Create, Read, Update).

**Этап 4. Реализация REST API**

**5.9. Реализация эндпоинтов**

**Создайте эндпоинты для всех сущностей с использованием Dependency Injection:**

python

_\# src/api/routes/orders.py_

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from typing import List

from src.database import get_db

from src.schemas.order import OrderCreate, OrderRead, OrderUpdate

from src.core.services.order_service import OrderService

from src.routers.deps import get_order_service

router = APIRouter(prefix="/orders", tags=\["orders"\])

@router.get("/", response_model=List\[OrderRead\])

def get_orders(

user_id: int,

db: Session = Depends(get_db),

service: OrderService = Depends(get_order_service)

):

"""Получение всех заказов пользователя."""

return service.get_user_orders(user_id)

@router.get("/{order_id}", response_model=OrderRead)

def get_order(

order_id: int,

db: Session = Depends(get_db),

service: OrderService = Depends(get_order_service)

):

"""Получение заказа по ID."""

order = service.get_order(order_id)

if not order:

raise HTTPException(status_code=404, detail="Order not found")

return order

@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)

def create_order(

order_data: OrderCreate,

db: Session = Depends(get_db),

service: OrderService = Depends(get_order_service)

):

"""Создание нового заказа."""

try:

return service.create_order(order_data)

except ValueError as e:

raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{order_id}/status", response_model=OrderRead)

def update_order_status(

order_id: int,

status_update: OrderUpdate,

db: Session = Depends(get_db),

service: OrderService = Depends(get_order_service)

):

"""Обновление статуса заказа."""

try:

return service.update_order_status(order_id, status_update.status)

except ValueError as e:

raise HTTPException(status_code=400, detail=str(e))

**5.10. Регистрация роутеров**

**В главном файле** main.py **зарегистрируйте все роутеры:**

python

_\# src/main.py_

from fastapi import FastAPI

from src.api.routes import users, products, orders, order_items

app = FastAPI(

title="Project Title",

description="Description of your project",

version="0.1.0"

)

_\# Регистрация роутеров_

app.include_router(users.router)

app.include_router(products.router)

app.include_router(orders.router)

app.include_router(order_items.router)

@app.get("/health", status_code=200)

def health_check():

"""Health check endpoint."""

return {"status": "ok", "version": "0.1.0"}

**Результат:** Полноценное REST API с эндпоинтами для всех сущностей.

**Этап 5. Тестирование и устранение N+1**

**5.11. Тестирование API**

1.  **Проверьте все эндпоинты** через Swagger UI (/docs).
2.  **Создайте тестовые данные** (минимум 5 пользователей, 10 товаров, 5 заказов).
3.  **Напишите простые тесты** для основных эндпоинтов:

python

_\# tests/test_orders.py_

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_create_order():

response = client.post(

"/orders/",

json={

"user_id": 1,

"items": \[

{"product_id": 1, "quantity": 2},

{"product_id": 2, "quantity": 1}

\]

}

)

assert response.status_code == 201

data = response.json()

assert "id" in data

assert data\["user_id"\] == 1

**5.12. Диагностика и устранение N+1 запросов**

1.  **Включите логирование SQL-запросов** (echo=True в create_engine).
2.  **Найдите потенциальные N+1 проблемы** в ваших эндпоинтах (особенно в GET с вложенными данными).
3.  **Примените** selectinload для жадной загрузки связанных данных:

python

from sqlalchemy.orm import selectinload

@router.get("/with-items/", response_model=List\[OrderWithItemsRead\])

def get_orders_with_items(

db: Session = Depends(get_db),

service: OrderService = Depends(get_order_service)

):

"""Получение заказов с позициями (без N+1)."""

orders = db.query(Order).options(

selectinload(Order.items).selectinload(OrderItem.product)

).all()

return orders

1.  **Добавьте в README описание** того, как вы решили проблему N+1 в вашем проекте.

**Результат:** Отсутствие N+1 запросов в основных эндпоинтах.

**Этап 6. Документация и сдача**

**5.13. Оформление документации**

**В README.md опишите:**

- Название проекта и его цель
- Команда (состав)
- Технологический стек
- Инструкция по установке и запуску
- Инструкция по миграциям
- Ссылка на документацию API (/docs)
- Демонстрационные данные (как заполнить БД)

**5.14. Проверка зависимостей**

1.  **Экспортируйте зависимости:**

bash

pip freeze > requirements.txt

1.  **Проверьте работу проекта** в чистом окружении (fresh venv):

bash

python -m venv .venv-test

source .venv-test/bin/activate

pip install -r requirements.txt

alembic upgrade head

uvicorn src.main:app --reload

**5.15. Сдача работы**

1.  **Проверьте структуру репозитория:**

text

team-XX-project/

├── .github/workflows/ci.yml # (опционально, если настроен CI)

├── src/

│ ├── \__init_\_.py

│ ├── main.py

│ ├── config.py

│ ├── database.py

│ ├── models/

│ ├── schemas/

│ ├── api/routes/

│ ├── core/services/

│ ├── core/interfaces/

│ └── routers/deps.py

├── alembic/versions/

├── alembic.ini

├── tests/

├── docs/

│ ├── requirements.md

│ ├── data-model.md

│ └── api-design.md

├── requirements.txt

├── .env.example

├── .gitignore

└── README.md

1.  **Загрузите код в репозиторий** и добавьте ссылку в отчёт по спринту.
2.  **Подготовьте демонстрацию** (живой показ работы API через Swagger).

**6\. Формат сдачи**

1.  Git-репозиторий команды со всем кодом.
2.  Рабочий проект, запускающийся по инструкции из README.
3.  Документация в директории docs/.
4.  Демонстрация работы API на спринт-ревью (5–7 минут).

**7\. Критерии оценивания**

| №   | Критерий | Вес | Описание |
| --- | --- | --- | --- |
| 1   | Проектирование (требования, модели, API) | 15% | Требования описаны, модели спроектированы, API-дизайн документирован |
| 2   | Модели данных | 15% | Модели реализованы корректно, есть связи, индексы, бизнес-методы |
| 3   | Миграции Alembic | 10% | Настроен Alembic, миграции созданы и работают |
| 4   | Реализация API | 20% | Все эндпоинты работают, коды ответов корректны, валидация работает |
| 5   | Бизнес-логика и сервисы | 15% | Сервисы реализованы, транзакции корректны |
| 6   | N+1 устранена | 10% | Проблема N+1 диагностирована и устранена с использованием eager loading |
| 7   | Тесты | 5%  | Написаны тесты для основных эндпоинтов |
| 8   | Документация и README | 10% | README содержит все необходимые разделы, документы в docs/ заполнены |

**8\. Шкала оценивания**

| Уровень | Диапазон баллов | Характеристика |
| --- | --- | --- |
| Базовый | 60–79% | Проект работает, но есть недочёты в архитектуре, документации или N+1 |
| Базовый + | 80–89% | Все критерии выполнены на хорошем уровне |
| Базовый ++ | 90–100% | Отличная работа: качественный код, чистая архитектура, N+1 устранена, документация полная |
| Ниже базового | < 60% | Задание выполнено не в полном объёме или проект не работает |

**9\. Методические рекомендации**

Для студентов

1.  Начинайте с проектирования — продуманная архитектура сэкономит часы разработки.
2.  Используйте Git с самого начала — делайте коммиты после каждого завершённого этапа.
3.  Включайте echo=True для SQLAlchemy при отладке, чтобы видеть все запросы.
4.  Следите за N+1 — это одна из самых частых проблем в ORM .
5.  Документируйте API через docstrings — они автоматически попадут в Swagger.
6.  Тестируйте транзакции — убедитесь, что при ошибке все изменения откатываются.
7.  Читайте ошибки Alembic — в них часто указано точное решение проблемы.

Для преподавателей

1.  Проверьте, что все участники команды внесли вклад (через историю коммитов).
2.  Убедитесь, что N+1 устранена (проверьте через логи SQL-запросов).
3.  Оцените качество проектирования — продуманность модели данных и API.
4.  При проверке транзакций убедитесь, что в случае ошибки данные не сохраняются.