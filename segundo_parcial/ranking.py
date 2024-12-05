import pygame
import json
import os
from variables import *
from funciones import *

pygame.init()
fuente = pygame.font.SysFont("Arial Narrow",32)
fuente_boton = pygame.font.SysFont("Arial Narrow",23)
boton_volver = {}
boton_volver["superficie"] = pygame.Surface(TAMAÑO_BOTON_VOLVER)
boton_volver["rectangulo"] = boton_volver["superficie"].get_rect()
boton_volver["superficie"].fill(COLOR_AZUL)

top_10 = "partidas.json"

def mostrar_rankings(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event]):
    retorno = "rankings"
    
    top_10_cargado = cargar_top_10(top_10)

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            
            if boton_volver["rectangulo"].collidepoint(evento.pos):
                print("VOLVER AL MENU")
                # CLICK_SONIDO.play()
                retorno = "menu"
    
    pantalla.fill(COLOR_BLANCO)
    boton_volver["rectangulo"] = pantalla.blit(boton_volver["superficie"],(10,10))
    mostrar_texto(boton_volver["superficie"],"VOLVER",(10,10),fuente_boton,COLOR_BLANCO)

    #muestro el top 10 
    y_inicial = 100 #cordenada inicial
    y_incremental = 40 #incremento las filas

    mostrar_texto(pantalla,f"TOP 10 PUNTAJES",(20,50),fuente,COLOR_NEGRO)
    if top_10_cargado:
        for i, entrada in enumerate(top_10_cargado):
            texto = f"{i+1}. {entrada['nombre']} - {entrada['puntaje']} pts"
            mostrar_texto(pantalla, texto,(20, y_inicial + i * y_incremental), fuente, COLOR_NEGRO)
    else:
        mostrar_texto(pantalla, "No hay partidas registradas",(20, y_inicial), fuente, COLOR_NEGRO)
    
    return retorno
                
    
    