import speech_recognition as sr
import pyttsx3

# Inicializa el motor de texto a voz
def texto_a_audio(comando):
    palabra = pyttsx3.init()
    palabra.say(comando)
    palabra.runAndWait()

# Captura audio desde el micrófono
def capturar_voz():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    try:
        with microphone as fuente:
            print("Ajustando ruido ambiental...")
            recognizer.adjust_for_ambient_noise(fuente)
            print("Escuchando...")
            audio = recognizer.listen(fuente)
        texto = recognizer.recognize_google(audio, language="es-PE")
        return texto.lower()
    except sr.UnknownValueError:
        return "No entendí lo que dijiste."
    except sr.RequestError:
        return "Error con el servicio de reconocimiento de voz."

# Flujo principal
if __name__ == "__main__":
    texto_a_audio("Hola, soy tu asistente virtual. Dime algo.")
    print("Di algo:")
    mensaje = capturar_voz()
    print(f"Dijiste: {mensaje}")
    texto_a_audio(f"Dijiste: {mensaje}")
