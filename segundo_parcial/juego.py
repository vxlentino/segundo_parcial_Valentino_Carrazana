import pygame
import time
from variables import *
from funciones import *
# from funciones import mostrar_texto_pantalla

pygame.init()
pygame.mixer.init()

# pygame.mixer.music.load("d:\GOOGLE\Undertale - Megalovania _ HQ [kBoFfB9fQZQ].mp3")  # Ruta del archivo
# pygame.mixer.music.set_volume(0.5)  # Ajusta el volumen (0.0 a 1.0)
# pygame.mixer.music.play(-1)  # -1 para reproducir en bucle infinito

pantalla = pygame.display.set_mode(VENTANA)

imagen = pygame.image.load("d:\GOOGLE\preguntados.jpg")
imagen_preguntados = pygame.transform.scale(imagen, (ANCHO, ALTO))
preguntados_rectangulo = imagen_preguntados.get_rect()
preguntados_rectangulo.topleft = (0, 0)

#fuentes
fuente_pregunta = pygame.font.SysFont("Arial Narrow",30)
fuente_respuesta = pygame.font.SysFont("Arial Narrow",23)
fuente_texto = pygame.font.SysFont("Arial Narrow",25)

#cargo las preguntas del archivo
lista_preguntas = cargar_preguntas("preguntas.csv")
mezclar_lista(lista_preguntas)

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


comodines_disponibles = {
    "bomba": True,
    "x2": True,
    "doble_chance": True,
    "pasar": True
    }

#botones 
boton_bomba = pygame.Surface((150, 50))
boton_x2 = pygame.Surface((150, 50))
boton_doble_chance = pygame.Surface((150, 50))
boton_pasar = pygame.Surface((150, 50))

# Asignar colores o imágenes
boton_bomba.fill(COLOR_ROJO)
boton_x2.fill(COLOR_VERDE)
boton_doble_chance.fill(COLOR_AZUL)
boton_pasar.fill(COLOR_AMARILLO)

# Definir rectángulos
rect_bomba = boton_bomba.get_rect(topleft=(600, 300))
rect_x2 = boton_x2.get_rect(topleft=(600, 350))
rect_doble_chance = boton_doble_chance.get_rect(topleft=(600, 400))
rect_pasar = boton_pasar.get_rect(topleft=(600, 450))

# Lista de botones
lista_comodines = [boton_bomba, boton_x2, boton_doble_chance, boton_pasar]
lista_rectangulos_comodines = [rect_bomba, rect_x2, rect_doble_chance, rect_pasar]


#variables globales
indice = 0 #INMUTABLE -> En la funcion las declaro como global
bandera_respuesta = False #INMUTABLE -> En la funcion las declaro como global
contador_correctas = 0 #contador de respuestas correctas


limite_tiempo_general = 300 #5 minutos
tiempo_inicio = time.time() #tiempo inicial del juego



