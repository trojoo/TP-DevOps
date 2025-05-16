import random

preguntas = [{"pregunta": "¿Cuál es la capital de Francia?",
              "opciones": ["Madrid", "París", "Roma", "Berlín"],"respuesta_correcta": "París"},
             {"pregunta": "¿Cuántos planetas hay en el sistema solar?",
              "opciones": ["7", "8", "9", "10"],"respuesta_correcta": "8"},
             {"pregunta": "¿Quién es el presidente de Argentina en 2025?",
              "opciones": ["Javier Milei", "Juan Domingo Perón", "Axel Kicillof", "Mauricio Macri"],"respuesta_correcta": "Javier Milei"},
             {"pregunta": "¿A qué se hace referencia cuando se dice K8?",
              "opciones": ["8 Kilómetros", "Kubernetes", "Perro Policias", "Un lenguaje de programación"],"respuesta_correcta": "Kubernetes"}]

random.shuffle(preguntas)

nombre_jugador = input("Ingrese su nombre: ")
print(f"\n¡Bienvenido/a, {nombre_jugador} al juego de la Trivia!\nElija la opción correcta 'A', 'B', 'C' o 'D' \nComencemos...\n")

respuestas_correctas = 0
respuestas_incorrectas = 0

letras = ['A', 'B', 'C', 'D']

for i, pregunta in enumerate(preguntas, 1):
    print(f"Pregunta {i}: {pregunta['pregunta']}")
    
    opciones = pregunta["opciones"]
    for letra_indice, opcion in enumerate(opciones):
        print(f"  {letras[letra_indice]}. {opcion}")
    print("")
    respuesta = input("Tu respuesta (A, B, C o D): ").upper()
    
    while respuesta != "A" and respuesta != "B" and respuesta != "C" and respuesta != "D":
        
        respuesta = input("Opción inválida. Ingresa A, B, C o D: ").upper()
    
    indice = letras.index(respuesta)
    respuesta_usuario = opciones[indice]
    
    if respuesta_usuario == pregunta["respuesta_correcta"]:
        print("")
        print("¡Correcto!\n")
        respuestas_correctas += 1
    else:
        print("")
        print(f"Incorrecto. La respuesta correcta era: {pregunta['respuesta_correcta']}\n")
        respuestas_incorrectas += 1

print("Resultado Final")
print(f"{nombre_jugador}, tu puntuación fue de: ")
print(f"Respuestas correctas: {respuestas_correctas}")
print(f"Respuestas incorrectas: {respuestas_incorrectas}")
