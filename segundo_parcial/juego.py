import pygame
import time
from variables import *
from funciones import *


# pygame.mixer.music.load("d:\GOOGLE\Undertale - Megalovania _ HQ [kBoFfB9fQZQ].mp3")  # Ruta del archivo
# pygame.mixer.music.set_volume(0.5)  # Ajusta el volumen (0.0 a 1.0)
# pygame.mixer.music.play(-1)  # -1 para reproducir en bucle infinito



imagen = pygame.image.load("C:\\Users\\valen\\OneDrive\\Escritorio\\segundo_parcial_Valentino_Carrazana\\segundo_parcial\\preguntados.jpg")
imagen_preguntados = pygame.transform.scale(imagen, (ANCHO, ALTO))
preguntados_rectangulo = imagen_preguntados.get_rect()
preguntados_rectangulo.topleft = (0, 0)


#variables globales
lista_preguntas_juego_actual = []
indice_pregunta_actual = 0 #INMUTABLE -> En la funcion las declaro como global
bandera_respuesta = False #INMUTABLE -> En la funcion las declaro como global
respuesta_seleccionada_idx = -1 #-1 significa ninguna seleccionada
contador_correctas = 0 #contador de respuestas correctas

#variables para comodines
efecto_x2_activo = False
doble_chance_activa = False
respuestas_eliminadas_bomba = [] #para almacenar los indices de respuestas incorrectas eliminadas por la bomba

comodines_disponibles_actual = {
    "bomba": True,
    "x2": True,
    "doble_chance": True,
    "pasar": True
    }
tiempo_inicio_partida = 0 #para resetear el tiempo de la partida

#estructura del juego
cuadro_pregunta = {}
cuadro_pregunta["superficie"] = pygame.Surface((580,250))
cuadro_pregunta["rectangulo"] = cuadro_pregunta["superficie"].get_rect()

cartas_respuestas = []
for i in range(3):
    cuadro_respuesta = {}
    cuadro_respuesta["superficie"] = pygame.Surface((690,86))    
    cuadro_respuesta["rectangulo"] = cuadro_respuesta["superficie"].get_rect()
    cartas_respuestas.append(cuadro_respuesta)


#botones 
boton_bomba = pygame.Surface((150, 50))
boton_x2 = pygame.Surface((150, 50))
boton_doble_chance = pygame.Surface((150, 50))
boton_pasar = pygame.Surface((150, 50))


#definir rectangulos
rect_bomba = boton_bomba.get_rect(topleft=(600, 300))
rect_x2 = boton_x2.get_rect(topleft=(600, 350))
rect_doble_chance = boton_doble_chance.get_rect(topleft=(600, 400))
rect_pasar = boton_pasar.get_rect(topleft=(600, 450))

#lista de botones
lista_comodines_superficies = [boton_bomba, boton_x2, boton_doble_chance, boton_pasar]
lista_rectangulos_comodines = [rect_bomba, rect_x2, rect_doble_chance, rect_pasar]


limite_tiempo_general = 120 #2 minutos



