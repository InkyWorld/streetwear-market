"""Main FastAPI application."""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api import brand_router, catalog_router, customer_router, order_router, product_router
from app.core.config import settings
from app.domain.exceptions import AppException

# Create FastAPI app
app = FastAPI(
    title="Streetwear Market API",
    description="E-commerce Web API for streetwear and sneakers",
    version="0.1.0",
    debug=settings.is_debug,
)


# Exception handlers
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """Handle application exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message, "error_type": exc.__class__.__name__},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": exc.errors(),
        },
    )


# Health check endpoint
@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


# Include routers
app.include_router(product_router.router)
app.include_router(catalog_router.router)
app.include_router(brand_router.router)
app.include_router(customer_router.router)
app.include_router(order_router.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.is_debug,
    )
