import pygame
from variables import *
from menu import *
from juego import *
from configuracion import *
from ranking import *
from fin_del_juego import *


#configuraciones
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("PREGUNTADOS")

pantalla = pygame.display.set_mode(VENTANA)
corriendo = True
tiempo = pygame.time.Clock()
datos_juego = {"puntuacion":0, "vidas":CANTIDAD_VIDAS, "nombre":"", "volumen_musica":100}
primer_ventana = "menu"
musica_bandera = False
comodines_usados = {"bomba": False, "x2": False, "doble_chance": False, "pasar": False}
puntaje = 0

#arranco en juego
while corriendo:
    tiempo.tick(FPS)
    eventos = pygame.event.get()

    if primer_ventana == "menu":
        primer_ventana = mostrar_menu(pantalla,eventos)
    elif primer_ventana == "juego":
        if musica_bandera == False:
            porcentaje_vol = datos_juego["volumen_musica"] / 100
            musica_bandera = True
        primer_ventana = mostrar_juego(pantalla, eventos, datos_juego, comodines_usados, puntaje)
    elif primer_ventana == "configuraciones":
        primer_ventana = mostrar_configuracion(pantalla, eventos, datos_juego)
    elif primer_ventana == "rankings":
        primer_ventana = mostrar_rankings(pantalla, eventos)
    elif primer_ventana == "terminado":
        if musica_bandera == True:
            pygame.mixer.music.stop()
            musica_bandera = False            
        primer_ventana = mostrar_fin_juego(pantalla, eventos, datos_juego)
    elif primer_ventana == "salir":
        corriendo = False

    #actualizo
    pygame.display.flip()

pygame.quit()