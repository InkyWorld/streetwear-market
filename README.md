# Streetwear Market API

E-commerce Web API for streetwear and sneakers market. Built with FastAPI, SQLAlchemy, and PostgreSQL.

## Technology Stack

- **Python**: 3.12+
- **Framework**: FastAPI
- **Database ORM**: SQLAlchemy 2.0 (async)
- **Database**: PostgreSQL
- **Package Manager**: uv
- **Migrations**: Alembic
- **Validation**: Pydantic v2
- **Testing**: pytest + httpx + pytest-asyncio
- **Code Quality**: ruff + black + mypy

## Architecture

The project follows a layered architecture:

```
app/
├── api/              # API routers and endpoints
├── services/         # Business logic layer
├── repositories/     # Data access layer
├── models/          # SQLAlchemy ORM models
├── schemas/         # Pydantic DTO schemas
├── domain/          # Domain exceptions
└── core/            # Configuration and database setup
```

## Prerequisites

- Python 3.12 or higher
- PostgreSQL 13+
- uv package manager

## Setup

### 1. Install dependencies

```bash
uv sync
```

### 2. Configure environment

Copy `.env.example` to `.env` and update with your database credentials:

```bash
cp .env.example .env
```

Edit `.env`:

```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/streetwear_market
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=True
```

### 3. Create database

Ensure PostgreSQL is running and create the database:

```bash
createdb streetwear_market
```

### 4. Run migrations

```bash
uv run alembic upgrade head
```

## Running the Application

### Development Mode

```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the application is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing

### Run all tests

```bash
uv run pytest
```

### Run specific test file

```bash
uv run pytest tests/integration/test_product_crud.py
```

### Run with coverage

```bash
uv run pytest --cov=app
```

## Code Quality

### Format code

```bash
uv run black app tests
```

### Lint code

```bash
uv run ruff check app tests
```

### Type checking

```bash
uv run mypy app
```

### All checks together

```bash
uv run black app tests && uv run ruff check app tests && uv run mypy app && uv run pytest
```

## API Endpoints

### Product Endpoints

- `GET /api/product` - List all products
- `GET /api/product/{id}` - Get product by ID
- `POST /api/product` - Create new product
- `PUT /api/product/{id}` - Update product
- `DELETE /api/product/{id}` - Delete product

### Catalog Endpoints

- `GET /api/catalog` - List all catalogs
- `GET /api/catalog/{id}` - Get catalog by ID
- `POST /api/catalog` - Create new catalog

### Brand Endpoints

- `GET /api/brand` - List all brands
- `GET /api/brand/{id}` - Get brand by ID
- `POST /api/brand` - Create new brand

### Customer Endpoints

- `GET /api/customer` - List all customers
- `GET /api/customer/{id}` - Get customer by ID
- `POST /api/customer` - Create new customer

### Order Endpoints

- `GET /api/order` - List all orders
- `GET /api/order/{id}` - Get order by ID
- `POST /api/order` - Create new order
- `GET /api/order/customer/{customer_id}` - List orders for a specific customer

### Health Check

- `GET /health` - Health check endpoint

## Example Requests

### Create a Catalog

```bash
curl -X POST http://localhost:8000/api/catalog \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sneakers",
    "description": "Athletic footwear"
  }'
```

### Create a Brand

```bash
curl -X POST http://localhost:8000/api/brand \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nike",
    "description": "Sportswear brand"
  }'
```

### Create a Product

```bash
curl -X POST http://localhost:8000/api/product \
  -H "Content-Type: application/json" \
  -d '{
    "sku": "NIKE-AIR-001",
    "name": "Nike Air Max 90",
    "description": "Classic sneaker",
    "price": 150.0,
    "currency": "USD",
    "size": "10",
    "color": "White",
    "season": "SS",
    "in_stock": true,
    "category_id": 1,
    "brand_id": 1
  }'
```

### Create a Customer

```bash
curl -X POST http://localhost:8000/api/customer \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890"
  }'
