import speech_recognition as sr
import pyttsx3
import tkinter as tk
#import tkinter.font as tkFont
from PIL import Image, ImageTk
import threading
import queue
import json
import random

defaultBgColor = "#3d6e82"
defaultFgColor = "#5fa8b4"
defaultFont = "Helvetica"

recognizer = sr.Recognizer()
microphone = sr.Microphone()
engine = pyttsx3.init()
engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0')


root = tk.Tk()
root.iconbitmap("IMG/icon.ico")
root.geometry("800x600")
root.title("ASISTENTE VIRTUAL")
root.config(bg=defaultBgColor)
root.resizable(False, False) # deshabilita redimensionamiento
root.maxsize(800, 600) # establece tamaño máximo
root.minsize(800, 600)

# Dimensiones del tablero
WIDTH = 400  
HEIGHT = 400

# Tamaño de las celdas 
CELL_SIZE = 25

class Grid:
    def __init__(self, canvas, width, height, cell_size):
        self.canvas = canvas
        self.WIDTH = width
        self.HEIGHT = height
        self.CELL_SIZE = cell_size

        x1, y1 = random.randint(0, 15), random.randint(0, 15)
        x2, y2 = random.randint(0, 15), random.randint(0, 15)
        self.user_cell = (x1, y1)
        self.goal_cell = (x2, y2)

        self.obstacle_cells = []

        for _ in range(90):
            x3, y3 = random.randint(0, 15), random.randint(0, 15)

            if (x3, y3) != (x2, y2) and (x3, y3) != (x1, y1):
                self.obstacle_cells.append((x3, y3))

        self.cells = []
        self.initialize_cells()
        self.draw_cells()
        
    def initialize_cells(self):
        for row in range(20):
            for col in range(20):
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                fill_color = "white"
                if (row, col) == self.user_cell:
                    fill_color = "green"
                elif (row, col) == self.goal_cell:
                    fill_color = "red"
                elif (row, col) in self.obstacle_cells:
                    fill_color = "black"

                cell = self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color)
                self.cells.append(cell)

    def draw_cells(self):
        for cell_id in self.cells:
            self.canvas.delete(cell_id)  # Borrar celdas antiguas

        self.initialize_cells()

    def move_up(self, evt):
        self.try_move(self.user_cell[0] - 1, self.user_cell[1])

    def move_down(self, evt):
        self.try_move(self.user_cell[0] + 1, self.user_cell[1])

    def move_left(self, evt):
        self.try_move(self.user_cell[0], self.user_cell[1] - 1)

    def move_right(self, evt):
        self.try_move(self.user_cell[0], self.user_cell[1] + 1)

    def try_move(self, row, col):
        if (row >= 0 and row < 20 and col >= 0 and col < 20 and
                (row, col) not in self.obstacle_cells):
            self.user_cell = (row, col)
            self.draw_cells()

# Queue for communication between threads
queue_ui_to_main = queue.Queue()
queue_main_to_ui = queue.Queue()
image_queue = queue.Queue()

# Initialize images/widgets globally
image = Image.open("IMG/background.png")
image = image.resize((750, 450))
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(root, image = photo)

print((root.winfo_reqwidth()))
image_label.grid(column=0, row=0, pady=10, padx=((800 - photo.width())/ 2))
image_label.config(bg=defaultBgColor)
image_queue.put(photo)

lbl_text = tk.Label(root, text="Haz click en el boton 'Iniciar' para empezar", font=(defaultFont, 16, "bold"))
lbl_text.config(bg=defaultBgColor,
                fg=defaultFgColor,
                font=(defaultFont, 20, "bold"))
lbl_text.grid(column=0, row=1)

with open('basedatos.json', encoding="utf-8") as archivo:
    datos = json.load(archivo)

def texto_a_audio(text):
    engine.say(text)
    engine.runAndWait()

