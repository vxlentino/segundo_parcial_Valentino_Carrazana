import pygame
from variables import *
from funciones import mostrar_texto

pygame.init()

fuente_boton = pygame.font.SysFont("Arial Narrow",23)
fuente_volumen = pygame.font.SysFont("Arial Narrow",50)

#botones de ajuste de volumen
boton_suma = {}
boton_suma["superficie"] = pygame.Surface(TAMAÑO_BOTON_VOLUMEN)
boton_suma["rectangulo"] = boton_suma["superficie"].get_rect()
boton_suma["superficie"].fill(COLOR_ROJO)
boton_resta = {}
boton_resta["superficie"] = pygame.Surface(TAMAÑO_BOTON_VOLUMEN)
boton_resta["rectangulo"] = boton_resta["superficie"].get_rect()
boton_resta["superficie"].fill(COLOR_ROJO)
boton_volver = {}
boton_volver["superficie"] = pygame.Surface(TAMAÑO_BOTON_VOLVER)
boton_volver["rectangulo"] = boton_volver["superficie"].get_rect()
boton_volver["superficie"].fill(COLOR_AZUL)

def mostrar_configuracion(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict) -> str:
    retorno = "configuraciones"
    
    #manejo de eventos
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_suma["rectangulo"].collidepoint(evento.pos):
                print("SUMA VOLUMEN")
                
                if datos_juego["volumen_musica"] < 100:
                    datos_juego["volumen_musica"] += 5
                    pygame.mixer.music.set_volume(datos_juego["volumen_musica"] / 100)#acutaliza el volumen
                CLICK_SONIDO.play()
            elif boton_resta["rectangulo"].collidepoint(evento.pos):
                print("RESTA VOLUMEN")
                if datos_juego["volumen_musica"] > 0:
                    datos_juego["volumen_musica"] -= 5
                    pygame.mixer.music.set_volume(datos_juego["volumen_musica"] / 100)#acutaliza el volumen
                CLICK_SONIDO.play()
            elif boton_volver["rectangulo"].collidepoint(evento.pos):
                print("VOLVER AL MENU")
                CLICK_SONIDO.play()
                retorno = "menu"

    #dibujar fondo          
    pantalla.fill(COLOR_BLANCO)
    
    pos_x = (ANCHO - ANCHO_BOTON) // 2

    #dibujar botones
    boton_suma["rectangulo"] = pantalla.blit(boton_suma['superficie'],(610,200))
    boton_resta["rectangulo"] = pantalla.blit(boton_resta['superficie'],(20,200))
    boton_volver["rectangulo"] = pantalla.blit(boton_volver['superficie'],(10,10))
    
    mostrar_texto(boton_suma["superficie"],"VOL +",(0,10),fuente_boton,COLOR_NEGRO)
    mostrar_texto(boton_resta["superficie"],"VOL -",(0,10),fuente_boton,COLOR_NEGRO)
    mostrar_texto(boton_volver["superficie"],"VOLVER",(10,10),fuente_boton,COLOR_BLANCO)

    #porcentaje de volumen
    mostrar_texto(pantalla,f"{datos_juego["volumen_musica"]} %",(300,230),fuente_volumen,COLOR_NEGRO)
    
    #barra de volumen
    barra_rect = pygame.Rect(100, 300, 530, 30)#contorno de la barra
    nivel_volumen_rect = pygame.Rect(100, 300, int(530 * datos_juego["volumen_musica"] / 100), 30)#nivel actual

    pygame.draw.rect(pantalla, COLOR_GRIS_OSCURO, barra_rect)#fondo de la barra
    pygame.draw.rect(pantalla, COLOR_VERDE, nivel_volumen_rect)#nivel del volumen actual
    pygame.draw.rect(pantalla, COLOR_NEGRO, barra_rect, 2)#contorno

    return retorno
                
