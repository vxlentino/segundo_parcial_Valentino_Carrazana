import pygame
import json
import csv
from datetime import datetime
from variables import *
from funciones import *
from juego import *

pygame.init()

fuente = pygame.font.SysFont("Arial Narrow",40)
cuadro = {}
cuadro["superficie"] = pygame.Surface(CUADRO_TEXTO)
cuadro["rectangulo"] = cuadro["superficie"].get_rect()
cuadro['superficie'].fill(COLOR_AZUL)
nombre = ""
preguntas = cargar_preguntas("preguntas.csv")

def mostrar_fin_juego(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict) -> str:
    global nombre
    retorno = "terminado"

    pantalla.fill(COLOR_BLANCO)
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            #Estaria bueno forzarle al usuario que no pueda salir del juego hasta que guarde la puntuacion -> A gusto de ustedes
            if nombre.strip() != "":#bloqueo la salida hasta que ingrese el nombre
                retorno = "salir"

        elif evento.type == pygame.KEYDOWN:
            bloc_mayus = pygame.key.get_mods() and pygame.KMOD_CAPS
            letra_presionada = pygame.key.name(evento.key)
            
            if letra_presionada == "backspace" and len(nombre) > 0:
                nombre = nombre[0:-1]#Elimino el ultimo
                cuadro["superficie"].fill(COLOR_AZUL)
            
            if letra_presionada == "space":
                nombre += " "
            
            elif len(letra_presionada) == 1 and letra_presionada.isalnum():
                if bloc_mayus != 0:
                    nombre += letra_presionada.upper()
                else:
                    nombre += letra_presionada.lower()

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if cuadro["rectangulo"].collidepoint(evento.pos):#si hace click en el cuadro de texto
                if nombre.strip() != "":#si el nombre no esta vacio, lo guardo y vuelvo al menu

                    # resultados_preguntas = datos_juego["resultados_preguntas"]
                    # actualizar_estadisticas_preguntas(preguntas, resultados_preguntas)
                    # guardar_estadisticas_preguntas("preguntas.csv", preguntas)

                    #guardo en archivo JSON
                    datos = {
                        "nombre": nombre.strip(),#.strip() limpia los espacios no deseados
                        "puntaje": datos_juego["puntuacion"],
                        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    }
                    guardar_puntaje(datos)
                    print("se guardo el puntaje")
                    nombre = ""
                    datos_juego["puntuacion"] = 0
                    datos_juego["vidas"] = CANTIDAD_VIDAS
                    retorno = "menu"



    #donde el usuario escribe el nombre
    cuadro["rectangulo"] = pantalla.blit(cuadro["superficie"],(130,200))
    mostrar_texto(cuadro["superficie"],nombre,(10,0),fuente,COLOR_BLANCO)
    mostrar_texto(pantalla, "tiene que ingresar un nombre", (150, 250), fuente, COLOR_NEGRO)

    #muestro el puntaje del usuario
    mostrar_texto_simple(pantalla, "usted obtuvo:", (150, 150), fuente, COLOR_NEGRO)
    mostrar_texto_simple(pantalla, str(datos_juego["puntuacion"]), (350,150), fuente, COLOR_NEGRO)

    # mostrar_texto_simple(pantalla, f"aciertos: {pregunta_actual['cantidad_aciertos']}")
    
    return retorno