def capturar_voz(reconocer, microfono, tiempo_ruido=0.1):
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
    send_text_to_ui("¿Cómo te llamas?")
    texto_a_audio("¿Cómo te llamas?")
    mic_label.grid(column=0, row=2, pady=0)
    nombre = enviar_voz()
    nombre = nombre.capitalize()
    mic_label.grid_forget()
    send_text_to_ui("¡Hola " + nombre + "!")
    texto_a_audio("Hola {}. Mucho gusto.".format(nombre))
    texto_a_audio(datos["bienvenida"])
    texto_a_audio(
        "{}, por ahora este programa incluye estos juegos:".format(
            nombre))
    
    #WHILE PARA REPETIR O CAMBIAR DE OPCIONES
    while True:
        image = Image.open("IMG/upperBackground.png")
        image = image.resize((750, 142))
        photo = ImageTk.PhotoImage(image)
        image_queue.put(photo)
        send_text_to_ui("Opciones disponibles:")

        # Mostrar cada opción en su propia fila
        lbl_opcion1 = tk.Label(
            root, text="Cuestionario",
            font=("Helvetica", 16, "bold"), anchor="center", 
            bg=defaultFgColor, fg=defaultBgColor,
            width=20,
        )
        lbl_opcion1.grid(column=0, row=2, pady=5, sticky="ew")

        lbl_opcion2 = tk.Label(
            root, text="Ahorcado",
            font=("Helvetica", 16, "bold"), anchor="center",
            bg=defaultFgColor, fg=defaultBgColor,
            width=20, 
        )
        lbl_opcion2.grid(column=0, row=3, pady=5, sticky="ew")

        lbl_opcion3 = tk.Label(
            root, text="Laberinto",
            font=("Helvetica", 16, "bold"), anchor="center",
            bg=defaultFgColor, fg=defaultBgColor,
            width=20
        )
        lbl_opcion3.grid(column=0, row=4, pady=5, sticky="ew")

        lbl_opcion4 = tk.Label(
            root, text="Globos",
            font=("Helvetica", 16, "bold"), anchor="center",
            bg=defaultFgColor, fg=defaultBgColor,
            width=20
        )
        lbl_opcion4.grid(column=0, row=5, pady=5, sticky="ew")

        lbl_opcion5 = tk.Label(
            root, text="Salir",
            font=("Helvetica", 16, "bold"), anchor="center",
            bg=defaultFgColor, fg=defaultBgColor,
            width=20
        )
        lbl_opcion5.grid(column=0, row=6, pady=5, sticky="ew")

        # Información adicional por voz
        texto_a_audio(
            "Las opciones son: Cuestionario, Ahorcado, Laberinto y Globos. "
            "Por favor, di la opción que deseas elegir."
        )
        send_text_to_ui("¿Qué opción eliges?")

        # Esperar respuesta por voz
        mic_label.grid(column=0, row=7, pady=10)
        respuesta = enviar_voz()
        mic_label.grid_forget()
        lbl_opcion1.grid_forget()
        lbl_opcion2.grid_forget()
        lbl_opcion3.grid_forget()
        lbl_opcion4.grid_forget()
        lbl_opcion5.grid_forget()

        if respuesta == "cuestionario":
            print ("Cuestionario")

            def comp(solucion, rpta):
                if rpta == solucion:
                    tus_respuestas.append(1)
                else:
                    tus_respuestas.append(0)

            image = Image.open("IMG/cuestionario.png")
            image = image.resize((750, 425))
            photo = ImageTk.PhotoImage(image)
            image_queue.put(photo)

            send_text_to_ui("Elegiste la opcion CUESTIONARIO.")
            texto_a_audio("Elegiste la opcion CUESTIONARIO.")
            texto_a_audio("Se te realizaran 10 preguntas y al final se te mostrara tu puntaje en conjunto de las justificaciones de las respuestas erroneas.")
            send_text_to_ui("¿Empezamos?\n1) Claro 2) No")
            texto_a_audio("¿Estas listo?")

            mic_label.grid(column=0, row=2, pady=0)
            respuesta = enviar_voz()
            mic_label.grid_forget()

            if respuesta == "claro":
                tus_respuestas = []

                send_text_to_ui("Responde con una palabra que inicie con la letra de la opcion que quieras elejir")

                for i in range(3):
                    preguntas(i+1)
                    respuesta = "a"
                    ruta = "P"+str(i+1)+"_RESPUESTA"                
                    comp(datos[ruta], respuesta[0])
                
                image = Image.open("IMG/cuestionario.png")
                image = image.resize((790, 450))
                photo = ImageTk.PhotoImage(image)
                image_queue.put(photo)

                send_text_to_ui("Terminamos, veamos tus resultados...")
                texto_a_audio("Terminamos, veamos tus resultados...")

                calificacion = 0

                for punto in tus_respuestas:
                    if punto == 1:
                        calificacion = calificacion + 1

                msg = "Tu puntuacion ha sido de "+ str(calificacion) + " sobre 10."
                send_text_to_ui(msg)
                texto_a_audio(msg)

                if calificacion == 10:
                    send_text_to_ui("Lo has hecho fenomenal. Sigue asi")
                    texto_a_audio("Lo has hecho fenomenal. Sigue asi")
                else:
                    if calificacion > 5:
                        send_text_to_ui("Aún estas en camino pero pronto serás todo un genio.")
                        texto_a_audio("Aún estas en camino pero pronto serás todo un genio.")
                    else:
                        send_text_to_ui("No te rindas, se que puedes lograrlo.")
                        texto_a_audio("No te rindas, se que puedes lograrlo.")

                    send_text_to_ui("Has fallado en las siguiente preguntas:")
                    texto_a_audio("Has fallado en las siguiente preguntas:")

                    for i, elemento in enumerate(tus_respuestas):
                        if elemento == 0:
                            ruta = "IMG/P"+str(i+1)+".jpg"
                            image = Image.open(ruta)
                            image = image.resize((790, 450))
                            photo = ImageTk.PhotoImage(image)
                            image_queue.put(photo)
                            msg = "Pregunta " + str(i+1) + "\nEsta es la Respuesta Correcta:" + datos["P"+str(i+1)+"_RESPUESTA"]
                            send_text_to_ui(msg)
                            texto_a_audio(msg)
                            msg = "debido a que" + datos["P"+str(i+1)+"_JUSTIFICACION"]
                            texto_a_audio(msg)

            image = Image.open("IMG/cuestionario.png")
            image = image.resize((790, 450))
            photo = ImageTk.PhotoImage(image)
            image_queue.put(photo)

            send_text_to_ui("Bueno, eso es todo aqui, espero vuelvas para retar tus conocimientos.")
            texto_a_audio("Bueno, eso es todo aqui en cuestioanrio, espero vuelvas para retar tus conocimientos.")

        elif respuesta == "ahorcado":
            jugar_ahorcado()
        
        elif respuesta == "laberinto de instrucciones":
            image = Image.open("IMG/fondolaberinto.jpg")
            image = image.resize((790, 450))
            photo = ImageTk.PhotoImage(image)
            image_queue.put(photo)

            canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
            canvas.grid(column=0, row=0, pady=20)  # Posiciona el canvas en la columna 1

            grid = Grid(canvas, WIDTH, HEIGHT, CELL_SIZE)

            while True:
                send_text_to_ui("Escuchando tus indicaciones...")
                texto_a_audio("Escuchando tus indicaciones...")
                mic_label.grid(column=0, row=2, pady=10)                
                respuesta = enviar_voz()
                mic_label.grid_forget();
                if respuesta == "arriba":
                    grid.move_up(None)
                elif respuesta == "abajo":
                    grid.move_down(None)
                elif respuesta == "derecha":
                    grid.move_right(None)
                elif respuesta == "izquierda":
                    grid.move_left(None)
                else:
                    texto_a_audio("No es una dirección válida, dime una dirección válida.")

                if grid.user_cell == grid.goal_cell:
                    texto_a_audio("¡Felicidades, llegaste a tu destino!")
                    break
                    
            canvas.destroy()

        elif respuesta == "salir":
            send_text_to_ui("Ha sido un gusto poder ayudarte, regresa pronto.")
            texto_a_audio("Ha sido un gusto poder ayudarte, regresa pronto.")
            break

        """image = Image.open("IMG/juegos.png")
        image = image.resize((790, 450))
        photo = ImageTk.PhotoImage(image)
        image_queue.put(photo)""" 


