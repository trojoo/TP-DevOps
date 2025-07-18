import os
from flask import Flask, jsonify, request
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from werkzeug.exceptions import HTTPException


APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
print(f"Initializing Sentry with release: {APP_VERSION}")

# Inicializar Sentry
sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[FlaskIntegration()],
    release=APP_VERSION,
    auto_session_tracking=True,
    attach_stacktrace=True,
    request_bodies="medium",
    send_client_reports=True,
    traces_sample_rate=1.0,
    environment=os.environ.get('FLASK_ENV', 'production')
)

app = Flask(__name__)


# Base de datos en memoria
books = [
    {"id": 1, "title": "El Principito", "author": "Antoine de Saint-Exupéry"},
    {"id": 2, "title": "Cien años de soledad", "author": "Gabriel García Márquez"},
    {"id": 3, "title": "El Peregrino", "author": "Paulo Coelho"},
    {"id": 4, "title": "Big data con python: Recolección, almacenamiento y proceso", "author": "Adrián Riesco Rodríguez,"}
]
next_id = 5

# Health Check Endpoint
@app.route('/health')
def health_check():
    sentry_ok = bool(os.environ.get('SENTRY_DSN')) 
    return jsonify({
        "status": "healthy",
        "sentry": "configured" if sentry_ok else "missing_dsn"
    }), 200


@app.route('/version')
def show_version():
    return {
        "docker_version": os.getenv("APP_VERSION", "missing"),
        "sentry_release": sentry_sdk.Hub.current.client.options['release'] if sentry_sdk.Hub.current.client else "sentry_not_initialized"
    }, 200    

# Obtener todos los libros
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)


# Nuevo endpoint: Obtener libro aleatorio
@app.route('/books/random', methods=['GET'])
def get_random_book():
    if not books:
        return jsonify({"error": "No hay libros disponibles"}), 404
    
    random_book = random.choice(books)
    return jsonify(random_book)


# Obtener un libro por ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if b['id'] == book_id), None)
    if book:
        return jsonify(book)
    return jsonify({"error": "Libro no encontrado"}), 404

# Crear un nuevo libro
@app.route('/books', methods=['POST'])
def create_book():
    global next_id
    data = request.get_json()
    
    if not data or 'title' not in data or 'author' not in data:
        return jsonify({"error": "Datos incompletos"}), 400
    
    new_book = {
        "id": next_id,
        "title": data['title'],
        "author": data['author']
    }
    next_id += 1
    books.append(new_book)
    return jsonify(new_book), 201

# Actualizar un libro existente
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    book = next((b for b in books if b['id'] == book_id), None)
    
    if not book:
        return jsonify({"error": "Libro no encontrado"}), 404
    
    if 'title' in data:
        book['title'] = data['title']
    if 'author' in data:
        book['author'] = data['author']
    
    return jsonify(book)

# Eliminar un libro
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    initial_length = len(books)
    books = [b for b in books if b['id'] != book_id]
    
    if len(books) < initial_length:
        return jsonify({"message": "Libro eliminado correctamente"}), 200
    return jsonify({"error": "Libro no encontrado"}), 404

# Endpoint para generar errores intencionales
@app.route('/error', methods=['GET'])
def trigger_error():
    try:
        1 / 0
    except Exception as e:
        app.logger.error(f"Error captured: {str(e)}")  # Log local
        sentry_sdk.capture_exception(e)
        return jsonify({"error": str(e)}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    # Reportar a Sentry
    sentry_sdk.capture_exception(e)
    
    # Manejar errores HTTP
    if isinstance(e, HTTPException):
        return e
    
    # Manejar otros errores
    return jsonify({"error": "Internal Server Error"}), 500    


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    # Deshabilitar Sentry en modo desarrollo
    if debug:
        sentry_sdk.init(dsn="")
    
    app.run(host='0.0.0.0', port=port, debug=debug)    