# syntax=docker/dockerfile:1
FROM python:3.13-slim

# Dependencias del sistema necesarias para WeasyPrint y psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY . .

# Recolectar estáticos (SECRET_KEY temporal solo para este paso)
RUN SECRET_KEY=build-only-secret python manage.py collectstatic --no-input

EXPOSE 8000

CMD ["gunicorn", "edgecom.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
