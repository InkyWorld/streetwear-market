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

## Project Structure

```
streetwear-market/
├── app/
│   ├── api/                    # API routers
│   │   ├── product_router.py   # Product endpoints
│   │   └── catalog_router.py   # Catalog endpoints
│   ├── services/               # Business logic
│   │   └── __init__.py         # Services (Product, Catalog, Brand)
│   ├── repositories/           # Data access
│   │   └── __init__.py         # Repositories
│   ├── models/                 # Database models
│   │   └── __init__.py         # Product, Catalog, Brand models
│   ├── schemas/                # Pydantic schemas
│   │   └── __init__.py         # DTOs for all models
│   ├── domain/                 # Domain layer
│   │   └── exceptions.py       # Custom exceptions
│   └── core/                   # Core configuration
│       ├── config.py           # Settings
│       └── database.py         # Database connection
├── alembic/                    # Database migrations
│   ├── versions/               # Migration files
│   ├── env.py                  # Alembic environment
│   └── script.py.mako          # Migration template
├── tests/
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
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
