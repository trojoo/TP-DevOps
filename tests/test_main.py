import pytest
import sys
import os

# Añadir src al path para importaciones
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Import from src package instead of directly
from src import main  # Import the main module to reset state
from src.main import app as flask_app  # Import app from src.main

@pytest.fixture(autouse=True)
def reset_state():
    """Fixture to reset application state before each test"""
    # Reset books to initial state
    main.books = [
        {"id": 1, "title": "El Principito", "author": "Antoine de Saint-Exupéry"},
        {"id": 2, "title": "Cien años de soledad", "author": "Gabriel García Márquez"},
        {"id": 3, "title": "El Peregrino", "author": "Paulo Coelho"},
        {"id": 4, "title": "Big data con python: Recolección, almacenamiento y proceso", "author": "Adrián Riesco Rodríguez,"}
    ]
    main.next_id = 5  # Reset next ID counter

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert b"healthy" in response.data

def test_get_all_books(client):
    response = client.get('/books')
    assert response.status_code == 200
    assert len(response.json) == 4  # Updated to match initial state

def test_get_single_book(client):
    response = client.get('/books/1')
    assert response.status_code == 200
    assert response.json['id'] == 1
    assert "Principito" in response.json['title']

def test_create_book(client):
    new_book = {
        "title": "Don Quijote de la Mancha",
        "author": "Miguel de Cervantes"
    }
    response = client.post('/books', json=new_book)
    assert response.status_code == 201
    assert response.json['id'] == 5  # Updated to match next_id
    assert response.json['title'] == new_book['title']
    
    # Verificar que se añadió a la base de datos
    response = client.get('/books')
    assert len(response.json) == 5

def test_update_book(client):
    updated_data = {"title": "El Principito (Edición Especial)"}
    response = client.put('/books/1', json=updated_data)
    assert response.status_code == 200
    assert response.json['title'] == updated_data['title']
    
    # Verificar persistencia - check JSON directly
    response = client.get('/books/1')
    assert response.json['title'] == "El Principito (Edición Especial)"

def test_delete_book(client):
    # We delete book with id=2 (Cien años de soledad)
    response = client.delete('/books/2')
    assert response.status_code == 200
    assert "eliminado" in response.json['message']
    
    # Verificar que ya no existe
    response = client.get('/books/2')
    assert response.status_code == 404

def test_error_endpoint(client):
    response = client.get('/error')
    assert response.status_code == 500
    # Check for specific error message in JSON response
    assert "error" in response.json
    assert "division by zero" in response.json['error']

#Final    