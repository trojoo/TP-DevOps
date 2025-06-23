# ==================== ETAPA DE CONSTRUCCIÓN ====================
FROM python:3.11-slim-bullseye as builder

# Configura variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependencias del sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ==================== ETAPA DE PRODUCCIÓN ====================
FROM python:3.11-slim-bullseye

ARG APP_VERSION=1.0.0

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT=5000
ENV SENTRY_DSN=""
# Usa el argumento aquí
ENV APP_VERSION=$APP_VERSION

RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Crea usuario no-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

RUN mkdir -p /app/src && chown -R appuser:appuser /app
WORKDIR /app
USER appuser

COPY --chown=appuser:appuser --from=builder /root/.local /home/appuser/.local

COPY --chown=appuser:appuser src/ ./src

# Añade .local al PATH
ENV PATH="/home/appuser/.local/bin:${PATH}"

EXPOSE $PORT

CMD ["sh", "-c", "gunicorn -w 4 -b 0.0.0.0:$PORT src.main:app"]