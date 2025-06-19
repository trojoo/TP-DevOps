from flask import Flask, jsonify, request

app = Flask(__name__)

# Base de datos en memoria
books = [
    {"id": 1, "title": "El Principito", "author": "Antoine de Saint-Exupéry"},
    {"id": 2, "title": "Cien años de soledad", "author": "Gabriel García Márquez"}
]
next_id = 3

# Health Check Endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "La aplicación está funcionando correctamente"}), 200

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

if __name__ == '__main__':
    app.run(debug=True)