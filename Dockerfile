# ==================== ETAPA DE CONSTRUCCIÓN ====================
FROM python:3.11-slim-bullseye as builder

# Configura variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependencias del sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Crea directorio de trabajo
WORKDIR /app

# Instala dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


# ==================== ETAPA DE PRODUCCIÓN ====================
FROM python:3.11-slim-bullseye

# Configura variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/root/.local/bin:${PATH}"

# Crea usuario no-root para mayor seguridad
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Crea directorio de trabajo y establece permisos
WORKDIR /app
RUN chown appuser:appuser /app
USER appuser

# Copia dependencias instaladas desde la etapa de construcción
COPY --chown=appuser:appuser --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .

# Expone el puerto de la aplicación
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["newrelic-admin", "run-program", "python", "src/main.py"]


