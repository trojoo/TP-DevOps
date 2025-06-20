import os  # Agregar al inicio del archivo
from flask import Flask, jsonify, request
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from werkzeug.exceptions import HTTPException

# Inicializar Sentry
sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[FlaskIntegration()],
    release=os.environ.get('APP_VERSION', '1.0.0'),
    traces_sample_rate=1.0,
    send_default_pii=True,
    environment=os.environ.get('FLASK_ENV', 'production')
)

app = Flask(__name__)

# Base de datos en memoria
books = [
    {"id": 1, "title": "El Principito", "author": "Antoine de Saint-Exupéry"},
    {"id": 2, "title": "Cien años de soledad", "author": "Gabriel García Márquez"}
]
next_id = 3

# Health Check Endpoint
@app.route('/health')
def health_check():
    # Verificar conexión a Sentry
    sentry_ok = False
    if sentry_sdk.Hub.current.client:
        try:
            sentry_sdk.capture_message("Health check test")
            sentry_ok = True
        except:
            pass
    
    return jsonify({
        "status": "healthy",
        "sentry": "connected" if sentry_ok else "disabled"
    }), 200

# Obtener todos los libros
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

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
        # Generar una excepción de división por cero
        result = 1 / 0
    except Exception as e:
        # Capturar y reportar el error a Sentry
        sentry_sdk.capture_exception(e)
        return jsonify({"error": str(e)}), 500
        
    return jsonify({"result": result}), 200

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