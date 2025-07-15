#generar contraseñas en python

import random
import string

def generar_contraseña(longitud=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation #(string.ascii_letters)incluye letras mayusculas y minusculas, (string.digits)incluye numero del 0-9
                                                                           #(string.punctuation)incluye simbolos (!@#$%^&*, etc.)

    contraseña = ''.join(random.choice(caracteres) for _ in range(longitud))#random.choice me elige un caracter aleatorio
                                                                            #''.join(...) une todos los caracteres en una cadena   

    print("contraseña generada:", generar_contraseña(12))#se genera e imprime una contraseña de 12 caracteres
                                                                                                                                               