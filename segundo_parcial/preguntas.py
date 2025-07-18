import csv
import os

lista_preguntas = [
    {"pregunta":"¿En qué ciudad nació Lionel Messi?", "respuesta_1":"Rosario","respuesta_2":"Buenos Aires","respuesta_3":"Córdoba","respuesta_correcta":1},
    {"pregunta": "¿Cuál es la capital de Argentina?", "respuesta_1": "Buenos Aires", "respuesta_2": "Córdoba", "respuesta_3": "Rosario", "respuesta_correcta": 1},
    {"pregunta": "¿En qué año ganó Argentina su primer mundial de fútbol?", "respuesta_1": "1978", "respuesta_2": "1986", "respuesta_3": "2002", "respuesta_correcta": 1},
    {"pregunta": "¿Quién es conocido como el 'Padre de la Patria' en Argentina?", "respuesta_1": "Juan Manuel de Rosas", "respuesta_2": "José de San Martín", "respuesta_3": "Manuel Belgrano", "respuesta_correcta": 2},
    {"pregunta": "¿Cuál es el pico más alto de Argentina?", "respuesta_1": "Cerro Aconcagua", "respuesta_2": "Cerro Tronador", "respuesta_3": "Cerro Fitz Roy", "respuesta_correcta": 1},
    {"pregunta": "¿Qué río separa a Argentina de Uruguay?", "respuesta_1": "Río Paraná", "respuesta_2": "Río Colorado", "respuesta_3": "Río de la Plata", "respuesta_correcta": 3},
    {"pregunta": "¿Quién compuso la canción 'Gracias a la Vida'?", "respuesta_1": "Mercedes Sosa", "respuesta_2": "Charly García", "respuesta_3": "Violeta Parra", "respuesta_correcta": 3},
    {"pregunta": "¿En qué año fue elegido presidente Néstor Kirchner?", "respuesta_1": "2000", "respuesta_2": "2003", "respuesta_3": "2007", "respuesta_correcta": 2},
    {"pregunta": "¿En qué provincia se encuentra la ciudad de Ushuaia?", "respuesta_1": "Santa Cruz", "respuesta_2": "Chubut", "respuesta_3": "Tierra del Fuego", "respuesta_correcta": 3},
    {"pregunta": "¿Qué moneda se utiliza en Argentina?", "respuesta_1": "Dólar", "respuesta_2": "Peso", "respuesta_3": "Real", "respuesta_correcta": 2},
    {"pregunta": "¿Qué famoso cantante argentino popularizó el tango?", "respuesta_1": "Astor Piazzolla", "respuesta_2": "Carlos Gardel", "respuesta_3": "Sandro", "respuesta_correcta": 2},
    {"pregunta": "¿Cuál es la danza tradicional de Argentina?", "respuesta_1": "Salsa", "respuesta_2": "Cumbia", "respuesta_3": "Tango", "respuesta_correcta": 3},
    {"pregunta": "¿Cuál es el nombre del famoso glaciar en la Patagonia?", "respuesta_1": "Perito Moreno", "respuesta_2": "Martial", "respuesta_3": "Upsala", "respuesta_correcta": 1},
    {"pregunta": "¿Quién es el autor de 'Martín Fierro'?", "respuesta_1": "Jorge Luis Borges", "respuesta_2": "José Hernández", "respuesta_3": "Julio Cortázar", "respuesta_correcta": 2},
    {"pregunta": "¿Cuál es la montaña más alta de América del Sur?", "respuesta_1": "Cerro Bonete", "respuesta_2": "Monte Pissis", "respuesta_3": "Aconcagua", "respuesta_correcta": 3},
    {"pregunta": "¿Qué bebida es famosa en Argentina?", "respuesta_1": "Tequila", "respuesta_2": "Mate", "respuesta_3": "Pisco", "respuesta_correcta": 2},
    {"pregunta": "¿Cuál es el nombre del teatro más famoso de Buenos Aires?", "respuesta_1": "Teatro Colón", "respuesta_2": "Teatro Gran Rex", "respuesta_3": "Teatro Nacional", "respuesta_correcta": 1},
    {"pregunta": "¿Cuál es la Avenida más ancha del mundo ubicada en Buenos Aires?", "respuesta_1": "Avenida de Mayo", "respuesta_2": "Avenida Corrientes", "respuesta_3": "Avenida 9 de Julio", "respuesta_correcta": 3},
    {"pregunta": "¿Qué prócer argentino creó la bandera?", "respuesta_1": "Domingo Sarmiento", "respuesta_2": "José de San Martín", "respuesta_3": "Manuel Belgrano", "respuesta_correcta": 3},
    {"pregunta": "¿Qué actriz argentina fue esposa de Juan Domingo Perón?", "respuesta_1": "Tita Merello", "respuesta_2": "Eva Perón", "respuesta_3": "Libertad Lamarque", "respuesta_correcta": 2},
    {"pregunta": "¿En qué año fue la Guerra de las Malvinas?", "respuesta_1": "1980", "respuesta_2": "1982", "respuesta_3": "1984", "respuesta_correcta": 2},
    {"pregunta": "¿Cuál es el nombre del equipo de fútbol conocido como 'La Academia'?", "respuesta_1": "Boca Juniors", "respuesta_2": "Racing Club", "respuesta_3": "River Plate", "respuesta_correcta": 2},
    {"pregunta": "¿En qué provincia se encuentra la ciudad de Mendoza?", "respuesta_1": "Santa Fe", "respuesta_2": "San Juan", "respuesta_3": "Mendoza", "respuesta_correcta": 3},
    {"pregunta": "¿Cuál es el ave nacional de Argentina?", "respuesta_1": "Cóndor", "respuesta_2": "Ñandú", "respuesta_3": "Hornero", "respuesta_correcta": 3},
    {"pregunta": "¿Qué escritora argentina ganó el Premio Cervantes en 2018?", "respuesta_1": "Silvina Ocampo", "respuesta_2": "María Elena Walsh", "respuesta_3": "María Teresa Andruetto", "respuesta_correcta": 3},
    {"pregunta": "¿Qué ciudad argentina es conocida por sus cataratas?", "respuesta_1": "Misiones", "respuesta_2": "Puerto Iguazú", "respuesta_3": "Cataratas de Córdoba", "respuesta_correcta": 2}
]

# Nombre del archivo CSV
nombre_archivo = "preguntas.csv"

def crear_archivo_preguntas_si_no_existe():
    nombre_archivo = "preguntas.csv"
    if not os.path.exists(nombre_archivo):
        with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as archivo_csv:
            escritor = csv.DictWriter(archivo_csv, fieldnames=["pregunta", "respuesta_1", "respuesta_2", "respuesta_3", "respuesta_correcta"])
            escritor.writeheader()
            escritor.writerows(lista_preguntas)
        print(f"Archivo '{nombre_archivo}' creado con éxito.")
