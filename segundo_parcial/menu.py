import pygame
from variables import *
from funciones import *

pygame.init()


pantalla = pygame.display.set_mode(VENTANA)

fuente_menu = pygame.font.SysFont("Arial", 25)
lista_botones = []

for i in range(4):
    boton = {}
    boton['superficie'] = pygame.Surface(TAMAÑO_BOTON)
    boton['superficie'].fill(COLOR_ROJO)
    boton['rectangulo'] = boton['superficie'].get_rect()
    lista_botones.append(boton)
    

def mostrar_menu(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event])-> str:

    pantalla.fill(COLOR_BLANCO)
    #Gestionar eventos:
    retorno = "menu"
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(lista_botones)): 
                if lista_botones[i]["rectangulo"].collidepoint(evento.pos):
                    print(f"boton presionado: {i}")#debug
                    # CLICK_SONIDO.play()
                    if i == BOTON_SALIR:
                        retorno = "salir"  
                    elif i == BOTON_JUGAR:
                        retorno = "juego"  
                    elif i == BOTON_PUNTUACIONES:
                        print(f"boton presionado: {i}")#debug
                        retorno = "rankings"
                    elif i == BOTON_CONFIG:
                        retorno = "configuraciones"        
        elif evento.type == pygame.QUIT:
            retorno = "salir"


    # lista_botones[0]["rectangulo"] = pygame.rect(125,115, ANCHO_BOTON, ALTO_BOTON)
    # lista_botones[1]["rectangulo"] = pygame.rect(125,195, ANCHO_BOTON, ALTO_BOTON)
    # lista_botones[2]["rectangulo"] = pygame.rect(125,275, ANCHO_BOTON, ALTO_BOTON)
    # lista_botones[3]["rectangulo"] = pygame.rect(125,355, ANCHO_BOTON, ALTO_BOTON)


    pos_x = (ANCHO - ANCHO_BOTON) // 2
   
    lista_botones[0]["rectangulo"] = pantalla.blit(lista_botones[0]["superficie"],(pos_x,115))
    lista_botones[1]["rectangulo"] = pantalla.blit(lista_botones[1]["superficie"],(pos_x,195))
    lista_botones[2]["rectangulo"] = pantalla.blit(lista_botones[2]["superficie"],(pos_x,275))
    lista_botones[3]["rectangulo"] = pantalla.blit(lista_botones[3]["superficie"],(pos_x,355))

    mostrar_texto(pantalla, "JUEGO", (pos_x,127), fuente_menu, COLOR_NEGRO)
    mostrar_texto(pantalla, "CONFIGURACION", ( pos_x,208), fuente_menu, COLOR_NEGRO)
    mostrar_texto(pantalla, "PUNTUACION", ( pos_x,295), fuente_menu, COLOR_NEGRO)
    mostrar_texto(pantalla, "SALIR", ( pos_x,370), fuente_menu, COLOR_NEGRO)


    return retorno