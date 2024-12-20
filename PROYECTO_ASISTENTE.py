import speech_recognition as sr
import pyttsx3
import json
import time


def texto_a_audio(comando):
    """Convierte texto en audio."""
    palabra = pyttsx3.init()
    palabra.say(comando)
    palabra.runAndWait()


def capturar_voz(reconocer, microfono):
    """Captura audio desde el micrófono y lo convierte a texto."""
    try:
        with microfono as fuente:
            print("Ajustando ruido ambiental...")
            reconocer.adjust_for_ambient_noise(fuente)
            print("Escuchando...")
            audio = reconocer.listen(fuente)
        texto = reconocer.recognize_google(audio, language="es-PE")
        return texto.lower()
    except sr.UnknownValueError:
        texto_a_audio("No entendí lo que dijiste. Por favor, inténtalo de nuevo.")
        return None
    except sr.RequestError:
        texto_a_audio("Error con el servicio de reconocimiento de voz.")
        return None


def saludar_usuario(datos):
    """Realiza un saludo inicial al usuario."""
    texto_a_audio(datos['bienvenida'])
    print("Por favor, di tu nombre:")
    nombre = capturar_voz(recognizer, microphone)
    if nombre:
        texto_a_audio(f"Hola {nombre}. Mucho gusto.")
        print(f"Hola {nombre}, ahora te explicaré las opciones disponibles.")
        texto_a_audio("Ahora te explicaré las opciones disponibles.")
        return nombre
    else:
        texto_a_audio("No logré captar tu nombre. Intentémoslo otra vez.")
        return saludar_usuario(datos)


def menu_principal(nombre, datos):
    """Presenta el menú principal al usuario."""
    print(f"{nombre}, tienes 3 opciones disponibles:")
    texto_a_audio(f"{nombre}, tienes tres opciones disponibles.")
    print("\n1) Aprendizaje\n2) Test\n3) Juegos\n")
    texto_a_audio("Aprendizaje, Test o Juegos. ¿Cuál eliges?")
    while True:
        opcion = capturar_voz(recognizer, microphone)
        if opcion in ["aprendizaje", "test", "juegos"]:
            return opcion
        texto_a_audio("No entendí tu respuesta. Por favor, elige entre Aprendizaje, Test o Juegos.")


def aprendizaje(datos):
    """Funcionalidad de aprendizaje."""
    print("Has elegido la opción de Aprendizaje.")
    texto_a_audio("Has elegido la opción de Aprendizaje.")
    print(datos['aprendizaje'])
    texto_a_audio(datos['aprendizaje'])


def test(datos):
    """Funcionalidad de test."""
    print("Has elegido la opción de Test.")
    texto_a_audio("Has elegido la opción de Test.")
    print(datos['test'])
    texto_a_audio(datos['test'])


def juegos(datos):
    """Funcionalidad de juegos."""
    print("Has elegido la opción de Juegos.")
    texto_a_audio("Has elegido la opción de Juegos.")
    print(datos['juegos'])
    texto_a_audio(datos['juegos'])


if __name__ == "__main__":
    # Inicialización de componentes
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # Carga de datos desde el archivo JSON
    with open('basedatos.json', 'r') as archivo:
        datos = json.load(archivo)

    # Flujo principal
    nombre_usuario = saludar_usuario(datos)
    opcion = menu_principal(nombre_usuario, datos)

    # Ejecución de la funcionalidad seleccionada
    if opcion == "aprendizaje":
        aprendizaje(datos)
    elif opcion == "test":
        test(datos)
    elif opcion == "juegos":
        juegos(datos)
