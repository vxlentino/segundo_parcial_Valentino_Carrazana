import random
import time
import csv
import os
import json
from datetime import datetime
from variables import *
import pygame


# def mostrar_texto(superficie, texto, posicion, fuente, color=pygame.Color('black')):
#     palabras = [linea.split(' ') for linea in texto.splitlines()]  # Array 2D donde cada fila es una lista de palabras.
#     espacio = fuente.size(' ')[0]  # El ancho de un espacio.
#     max_ancho, max_alto = superficie.get_size()
#     x, y = posicion
#     for linea in palabras:
#         for palabra in linea:
#             superficie_palabra = fuente.render(palabra, False, color)
#             ancho_palabra, alto_palabra = superficie_palabra.get_size()
#             if x + ancho_palabra >= max_ancho:
#                 x = posicion[0]  # Reiniciar la posición x.
#                 y += alto_palabra  # Pasar a una nueva fila.
#             superficie.blit(superficie_palabra, (x, y))
#             x += ancho_palabra + espacio
#         x = posicion[0]  # Reiniciar la posición x.
#         y += alto_palabra  # Pasar a una nueva fila.


# def mostrar_texto(
#     superficie, 
#     texto, 
#     posicion=(0, 0), 
#     fuente=None, 
#     color=pygame.Color('black'), 
#     max_ancho=None, 
#     espaciado_lineas=0
# ):

#     if fuente is None:
#         fuente = pygame.font.SysFont('Arial', 20)  # Fuente por defecto.

#     if max_ancho is None:
#         max_ancho = superficie.get_width()  # Usa el ancho de la superficie si no se especifica.

#     palabras = [linea.split(' ') for linea in texto.splitlines()]  # Divide por líneas y palabras.
#     espacio = fuente.size(' ')[0]  # Ancho de un espacio.
#     x, y = posicion

#     for linea in palabras:
#         for palabra in linea:
#             superficie_palabra = fuente.render(palabra, True, color)
#             ancho_palabra, alto_palabra = superficie_palabra.get_size()
            
#             # Si el texto excede el ancho máximo, pasa a la siguiente línea.
#             if x + ancho_palabra > max_ancho:
#                 x = posicion[0]  # Reinicia la posición x.
#                 y += alto_palabra + espaciado_lineas  # Pasa a una nueva fila.

#             superficie.blit(superficie_palabra, (x, y))
#             x += ancho_palabra + espacio  # Avanza para la siguiente palabra.

#         # Salta a la siguiente línea al terminar una fila completa de texto.
#         x = posicion[0]
#         y += alto_palabra + espaciado_lineas

def mostrar_texto(pantalla, texto, posicion, fuente, color):
    # Aquí usamos 'fuente.size()' para obtener el tamaño del texto correctamente
    ancho_texto, alto_texto = fuente.size(texto)
    superficie_texto = fuente.render(texto, True, color)
    pantalla.blit(superficie_texto, posicion)
    

def mostrar_texto_simple(surface, texto, posicion, fuente, color=pygame.Color('black')):
    text_surface = fuente.render(texto, True, color)  # Renderizar el texto.
    surface.blit(text_surface, posicion)

def mezclar_lista(lista_preguntas:list) -> None:
    random.shuffle(lista_preguntas)
    
def verificar_respuesta(datos_juego:dict,pregunta_actual:dict,respuesta:int) -> bool:
    if respuesta == pregunta_actual["respuesta_correcta"]:
        datos_juego["puntuacion"] += PUNTUACION_ACIERTO
        retorno = True
    else:
        #SIN PUNTOS NEGATIVOS
        if datos_juego["puntuacion"] > PUNTUACION_ERROR:
            datos_juego["puntuacion"] -= PUNTUACION_ERROR
            
        #CON PUNTOS NEGATIVOS
        #datos_juego["puntuacion"] -= PUNTUACION_ERROR
        
        datos_juego["vidas"] -= 1
        retorno = False
    
    return retorno
    


def reiniciar_estadisticas(datos_juego:dict):
    datos_juego["puntuacion"] = 0
    datos_juego["vidas"] = CANTIDAD_VIDAS



def cargar_preguntas(nombre_archivo):
    with open(nombre_archivo, mode="r", encoding="utf-8") as archivo_csv:
        lector = csv.DictReader(archivo_csv)
        return list(lector)



def guardar_puntaje(datos):
    if not os.path.exists("partidas.json"):
        with open("partidas.json", "w") as archivo:
            archivo.write("[]")  # Crear un JSON vacío como lista.

    #leo el historial del archivo        
    with open("partidas.json", "r") as archivo:
        historial = json.load(archivo)
    
    #agrego el nuevo puntaje
    historial.append({
        "nombre": datos["nombre"],
        "puntaje": datos["puntaje"],
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    #guardo elm historial con las actualizaciones
    with open("partidas.json", "w") as archivo:
        json.dump(historial, archivo, indent=4)






def cargar_top_10(path:str) -> list:
    lista = []
    with open(path, "r") as archivo:
        contenido = archivo.read() #leo el contenido del archivo
        datos = json.loads(contenido)#convierto el contenido en una lista

        for elemento in datos:
            diccionario = dict()
            diccionario["nombre"] = elemento.get("nombre", "desconocido")
            diccionario["puntaje"] = elemento.get("puntaje", 0)
            diccionario["fecha"] = elemento.get("fecha", "sin fecha")
            lista.append(diccionario)

    #ordeno los puntajes para sacar el mejor
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[i]["puntaje"] < lista[j]["puntaje"]:
                #intercambio los elemnemtos
                lista[i], lista[j] = lista[j], lista[i]

    top_10 = lista[:10]
      

    return top_10

def comodin_X2(puntaje):
    puntos = puntaje * 2

    return puntos

def comodin_doble_chance(pregunta, respuesta_dada, puntaje):
    segunda_oportunidad = False
    if respuesta_dada == pregunta["respuesta"][pregunta["respuesta_correcta"]]:
        segunda_oportunidad = True

    return segunda_oportunidad


def manejar_tiempo_general(tiempo_inicio, limite_tiempo, datos_juego):
    tiempo_actual = time.time()
    tiempo_restante = max(0, int(limite_tiempo - (tiempo_actual - tiempo_inicio)))

    tiempo_agotado = False

    if tiempo_restante == 0:
        datos_juego["vidas"] = 0  # el jugador se queda sin vidas cuando se acaba el tiempo general
        tiempo_agotado = True  #el tiempo se agoto
    
    return tiempo_agotado

def mostrar_tiempo(pantalla, tiempo_restante):
    fuente_tiempo = pygame.font.SysFont("Arial Narrow", 30)
    texto_tiempo = fuente_tiempo.render(f"Tiempo restante: {tiempo_restante}s", True, COLOR_NEGRO)
    pantalla.blit(texto_tiempo, (10, 10))