```

### Create an Order

```bash
curl -X POST http://localhost:8000/api/order \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "items": [
      {
        "product_id": 1,
        "quantity": 2
      }
    ]
  }'
```

### Get Order

```bash
curl -X GET http://localhost:8000/api/order/1 \
  -H "Content-Type: application/json"
```

### List Customer Orders

```bash
curl -X GET "http://localhost:8000/api/order/customer/1" \
  -H "Content-Type: application/json"
```

## Project Structure

```
streetwear-market/
├── app/
│   ├── api/                    # API routers
│   │   ├── product_router.py   # Product endpoints
│   │   ├── catalog_router.py   # Catalog endpoints
│   │   ├── brand_router.py     # Brand endpoints
│   │   ├── customer_router.py  # Customer endpoints
│   │   └── order_router.py     # Order endpoints
│   ├── services/               # Business logic
│   │   ├── product.py          # Product service
│   │   ├── catalog.py          # Catalog service
│   │   ├── brand.py            # Brand service
│   │   ├── customer.py         # Customer service
│   │   ├── order.py            # Order service
│   │   └── __init__.py
│   ├── repositories/           # Data access
│   │   ├── product.py          # Product repository
│   │   ├── catalog.py          # Catalog repository
│   │   ├── brand.py            # Brand repository
│   │   ├── customer.py         # Customer repository
│   │   ├── order.py            # Order repository
│   │   ├── base.py             # Base repository
│   │   └── __init__.py
│   ├── models/                 # Database models
│   │   ├── product.py          # Product model
│   │   ├── catalog.py          # Catalog model
│   │   ├── brand.py            # Brand model
│   │   ├── customer.py         # Customer model
│   │   ├── order.py            # Order and OrderItem models
│   │   ├── base.py             # Base model
│   │   └── __init__.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── product.py          # Product DTO
│   │   ├── catalog.py          # Catalog DTO
│   │   ├── brand.py            # Brand DTO
│   │   ├── customer.py         # Customer DTO
│   │   ├── order.py            # Order DTO
│   │   └── __init__.py
│   ├── domain/                 # Domain layer
│   │   └── exceptions.py       # Custom exceptions
│   └── core/                   # Core configuration
│       ├── config.py           # Settings
│       └── database.py         # Database connection
├── alembic/                    # Database migrations
│   ├── versions/
│   │   ├── 001_initial_schema.py        # Product, Catalog, Brand
│   │   └── 002_add_customer_order_schema.py  # Customer, Order, OrderItem
│   ├── env.py                  # Alembic environment
│   └── script.py.mako          # Migration template
├── tests/
│   ├── unit/                   # Unit tests
│   │   ├── test_customer_order_models.py
│   │   └── test_customer_order_schemas.py
│   ├── integration/            # Integration tests
│   │   ├── test_product_crud.py
│   │   ├── test_customer_crud.py
│   │   └── test_order_crud.py
│   └── conftest.py             # Pytest fixtures
├── main.py                     # FastAPI application entry point
├── pyproject.toml              # Project dependencies
├── .env.example                # Environment variables template
├── alembic.ini                 # Alembic configuration
└── README.md                   # This file
```

## Development Workflow

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Run code quality checks: `uv run black app tests && uv run ruff check app tests`
4. Run tests: `uv run pytest`
5. Commit with descriptive message: `git commit -m "Add feature description"`
6. Push and create a pull request

## Git Commit Policy

Each completed logical step should be committed with clear, descriptive English messages:

```
Initialize project structure
Configure uv environment
Add async database session factory
Implement product repository CRUD methods
Add integration tests for product conflict scenarios
```

## Error Handling

The API returns standardized error responses:

- `400 Bad Request`: Invalid request format
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource conflict (e.g., duplicate SKU)
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

Error response format:

```json
{
  "detail": "Error message",
  "error_type": "ErrorClassName"
}
```

## License

This project is part of a practical assignment for e-commerce API development.