def mostrar_juego(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict, comodines_usados_param:dict, puntaje_param:int) -> str:
    global indice_pregunta_actual, bandera_respuesta, contador_correctas, respuesta_seleccionada_idx
    global lista_preguntas_juego_actual, comodines_disponibles_actual, tiempo_inicio_partida
    global efecto_x2_activo, doble_chance_activa, respuestas_eliminadas_bomba 

    retorno = "juego"

    #logica del reinicio de juego o inicio de partida
    #esto asegura que solo reinicie las preguntas y comodines al inicio de una *nueva* partida
    if datos_juego["vidas"] == CANTIDAD_VIDAS and datos_juego["puntuacion"] == 0 and indice_pregunta_actual == 0 and not lista_preguntas_juego_actual:
        lista_preguntas_juego_actual = cargar_preguntas("preguntas.csv")
        mezclar_lista(lista_preguntas_juego_actual)
        indice_pregunta_actual = 0
        bandera_respuesta = False
        respuesta_seleccionada_idx = -1 #reinicio tambien este indice al inicio de la partida
        contador_correctas = 0
        comodines_disponibles_actual = { #reinicia los comodines
            "bomba": True,
            "x2": True,
            "doble_chance": True,
            "pasar": True
        }
        tiempo_inicio_partida = time.time() #reinicia el tiempo de la partida
        efecto_x2_activo = False
        doble_chance_activa = False
        respuestas_eliminadas_bomba.clear()


    #si las vidas llegan a 0 o si se acaban las preguntas, el juego termina.
    if datos_juego["vidas"] <= 0:
        return "terminado"
    #asegurarse de que hay preguntas en la lista
    if not lista_preguntas_juego_actual:        
        return "terminado" #forzar a "terminado" si no hay preguntas para evitar errores
    #si el indice actual excede la cantidad de preguntas, el juego termina
    if indice_pregunta_actual >= len(lista_preguntas_juego_actual):
        return "terminado"

    #obtiene la pregunta actual solo despues de verificar las condiciones de fin de juego
    pregunta_actual = lista_preguntas_juego_actual[indice_pregunta_actual]

    #gestion del tiempo de partida
    tiempo_agotado = manejar_tiempo_general(tiempo_inicio_partida, limite_tiempo_general, datos_juego)
    if tiempo_agotado:
        return "terminado" #si el tiempo se agota, termina el juego

    tiempo_restante = int(limite_tiempo_general - (time.time() - tiempo_inicio_partida))
    if tiempo_restante < 0:
        tiempo_restante = 0


    #dibujo la base
    pantalla.blit(imagen_preguntados, preguntados_rectangulo)
    cuadro_pregunta["superficie"].fill(COLOR_PREGUNTADOS)
    mostrar_texto(cuadro_pregunta["superficie"], f"{pregunta_actual['pregunta']}", (20, 20), FUENTE_PREGUNTA, COLOR_NEGRO, ancho_max=cuadro_pregunta["superficie"].get_width() - 40)
    pantalla.blit(cuadro_pregunta["superficie"],(80,200))


    for i, carta in enumerate(cartas_respuestas):
        # Determinar el color de fondo de la carta
        if i in respuestas_eliminadas_bomba:
            carta["superficie"].fill(COLOR_GRIS_CLARO) # Color para respuestas eliminadas por bomba
            texto_color = COLOR_GRIS_OSCURO
            texto_respuesta = "ELIMINADA" # Mostrar texto "ELIMINADA"
            centrado_texto = True
        elif not bandera_respuesta: # Si aún no se ha respondido, son blancas
            carta["superficie"].fill(COLOR_BLANCO)
            texto_color = COLOR_NEGRO
            centrado_texto = False # Asume que tus textos de respuesta normal no están centrados
        elif i == respuesta_seleccionada_idx: # Si es la respuesta seleccionada (ya pintada en evento)
            # El color ya fue establecido en el evento MOUSEBUTTONDOWN (verde/rojo)
            # Solo aseguramos que el texto se dibuje encima en negro
            texto_color = COLOR_NEGRO
            centrado_texto = False
        else: # Las otras respuestas después de seleccionar una
            carta["superficie"].fill(COLOR_BLANCO)
            texto_color = COLOR_NEGRO
            centrado_texto = False

        # Obtener el texto de la respuesta original
        if i == 0: texto_original = pregunta_actual['respuesta_1']
        elif i == 1: texto_original = pregunta_actual['respuesta_2']
        elif i == 2: texto_original = pregunta_actual['respuesta_3']
        
        # Dibujar el texto en la superficie de la carta
        if i in respuestas_eliminadas_bomba:
            # Si fue eliminada por bomba, el texto es "ELIMINADA"
            mostrar_texto(carta["superficie"], texto_respuesta, (carta["superficie"].get_width() // 2, carta["superficie"].get_height() // 2), FUENTE_RESPUESTA, texto_color, centrado=True)
        else:
            # Si no fue eliminada por bomba, usa el texto original
            mostrar_texto(carta["superficie"], texto_original, (20, 20), FUENTE_RESPUESTA, texto_color) # Ya no usar centrado=True aquí para respuestas normales.

        # Blitear la superficie de la carta a la pantalla principal
        cartas_respuestas[i]['rectangulo'] = pantalla.blit(carta['superficie'],(23,583 + i * 103)) # Ajusta 103 por tu espacio entre cartas


    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            return "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            #logica de respuestas
            if not bandera_respuesta:
                for i in range(len(cartas_respuestas)):
                    if cartas_respuestas[i]['rectangulo'].collidepoint(evento.pos):

                        if i in respuestas_eliminadas_bomba:
                            print("no se puede seleccionar una respuesta eliminada")
                            continue

                        respuesta_usuario = (i + 1)
                        respuesta_seleccionada_idx = i

                        puntos_a_sumar = PUNTUACION_ACIERTO
                        
                        if int(respuesta_usuario) == int(pregunta_actual['respuesta_correcta']):
                            cartas_respuestas[i]['superficie'].fill(COLOR_VERDE)
                            print("RESPUESTA CORRECTA")
                            if efecto_x2_activo:
                                puntos_a_sumar *= 2
                                efecto_x2_activo = False
                                print("puntos X2")
                            datos_juego["puntuacion"] += puntos_a_sumar 
                            contador_correctas += 1                        
                            if contador_correctas == 5:
                                datos_juego["vidas"] += 1
                                contador_correctas = 0
                                print("GANASTE UNA VIDA!!!")
                        else:
                            cartas_respuestas[i]['superficie'].fill(COLOR_ROJO)
                            print("RESPUESTA INCORRECTA")

                            if doble_chance_activa:
                                print("doble chande no pierdes vida y podes volver a intentar")
                                doble_chance_activa = False
                                bandera_respuesta = False
                                respuesta_seleccionada_idx = -1

                                if efecto_x2_activo:
                                    efecto_x2_activo = False
                                    print("efecto X2 desactivado (respues incorrecta y doble chance)")

                                continue

                            else:
                                datos_juego["vidas"] -= 1
                                if efecto_x2_activo:
                                    efecto_x2_activo = False
                                    print("efecto X2 desactivado (respuesta incorrecta)")
                                bandera_respuesta = True

                        print(f"SE HIZO CLICK EN UNA RESPUESTA {respuesta_usuario}")
                        bandera_respuesta = True

                        if respuesta_seleccionada_idx == 0:
                            texto_respuesta_actual = pregunta_actual["respuesta_1"]
                        elif respuesta_seleccionada_idx == 1:
                            texto_respuesta_actual = pregunta_actual["respuesta_2"]
                        elif respuesta_seleccionada_idx == 2:
                            texto_respuesta_actual = pregunta_actual["respuesta_3"]

                        mostrar_texto(cartas_respuestas[i]["superficie"], texto_respuesta_actual, (20, 20), FUENTE_RESPUESTA, COLOR_NEGRO)
                        

                        pantalla.blit(cartas_respuestas[i]['superficie'], cartas_respuestas[i]['rectangulo'].topleft)
                        pygame.display.update(cartas_respuestas[i]['rectangulo']) 
                        
                        break

                #logica de comodines
                for i in range(len(lista_rectangulos_comodines)):
                    if lista_rectangulos_comodines[i].collidepoint(evento.pos):
                        if i == 0 and comodines_disponibles_actual["bomba"] and not bandera_respuesta:
                            comodines_disponibles_actual["bomba"] = False
                            print("comodin bomba activado")
                            #logica para la bomba (ej eliminar una respuesta incorrecta)
                            respuestas_incorrectas_indices = []
                            for j in range(1, 4): #las respuestas estan en 'respuesta_1', 'respuesta_2', 'respuesta_3'
                                if str(j) != str(pregunta_actual['respuesta_correcta']):
                                    respuestas_incorrectas_indices.append(j - 1) #guardar el indice (0, 1, 2)

                            import random
                            random.shuffle(respuestas_incorrectas_indices)

                            respuestas_eliminadas_bomba.clear()                            
                            if len(respuestas_incorrectas_indices) >=1:
                                respuestas_eliminadas_bomba.append(respuestas_incorrectas_indices[0])
                            if len(respuestas_incorrectas_indices) >=2:                                
                                respuestas_eliminadas_bomba.append(respuestas_incorrectas_indices[1])  


                            boton_bomba.fill(COLOR_GRIS_OSCURO) # Rellenar el botón mismo
                            mostrar_texto(boton_bomba, "BOMBA", (boton_bomba.get_width() // 2, boton_bomba.get_height() // 2), FUENTE_TEXTO_COMUN, COLOR_BLANCO, centrado=True)
                            pantalla.blit(boton_bomba, lista_rectangulos_comodines[i])
                            pygame.display.update(lista_rectangulos_comodines[i])

                            # pygame.draw.rect(pantalla, COLOR_GRIS_OSCURO, lista_rectangulos_comodines[i]) # Pinta el botón de gris
                            # mostrar_texto(lista_comodines_superficies[i], "BOMBA", (lista_comodines_superficies[i].get_width() // 2, lista_comodines_superficies[i].get_height() // 2), FUENTE_TEXTO_COMUN, COLOR_BLANCO, centrado=True)
                            # pantalla.blit(lista_comodines_superficies[i], lista_rectangulos_comodines[i])
                            # pygame.display.update(lista_rectangulos_comodines[i])   

       
                        elif i == 1 and comodines_disponibles_actual["x2"] and not bandera_respuesta:
                            comodines_disponibles_actual["x2"] = False
                            print("comodin x2 activado")
                            #aplicar x2 al puntaje de la próxima respuesta correcta
                            boton_bomba.fill(COLOR_GRIS_OSCURO) # Rellenar el botón mismo
                            mostrar_texto(boton_bomba, "X2", (boton_bomba.get_width() // 2, boton_bomba.get_height() // 2), FUENTE_TEXTO_COMUN, COLOR_BLANCO, centrado=True)
                            pantalla.blit(boton_bomba, lista_rectangulos_comodines[i])
                            pygame.display.update(lista_rectangulos_comodines[i])

                        elif i == 2 and comodines_disponibles_actual["doble_chance"] and not bandera_respuesta:
                            comodines_disponibles_actual["doble_chance"] = False
                            doble_chance_activa = True
                            print("comodin doble_chance activado")
                            #logica para la doble chance
                            boton_bomba.fill(COLOR_GRIS_OSCURO) # Rellenar el botón mismo
                            mostrar_texto(boton_bomba, "DOBLE CHANCE", (boton_bomba.get_width() // 2, boton_bomba.get_height() // 2), FUENTE_TEXTO_COMUN, COLOR_BLANCO, centrado=True)
                            pantalla.blit(boton_bomba, lista_rectangulos_comodines[i])
                            pygame.display.update(lista_rectangulos_comodines[i])

                        elif i == 3 and comodines_disponibles_actual["pasar"]:
                            comodines_disponibles_actual["pasar"] = False
                            print("comodin pasar activado")
                            indice_pregunta_actual += 1 #pasa a la siguiente pregunta
                            tiempo_inicio_partida = time.time() #reinicia el contador para el tiempo_restante general
                            bandera_respuesta = False
                            respuesta_seleccionada_idx = -1

                            respuestas_eliminadas_bomba.clear()
                            efecto_x2_activo = False
                            doble_chance_activa = False

                            boton_bomba.fill(COLOR_GRIS_OSCURO) # Rellenar el botón mismo
                            mostrar_texto(boton_bomba, "PASAR", (boton_bomba.get_width() // 2, boton_bomba.get_height() // 2), FUENTE_TEXTO_COMUN, COLOR_BLANCO, centrado=True)
                            pantalla.blit(boton_bomba, lista_rectangulos_comodines[i])
                            pygame.display.update(lista_rectangulos_comodines[i])


                            pygame.display.flip()

                            break

    #dibujo preguntas y respuestas
    if bandera_respuesta: #si se acabo de responder, pauso brevemente antes de la siguiente pregunta
        pygame.time.delay(1000)
        indice_pregunta_actual += 1 # AVANZA AQUÍ LA PREGUNTA
        tiempo_inicio_partida = time.time() # Reinicia el tiempo para la próxima pregunta
        bandera_respuesta = False # Resetear la bandera después de la pausa y el avance
        respuesta_seleccionada_idx = -1 #resetear el indice de la respuesta seleccionada

        respuestas_eliminadas_bomba.clear()
        efecto_x2_activo = False
        doble_chance_activa = False
    

    mostrar_texto_simple(pantalla, f"Tiempo restante: {tiempo_restante}s", (10, 70), FUENTE_TEXTO_COMUN, COLOR_NEGRO)
    mostrar_texto_simple(pantalla,f"PUNTUACION: {datos_juego['puntuacion']}",(10,10),FUENTE_TEXTO_COMUN,COLOR_NEGRO)
    mostrar_texto_simple(pantalla,f"VIDAS: {datos_juego['vidas']}",(10,40),FUENTE_TEXTO_COMUN,COLOR_NEGRO)



    mostrar_texto(cuadro_pregunta["superficie"], f"{pregunta_actual['pregunta']}", (20, 20), FUENTE_PREGUNTA, COLOR_NEGRO, ancho_max=cuadro_pregunta["superficie"].get_width() - 40) #40 para un margen de 20px a cada lado

    mostrar_texto(cartas_respuestas[0]["superficie"], f"{pregunta_actual['respuesta_1']}", (20, 20), FUENTE_RESPUESTA, COLOR_NEGRO)
    mostrar_texto(cartas_respuestas[1]["superficie"], f"{pregunta_actual['respuesta_2']}", (20, 20), FUENTE_RESPUESTA, COLOR_NEGRO)
    mostrar_texto(cartas_respuestas[2]["superficie"], f"{pregunta_actual['respuesta_3']}", (20, 20), FUENTE_RESPUESTA, COLOR_NEGRO)


    pantalla.blit(cuadro_pregunta["superficie"],(80,200))
    cartas_respuestas[0]['rectangulo'] = pantalla.blit(cartas_respuestas[0]['superficie'],(23,583))
    cartas_respuestas[1]['rectangulo'] = pantalla.blit(cartas_respuestas[1]['superficie'],(23,686))
    cartas_respuestas[2]['rectangulo'] = pantalla.blit(cartas_respuestas[2]['superficie'],(23,790))

    #dibuja los comodines
    for i, boton_surf in enumerate(lista_comodines_superficies):
        # Primero, rellenar el fondo del botón
        color_fondo_comodin = COLOR_ROJO if i == 0 else (COLOR_VERDE if i == 1 else (COLOR_AZUL if i == 2 else COLOR_AMARILLO))
        # Si el comodín está usado, cambiar el color de fondo a uno más oscuro
        if (i == 0 and not comodines_disponibles_actual["bomba"]) or \
           (i == 1 and not comodines_disponibles_actual["x2"]) or \
           (i == 2 and not comodines_disponibles_actual["doble_chance"]) or \
           (i == 3 and not comodines_disponibles_actual["pasar"]):
            color_fondo_comodin = COLOR_GRIS_OSCURO # O un color más atenuado para "usado"
        
        
        boton_surf.fill(color_fondo_comodin) # Rellena la superficie del botón

        # Luego, dibujar el texto sobre la superficie del botón (no directamente en la pantalla)
        texto_comodin = ""
        if i == 0: texto_comodin = "BOMBA"
        elif i == 1: texto_comodin = "X2"
        elif i == 2: texto_comodin = "DOBLE CHANCE"
        elif i == 3: texto_comodin = "PASAR"

        mostrar_texto(boton_surf, texto_comodin, # Dibuja sobre el botón_surf, no la pantalla
                      (boton_surf.get_width() // 2, boton_surf.get_height() // 2), # Centrado
                      FUENTE_TEXTO_COMUN, COLOR_BLANCO, centrado=True) # Pasamos centrado=True
        
        # Finalmente, blitear el botón_surf (con su fondo y texto) a la pantalla
        pantalla.blit(boton_surf, lista_rectangulos_comodines[i])



    return retorno