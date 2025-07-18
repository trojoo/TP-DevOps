API DE GESTIÓN DE LIBROS CON FLASK
==================================

Este proyecto es una API REST desarrollada en Python utilizando Flask. 
Permite gestionar libros mediante operaciones CRUD y está preparada 
para entornos de desarrollo, testing y producción.

FUNCIONALIDADES PRINCIPALES
---------------------------
- Obtener todos los libros
- Buscar libro por ID
- Crear nuevo libro
- Actualizar libro existente
- Eliminar libro
- Health Check (/health)
- Versión de la app (/version)
- Simulación de errores (/error)
- Monitoreo de errores con Sentry


ESTRUCTURA DEL PROYECTO
------------------------
.github/workflows/      → Workflows de GitHub Actions (CI)
src/                    → Código fuente principal (Flask app)
tests/                  → Pruebas automatizadas con pytest
Dockerfile              → Imagen Docker de la app
docker-compose.yml      → Orquestación de servicios (si aplica)
requirements.txt        → Dependencias de Python
pytest.ini              → Configuración de pytest
README.txt              → Este archivo

CÓMO CORRER LA APP
------------------

REQUISITOS:
- Python 3.11
- Docker (opcional)
- pip y venv (si no usás Docker)

OPCIÓN 1: Local con Python
--------------------------
python -m venv venv
source venv/bin/activate    (en Windows: venv\Scripts\activate)
pip install -r requirements.txt
export FLASK_ENV=development
python src/main.py

OPCIÓN 2: Con Docker
--------------------
docker build -t flask-libros .
docker run -p 5000:5000 flask-libros

OPCIÓN 3: Docker Compose
------------------------
docker-compose up --build

TESTS AUTOMATIZADOS
-------------------
El proyecto incluye tests con pytest.

Para correr tests localmente:
    pytest

Los tests también se ejecutan automáticamente en cada push o pull request 
gracias a GitHub Actions (.github/workflows/ci.yml).

MONITOREO CON SENTRY
---------------------
Para activar el monitoreo de errores, configurar la variable de entorno:
    export SENTRY_DSN="https://8583b3517d96fcef915a37c4c627cba4@o4509531922169856.ingest.us.sentry.io/4509532148531200"

ENDPOINTS DISPONIBLES
---------------------
GET     /books          → Obtener todos los libros
GET     /books/<id>     → Obtener libro por ID
POST    /books          → Crear nuevo libro
PUT     /books/<id>     → Actualizar libro existente
DELETE  /books/<id>     → Eliminar libro
GET     /health         → Verificar estado de la app
GET     /version        → Mostrar versión de la app
GET     /error          → Simular error para testear logs