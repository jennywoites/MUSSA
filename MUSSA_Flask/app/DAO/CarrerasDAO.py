import datetime
import os

from flask import current_app

from app import db
from app.models.user_models import User, Role
from app.models.carreras_models import Carrera, Creditos, Orientacion, Materia

RUTA_PLANES_CSV = "../../../PlanesdeEstudio/CSV/"
RUTA_PLANES_INFO = "../../../PlanesdeEstudio/InfoCarrera/"

CARRERAS = {
    "9": ("Licenciatura en análisis de sistemas", "1986"),
    "10": ("Ingeniería en Informática", "1986")
}

TITULO = 0
PLAN = 1

DURACION = "DURACION"

ORIENTACIONES = "ORIENTACIONES"
NOMBRE = 0
CODIGO = 1

CREDITOS_TESIS= "CREDITOS_TESIS"
CREDITOS_TP_PROFESIONAL = "CREDITOS_TP_PROFESIONAL"
CREDITOS_OBLIGATORIAS = "CREDITOS_OBLIGATORIAS"
CREDITOS_ORIENTACION = "CREDITOS_ORIENTACION"
CREDITOS_ELECTIVAS_CON_TP = "CREDITOS_ELECTIVAS_CON_TP"
CREDITOS_ELECTIVAS_CON_TESIS = "CREDITOS_ELECTIVAS_CON_TESIS"
CREDITOS_ELECTIVAS_GENERAL = "CREDITOS_ELECTIVAS_GENERAL"
REQUIERE_SUFICIENCIA_IDIOMA = "REQUIERE_SUFICIENCIA_IDIOMA"

def create_carreras():
    # Create all tables
    db.create_all() #es necesario???

    for codigo in CARRERAS:
        carrera = CARRERAS[codigo]
        find_o_create_carrera(codigo, carrera[TITULO], carrera[PLAN])

    db.session.commit()


def find_o_create_carrera(codigo, titulo, plan):
    carrera = Carrera.query.filter(Carrera.codigo == codigo).first()

    if not carrera:
        carrera = crear_carrera(codigo, titulo, plan)
    return carrera


def get_nombre_carrera_para_archivo(titulo, plan, extension):
    vocales = {"á": "a", "é":"e", "í":"i", "ó":"o", "ú":"u"}

    titulo = titulo.lower()
    for vocal in vocales:
        while vocal in titulo:
            titulo = titulo.replace(vocal, vocales[vocal])

    palabras = titulo.split()
    palabras.append(plan)
    ruta = "_".join(palabras)

    ruta += "." + extension
    return ruta


def crear_carrera(codigo, titulo, plan):
    archivo_carrera = get_nombre_carrera_para_archivo(titulo, plan, "txt")
    datos = cargar_datos_carrera(archivo_carrera)

    carrera = Carrera(
        codigo = codigo,
        duracion_estimada_en_cuatrimestres = datos[DURACION],
        requiere_prueba_suficiencia_de_idioma = datos[REQUIERE_SUFICIENCIA_IDIOMA]
        )
   
    guardar_cantidad_de_creditos(carrera, datos)
    guardar_orientaciones(carrera, datos)

    #TODO
    #Cargar las materias para la carrera

    #TODO:
    #Cargar horarios iniciales guardados en el historial

    db.session.add(carrera)


def guardar_orientaciones(carrera, datos):
    orientaciones = datos[ORIENTACIONES]

    for orientacion in orientaciones:
        carrera.orientaciones.append(Orientacion(
            descripcion = orientacion[NOMBRE],
            clave_reducida = orientacion[CODIGO]
        ))


def guardar_cantidad_de_creditos(carrera, datos):
    creditos = Creditos(
        creditos_obligatorias = datos[CREDITOS_OBLIGATORIAS],
        creditos_orientacion = datos[CREDITOS_ORIENTACION],
        creditos_electivas_general = datos[CREDITOS_ELECTIVAS_GENERAL],
        creditos_electivas_con_tp = datos[CREDITOS_ELECTIVAS_CON_TP],
        creditos_electivas_con_tesis = datos[CREDITOS_ELECTIVAS_CON_TESIS],
        creditos_tesis = datos[CREDITOS_TESIS],
        creditos_tp_profesional = datos[CREDITOS_TP_PROFESIONAL]
        )

    carrera.creditos = creditos


def cargar_datos_carrera(nombre_arch):
    dir = os.path.dirname(__file__)
    ruta = os.path.join(dir, RUTA_PLANES_INFO + nombre_arch)

    dic_datos = {}
    with open(ruta, 'r') as arch:
        for linea in arch:
            linea = linea.rstrip()

            etiqueta, datos = linea.split(";")
            etiqueta = etiqueta[1:len(etiqueta)-1]
            datos = datos.split("-")
            datos = [] if len(datos)==1 and datos[0] == "NULL" else datos

            if len(datos) == 1: #Salvo las orientaciones, todas son unico valor numerico entero
                dato = datos[0]
                dato = dato[1:len(dato)-1]
                dic_datos[etiqueta] = int(dato)
            else:
                orientaciones = []
                for dato in datos:
                    dato = dato[1:len(dato)-1]
                    orientacion, cod_orientacion = dato.split(":")
                    orientaciones.append((orientacion, cod_orientacion))
                dic_datos[etiqueta] = orientaciones

    return dic_datos