import pygame
import json
import csv
from datetime import datetime
from variables import *
from funciones import *


input_nombre = "" #la cadena donde se guarda el nombre que el usuario escribe
input_rect = pygame.Rect(ANCHO // 2 - 150, ALTO // 2 + 100, 300, 50) #rectangulo para el campo de texto
input_activo = True #el input box esta activo por defecto para que el usuario pueda empezar a escribir
color_input_borde = COLOR_AZUL #color del borde cuando el input esta vacio
color_input_fondo = COLOR_GRIS_CLARO #fondo del input box

#configuración del botón "guardar y volver"
boton_guardar_rect = pygame.Rect(ANCHO // 2 - 150, ALTO - 150, 300, 60)

#mensaje error cuando el usuario no ponga un nombre
mensaje_error_nombre = False


def mostrar_fin_juego(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict) -> str:
    global input_nombre, input_activo, mensaje_error_nombre


    retorno = "terminado"
    pantalla.fill(COLOR_BLANCO)
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            if input_nombre.strip() != "":#bloqueo la salida hasta que ingrese el nombre
                retorno = "salir"

        elif evento.type == pygame.KEYDOWN:
            if input_activo: #solo procesa si el campo de texto está activo
                if evento.key == pygame.K_BACKSPACE:
                    input_nombre = input_nombre[:-1] #eliminar el ultimo caracter
                    mensaje_error_nombre = False #oculta el mensaje de error si el usuario empieza a escribir
                elif evento.key == pygame.K_RETURN: #si presiona ENTER
                    if input_nombre.strip() != "": #si hay un nombre valido
                        datos_juego["nombre"] = input_nombre.strip() #asignar el nombre
                        guardar_puntaje(datos_juego) #llamar a la funcion para guardar                        
                        
                        #reiniciar para la proxima partida
                        input_nombre = "" 
                        datos_juego["puntuacion"] = 0
                        datos_juego["vidas"] = CANTIDAD_VIDAS
                        mensaje_error_nombre = False
                        retorno = "menu" #volver al menu
                    else:
                        mensaje_error_nombre = True #mostrar mensaje si el nombre esta vacío
                else:
                    #limitar el largo del nombre para que no se salga del cuadro
                    if len(input_nombre) < 20: 
                        input_nombre += evento.unicode #añadir el caracter presionado

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            print(f"  MOUSEBUTTONDOWN. Pos: {evento.pos}")
            #detectar clic en el campo de texto para activarlo/desactivarlo
            if input_rect.collidepoint(evento.pos):
                input_activo = not input_activo
            else:
                input_activo = False #si clickea fuera, el input se desactiva
            
            #detectar clic en el boton "Guardar y Volver"
            if boton_guardar_rect.collidepoint(evento.pos):
                if input_nombre.strip() != "": #solo guardar si el nombre no esta vacío
                    datos_juego["nombre"] = input_nombre.strip() 
                    guardar_puntaje(datos_juego) 
                    print("Puntaje guardado por botón.")
                    
                    #reiniciar variables para una nueva partida
                    input_nombre = ""
                    datos_juego["puntuacion"] = 0
                    datos_juego["vidas"] = CANTIDAD_VIDAS
                    mensaje_error_nombre = False #oculta el mensaje de error

                    retorno = "menu" #cambia el estado a "menu"
                else:
                    mensaje_error_nombre = True #muestra mensaje si el nombre está vacío al intentar guardar


    #dibujo la pantalla de fin del juego    
    #titulo
    mostrar_texto(pantalla, "¡Juego Terminado!", 
                  (ANCHO // 2 - FUENTE_TITULO.size("¡Juego Terminado!")[0] // 2, 50), 
                  FUENTE_TITULO, COLOR_NEGRO)

    #mostrar puntaje final
    mostrar_texto(pantalla, f"Puntuación final: {datos_juego['puntuacion']}", 
                  (ANCHO // 2 - FUENTE_NORMAL.size(f"Puntuación final: {datos_juego['puntuacion']}")[0] // 2, 150), 
                  FUENTE_NORMAL, COLOR_NEGRO)
    
    #mensaje para ingresar el nombre
    mostrar_texto(pantalla, "Ingresa tu nombre para el Ranking:", 
                  (ANCHO // 2 - FUENTE_NORMAL.size("Ingresa tu nombre para el Ranking:")[0] // 2, ALTO // 2 + 30), 
                  FUENTE_NORMAL, COLOR_NEGRO)

    #dibujar el campo de texto (input box)
    pygame.draw.rect(pantalla, color_input_fondo, input_rect) # Fondo del input
    #borde del input, cambia de color si esta activo
    pygame.draw.rect(pantalla, color_input_borde if input_activo else COLOR_GRIS_OSCURO, input_rect, 3) 
    
    #texto dentro del input box
    superficie_texto_input = FUENTE_INPUT.render(input_nombre, True, COLOR_NEGRO)
    #ajustar la posición del texto para que esté un poco más hacia la izquierda del borde y centrado verticalmente
    texto_rect = superficie_texto_input.get_rect(x=input_rect.x + 5, centery=input_rect.centery)
    pantalla.blit(superficie_texto_input, texto_rect)

    #mostrar mensaje de error si el nombre esta vacio y se intento guardar
    if mensaje_error_nombre:
        mostrar_texto(pantalla, "¡Debes ingresar un nombre!", 
                      (ANCHO // 2 - FUENTE_NORMAL.size("¡Debes ingresar un nombre!")[0] // 2, input_rect.bottom + 10), 
                      FUENTE_NORMAL, COLOR_ROJO)

    #dibujar el botón "guardar y Volver al Menu"
    pygame.draw.rect(pantalla, COLOR_VERDE, boton_guardar_rect) #fondo del boton
    #centrar el texto en el boton
    mostrar_texto(pantalla, "Guardar y Volver", 
                  (boton_guardar_rect.x + (boton_guardar_rect.width - FUENTE_BOTON.size("Guardar y Volver")[0]) // 2, 
                   boton_guardar_rect.y + (boton_guardar_rect.height - FUENTE_BOTON.size("Guardar y Volver")[1]) // 2), 
                  FUENTE_BOTON, COLOR_BLANCO)




    return retorno



    
