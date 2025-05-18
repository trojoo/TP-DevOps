
from src.main import validar_respuesta

def test_validar_respuesta():
    opciones = ["A", "B", "C", "D"]
    assert validar_respuesta("B", opciones) == "B"
    assert validar_respuesta("E", opciones) is None
