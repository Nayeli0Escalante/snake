# Importa las bibliotecas necesarias
import turtle  # Para la interfaz gráfica
import time  # Para pausar el juego
import random  # Para generar números aleatorios
import pygame  # Para manejar sonidos

# Inicializa Pygame
pygame.init()

# Configura la pantalla de Pygame (no se mostrará)
pygame.mixer.init()

# Carga archivos de sonido
pygame.mixer.music.load(r'C:\Users\HP\Music\Playlists\sonido\inicio.wav')
comida_sound = pygame.mixer.Sound(r'C:\Users\HP\Music\Playlists\sonido\comida.wav')
colision_sound = pygame.mixer.Sound(r'C:\Users\HP\Music\Playlists\sonido\colision.wav')
movimiento_sound = pygame.mixer.Sound(r'C:\Users\HP\Music\Playlists\sonido\movimiento.wav')
fin_sound = pygame.mixer.Sound(r'C:\Users\HP\Music\Playlists\sonido\fin.wav')

# Configuración inicial del juego
posponer = 0.15  # Modificar este valor cambia la velocidad de la serpiente
puntaje = 0 #Esta variable se utiliza para llevar la cuenta del puntaje del jugador. Al inicio del juego, el puntaje se establece en cero.
max_puntaje = 0 #  Esta variable almacena el máximo puntaje alcanzado durante la sesión de juego.
en_pausa = False # Esta variable indica si el juego está en pausa o no. Al inicio del juego, se establece en False,
juego_terminado = False #Esta variable indica si el juego ha terminado o no

# Dimensiones de la ventana
ventana_ancho = 600
ventana_alto = 600

# Dimensiones de la cuadrícula
cuadricula_ancho = 580
cuadricula_alto = 580
cuadricula_tamanio = 20  # Tamaño de cada cuadrado de la cuadrícula

# Inicializa la ventana de Turtle
window = turtle.Screen() # Crea una ventana gráfica para el juego
window.title("Snake") #Establece el título de la ventana como "Snake".
window.bgcolor("#88DC65") #Establece el color de fondo de la ventana en un tono de verde
window.setup(width=ventana_ancho, height=ventana_alto) #Establece el tamaño de la ventana.
window.tracer(0)  # Desactiva la animación

# Crea una nueva pluma para dibujar la cuadrícula
grid_pen = turtle.Turtle() #Crea un nuevo objeto Turtle (pluma) que se utilizará para dibujar la cuadrícula
grid_pen.color("#00C040") #Establece el color de la pluma
grid_pen.penup()
grid_pen.hideturtle() #Oculta la forma de la pluma para que no sea visible en la ventana

