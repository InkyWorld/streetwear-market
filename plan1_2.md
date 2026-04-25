# Plan 1.2 — Детальний план для Учасника 2 (Domain/Integration & QA)

## 0) Мета Учасника 2
Закрити функціональність Catalog, Customer, Order та забезпечити інтеграційну якість рішення, щоб проєкт відповідав вимогам лабораторної і був готовий до демонстрації.

## 0.1) Умова старту Учасника 2 (обов'язково)
1. Учасник 2 починає роботу тільки після повного завершення блоку Учасника 1.
2. Обов'язковий handoff від Учасника 1: зелений тест-ран, актуальна документація, стабільна main-гілка.
3. Учасник 2 виконує другу половину робіт без дублювання реалізованих модулів Учасника 1.

## 0.2) Обов'язкові правила командної роботи
1. Єдине віртуальне оточення та менеджер залежностей: uv.
2. Кожну завершену дію фіксувати окремим git-комітом.
3. Усі commit messages писати англійською, чітко по суті змін.
4. Перед кожним комітом проганяти тести та базові перевірки якості.

## 0.3) Спрощена структура проєкту (зона Учасника 2)
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

Що саме робить Учасник 2 у цій структурі:
1. app/models:
   - Customer, Order, OrderItem, Catalog (якщо не завершено Учасником 1)
2. app/schemas:
   - CustomerCreateDTO/ReadDTO
   - OrderCreateDTO/ReadDTO
   - CatalogCreateDTO/ReadDTO (за потреби доповнення)
3. app/repositories:
   - CustomerRepository
   - OrderRepository (create_with_items, list, get_by_id)
   - CatalogRepository (за потреби розширення)
4. app/services:
   - CustomerService
   - OrderService (перевірки customer/product, total_amount)
   - CatalogService (за потреби)
5. app/api:
   - customer_router.py
   - order_router.py
   - доповнення catalog_router.py
6. app/domain:
   - базові перевірки інваріантів замовлення (quantity > 0, items not empty)
7. tests:
   - unit: валідація DTO/правила сервісу
   - integration: customer/order/cross-entity сценарії

Послідовність реалізації (що і як):
1. Прийняти handoff від Учасника 1 і зафіксувати контракти.
2. Реалізувати моделі та міграції своєї зони.
3. Додати repositories.
4. Додати services з бізнес-правилами.
5. Підключити API endpoints.
6. Закрити unit + integration тести до повного покриття.

## 1) Підготовка і синхронізація
1. Узгодити з Учасником 1:
   - naming endpoint-ів
   - структуру DTO
   - формат помилок
   - правила транзакцій
2. Перевірити структуру гілок і домовитись про інтеграційні точки (щонайменше 2 проміжні merge).
3. Підтвердити спільну схему БД і naming conventions.
4. Підтвердити, що локальне середовище запущене через uv (uv sync, uv run pytest).
5. Зафіксувати кожен завершений крок окремим англомовним комітом.

## 2) Моделі та міграції (зона Учасника 2)
1. Створити ORM-моделі:
   - Catalog (або Category)
   - Customer
   - Order
   - OrderItem
2. Додати ключові поля:
   - Catalog: id, name, slug, description
   - Customer: id, full_name, email, phone
   - Order: id, customer_id, status, total_amount, created_at
   - OrderItem: id, order_id, product_id, quantity, unit_price
3. Налаштувати зовнішні ключі та індекси (email, slug, status).
4. Створити та прогнати міграції Alembic.

## 3) DTO та валідація
1. Catalog DTO:
   - CatalogCreateDTO, CatalogReadDTO
2. Customer DTO:
   - CustomerCreateDTO, CustomerReadDTO
3. Order DTO:
   - OrderCreateDTO (список items), OrderReadDTO
4. Перевірки:
   - email формат
   - quantity > 0
   - customer/product існують
   - список позицій замовлення не порожній

## 4) Repository Layer
1. CatalogRepository:
   - list, get_by_id, create
2. CustomerRepository:
   - list, get_by_id, create
3. OrderRepository:
   - list, get_by_id, create_with_items
4. Додати атомарність для операції create order (через транзакцію).

## 5) Service Layer
1. CatalogService:
   - list_catalogs, get_catalog, create_catalog
