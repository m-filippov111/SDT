**Лекция 3.3: Работа с базой данных из приложения**

1.  **Введение в ORM и SQLAlchemy**

**1.1. Что такое ORM?**

**ORM** (Object-Relational Mapping) — это технология, которая связывает мир объектов Python с реляционными базами данных, позволяя работать с таблицами через Python-объекты вместо написания SQL-запросов вручную .

**Основные преимущества ORM:**

| Преимущество | Описание |
| --- | --- |
| **Меньше кода** | ORM автоматически генерирует SQL-запросы |
| **Читаемость** | Логика пишется на понятном языке Python |
| **Кросс-база** | Код можно перенести между разными СУБД (PostgreSQL, SQLite, MySQL) с минимальными изменениями |
| **Безопасность** | Автоматическая защита от SQL-инъекций |

**Недостатки ORM:**

- Некоторый "накладной" вес из-за автоматической генерации SQL
- Требует изучения синтаксиса конкретной ORM
- Иногда ORM ведёт себя неочевидно, и приходится разбираться во внутренних механизмах

**1.2. SQLAlchemy: архитектура и особенности**

SQLAlchemy — одна из самых популярных ORM для Python, которая делится на две большие части :

1.  **Core** — низкоуровневый слой для работы с SQL (ручное написание запросов)
2.  **ORM** — высокоуровневый слой для работы с объектами Python

В отличие от Django ORM, которая "идёт с батарейками" и требует меньше кода, SQLAlchemy даёт разработчику больше контроля и гибкости, но требует явной конфигурации .

**2\. Модели данных в SQLAlchemy**

**2.1. Создание моделей**

Модель в SQLAlchemy — это класс, наследующий от declarative_base() и соответствующий таблице в базе данных .

python

from sqlalchemy import Column, Integer, String, ForeignKey

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):

\__tablename__ = 'users'

id = Column(Integer, primary_key=True, index=True)

name = Column(String(50), nullable=False)

email = Column(String(50), unique=True, nullable=False)

class Post(Base):

\__tablename__ = 'posts'

id = Column(Integer, primary_key=True)

title = Column(String(200), nullable=False)

content = Column(String, nullable=False)

user_id = Column(Integer, ForeignKey('users.id'))

user = relationship('User', back_populates='posts')

User.posts = relationship('Post', back_populates='user')

**2.2. Основные типы полей**

| Тип SQLAlchemy | Назначение |
| --- | --- |
| Integer | Целое число |
| String | Строка (требуется указать длину) |
| Text | Длинный текст (без ограничения длины) |
| Boolean | Логическое значение |
| DateTime | Дата и время |
| Float | Число с плавающей точкой |
| ForeignKey | Внешний ключ для связи с другой таблицей |

**2.3. Связи между моделями**

**Один-ко-многим** (как User → Post выше):

- ForeignKey в дочерней модели
- relationship с обеих сторон

**Многие-ко-многим** требует промежуточной таблицы:

python

_\# Промежуточная таблица_

user_roles = Table('user_roles', Base.metadata,

Column('user_id', Integer, ForeignKey('users.id')),

Column('role_id', Integer, ForeignKey('roles.id'))

)

class User(Base):

_\# ..._

roles = relationship('Role', secondary=user_roles, back_populates='users')

**3\. Сессии и запросы**

**3.1. Что такое сессия?**

**Сессия** (Session) — это "рабочая область" для взаимодействия с базой данных. Она управляет транзакциями и отслеживает изменения объектов в памяти.

**Ключевые понятия:**

- **Identity Map** — структура внутри сессии, гарантирующая, что для каждой записи в БД существует только один объект Python
- **Unit of Work** — паттерн, при котором все изменения накапливаются и отправляются в БД одним пакетом при commit()

**3.2. Настройка подключения и создание сессий**

python

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

_\# Движок — точка подключения к БД_

engine = create_engine(

"postgresql+psycopg2://user:password@localhost:5432/mydb",

pool_size=10, _\# размер пула соединений_

max_overflow=20 _\# дополнительные соединения при пиковой нагрузке_

)

_\# Фабрика сессий_

Session = sessionmaker(bind=engine)

_\# Использование сессии_

with Session() as session:

_\# работа с БД_

session.commit() _\# фиксация изменений_

**3.3. Базовые запросы**

**Чтение данных:**

python

_\# Получить всех пользователей_

users = session.query(User).all()

_\# Получить первого пользователя с именем "Alice"_