# Dibuja la cuadrícula
for x in range(-cuadricula_ancho // 2, cuadricula_ancho // 2 + 1, cuadricula_tamanio):
    grid_pen.goto(x, -cuadricula_alto // 2)
    grid_pen.pendown() #Baja la pluma para comenzar a dibujar.
    grid_pen.goto(x, cuadricula_alto // 2)
    grid_pen.penup()

for y in range(-cuadricula_alto // 2, cuadricula_alto // 2 + 1, cuadricula_tamanio):
    grid_pen.goto(-cuadricula_ancho // 2, y)
    grid_pen.pendown()
    grid_pen.goto(cuadricula_ancho // 2, y)
    grid_pen.penup()

# Crea la cabeza de la serpiente
cabeza = turtle.Turtle()
cabeza.speed(0)
cabeza.shape("circle") #Define la forma de la cabeza de la serpiente
cabeza.color("#FF5733")
cabeza.penup()
cabeza.goto(0, 0) #Esta es la posición inicial de la cabeza en el centro de la ventana.
cabeza.direction = "stop"  # Dirección inicial de la serpiente

# Crea la comida
comida = turtle.Turtle()
comida.speed(0)
comida.shape("circle")
comida.color("#FFD700")
comida.penup()
comida_offset = cuadricula_tamanio // 2  # Para centrar la comida en un cuadrado

# Crea un texto para mostrar el puntaje
texto = turtle.Turtle()
texto.speed(0)
texto.color("white")
texto.penup()
texto.hideturtle()
texto.goto(0, ventana_alto // 2 - 40)

# Función para imprimir el texto con mayor grosor
def printText():
    global max_puntaje
    if puntaje > max_puntaje:
        max_puntaje = puntaje
    texto.clear()
    texto.write(
        f"Puntaje:{puntaje}     Máximo puntaje: {max_puntaje}",
        align="center",
        font=("Times New Roman", 21, "bold")  # Ajusta el grosor del texto aquí
    )

# Lista de segmentos del cuerpo de la serpiente
cuerpo = []
# Colores para los segmentos del cuerpo
colores = ['#FF6347', '#FF7F50', '#FFA07A', '#FF8C00', '#FFA500', '#FFD700']

# Lista de sonidos
SONIDOS = [pygame.mixer.music, comida_sound, colision_sound, movimiento_sound, fin_sound]

# Función para reproducir un sonido según el índice proporcionado
def reproducir_sonido(indice):
    SONIDOS[indice].play()

# Funciones para cambiar la dirección de la serpiente
def arriba():
    if cabeza.direction != "down":
        cabeza.direction = "up"

def abajo():
    if cabeza.direction != "up":
        cabeza.direction = "down"

def izquierda():
    if cabeza.direction != "right":
        cabeza.direction = "left"

def derecha():
    if cabeza.direction != "left":
        cabeza.direction = "right"

# Función para iniciar o reiniciar el juego
def inicio():
    global en_pausa, juego_terminado
    if en_pausa:
        en_pausa = False
        juego_terminado = False
        mover_snake()
    elif juego_terminado:
        reiniciar_juego()
    else:
        return

# Función para pausar el juego
def pausa():
    global en_pausa
    en_pausa = True

# Función para mover la serpiente
def mover_snake():
    global en_pausa
    if en_pausa or juego_terminado:
        return
    movimiento()
    window.update()
    borde()
    colision_comida()
    mordida()
    mov_cuerpo()
    time.sleep(posponer)
    window.ontimer(mover_snake, 0)

# Función para reiniciar el juego
def reiniciar_juego():
    global puntaje, cuerpo, en_pausa, juego_terminado
    cabeza.goto(0, 0)
    cabeza.direction = "stop"
    comida_goto()
    puntaje = 0
    printText()
    for segmento in cuerpo:
        segmento.goto(1000, 1000)
    cuerpo.clear()
    en_pausa = False
    juego_terminado = False
    reproducir_sonido(0)  # Reproduce el sonido de inicio
    mover_snake()

# Función para colocar la comida en una nueva ubicación aleatoria
def comida_goto():
    global comida
    comida_x = random.randint(-cuadricula_ancho // 2 + comida_offset, cuadricula_ancho // 2 - comida_offset)
    comida_y = random.randint(-cuadricula_alto // 2 + comida_offset, cuadricula_alto // 2 - comida_offset)
    comida_x -= (comida_x % cuadricula_tamanio)  # Ajusta a la posición del cuadrado más cercano
    comida_y -= (comida_y % cuadricula_tamanio)  # Ajusta a la posición del cuadrado más cercano
    comida.goto(comida_x, comida_y)

# Función para mover la serpiente
def movimiento():
    if cabeza.direction == "up":
        cabeza.sety(cabeza.ycor() + cuadricula_tamanio)
        reproducir_sonido(3)  # Reproduce el sonido de movimiento
    elif cabeza.direction == "down":
        cabeza.sety(cabeza.ycor() - cuadricula_tamanio)
        reproducir_sonido(3)  # Reproduce el sonido de movimiento
    elif cabeza.direction == "left":
        cabeza.setx(cabeza.xcor() - cuadricula_tamanio)
        reproducir_sonido(3)  # Reproduce el sonido de movimiento
    elif cabeza.direction == "right":
        cabeza.setx(cabeza.xcor() + cuadricula_tamanio)
        reproducir_sonido(3)  # Reproduce el sonido de movimiento

# Función para crear un nuevo segmento del cuerpo
def crear_segmento():
    global puntaje
    segmento = turtle.Turtle()
    turtle.colormode(255)
    segmento.speed(0)
    segmento.shape("circle")
    color_index = puntaje % len(colores)
    color = colores[color_index]
    segmento.color(color)
    segmento.penup()
    cuerpo.append(segmento)
    puntaje += 1
    printText()

# Función para detectar colisión con la comida
def colision_comida():
    global comida
    if cabeza.distance(comida) < cuadricula_tamanio:
        comida_goto()
        crear_segmento()
        reproducir_sonido(1)  # Reproduce el sonido de comida

# Función para mover el cuerpo de la serpiente
def mov_cuerpo():
    totalSeg = len(cuerpo)
    for segmento in range(totalSeg - 1, 0, -1):
        x = cuerpo[segmento - 1].xcor()
        y = cuerpo[segmento - 1].ycor()
        cuerpo[segmento].goto(x, y)
    if totalSeg > 0:
        x = cabeza.xcor()
        y = cabeza.ycor()
        cuerpo[0].goto(x, y)

# Función para detectar colisión con el borde
def borde():
    global puntaje, juego_terminado
    if (
        cabeza.xcor() < -ventana_ancho // 2
        or cabeza.xcor() > ventana_ancho // 2 - cuadricula_tamanio
        or cabeza.ycor() < -ventana_alto // 2
        or cabeza.ycor() > ventana_alto // 2 - cuadricula_tamanio
    ):
        cabeza.goto(0, 0)
        cabeza.direction = "stop"
        for segmento in cuerpo:
            segmento.goto(1000, 1000)
        cuerpo.clear()
        juego_terminado = True
        printText()
        reproducir_sonido(4)  # Reproduce el sonido de fin

# Función para detectar colisión con el cuerpo de la serpiente
def mordida():
    global puntaje, juego_terminado
    for segmento in cuerpo:
        if cabeza.distance(segmento) < cuadricula_tamanio:
            cabeza.goto(0, 0)
            cabeza.direction = "stop"
            for segmento in cuerpo:
                segmento.goto(1000, 1000)
            cuerpo.clear()
            puntaje = 0
            juego_terminado = True
            printText()
            reproducir_sonido(2)  # Reproduce el sonido de colisión

# Configura los eventos de teclado
window.listen()
window.onkeypress(arriba, "Up")
window.onkeypress(abajo, "Down")
window.onkeypress(izquierda, "Left")
window.onkeypress(derecha, "Right")
window.onkeypress(inicio, "space")
window.onkeypress(pausa, "p")

# Inicia el juego
reiniciar_juego()

# Mantiene la ventana abierta hasta que se cierre manualmente
turtle.done()