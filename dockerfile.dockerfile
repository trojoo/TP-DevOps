# Etapa 1: build (innecesaria si no hay compilación, pero se deja claro por estructura)
FROM python:3.11-slim as builder

# Seteo de variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Carpeta de trabajo
WORKDIR /app

# Instalo dependencias
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copio el resto de la app
COPY . .

# Etapa final
FROM python:3.11-slim

WORKDIR /app

# Copio la app ya preparada
COPY --from=builder /app /app

# Expongo puerto (si usás Flask)
EXPOSE 5000

# Comando de ejecución (ajustar si usás Flask o similar)
CMD ["python", "tp_devops.py"]