def mostrar_juego(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict, comodines_usados, puntaje) -> str:
    global indice, bandera_respuesta, contador_correctas

    retorno = "juego"
    
    cuadro_pregunta["superficie"].fill(COLOR_PREGUNTADOS)

    for carta in cartas_respuestas:
        carta["superficie"].fill(COLOR_BLANCO)

    #dibuja comodines
    for i, rect_comodin in enumerate(lista_rectangulos_comodines):
        pygame.draw.rect(pantalla, COLOR_BLANCO, rect_comodin)
        mostrar_texto(pantalla, f"comodin{i}", rect_comodin.topleft, fuente_texto, COLOR_NEGRO)
        
    if bandera_respuesta:
        pygame.time.delay(500)
        bandera_respuesta = False
        
    pregunta_actual = lista_preguntas[indice]

    #gestiono el tiempo
    tiempo_agotado = manejar_tiempo_general(tiempo_inicio, limite_tiempo_general, datos_juego)

    if tiempo_agotado:
        retorno = "terminado"

    tiempo_restante = int(limite_tiempo_general - (time.time() - tiempo_inicio))

    if tiempo_restante < 0:
        tiempo_restante = 0 

    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(cartas_respuestas)):
                if cartas_respuestas[i]['rectangulo'].collidepoint(evento.pos):
                    # respuesta_seleccionada = i
                    respuesta_usuario = (i + 1)
                    
                    if int(respuesta_usuario) == int(pregunta_actual['respuesta_correcta']):
                        # actualizar_estadisticas(pregunta_actual, acierto = True)
                        cartas_respuestas[i]['superficie'].fill(COLOR_VERDE)
                        print("RESPUESTA CORRECTA")
                        datos_juego["puntuacion"] += 10
                        contador_correctas += 1

                        if contador_correctas == 5:
                            datos_juego["vidas"] += 1
                            contador_correctas = 0
                            print("GANASTE UNA VIDA!!!")

                    else:
                        # actualizar_estadisticas(pregunta_actual, acierto = False)
                        cartas_respuestas[i]['superficie'].fill(COLOR_ROJO)
                        print("RESPUESTA INCORRECTA")
                        datos_juego["vidas"] -= 1
                        if datos_juego["vidas"] <= 0:
                            retorno = "terminado"
                    
                    print(f"SE HIZO CLICK EN UNA RESPUESTA {respuesta_usuario}")
                    bandera_respuesta = True
                    
                    if indice == len(lista_preguntas) - 1:
                        indice = 0
                        mezclar_lista(lista_preguntas)
                    else:
                        indice += 1

            for i in range(len(lista_rectangulos_comodines)):
                if lista_rectangulos_comodines[i].collidepoint(evento.pos):
                    if i == 0 and comodines_disponibles["bomba"]:
                        comodines_disponibles["bomba"] = False
                        print("comodin bomba activado")
                    elif i == 1 and comodines_disponibles["x2"]:
                        comodines_disponibles["x2"] = False
                        print("comodin x2 activado")
                        datos_juego["puntuacion"] *= 2
                    elif i == 2 and comodines_disponibles["doble_chance"]:
                        comodines_disponibles["doble_chance"] = False
                        print("comodin doble_chance activado")
                    elif i == 3 and comodines_disponibles["pasar"]:
                        comodines_disponibles["pasar"] = False
                        print("comodin pasar activado")

                    #actualizo
                    pygame.display.flip()


    # Detener la música al salir
    pygame.mixer.music.stop()
    pygame.quit()


    mostrar_texto(cuadro_pregunta["superficie"], f"{pregunta_actual['pregunta']}", (20, 20), fuente_pregunta, COLOR_NEGRO)
    mostrar_texto(cartas_respuestas[0]["superficie"], f"{pregunta_actual['respuesta_1']}", (20, 20), fuente_respuesta, COLOR_NEGRO)
    mostrar_texto(cartas_respuestas[1]["superficie"], f"{pregunta_actual['respuesta_2']}", (20, 20), fuente_respuesta, COLOR_NEGRO)
    mostrar_texto(cartas_respuestas[2]["superficie"], f"{pregunta_actual['respuesta_3']}", (20, 20), fuente_respuesta, COLOR_NEGRO)



    pantalla.blit(imagen_preguntados, preguntados_rectangulo)
    pantalla.blit(cuadro_pregunta["superficie"],(80,200))
    
    mostrar_texto_simple(pantalla, f"tiempo restante: {tiempo_restante}s", (10, 70), fuente_texto, COLOR_NEGRO)

    cartas_respuestas[0]['rectangulo'] = pantalla.blit(cartas_respuestas[0]['superficie'],(23,583))
    cartas_respuestas[1]['rectangulo'] = pantalla.blit(cartas_respuestas[1]['superficie'],(23,686))
    cartas_respuestas[2]['rectangulo'] = pantalla.blit(cartas_respuestas[2]['superficie'],(23,790))

    for i, boton in enumerate(lista_comodines):
        pantalla.blit(boton, lista_rectangulos_comodines[i])

    mostrar_texto(pantalla, "bomba_usada", (rect_bomba.x + 5, rect_bomba.y + 5), fuente_texto, COLOR_BLANCO)
    mostrar_texto(pantalla, "x2_usada", (rect_x2.x + 5, rect_x2.y + 5), fuente_texto, COLOR_BLANCO)
    mostrar_texto(pantalla, "doble_chance_usada", (rect_doble_chance.x + 5 , rect_doble_chance.y + 5), fuente_texto, COLOR_BLANCO)
    mostrar_texto(pantalla, "pasar_usada", (rect_pasar.x + 5, rect_pasar.y + 5), fuente_texto, COLOR_BLANCO)

    mostrar_texto(pantalla,f"PUNTUACION: {datos_juego['puntuacion']}",(10,10),fuente_texto,COLOR_NEGRO)
    mostrar_texto(pantalla,f"VIDAS: {datos_juego['vidas']}",(10,40),fuente_texto,COLOR_NEGRO)

    pygame.display.flip()

    return retorno