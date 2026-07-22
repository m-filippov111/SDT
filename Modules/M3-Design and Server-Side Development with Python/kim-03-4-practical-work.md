**Практическое занятие 3.4. Инъекция зависимостей и чистая архитектура**

**1\. Назначение**

Сформировать навыки использования механизма инъекции зависимостей в FastAPI для построения тестируемых приложений с чистой архитектурой.

**2\. Проверяемые результаты обучения**

| Код | Индикатор | Уровень | Дескриптор освоения |
| --- | --- | --- | --- |
| PL-1.1 | Разрабатывает и отлаживает прикладные решения разной сложности с использованием Python, тестирует, испытывает и оценивает их качество | С   | Обучающийся способен использовать инъекцию зависимостей через Depends(), правильно организовывать провайдеры зависимостей, разделять слои приложения |

**3\. Условия выполнения**

| Параметр | Значение |
| --- | --- |
| **Форма контроля** | Практическая работа |
| **Время выполнения** | 2 академических часа |
| **Формат сдачи** | Git-репозиторий с кодом |
| **Режим выполнения** | Командный (2–3 человека) |
| **Используемые инструменты** | Python 3.10+, FastAPI, pytest |

**4\. Задание**

**Этап 1. Проектирование слоёв приложения**

Создайте структуру проекта для сервиса управления заказами:

text

order_service/

├── src/

│ ├── \__init_\_.py

│ ├── main.py

│ ├── api/

│ │ ├── \__init_\_.py

│ │ ├── routes/

│ │ │ ├── \__init_\_.py

│ │ │ └── orders.py

│ │ └── schemas/

│ │ ├── \__init_\_.py

│ │ └── order.py

│ ├── core/

│ │ ├── \__init_\_.py

│ │ ├── entities/

│ │ │ ├── \__init_\_.py

│ │ │ └── order.py

│ │ ├── services/

│ │ │ ├── \__init_\_.py

│ │ │ └── order_service.py

│ │ └── interfaces/

│ │ ├── \__init_\_.py

│ │ └── order_repository.py

│ ├── infrastructure/

│ │ ├── \__init_\_.py

│ │ └── repositories/

│ │ ├── \__init_\_.py

│ │ └── in_memory_order_repository.py

│ └── routers/

│ ├── \__init_\_.py

│ └── deps.py

└── tests/

├── \__init_\_.py

└── test_order_service.py

**Этап 2. Реализация слоёв**

**1\. Доменный слой (**core/entities/order.py**):**

python

from datetime import datetime

from typing import List, Optional

from enum import Enum

class OrderStatus(str, Enum):

PENDING = "pending"

CONFIRMED = "confirmed"

SHIPPED = "shipped"

DELIVERED = "delivered"

CANCELLED = "cancelled"

class OrderItem:

def \__init_\_(self, product_id: int, quantity: int, price: float):

self.product_id = product_id

self.quantity = quantity

self.price = price

@property

def total(self) -> float:

return self.quantity \* self.price

class Order:

def \__init_\_(

self,

user_id: int,

items: List\[OrderItem\],

status: OrderStatus = OrderStatus.PENDING,

order_id: Optional\[int\] = None

):

self.id = order_id

self.user_id = user_id

self.items = items

self.status = status

self.created_at = datetime.now()

@property

def total_amount(self) -> float:

return sum(item.total for item in self.items)

def confirm(self):

if self.status != OrderStatus.PENDING:

raise ValueError("Можно подтвердить только заказ в статусе PENDING")

self.status = OrderStatus.CONFIRMED

def ship(self):

if self.status != OrderStatus.CONFIRMED:

raise ValueError("Можно отправить только подтверждённый заказ")

self.status = OrderStatus.SHIPPED

**2\. Интерфейс репозитория (**core/interfaces/order_repository.py**):**

python

from abc import ABC, abstractmethod

from typing import List, Optional

from src.core.entities.order import Order

class OrderRepository(ABC):

@abstractmethod

def save(self, order: Order) -> Order:

pass

@abstractmethod

def get_by_id(self, order_id: int) -> Optional\[Order\]:

pass

@abstractmethod

def get_by_user(self, user_id: int) -> List\[Order\]:

pass

@abstractmethod

def delete(self, order_id: int) -> bool:

