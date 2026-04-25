# Plan 1.1 — Детальний план для Учасника 1 (Backend/API Lead)

## 0) Мета Учасника 1
Побудувати основний backend-каркас і повністю реалізувати Product CRUD за шаровою архітектурою з Repository + Service + DTO, включно з тестами та документацією запуску.

## 0.1) Порядок виконання між учасниками (обов'язково)
1. Першу половину робіт повністю виконує Учасник 1.
2. Учасник 2 починає свою половину тільки після завершення чеклиста Учасника 1.
3. Передача робіт відбувається через чіткий handoff: стабільна main-гілка, проходження всіх тестів, оновлена документація.

## 0.2) Обов'язкові правила командної роботи
1. Єдине віртуальне оточення та менеджер залежностей: uv.
2. Кожна завершена дія фіксується окремим git-комітом.
3. Усі commit messages мають бути англійською, змістовними та конкретними.
4. Перед кожним комітом обов'язково запускати тести і перевірки якості коду.

## 0.3) Спрощена структура проєкту (зона Учасника 1)
Базова структура (спільна для команди):
- app/api
- app/services
- app/repositories
- app/domain
- app/models
- app/schemas
- app/core
- tests/unit
- tests/integration
- alembic/versions
- docs

Що саме робить Учасник 1 у цій структурі:
1. app/models:
   - створює Product, Catalog, Brand (базові ORM-моделі)
2. app/schemas:
   - ProductCreateDTO, ProductUpdateDTO, ProductReadDTO, ProductListItemDTO
3. app/repositories:
   - ProductRepository (CRUD + перевірка унікальності SKU)
   - базовий CatalogRepository (list/get/create)
4. app/services:
   - ProductService (get/create/update/delete)
   - базовий CatalogService
5. app/api:
   - product_router.py (повний CRUD)
   - catalog_router.py (GET list, GET by id, POST)
6. app/core:
   - config, db session, dependency wiring, error mapping
7. tests:
   - unit: правила/валідація Product
   - integration: Product CRUD + негативні сценарії

Послідовність реалізації (що і як):
1. Спочатку моделі + міграції.
2. Потім repositories.
3. Потім services (бізнес-правила).
4. Потім API routers.
5. Потім unit та integration тести до повного покриття.

## 1) Передстартовий етап
1. Підтвердити з командою фінальний стек (FastAPI, SQLAlchemy, PostgreSQL, Alembic).
2. У репозиторії створити базову структуру:
   - app/api
   - app/services
   - app/repositories
   - app/models
   - app/schemas
   - app/core
   - tests
3. Налаштувати залежності в pyproject.toml:
   - fastapi, uvicorn
   - sqlalchemy, asyncpg, alembic
   - pydantic-settings
   - pytest, pytest-asyncio, httpx
   - ruff, black, mypy
4. Ініціалізувати середовище через uv:
   - uv sync
   - uv run pytest (перевірка, що тести запускаються)
5. Створити .env.example з параметрами підключення до БД.
6. Додати README з командою запуску проєкту через uv.
7. Після кожного кроку зробити окремий коміт англійською (наприклад: "Initialize project structure", "Configure uv environment").

## 2) Конфігурація та інфраструктура
1. Реалізувати конфігурацію через settings-клас:
   - DATABASE_URL
   - APP_HOST, APP_PORT
   - DEBUG
2. Налаштувати async engine + session factory SQLAlchemy.
3. Додати dependency для отримання DB session у FastAPI.
4. Підключити Alembic до моделей та зробити стартову міграцію.
5. Перевірити підняття застосунку командою локального запуску через uv.
6. Зафіксувати кожен завершений підкрок окремим комітом англійською.

## 3) Домени й моделі (мінімум для інтеграції Product)
1. Створити ORM-моделі:
   - Product
   - Catalog (або Category)
   - Brand
2. Для Product додати поля:
   - id, sku, name, description
   - price, currency
   - category_id, brand_id
   - size, color, season, in_stock
   - created_at, updated_at
3. Описати зв'язки:
   - Product -> Catalog (many-to-one)
   - Product -> Brand (many-to-one)
