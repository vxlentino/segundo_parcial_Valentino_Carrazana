import random
import time
import csv
import os
import json
from datetime import datetime
from variables import *
import pygame


def mostrar_texto(superficie: pygame.Surface, texto: str, posicion: tuple[int, int], fuente: pygame.font.Font, color: tuple[int,int,int], centrado: bool = False, ancho_max: int = None) -> None:
    """
    Muestra texto en una superficie de Pygame.

    Args:
        superficie_destino:la superficie donde se dibujará el texto.
        texto:el string de texto a mostrar.
        posicion:una tupla (x, y) que representa la esquina superior izquierda del texto
                  o el centro si 'centrado' es True.
        fuente:el objeto de fuente de Pygame.
        color:el color del texto (tupla RGB).
        centrado:si es True, 'posicion' se considera el centro del texto.
                  si es False (por defecto), 'posicion' es la esquina superior izquierda.
    """
    if ancho_max is None: #si no hay ancho_max, se comporta como antes (una sola línea)
        render = fuente.render(texto, True, color)
        rect = render.get_rect()
        if centrado:
            rect.center = posicion
        else:
            rect.topleft = posicion
        superficie.blit(render, rect)
    else: #si hay ancho_max, envolver el texto
        palabras = texto.split(' ')
        lineas = []
        linea_actual = ""
        espacio = fuente.size(" ")[0] #ancho de un espacio

        for palabra in palabras:
            ancho_palabra, alto_palabra = fuente.size(palabra)
            
            #si la palabra es más grande que el ancho_max, la cortamos
            if ancho_palabra > ancho_max:
                #caso extremo:si una palabra es muy larga, la tratamos como linea 

                # asumimos que las palabras individuales suelen caber.
                if linea_actual: # Si hay algo en la línea actual, añadirla y empezar una nueva
                    lineas.append(linea_actual)
                linea_actual = palabra # Esta palabra será una línea por sí misma (y se cortará si excede el ancho_max)
                lineas.append(linea_actual)
                linea_actual = ""
                continue


            if fuente.size(linea_actual + palabra)[0] + espacio > ancho_max and linea_actual:
                lineas.append(linea_actual)
                linea_actual = palabra + " "
            else:
                linea_actual += palabra + " "
        
        if linea_actual:
            lineas.append(linea_actual)
        
        y_offset = 0
        for linea in lineas:
            render = fuente.render(linea.strip(), True, color) # .strip() para quitar el espacio extra al final
            rect = render.get_rect()
            
            #ajustar la posición de cada línea
            if centrado:
                rect.centerx = posicion[0]
                rect.top = posicion[1] + y_offset
            else:
                rect.topleft = (posicion[0], posicion[1] + y_offset)
            
            superficie.blit(render, rect)
            y_offset += fuente.get_linesize() #avanza para la siguiente línea

    

def mostrar_texto_simple(surface, texto, posicion, fuente, color=pygame.Color('black')):
    texto_renderizado = fuente.render(texto, True, color)  # Renderizar el texto.
    surface.blit(texto_renderizado, posicion)




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
        "puntaje": datos["puntuacion"],
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    #guardo elm historial con las actualizaciones
    with open("partidas.json", "w") as archivo:
        json.dump(historial, archivo, indent=4)





def crear_archivo_partida_si_no_existe():
    path_partidas = "partidas.json"
    if not os.path.exists(path_partidas):
        try:
            with open(path_partidas, "w", encoding="utf-8") as archivo:
                json.dump([], archivo, indent=4) # creo un JSON valido con una lista vacia
            print(f"Archivo '{path_partidas}' creado exitosamente.")
        except IOError as e:
            print(f"Error al crear el archivo '{path_partidas}': {e}")






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