pass

**3\. Сервис (**core/services/order_service.py**):**

python

from typing import List, Optional

from src.core.entities.order import Order, OrderItem, OrderStatus

from src.core.interfaces.order_repository import OrderRepository

class OrderService:

def \__init_\_(self, repository: OrderRepository):

self.\_repository = repository

def create_order(self, user_id: int, items: List\[OrderItem\]) -> Order:

order = Order(user_id=user_id, items=items)

return self.\_repository.save(order)

def get_order(self, order_id: int) -> Optional\[Order\]:

return self.\_repository.get_by_id(order_id)

def get_user_orders(self, user_id: int) -> List\[Order\]:

return self.\_repository.get_by_user(user_id)

def confirm_order(self, order_id: int) -> Order:

order = self.\_repository.get_by_id(order_id)

if not order:

raise ValueError("Заказ не найден")

order.confirm()

return self.\_repository.save(order)

def cancel_order(self, order_id: int) -> Order:

order = self.\_repository.get_by_id(order_id)

if not order:

raise ValueError("Заказ не найден")

if order.status != OrderStatus.PENDING:

raise ValueError("Можно отменить только заказ в статусе PENDING")

order.status = OrderStatus.CANCELLED

return self.\_repository.save(order)

**4\. Реализация репозитория (**infrastructure/repositories/in_memory_order_repository.py**):**

python

from typing import List, Optional

from src.core.entities.order import Order

from src.core.interfaces.order_repository import OrderRepository

class InMemoryOrderRepository(OrderRepository):

def \__init_\_(self):

self.\_store = {}

self.\_counter = 1

def save(self, order: Order) -> Order:

if order.id is None:

order.id = self.\_counter

self.\_counter += 1

self.\_store\[order.id\] = order

return order

def get_by_id(self, order_id: int) -> Optional\[Order\]:

return self.\_store.get(order_id)

def get_by_user(self, user_id: int) -> List\[Order\]:

return \[order for order in self.\_store.values() if order.user_id == user_id\]

def delete(self, order_id: int) -> bool:

if order_id in self.\_store:

del self.\_store\[order_id\]

return True

return False

**Этап 3. Настройка зависимостей**

**Файл** routers/deps.py**:**

python

from fastapi import Depends

from src.core.services.order_service import OrderService

from src.infrastructure.repositories.in_memory_order_repository import InMemoryOrderRepository

def get_order_repository():

"""Провайдер репозитория."""

return InMemoryOrderRepository()

def get_order_service(

repository: InMemoryOrderRepository = Depends(get_order_repository)

) -> OrderService:

"""Провайдер сервиса."""

return OrderService(repository)

**Файл** api/routes/orders.py**:**

python

from fastapi import APIRouter, Depends, HTTPException

from typing import List

from src.api.schemas.order import OrderCreate, OrderRead, OrderItemSchema

from src.core.services.order_service import OrderService

from src.core.entities.order import OrderItem

from src.routers.deps import get_order_service

router = APIRouter(prefix="/orders", tags=\["orders"\])

@router.get("/", response_model=List\[OrderRead\])

async def get_orders(

user_id: int,

service: OrderService = Depends(get_order_service)

):

"""Получение всех заказов пользователя."""

orders = service.get_user_orders(user_id)

return orders

@router.get("/{order_id}", response_model=OrderRead)

async def get_order(

order_id: int,

service: OrderService = Depends(get_order_service)

):

"""Получение заказа по ID."""

order = service.get_order(order_id)

if not order:

raise HTTPException(status_code=404, detail="Заказ не найден")

return order

@router.post("/", response_model=OrderRead, status_code=201)

async def create_order(

order_data: OrderCreate,

service: OrderService = Depends(get_order_service)

):

"""Создание нового заказа."""

items = \[

OrderItem(

product_id=item.product_id,

quantity=item.quantity,

price=item.price

)

for item in order_data.items

\]

order = service.create_order(order_data.user_id, items)

return order

@router.post("/{order_id}/confirm", response_model=OrderRead)

async def confirm_order(

order_id: int,

service: OrderService = Depends(get_order_service)

):

"""Подтверждение заказа."""

try:

order = service.confirm_order(order_id)

return order

except ValueError as e:

raise HTTPException(status_code=400, detail=str(e))

