import pytest
import sys
import os

# Añadir src al path para importaciones
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))


from main import app as flask_app

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
    assert b"funcionando correctamente" in response.data

def test_get_all_books(client):
    response = client.get('/books')
    assert response.status_code == 200
    assert len(response.json) == 2

def test_get_single_book(client):
    response = client.get('/books/1')
    assert response.status_code == 200
    assert response.json['id'] == 1
    assert b"Principito" in response.data

def test_create_book(client):
    new_book = {
        "title": "Don Quijote de la Mancha",
        "author": "Miguel de Cervantes"
    }
    response = client.post('/books', json=new_book)
    assert response.status_code == 201
    assert response.json['id'] == 3
    assert response.json['title'] == new_book['title']
    
    # Verificar que se añadió a la base de datos
    response = client.get('/books')
    assert len(response.json) == 3

def test_update_book(client):
    updated_data = {"title": "El Principito (Edición Especial)"}
    response = client.put('/books/1', json=updated_data)
    assert response.status_code == 200
    assert response.json['title'] == updated_data['title']
    
    # Verificar persistencia
    response = client.get('/books/1')
    assert b"Edición Especial" in response.data

def test_delete_book(client):
    response = client.delete('/books/2')
    assert response.status_code == 200
    assert b"eliminado" in response.data
    
    # Verificar que ya no existe
    response = client.get('/books/2')
    assert response.status_code == 404

def test_error_endpoint(client):
    response = client.get('/error')
    assert response.status_code == 500
    assert b"Internal Server Error" in response.data   