4. Згенерувати і застосувати міграцію.

## 4) DTO/Schema-шар
1. Створити Pydantic-схеми:
   - ProductCreateDTO
   - ProductUpdateDTO
   - ProductReadDTO
   - ProductListItemDTO
2. Валідація:
   - price > 0
   - sku не порожній
   - name мінімальна довжина
3. Уніфікувати формат помилок валідації (стандарт FastAPI + власні повідомлення сервісу).

## 5) Repository Layer
1. Описати контракт ProductRepository:
   - get_by_id
   - list (із фільтрами, якщо встигнете)
   - create
   - update
   - delete
2. Реалізувати SQLAlchemy-репозиторій.
3. Додати перевірку унікальності sku.
4. Повернення None/Result обробляти передбачувано, без винятків у контролерах.

## 6) Service Layer
1. Створити ProductService:
   - get_product
   - create_product
   - update_product
   - delete_product
2. Бізнес-правила:
   - SKU унікальний
   - ціна не від'ємна
   - заборонити оновлення неіснуючого продукту
3. Кидати доменні помилки (наприклад NotFoundError, ConflictError), які мапляться на HTTP-коди.

## 7) API Layer (контролери)
1. Реалізувати endpoint-и:
   - GET /api/product/{id}
   - POST /api/product
   - PUT /api/product/{id}
   - DELETE /api/product/{id}
2. Для сумісності з вимогами додати:
   - GET /api/catalog
   - GET /api/catalog/{id}
   - POST /api/catalog
3. HTTP-коди:
   - GET 200
   - POST 201
   - PUT 200
   - DELETE 204
   - 404 для not found
   - 409 для конфліктів
4. Перевірити коректну OpenAPI-специфікацію.

## 8) Тестування (обов'язково)
1. Налаштувати тестову БД (окрема схема/окремий контейнер).
2. Написати інтеграційні тести для Product CRUD:
   - create -> get -> update -> delete
3. Негативні кейси:
   - get неіснуючого id -> 404
   - duplicate sku -> 409
   - невалідна ціна -> 422
4. Додати edge-case сценарії:
   - порожні/граничні значення полів
   - паралельні або повторні запити на створення з однаковим SKU
   - часткові оновлення, які не повинні ламати валідні дані
5. Забезпечити повне покриття коду зони Учасника 1 тестами в різних сценаріях (unit + integration).
6. Досягти стабільного проходження тестів перед merge.
7. Комітити кожне розширення тестів окремим англомовним комітом.

## 9) Git-процес і внесок
1. Працювати у feature-гілках:
   - feature/backend-setup
   - feature/product-crud
2. Кожен pull request:
   - короткий опис
   - що перевірено локально
   - чеклист виконаних вимог
3. Не пушити зламані тести у main.
4. Правило granular commits: одна завершена дія = один коміт.
5. Приклади якісних commit messages англійською:
   - Add async database session factory
   - Implement product repository CRUD methods
   - Add integration tests for product conflict scenarios

## 10) Календар на 2 тижні
### Тиждень 1
1. День 1-2: каркас, залежності, конфіг, БД.
2. День 3-4: моделі + міграції.
3. День 5-7: репозиторій і сервіс Product.

### Тиждень 2
1. День 8-9: API endpoint-и Product + Catalog.
2. День 10-11: тести Product CRUD.
3. День 12: обробка помилок, стабілізація.
4. День 13: рев'ю з учасником 2, інтеграція.
5. День 14: фінальна перевірка, демо.

## 11) Чеклист готовності Учасника 1
- Product CRUD повністю реалізований.
- Міграції застосовуються з нуля.
- Локальний запуск описаний і відтворюється.
- Є повне покриття коду тестами в різних сценаріях: позитивні, негативні, edge-case, валідація, конфлікти.
- Код пройшов lint/format/tests.
- Середовище та команди запуску працюють через uv.
- Усі кроки зафіксовані послідовними англомовними комітами.
- Оформлено handoff для Учасника 2 (документація + стабільний стан main).