def verificar_victoria(cadena):
    if "_" not in cadena:
        return True
    return False


def preguntas(i):    
    ruta = "IMG/P"+str(i)+".jpg"
    image = Image.open(ruta)
    image = image.resize((790, 450))
    photo = ImageTk.PhotoImage(image)
    image_queue.put(photo)

    respuesta = "PE_"+str(i)
    send_text_to_ui("Pregunta 0"+str(i)+"\nElige sabiamente...")
    texto_a_audio(datos[respuesta])

def actualizar_imagen_ahorcado(contador):
    nombre = "IMG/ahorcado" + str(contador + 1) + ".png"
    image = Image.open(nombre)
    image = image.resize((200, 350))
    photo = ImageTk.PhotoImage(image)
    image_queue.put(photo)

def texto_ahorcado(palabra):
    cadena = ""

    for i in range(len(palabra) - 1):
        cadena += "_ "

    cadena += "_"

    return cadena

def actualizar_cadena(info, letra):
    """Actualiza la cadena mostrada con la letra correcta."""
    for i in range(len(info[0])):
        if info[0][i] == letra:
            info[1] = info[1][:(2 * i)] + letra + info[1][(2 * i + 1):]

def cond(opcion):
                if opcion == "no":
                    return True
                else:
                    return False

