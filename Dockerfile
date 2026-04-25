FROM python:3.12-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir -U pip setuptools wheel

# Copy project files
COPY . .

# Install project dependencies
RUN pip install --no-cache-dir -e .

# Install development dependencies for alembic
RUN pip install --no-cache-dir alembic

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