user = session.query(User).filter(User.name == "Alice").first()

_\# Фильтрация с условиями_

users = session.query(User).filter(User.age > 30).all()

_\# Сортировка_

users = session.query(User).order_by(User.name).all()

**Создание и обновление:**

python

_\# Создание_

new_user = User(name="John", email="john@example.com")

session.add(new_user)

session.commit()

_\# Обновление_

user = session.query(User).filter(User.name == "John").first()

user.email = "new_email@example.com"

session.commit()

_\# Удаление_

session.delete(user)

session.commit()

**3.4. Пул соединений**

**Пул соединений** — это механизм, который поддерживает открытые соединения с БД для повторного использования, вместо создания нового при каждом запросе .

**Преимущества пула:**

- Снижение накладных расходов на установку соединений
- Ограничение максимального числа одновременных соединений
- Управление временем жизни соединений

**Настройка пула через** create_engine**:**

python

engine = create_engine(

"postgresql+psycopg2://...",

pool_size=20, _\# размер пула_

max_overflow=10, _\# доп. соединения сверх pool_size_

pool_timeout=30, _\# таймаут ожидания соединения_

pool_recycle=3600 _\# пересоздание соединений через час_

)

**4\. Миграции с Alembic**

**4.1. Миграции**

При разработке приложения структура базы данных меняется: добавляются новые таблицы, изменяются поля. **Миграции** — это инструмент для управления этими изменениями, который :

- Автоматизирует изменения в структуре БД
- Хранит историю изменений (как Git, но для БД)
- Позволяет откатывать изменения, если что-то пошло не так
- Синхронизирует базу данных у всех членов команды

**4.2. Настройка Alembic**

bash

_\# Установка_

pip install alembic

_\# Инициализация_

alembic init alembic

**Настройка** alembic.ini**:**

ini

sqlalchemy.url = postgresql+psycopg2://user:password@localhost:5432/mydb

**Настройка** env.py**:** необходимо указать target_metadata — метаданные ваших моделей SQLAlchemy .

python

_\# env.py_

from myapp.models import Base _\# импорт базового класса_

target_metadata = Base.metadata

**4.3. Рабочий процесс с миграциями**

**Шаг 1.** Изменяем модели (models.py):

python

class User(Base):

\__tablename__ = 'users'

id = Column(Integer, primary_key=True)

name = Column(String(50))

age = Column(Integer, nullable=True) _\# новое поле_

**Шаг 2.** Генерируем миграцию:

bash

alembic revision --autogenerate -m "Add age column to users"

**Шаг 3.** Применяем миграцию:

bash

alembic upgrade head

**4.4. Структура миграции**

Файл миграции содержит две функции :

python

def upgrade():

op.add_column('users', sa.Column('age', sa.Integer(), nullable=True))

def downgrade():

op.drop_column('users', 'age')

**4.5. Управление версиями**

bash

_\# Проверить текущую версию_

alembic current

_\# Откатить последнюю миграцию_

alembic downgrade -1

_\# Откатить к конкретной версии_

alembic downgrade &lt;revision_id&gt;

**4.6. Типичные ошибки**

| Ошибка | Решение |
| --- | --- |
| "Target database is not up to date" | Выполнить alembic upgrade head перед созданием новой миграции |
| Конфликты ревизий в команде | Использовать alembic merge для объединения миграций |
| Ошибка подключения к БД | Проверить sqlalchemy.url в alembic.ini |

**5\. Транзакции**

**5.1. Что такое транзакция?**

**Транзакция** — это логическая единица работы с базой данных, которая либо выполняется полностью, либо не выполняется вообще (атомарность). Транзакции обладают свойствами **ACID**.

**5.2. Управление транзакциями в SQLAlchemy**

**Режим "commit as you go"** — транзакция начинается автоматически при первом запросе и завершается явным вызовом commit() или rollback() :

python

with Session() as session:

session.add(user1)

session.add(user2)

session.commit() _\# фиксация всех изменений_

**Режим "begin once"** — транзакция управляется через контекстный менеджер :

python

with Session() as session:

with session.begin():

session.add(user1)

session.add(user2)

_\# транзакция автоматически фиксируется при выходе из блока_

**Обработка ошибок:**

python

with Session() as session:

try:

session.add(user)

session.commit()

except IntegrityError:

session.rollback()

raise ValueError("Пользователь с таким email уже существует")

**6\. Проблема N+1 запросов и её решение**