@router.post("/{order_id}/cancel", response_model=OrderRead)

async def cancel_order(

order_id: int,

service: OrderService = Depends(get_order_service)

):

"""Отмена заказа."""

try:

order = service.cancel_order(order_id)

return order

except ValueError as e:

raise HTTPException(status_code=400, detail=str(e))

**Pydantic-схемы (**api/schemas/order.py**):**

python

from pydantic import BaseModel, Field

from typing import List

from datetime import datetime

from src.core.entities.order import OrderStatus

class OrderItemSchema(BaseModel):

product_id: int

quantity: Annotated\[int, Field(gt=0)\]

price: Annotated\[float, Field(gt=0)\]

class OrderCreate(BaseModel):

user_id: int

items: List\[OrderItemSchema\]

class OrderRead(BaseModel):

id: int

user_id: int

items: List\[OrderItemSchema\]

status: OrderStatus

total_amount: float

created_at: datetime

**Этап 4. Тестирование с подменой зависимостей**

**Файл** tests/test_order_service.py**:**

python

import pytest

from unittest.mock import Mock

from src.core.services.order_service import OrderService

from src.core.entities.order import Order, OrderItem, OrderStatus

def test_create_order():

_\# Создаём мок репозитория_

mock_repo = Mock()

mock_repo.save.return_value = Order(

user_id=1,

items=\[OrderItem(product_id=1, quantity=2, price=10.0)\],

order_id=1

)

service = OrderService(mock_repo)

items = \[OrderItem(product_id=1, quantity=2, price=10.0)\]

order = service.create_order(1, items)

assert order.id == 1

assert order.user_id == 1

assert order.status == OrderStatus.PENDING

mock_repo.save.assert_called_once()

def test_confirm_order():

mock_repo = Mock()

order = Order(

user_id=1,

items=\[OrderItem(product_id=1, quantity=1, price=10.0)\],

order_id=1,

status=OrderStatus.PENDING

)

mock_repo.get_by_id.return_value = order

mock_repo.save.return_value = order

service = OrderService(mock_repo)

confirmed_order = service.confirm_order(1)

assert confirmed_order.status == OrderStatus.CONFIRMED

mock_repo.save.assert_called_once()

def test_confirm_order_not_found():

mock_repo = Mock()

mock_repo.get_by_id.return_value = None

service = OrderService(mock_repo)

with pytest.raises(ValueError, match="Заказ не найден"):

service.confirm_order(999)

**Этап 5. Интеграция с FastAPI через dependency_overrides**

Для тестирования эндпоинтов с подменой зависимостей используйте app.dependency_overrides:

python

_\# tests/test_routes.py_

from fastapi.testclient import TestClient

from src.main import app

from src.routers.deps import get_order_service

from src.core.services.order_service import OrderService

from src.core.entities.order import Order, OrderItem, OrderStatus

client = TestClient(app)

def test_get_order_endpoint():

_\# Создаём мок сервиса_

mock_service = Mock(spec=OrderService)

mock_service.get_order.return_value = Order(

user_id=1,

items=\[OrderItem(product_id=1, quantity=1, price=10.0)\],

order_id=1

)

_\# Подменяем зависимость_

app.dependency_overrides\[get_order_service\] = lambda: mock_service

response = client.get("/orders/1")

assert response.status_code == 200

assert response.json()\["id"\] == 1

_\# Очищаем override после теста_

app.dependency_overrides.clear()

**5\. Формат сдачи**

1.  Git-репозиторий с полной структурой проекта
2.  Запускающееся приложение FastAPI
3.  Тесты с использованием моков

**6\. Критерии оценивания**

| №   | Критерий | Вес | Описание |
| --- | --- | --- | --- |
| 1   | Структура проекта | 20% | Правильное разделение на слои (API, Core, Infrastructure) |
| 2   | Реализация доменного слоя | 20% | Сущности и бизнес-логика корректны |
| 3   | Сервис и репозиторий | 20% | Работают через интерфейсы, реализован DI |
| 4   | Настройка зависимостей | 15% | Depends() настроены правильно, провайдеры организованы |
| 5   | Маршруты (эндпоинты) | 15% | Все эндпоинты работают корректно |
| 6   | Тестирование | 10% | Написаны тесты с моками |