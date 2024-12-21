import speech_recognition as sr
import pyttsx3
import tkinter as tk
from PIL import Image, ImageTk
import threading
import queue
import json

recognizer = sr.Recognizer()
microphone = sr.Microphone()
engine = pyttsx3.init()

root = tk.Tk()
root.iconbitmap("IMG/icon.ico")
root.geometry("800x600")
root.title("ASISTENTE VIRTUAL")

# Initialize images/widgets globally
image_queue = queue.Queue()

image = Image.open("IMG/iaBackground.jpg")
image = image.resize((790, 450))
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(root, image = photo)
image_label.grid(column=0, row=0, pady=20)
image_queue.put(photo)

lbl_text = tk.Label(root, text="Haz click en el boton 'iniciar' para empezar", font=("Arial", 13, "bold"))
lbl_text.grid(column=0, row=1)

# Queue for communication between threads
queue_ui_to_main = queue.Queue()
queue_main_to_ui = queue.Queue()

with open('basedatos.json', 'r') as archivo:
    datos = json.load(archivo)

def texto_a_audio(text):
    engine.say(text)
    engine.runAndWait()

def capturar_voz(reconocer, microfono, tiempo_ruido=0.5):
    with microfono as fuente:
        reconocer.adjust_for_ambient_noise(fuente, duration=tiempo_ruido)
        print("Escuchando...")
        audio = reconocer.listen(fuente)

    respuesta = {
        "suceso": True,
        "error": None,
        "mensaje": None,
    }
    try:
        respuesta["mensaje"] = reconocer.recognize_google(audio, language="es-PE")
    except sr.RequestError:
        respuesta["suceso"] = False
        respuesta["error"] = "API no disponible"
    except sr.UnknownValueError:
        respuesta["error"] = "Habla ininteligible"
    return respuesta

def main_thread_logic():
    while True:
        command = queue_ui_to_main.get()
        if command == "start":
            execute_start_logic()

