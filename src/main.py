import random

LETRAS = ['A', 'B', 'C', 'D']

def obtener_preguntas():
    return [
        {
            "pregunta": "¿Cuál es la capital de Francia?",
            "opciones": ["Madrid", "París", "Roma", "Berlín"],
            "respuesta_correcta": "París"
        },
        {
            "pregunta": "¿Cuántos planetas hay en el sistema solar?",
            "opciones": ["7", "8", "9", "10"],
            "respuesta_correcta": "8"
        },
        {
            "pregunta": "¿Quién es el presidente de Argentina en 2025?",
            "opciones": ["Javier Milei", "Juan Domingo Perón", "Axel Kicillof", "Mauricio Macri"],
            "respuesta_correcta": "Javier Milei"
        },
        {
            "pregunta": "¿A qué se hace referencia cuando se dice K8?",
            "opciones": ["8 Kilómetros", "Kubernetes", "Perros Policía", "Un lenguaje de programación"],
            "respuesta_correcta": "Kubernetes"
        }
    ]

def validar_respuesta(letra, opciones):
    if letra.upper() in LETRAS:
        return opciones[LETRAS.index(letra.upper())]
    return None

def hacer_pregunta(pregunta_obj, numero):
    print(f"Pregunta {numero}: {pregunta_obj['pregunta']}")
    for i, opcion in enumerate(pregunta_obj["opciones"]):
        print(f"  {LETRAS[i]}. {opcion}")
    print("")

    respuesta = input("Tu respuesta (A, B, C o D): ").upper()

    while respuesta not in LETRAS:
        respuesta = input("Opción inválida. Ingresa A, B, C o D: ").upper()

    respuesta_usuario = validar_respuesta(respuesta, pregunta_obj["opciones"])
    correcta = respuesta_usuario == pregunta_obj["respuesta_correcta"]

    if correcta:
        print("\n¡Correcto!\n")
    else:
        print(f"\nIncorrecto. La respuesta correcta era: {pregunta_obj['respuesta_correcta']}\n")

    return correcta

def iniciar_juego():
    preguntas = obtener_preguntas()
    random.shuffle(preguntas)

    nombre_jugador = input("Ingrese su nombre: ")
    print(f"\n¡Bienvenido/a, {nombre_jugador} al juego de la Trivia!")
    print("Elija la opción correcta 'A', 'B', 'C' o 'D'\nComencemos...\n")

    correctas = 0
    incorrectas = 0

    for i, pregunta in enumerate(preguntas, 1):
        if hacer_pregunta(pregunta, i):
            correctas += 1
        else:
            incorrectas += 1

    print("Resultado Final")
    print(f"{nombre_jugador}, tu puntuación fue de: ")
    print(f"Respuestas correctas: {correctas}")
    print(f"Respuestas incorrectas: {incorrectas}")

if __name__ == "__main__":
    iniciar_juego()
