# ==================== ETAPA DE CONSTRUCCIÓN ====================
FROM python:3.11-slim-bullseye as builder

# Configura variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependencias del sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Crea directorio de trabajo
WORKDIR /app

# Copia e instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ==================== ETAPA DE PRODUCCIÓN ====================
FROM python:3.11-slim-bullseye

# Configura variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT=5000

# Instala dependencias mínimas del sistema
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Crea usuario no-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Crea estructura de directorios
RUN mkdir -p /app/src && chown -R appuser:appuser /app
WORKDIR /app
USER appuser

# Copia dependencias instaladas
COPY --chown=appuser:appuser --from=builder /root/.local /home/appuser/.local

# Copia código fuente
COPY --chown=appuser:appuser src/ ./src

# Añade .local al PATH
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Expone el puerto
EXPOSE $PORT

# Comando para ejecutar la aplicación
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:$PORT", "src.main:app"]