def execute_start_logic():
    send_text_to_ui("Bienvenid@")
    btn_start.grid_forget()  
    texto_a_audio("Bienvenido")
    send_text_to_ui("¿Comó te llamas?")
    texto_a_audio("¿Comó te llamas?")
    mic_label.grid(column=0, row=2, pady=10)
    nombre = enviar_voz()
    mic_label.grid_forget()
    send_text_to_ui("Hola " + nombre)
    texto_a_audio("Hola {}. Mucho gusto.".format(nombre))
    texto_a_audio(datos["bienvenida"])
    texto_a_audio(
        "{} ahora voy a explicarte sobre las opciones que tiene este programa. Tienes 3 opciones para escoger.".format(
            nombre))
    #WHILE PARA REPETIR O CAMBIAR DE OPCIONES
    send_text_to_ui("OPCIONES: 1) Aprendizaje   2) Cuestionario    3) Juegos")
    texto_a_audio("Aprendizaje. Cuestionario. Juegos.")
    texto_a_audio(
        "La opción Aprendizaje es donde podrás aprender todo con respecto a Programación. La opción Tests es donde podrás poner en práctica lo que aprendiste mediante preguntas. Y por último, la tercer opción, es Juegos, donde también podrás poner en acción lo que aprendiste jugando.")
    send_text_to_ui("¿Qué opción eliges?")
      
    respuesta = enviar_voz()

    if respuesta == "aprendizaje":

        image = Image.open("IMG/introduccionProgramacion.png")
        image = image.resize((790, 450))
        photo = ImageTk.PhotoImage(image)
        image_queue.put(photo)

        send_text_to_ui("Elegiste la opcion APRENDIZAJE.")
        texto_a_audio("Elegiste la opcion APRENDIZAJE.")
        texto_a_audio("Muy bien antes de empezar quisiera hacer una introduccion a el tema conocido como Programación.")
        send_text_to_ui("Definicion de PROGRAMACION.")
        texto_a_audio(datos['definicion'])
        send_text_to_ui("IMPORTANCIA.")
        texto_a_audio(datos['importancia'])
        send_text_to_ui("RAZONES.")
        texto_a_audio(datos['razones'])
        texto_a_audio("Como se puede apreciar en la imagen, la Programación contiene varios aspectos y caracteristicas importantes, tales como:")
        send_text_to_ui("Conceptos de Programacion.")
        texto_a_audio("Variables. Constantes. Tipos de datos. Operadores. Estructuras condicionales. Bucles. Funciones. Compiladores. Depuración. Algoritmos. Estructuras de datos. Programación Orientada a Objetos (POO).")
        
        respuesta = "estructuras de datos"

        if respuesta == "variables":
            texto_a_audio(datos['variables'])
        elif respuesta == "constantes":
            texto_a_audio(datos['constantes'])
        elif respuesta == "tipos de datos":
            texto_a_audio(datos['tipos_de_datos'])
        elif respuesta == "operadores":
            texto_a_audio(datos['operadores'])
        elif respuesta == "estructuras condicionales":
            texto_a_audio(datos['estructuras_condicionales'])
        elif respuesta == "bucles":
            texto_a_audio(datos['bucles'])
        elif respuesta == "funciones":
            texto_a_audio(datos['funciones'])
        elif respuesta == "compiladores":
            texto_a_audio(datos['compiladores'])
        elif respuesta == "depuracion":
            texto_a_audio(datos['depuracion'])
        elif respuesta == "algoritmos":
            texto_a_audio(datos['algoritmos'])
        elif respuesta == "estructuras de datos":
            
            send_text_to_ui("Estructuras de datos:")
            texto_a_audio(datos['estructuras_de_datos']['definicion'])
            texto_a_audio("existen distintos tipos de estructura, aqui te mostrare 5 de ellas.")
            send_text_to_ui("1) Arrays 2) Listas enlazadas 3) Pilas 4) Colas 5) Hash\n¿Por cual deseas empezar?")
            texto_a_audio("¿Por cual deseas empezar?")
            
            while True:

                respuesta = enviar_voz()

                if cond(respuesta) == True:
                    break

                if respuesta == "arreglos":
                    send_text_to_ui("Arrays:")
                    texto_a_audio(datos['estructuras_de_datos']['arreglos']['descripcion'])
                    texto_a_audio("aqui te presentamos ventajas y desventajas de este tipo de estructura. Ventajas:")
                    texto_a_audio(datos['estructuras_de_datos']['arreglos']['ventajas'])
                    texto_a_audio("Desventajas:")
                    texto_a_audio(datos['estructuras_de_datos']['arreglos']['desventajas'])
                
                elif respuesta == "listas enlazadas":
                    send_text_to_ui("Lista enlazadas:")
                    texto_a_audio(datos['estructuras_de_datos']['listas_enlazadas']['descripcion'])
                    texto_a_audio("aqui te presentamos ventajas y desventajas de este tipo de estructura. Ventajas:")
                    texto_a_audio(datos['estructuras_de_datos']['listas_enlazadas']['ventajas'])
                    texto_a_audio("Desventajas:")
                    texto_a_audio(datos['estructuras_de_datos']['listas_enlazadas']['desventajas'])
                
                elif respuesta == "pilas":
                    send_text_to_ui("Pilas:")
                    texto_a_audio(datos['estructuras_de_datos']['pilas']['descripcion'])
                    texto_a_audio("aqui te presentamos ventajas y desventajas de este tipo de estructura. Ventajas:")
                    texto_a_audio(datos['estructuras_de_datos']['pilas']['ventajas'])
                    texto_a_audio("Desventajas:")
                    texto_a_audio(datos['estructuras_de_datos']['pilas']['desventajas'])
                    
                elif respuesta == "colas":
                    send_text_to_ui("Colas:")
                    texto_a_audio(datos['estructuras_de_datos']['colas']['descripcion'])
                    texto_a_audio("aqui te presentamos ventajas y desventajas de este tipo de estructura. Ventajas:")
                    texto_a_audio(datos['estructuras_de_datos']['colas']['ventajas'])
                    texto_a_audio("Desventajas:")
                    texto_a_audio(datos['estructuras_de_datos']['colas']['desventajas'])

                elif respuesta == "hash":
                    send_text_to_ui("Hash:")
                    texto_a_audio(datos['estructuras_de_datos']['hash']['descripcion'])
                    texto_a_audio("aqui te presentamos ventajas y desventajas de este tipo de estructura. Ventajas:")
                    texto_a_audio(datos['estructuras_de_datos']['hash']['ventajas'])
                    texto_a_audio("Desventajas:")
                    texto_a_audio(datos['estructuras_de_datos']['hash']['desventajas'])

                send_text_to_ui("¿Deseas saber sobre otra estructura?\n1) Arrays 2) Listas enlazadas 3) Pilas 4) Colas 5) Hash 6) No")
                texto_a_audio("¿Deseas saber sobre otra estructura?")

        elif respuesta == "progrmacion orientada a objetos":
            send_text_to_ui("Programacion Orientada a Objetos:")
            texto_a_audio(datos['POO']['definicion'])
            texto_a_audio("existen distintos conceptos importantes en Programacion Orientada a objetos, aqui te mostrare 5 de ellas.")
            send_text_to_ui("1) Clases 2) Objetos 3) Herencia 4) Polimorfismo 5) Encapsulamiento\n¿Por cual deseas empezar?")
            texto_a_audio("¿Por cual deseas empezar?")

            while True:

                respuesta = enviar_voz()

                if cond(respuesta) == True:
                    break

                if respuesta == "clases":
                    send_text_to_ui("Clases:")
                    texto_a_audio(datos['POO']['clases']['definicion'])
                    texto_a_audio("Observa el ejemplo")
                    texto_a_audio(datos['POO']['arrays']['ejemplo'])
                                    
                elif respuesta == "objetos":
                    send_text_to_ui("Objetos:")
                    texto_a_audio(datos['POO']['objetos']['definicion'])
                    texto_a_audio("Observa el ejemplo")
                    texto_a_audio(datos['POO']['objetos']['ejemplo'])
                
                elif respuesta == "herencia":
                    send_text_to_ui("Herencia:")
                    texto_a_audio(datos['POO']['herencia']['definicion'])
                    texto_a_audio("Observa el ejemplo")
                    texto_a_audio(datos['POO']['herencia']['ejemplo'])
                                        
                elif respuesta == "polimorfismo":
                    send_text_to_ui("Polimorfismo:")
                    texto_a_audio(datos['POO']['polimorfismo']['definicion'])
                    texto_a_audio("Observa el ejemplo")
                    texto_a_audio(datos['POO']['polimorfismo']['ejemplo'])
                
                elif respuesta == "encapsulamiento":
                    send_text_to_ui("Encapsulamiento:")
                    texto_a_audio(datos['POO']['encapsulamiento']['definicion'])
                    texto_a_audio("Observa el ejemplo")
                    texto_a_audio(datos['POO']['encapsulamiento']['ejemplo'])

                send_text_to_ui("¿Deseas saber sobre otro concepto?\n1) Clases 2) Objetos 3) Herencia 4) Polimorfismo 5) Encapsulamiento 6) No")
                texto_a_audio("¿Deseas saber sobre otra estructura?")

    elif respuesta == "Cuestionario":
        print ("Cuestionario")
        
        def comp(solucion, rpta):
            if rpta == solucion:
                tus_respuestas.append(1)
            else:
                tus_respuestas.append(0)

        image = Image.open("IMG/perifericos.jpg")
        image = image.resize((790, 450))
        photo = ImageTk.PhotoImage(image)
        image_queue.put(photo)

        send_text_to_ui("Elegiste la opcion CUESTIONARIO.")
        texto_a_audio("Elegiste la opcion CUESTIONARIO.")
        texto_a_audio("Se te realizaran 10 preguntas y al final se te mostrara tu puntaje en conjunto de las justificaciones de las respuestas erroneas.")
        send_text_to_ui("¿Empezamos?\n1) Si 2) No")
        texto_a_audio("¿Estas listo?")

        respuesta = "si"

        if respuesta == "si":
            tus_respuestas = []
            image = Image.open("IMG/P1.jpg")
            image = image.resize((790, 450))
            photo = ImageTk.PhotoImage(image)
            image_queue.put(photo)
            send_text_to_ui("Pregunta 01\nElige sabiamente...")
            texto_a_audio(datos['PE_1'])

            respuesta = enviar_voz()

            comp(datos['P1_RESPUESTA'], respuesta)

            image = Image.open("IMG/P2.jpg")
            image = image.resize((790, 450))
            photo = ImageTk.PhotoImage(image)
            image_queue.put(photo)
            send_text_to_ui("Pregunta 02\nElige sabiamente...")
            texto_a_audio(datos['PE_2'])

            respuesta = enviar_voz()

            comp(datos['P2_RESPUESTA'], respuesta)

            image = Image.open("IMG/P3.jpg")
            image = image.resize((790, 450))
            photo = ImageTk.PhotoImage(image)
            image_queue.put(photo)
            send_text_to_ui("Pregunta 03\nElige sabiamente...")
            texto_a_audio(datos['PE_3'])

            respuesta = enviar_voz()

            comp(datos['P3_RESPUESTA'], respuesta)
            
            image = Image.open("IMG/P4.jpg")
            image = image.resize((790, 450))
            photo = ImageTk.PhotoImage(image)
            image_queue.put(photo)
            send_text_to_ui("Pregunta 04\nElige sabiamente...")
            texto_a_audio(datos['PE_4'], respuesta)

            respuesta = enviar_voz()

            comp(datos['P4_RESPUESTA'], respuesta)

            image = Image.open("IMG/P5.jpg")
            image = image.resize((790, 450))
            photo = ImageTk.PhotoImage(image)
            image_queue.put(photo)
            send_text_to_ui("Pregunta 05\nElige sabiamente...")
            texto_a_audio(datos['PE_5'])

            respuesta = enviar_voz()

            comp(datos['P5_RESPUESTA'], respuesta)

            image = Image.open("IMG/P6.jpg")
            image = image.resize((790, 450))
            photo = ImageTk.PhotoImage(image)
            image_queue.put(photo)
            send_text_to_ui("Pregunta 06\nElige sabiamente...")
            texto_a_audio(datos['PE_6'])

            respuesta = enviar_voz()

            comp(datos['P6_RESPUESTA'], respuesta)

            image = Image.open("IMG/P7.jpg")
            image = image.resize((790, 450))
            photo = ImageTk.PhotoImage(image)
            image_queue.put(photo)
            send_text_to_ui("Pregunta 07\nElige sabiamente...")
            texto_a_audio(datos['PE_7'])

            respuesta = enviar_voz()

            comp(datos['P7_RESPUESTA'], respuesta)

            image = Image.open("IMG/P8.jpg")
            image = image.resize((790, 450))
            photo = ImageTk.PhotoImage(image)
            image_queue.put(photo)
            send_text_to_ui("Pregunta 08\nElige sabiamente...")
            texto_a_audio(datos['PE_8'])

            respuesta = enviar_voz()

            comp(datos['P8_RESPUESTA'], respuesta)

            image = Image.open("IMG/P9.jpg")
            image = image.resize((790, 450))
            photo = ImageTk.PhotoImage(image)
            image_queue.put(photo)
            send_text_to_ui("Pregunta 09\nElige sabiamente...")
            texto_a_audio(datos['PE_9'])

            respuesta = enviar_voz()

            comp(datos['P9_RESPUESTA'], respuesta)

            image = Image.open("IMG/P10.jpg")
            image = image.resize((790, 450))
            photo = ImageTk.PhotoImage(image)
            image_queue.put(photo)
            send_text_to_ui("Pregunta 10\nElige sabiamente...")
            texto_a_audio(datos['PE_10'])

            respuesta = enviar_voz()

            comp(datos['P10_RESPUESTA'], respuesta)

            send_text_to_ui("Terminamos, veamos tus resultados...")
            texto_a_audio("Terminamos, veamos tus resultados...")

            t1 = "P"
            t2 = "_RESPUESTA"
            t3 = "_JUSTIFICACION"
            calificacion = 0
            
            for punto in tus_respuestas:
                if punto == 1:
                    calificacion + 1

            send_text_to_ui("Tu puntuacion ha sido de ", calificacion, " sobre 10.")
            texto_a_audio("Tu puntuacion ha sido de ", calificacion, " sobre 10.")

            for i, elemento in enumerate(tus_respuestas):
                if elemento == 1:
                    send_text_to_ui("Pregunta ", i+1, "\nRespuesta Correcta:", datos[t1+str(i+1)+t2])
                    texto_a_audio("Pregunta ", i+1, "\nRespuesta Correcta:", datos[t1+str(i+1)+t2])
                    texto_a_audio("debido a que", datos[t1+str(i+1)+t3])


    elif respuesta == "juegos":
        print ("juegos")
    else:
        print("no elegiste nada")