def jugar_ahorcado():
    while True:
        # Inicializar imagen inicial
        actualizar_imagen_ahorcado(0)

        send_text_to_ui("Empezamos con el juego")
        texto_a_audio("Empezamos con el juego")

        # Selección aleatoria de palabra
        keys = list(datos["ahorcado"].keys())
        palabra_elegida = random.choice(keys)
        palabra = datos["ahorcado"][palabra_elegida]["palabra"]

        print("Palabra elegida:", palabra_elegida)

        # Configuración inicial
        ahorcado_info = [palabra, texto_ahorcado(palabra), 0]  # [palabra, estado_actual, fallos]
        send_text_to_ui(ahorcado_info[1])
        lbl_track.grid(column=0, row=3)
        lbl_track.config(text=datos['ahorcado'][palabra_elegida]['pistas']['p1'])

        # Bucle de juego
        while True:
            texto_a_audio("Di una letra para intentar adivinar la palabra")
            mic_label.grid(column=0, row=2, pady=10)
            letra = enviar_voz()
            mic_label.grid_forget()

            if not letra or len(letra[0]) != 1:
                texto_a_audio("Por favor, di una sola letra.")
                continue

            letra = letra[0].lower()
            print("Se obtuvo la letra:", letra)

            # Procesar la letra
            if letra in ahorcado_info[1]:
                texto_a_audio("Ya elegiste esa letra.")
            elif letra in palabra:
                texto_a_audio(f"La letra {letra} está en la palabra.")
                actualizar_cadena(ahorcado_info, letra)
            else:
                texto_a_audio(f"La letra {letra} no está en la palabra.")
                ahorcado_info[2] += 1

            # Actualizar estado del juego
            send_text_to_ui(ahorcado_info[1])
            actualizar_imagen_ahorcado(ahorcado_info[2])

            # Dar segunda pista si hay 3 fallos
            if ahorcado_info[2] == 3:
                lbl_track.config(text=(
                    f"{datos['ahorcado'][palabra_elegida]['pistas']['p1']}\n"
                    f"{datos['ahorcado'][palabra_elegida]['pistas']['p2']}"
                ))

            # Verificar estado del juego
            if ahorcado_info[2] >= 6:  # Límite de 6 fallos
                lbl_track.config(text=f"PERDISTE. La palabra era: {palabra}")
                texto_a_audio(f"Perdiste. La palabra era {palabra}.")
                lbl_track.grid_forget()
                break

            if verificar_victoria(ahorcado_info[1]):
                lbl_track.config(text="¡Felicidades, has ganado!")
                texto_a_audio("¡Felicidades, has ganado!")
                lbl_track.grid_forget()
                break

        # Preguntar si se quiere jugar de nuevo
        send_text_to_ui("¿Deseas jugar otra partida?")
        texto_a_audio("¿Deseas jugar otra partida?")

        lbl_opcion_si = tk.Label(
        root, text="1) Sí",
        font=("Helvetica", 16), anchor="center"
        )
        lbl_opcion_si.grid(column=0, row=1, pady=5, sticky="ew")

        lbl_opcion_no = tk.Label(
            root, text="2) No",
            font=("Helvetica", 16), anchor="center"
        )
        lbl_opcion_no.grid(column=0, row=2, pady=5, sticky="ew")
        while True:
            respuesta = enviar_voz()
            if respuesta in ["no", "si"]:
                break
            else:
                texto_a_audio("Por favor, elige una de las opciones: sí o no.")

        if respuesta == "no":
            texto_a_audio("Gracias por jugar. ¡Hasta luego!")
            break

