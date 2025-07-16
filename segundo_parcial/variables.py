import pygame
pygame.init()

#COLORES
COLOR_BLANCO = (255,255,255,255)
COLOR_NEGRO = (0,0,0)
COLOR_VERDE = (0,255,0)
COLOR_ROJO = (255,0,0)
COLOR_AZUL = (0,0,255)
COLOR_VIOLETA = (134,23,219)
COLOR_PREGUNTADOS = (240,239,245,255)
COLOR_AMARILLO = (251, 255, 0)
COLOR_GRIS_OSCURO = (96,96,96)
COLOR_GRIS_CLARO = (200, 200, 200)


#RESOLUCION
ANCHO = 736
ALTO = 890
VENTANA = (ANCHO,ALTO)
#FRAMES
FPS = 60

#BOTONES
BOTON_JUGAR = 0
BOTON_CONFIG = 1
BOTON_PUNTUACIONES = 2
BOTON_SALIR = 3

#TAMAÑO DE BOTONES
TAMAÑO_PREGUNTA = (400,600)
TAMAÑO_RESPUESTA = (250,60)
ANCHO_BOTON = 250
ALTO_BOTON = 60
TAMAÑO_BOTON = (ANCHO_BOTON, ALTO_BOTON)
CUADRO_TEXTO = (250,50)
TAMAÑO_BOTON_VOLUMEN = (100,100)
TAMAÑO_BOTON_VOLVER = (100,40)
CLICK_SONIDO = pygame.mixer.Sound("C:\\Users\\valen\\OneDrive\\Escritorio\\segundo_parcial_Valentino_Carrazana\\segundo_parcial\\videoplayback (1).wav")
ERROR_SONIDO = pygame.mixer.Sound("C:\\Users\\valen\\OneDrive\\Escritorio\\segundo_parcial_Valentino_Carrazana\\segundo_parcial\error-126627 (1).wav")
MUSICA = pygame.mixer.music.load("C:\\Users\\valen\\OneDrive\\Escritorio\\segundo_parcial_Valentino_Carrazana\\segundo_parcial\\Undertale - Megalovania _ HQ (1).wav")

#VIDAS Y PUNTOS
CANTIDAD_VIDAS = 3
PUNTUACION_ACIERTO = 5
PUNTUACION_ERROR = 5


#FUENTES DEL JUEGO
FUENTE_TITULO = pygame.font.SysFont("Arial Narrow", 50)
FUENTE_NORMAL = pygame.font.SysFont("Arial Narrow", 40)
FUENTE_INPUT = pygame.font.SysFont("Arial Narrow", 35)
FUENTE_BOTON = pygame.font.SysFont("Arial Narrow", 30)
FUENTE_RESPUESTA = pygame.font.SysFont("Arial Narrow",23)
FUENTE_TEXTO_COMUN = pygame.font.SysFont("Arial Narrow",25) 
FUENTE_PREGUNTA = pygame.font.SysFont("Arial", 30) 