**6.1. Проблема N+1 запросов**

**Проблема N+1 запросов** — одна из самых известных ловушек при работе с ORM. Она возникает, когда сначала выполняется один запрос для получения списка объектов (1), а затем для каждого объекта выполняется отдельный запрос для загрузки связанных данных (N) .

**Пример возникновения проблемы:**

python

_\# 1 запрос: получаем всех пользователей_

users = session.query(User).all()

_\# N запросов: для каждого пользователя загружаем его посты_

for user in users:

print(user.posts) _\# каждый раз выполняется отдельный запрос!_

При 100 пользователях выполняется 101 запрос вместо одного.

**6.2. Влияние на производительность**

| Показатель | Без проблемы | С проблемой N+1 |
| --- | --- | --- |
| Количество запросов | 1   | N+1 |
| Время отклика | Малышое | Растёт линейно с N |
| Нагрузка на БД | Минимальная | Высокая (множество мелких запросов) |
| Масштабируемость | Хорошая | Плохая при росте данных |

**6.3. Решения проблемы**

**Решение 1. Жадная загрузка (Eager Loading) —** joinedload()

Загружает связанные данные одним запросом через JOIN :

python

from sqlalchemy.orm import joinedload

_\# Один запрос с JOIN_

users = session.query(User).options(joinedload(User.posts)).all()

for user in users:

print(user.posts) _\# данные уже загружены, запросов не будет_

**Решение 2. Подзапросная загрузка —** subqueryload()

Выполняет два запроса: первый для основных объектов, второй — для связанных данных через подзапрос :

python

from sqlalchemy.orm import subqueryload

users = session.query(User).options(subqueryload(User.posts)).all()

**Решение 3. Пакетная загрузка —** selectinload()

Выполняет два запроса, но для второго использует оператор IN с ID из первого запроса :

python

from sqlalchemy.orm import selectinload

users = session.query(User).options(selectinload(User.posts)).all()

**Рекомендация:** selectinload() часто оказывается наиболее эффективным для загрузки коллекций.

**6.4. Обнаружение проблемы**

- Используйте логирование SQL-запросов (echo=True в create_engine)
- Используйте расширения для обнаружения N+1 (например, nplusone для Django, аналогичные инструменты для FastAPI)

**7\. Практические рекомендации**

| Тема | Ключевые выводы |
| --- | --- |
| **SQLAlchemy** | Гибкая ORM, требующая явной настройки, но дающая полный контроль |
| **Модели** | Классы, наследующие от Base, с определением таблиц, полей и связей |
| **Сессии** | Рабочая область для взаимодействия с БД, управляет транзакциями и кэшированием |
| **Пул соединений** | Управляет повторным использованием соединений с БД для повышения производительности |
| **Alembic** | Инструмент для управления миграциями — автоматическая генерация и применение изменений |
| **Транзакции** | Обеспечивают атомарность операций, управляются через commit() и rollback() |
| **N+1 проблема** | Возникает при ленивой загрузке связанных данных; решается через joinedload(), selectinload() или subqueryload() |

**8\. Ссылки на материалы**

Документация

- [Git Book](https://git-scm.com/book/ru/v2)
- [GitHub Actions](https://docs.github.com/actions)
- [pytest](https://docs.pytest.org/)
- [ruff](https://docs.astral.sh/ruff/)
- [pre-commit](https://pre-commit.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)

**9\. Примеры**

- [Примеры .gitignore](https://github.com/github/gitignore)
- [GitHub Actions для Python](https://github.com/actions/starter-workflows/tree/main/ci)

**10\. Вопросы для самопроверки:**

1.  В чём разница между Core и ORM уровнями SQLAlchemy?
2.  Что такое сессия (Session) в SQLAlchemy и какие задачи она выполняет?
3.  Для чего нужны миграции и какую роль в них выполняет Alembic?
4.  Опишите последовательность команд для создания и применения миграции после изменения модели.
5.  Что такое транзакция и какими свойствами (ACID) она обладает?
6.  Чем отличается commit() от rollback() и как они используются при обработке ошибок?
7.  Зачем нужен пул соединений и какие параметры его настройки (pool_size, max_overflow) существуют?
8.  Какая ошибка возникает при превышении лимитов пула соединений?
9.  В чём суть проблемы N+1 запросов? Приведите пример её возникновения.
10. Какие существуют стратегии решения проблемы N+1? Чем selectinload отличается от joinedload и subqueryload?