def enviar_voz():
    while(True):
        palabra = capturar_voz(recognizer, microphone)
        if not palabra["suceso"]:
            print("Algo no está bien. No puedo reconocer tu micrófono o no lo tienes enchufado. <", palabra["error"], ">")
            texto_a_audio("Algo no está bien. No puedo reconocer tu micrófono o no lo tienes enchufado.")
            exit(1)
        if not palabra["mensaje"] == None:
            break
        else:
            texto_a_audio("Repite la palabra")
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
        global photo
        photo = image_queue.get_nowait()
        image_label.config(image = photo)
        print("de la ventana")
        print(root.winfo_reqwidth())
        print(photo.width())

        image_label.grid(column=0, row=0, pady=20, padx=((800 - photo.width())/ 2))



    except queue.Empty:
        pass

    root.after(100, update_ui)

def start():
    queue_ui_to_main.put("start")

# Start the main thread
main_thread = threading.Thread(target=main_thread_logic)
main_thread.daemon = True
main_thread.start()

mic_image = ImageTk.PhotoImage(Image.open("IMG/mic_icon.png").resize((45, 45)))
mic_label = tk.Label(root, image=mic_image, bd=0, width=45, height=45)

btn_start = tk.Button(root, text="Iniciar", command=start,
                      font=(defaultFont, 20, "bold"),
                      bg=defaultFgColor, fg=defaultBgColor,
                      borderwidth=0,
                      highlightthickness=0)

btn_start.grid(column=0, row=2, pady=10)

def on_enter(e):
    btn_start.config(font=(defaultFont, 20, "bold"), borderwidth=2, bg=defaultBgColor, fg=defaultFgColor)

def on_leave(e):
    btn_start.config(font=(defaultFont, 20, "bold"), borderwidth=0, bg=defaultFgColor, fg=defaultBgColor)

btn_start.bind("<Enter>", on_enter)
btn_start.bind("<Leave>", on_leave)

lbl_track=tk.Label(root, text=" ", font=(defaultFont, 16, "bold"))
lbl_track.config(bg=defaultBgColor,
                 fg=defaultFgColor, # color mostaza
                 font=(defaultFont, 16, "bold"))
# lbl_track.grid(column=0, row=2)

# Run the main loop directly
root.mainloop()