def cond(opcion):
                if opcion == "no":
                    return True
                else:
                    return False
                
def enviar_voz():
    palabra = capturar_voz(recognizer, microphone)
    if not palabra["suceso"]:
        print("Algo no está bien. No puedo reconocer tu micrófono o no lo tienes enchufado. <", palabra["error"], ">")
        texto_a_audio("Algo no está bien. No puedo reconocer tu micrófono o no lo tienes enchufado.")
        exit(1)
    return palabra["mensaje"].lower()

def send_text_to_ui(text):
    queue_main_to_ui.put(text)
    root.after(0, update_ui)

def update_ui():
    
    try:
        text = queue_main_to_ui.get_nowait() 
        lbl_text.config(text=text)
        
    except queue.Empty:
        pass
    
    try:
        photo = image_queue.get_nowait()     
        image_label.config(image = photo)        


    except queue.Empty: 
        pass
        
    root.after(100, update_ui)

def start():
    queue_ui_to_main.put("start")

# Start the main thread
main_thread = threading.Thread(target=main_thread_logic)
main_thread.daemon = True
main_thread.start()

mic_image = ImageTk.PhotoImage(Image.open("IMG/mic_icon.png").resize((40, 40)))
mic_label = tk.Label(root, image=mic_image, bd=0, width=40, height=40)

btn_start = tk.Button(root, text="Iniciar", command=start, font=("Arial", 12, "bold"))
btn_start.grid(column=0, row=2, pady=10)

# Run the main loop directly
root.mainloop()