2. CustomerService:
   - list_customers, get_customer, create_customer
3. OrderService:
   - list_orders, get_order, create_order
4. Бізнес-правила OrderService:
   - перевірка існування клієнта
   - перевірка існування продуктів
   - перевірка наявності на складі
   - обчислення total_amount
   - збереження order + order items однією транзакцією

## 6) API Layer
1. Реалізувати endpoint-и Catalog:
   - GET /api/catalog
   - GET /api/catalog/{id}
   - POST /api/catalog
2. Реалізувати endpoint-и Customer:
   - GET /api/customer
   - GET /api/customer/{id}
   - POST /api/customer
3. Реалізувати endpoint-и Order:
   - GET /api/order
   - GET /api/order/{id}
   - POST /api/order
4. Стандартизувати HTTP-коди:
   - GET 200
   - POST 201
   - 404 not found
   - 409 conflict (якщо доречно)
   - 422 validation
5. Кожен завершений endpoint-комплект комітити окремим комітом англійською.

## 7) Інтеграція з модулем Product
1. Використати ProductRepository/Service контракт Учасника 1 без дублювання логіки.
2. Узгодити формат product snapshot в OrderItem (ціна на момент замовлення).
3. Перевірити сумісність міграцій і порядок їх застосування.
4. Після інтеграції виконати smoke-тести всіх endpoint-ів.

## 8) Тестування (обов'язково)
1. Написати тести для Catalog:
   - create + list + get_by_id
2. Написати тести для Customer:
   - create + list + get_by_id
3. Написати тести для Order:
   - успішне створення
   - помилка при неіснуючому product_id
   - помилка при quantity <= 0
4. Інтеграційний бізнес-сценарій:
   - створити catalog
   - створити product
   - створити customer
   - створити order
   - перевірити total_amount і склад позицій
5. Додати edge-case сценарії:
   - порожній список items
   - дубльовані позиції в одному замовленні
   - невалідний email клієнта
6. Забезпечити повне покриття коду зони Учасника 2 тестами в різних сценаріях (unit + integration + contract).
7. Комітити кожен блок тестів окремим англомовним комітом.

## 9) Документація і демо-підготовка
1. Оновити README:
   - які модулі реалізував Учасник 2
   - приклади request/response для Catalog/Customer/Order
2. Підготувати короткий демо-сценарій на 5-7 хв:
   - створення клієнта
   - створення замовлення
   - перевірка отримання замовлення
3. Зафіксувати відомі обмеження (що лишається на наступні ітерації).

## 10) Календар на 2 тижні
### Тиждень 1
1. День 1-2: моделі Catalog/Customer/Order/OrderItem.
2. День 3-4: міграції + DTO.
3. День 5-7: repositories + services.

### Тиждень 2
1. День 8-9: API endpoint-и.
2. День 10-11: інтеграція з Product.
3. День 12-13: інтеграційні та негативні тести.
4. День 14: документація і демо.

## 11) Чеклист готовності Учасника 2
- Реалізовані Catalog/Customer/Order API згідно вимог.
- Замовлення створюється транзакційно і рахує суму коректно.
- Є повне покриття коду тестами в різних сценаріях: позитивні, негативні, edge-case, інтеграційні та контрактні.
- Документація оновлена, демо-сценарій підготовлений.
- Усі команди запуску виконуються через uv.
- Кожна завершена дія закомічена окремим якісним commit message англійською.

## 12) Remaining to DoD
- [x] Додати інтеграційні тести для Catalog: create + list + get_by_id.
- [x] Закрити edge-case тест для дубльованих позицій у одному Order (і зафіксувати очікувану поведінку).
- [x] Підтвердити повне покриття зони Учасника 2 через coverage report і закрити прогалини.
- [x] Додати/перевірити contract tests для сумісності з Product-модулем.
- [x] Оновити README прикладами request/response для Catalog, Customer, Order.
- [x] Підготувати демо-сценарій 5-7 хв: create customer -> create order -> get order.
- [x] Зафіксувати known limitations у документації.
- [x] Вирівняти середовище під вимогу запуску через uv (uv sync, uv run pytest).
- [ ] Кожен завершений блок доробок комітити окремим англомовним commit message.
