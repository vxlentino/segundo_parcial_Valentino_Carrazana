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

# Configuración del botón "Guardar y Volver"
boton_guardar_rect = pygame.Rect(ANCHO // 2 - 150, ALTO - 150, 300, 60)

#mensaje error cuando el usuario no ponga un nombre
mensaje_error_nombre = False


def mostrar_fin_juego(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict) -> str:
    global input_nombre, input_activo, mensaje_error_nombre


    retorno = "terminado"
    pantalla.fill(COLOR_BLANCO)
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            #estaria bueno forzarle al usuario que no pueda salir del juego hasta que guarde la puntuacion -> A gusto de ustedes
            if input_nombre.strip() != "":#bloqueo la salida hasta que ingrese el nombre
                retorno = "salir"

        elif evento.type == pygame.KEYDOWN:
            if input_activo: # Solo procesa si el campo de texto está activo
                if evento.key == pygame.K_BACKSPACE:
                    input_nombre = input_nombre[:-1] # Eliminar el último carácter
                    mensaje_error_nombre = False # Oculta el mensaje de error si el usuario empieza a escribir
                elif evento.key == pygame.K_RETURN: # Si presiona ENTER
                    if input_nombre.strip() != "": # Si hay un nombre válido
                        datos_juego["nombre"] = input_nombre.strip() # Asignar el nombre
                        guardar_puntaje(datos_juego) # Llamar a la función para guardar                        
                        
                        # Reiniciar para la próxima partida
                        input_nombre = "" 
                        datos_juego["puntuacion"] = 0
                        datos_juego["vidas"] = CANTIDAD_VIDAS
                        mensaje_error_nombre = False
                        retorno = "menu" # Volver al menú
                    else:
                        mensaje_error_nombre = True # Mostrar mensaje si el nombre está vacío
                else:
                    # Limitar el largo del nombre para que no se salga del cuadro
                    if len(input_nombre) < 20: 
                        input_nombre += evento.unicode # Añadir el carácter presionado

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            print(f"  MOUSEBUTTONDOWN. Pos: {evento.pos}")
            # Detectar clic en el campo de texto para activarlo/desactivarlo
            if input_rect.collidepoint(evento.pos):
                input_activo = not input_activo
            else:
                input_activo = False # Si clickea fuera, el input se desactiva
            
            # Detectar clic en el botón "Guardar y Volver"
            if boton_guardar_rect.collidepoint(evento.pos):
                if input_nombre.strip() != "": # Solo guardar si el nombre no está vacío
                    datos_juego["nombre"] = input_nombre.strip() 
                    guardar_puntaje(datos_juego) 
                    print("Puntaje guardado por botón.")
                    
                    # Reiniciar variables para una nueva partida
                    input_nombre = ""
                    datos_juego["puntuacion"] = 0
                    datos_juego["vidas"] = CANTIDAD_VIDAS
                    mensaje_error_nombre = False # Oculta el mensaje de error

                    retorno = "menu" # Cambia el estado a "menu"
                else:
                    mensaje_error_nombre = True # Muestra mensaje si el nombre está vacío al intentar guardar


    # --- Dibujar la pantalla de Fin de Juego ---
    
    # Título "¡Juego Terminado!"
    mostrar_texto(pantalla, "¡Juego Terminado!", 
                  (ANCHO // 2 - FUENTE_TITULO.size("¡Juego Terminado!")[0] // 2, 50), 
                  FUENTE_TITULO, COLOR_NEGRO)

    # Mostrar puntaje final
    mostrar_texto(pantalla, f"Puntuación final: {datos_juego['puntuacion']}", 
                  (ANCHO // 2 - FUENTE_NORMAL.size(f"Puntuación final: {datos_juego['puntuacion']}")[0] // 2, 150), 
                  FUENTE_NORMAL, COLOR_NEGRO)
    
    # Mensaje para ingresar el nombre
    mostrar_texto(pantalla, "Ingresa tu nombre para el Ranking:", 
                  (ANCHO // 2 - FUENTE_NORMAL.size("Ingresa tu nombre para el Ranking:")[0] // 2, ALTO // 2 + 30), 
                  FUENTE_NORMAL, COLOR_NEGRO)

    # Dibujar el campo de texto (input box)
    pygame.draw.rect(pantalla, color_input_fondo, input_rect) # Fondo del input
    # Borde del input, cambia de color si está activo
    pygame.draw.rect(pantalla, color_input_borde if input_activo else COLOR_GRIS_OSCURO, input_rect, 3) 
    
    # Texto dentro del input box
    superficie_texto_input = FUENTE_INPUT.render(input_nombre, True, COLOR_NEGRO)
    # Ajustar la posición del texto para que esté un poco más hacia la izquierda del borde y centrado verticalmente
    texto_rect = superficie_texto_input.get_rect(x=input_rect.x + 5, centery=input_rect.centery)
    pantalla.blit(superficie_texto_input, texto_rect)

    # Mostrar mensaje de error si el nombre está vacío y se intentó guardar
    if mensaje_error_nombre:
        mostrar_texto(pantalla, "¡Debes ingresar un nombre!", 
                      (ANCHO // 2 - FUENTE_NORMAL.size("¡Debes ingresar un nombre!")[0] // 2, input_rect.bottom + 10), 
                      FUENTE_NORMAL, COLOR_ROJO)

    # Dibujar el botón "Guardar y Volver al Menú"
    pygame.draw.rect(pantalla, COLOR_VERDE, boton_guardar_rect) # Fondo del botón
    # Centrar el texto en el botón
    mostrar_texto(pantalla, "Guardar y Volver", 
                  (boton_guardar_rect.x + (boton_guardar_rect.width - FUENTE_BOTON.size("Guardar y Volver")[0]) // 2, 
                   boton_guardar_rect.y + (boton_guardar_rect.height - FUENTE_BOTON.size("Guardar y Volver")[1]) // 2), 
                  FUENTE_BOTON, COLOR_BLANCO)




    return retorno



    
