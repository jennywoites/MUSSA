import os
from app import db
from app.models.carreras_models import Carrera, Creditos, Orientacion, Materia, TipoMateria, Correlativas

RUTA_PLANES_CSV = "../../../PlanesdeEstudio/CSV/"
RUTA_PLANES_INFO = "../../../PlanesdeEstudio/InfoCarrera/"

CARRERAS = {
    "09": ("Licenciatura en análisis de sistemas", "1986"),
    "10": ("Ingeniería en Informática", "1986")
}

TITULO = 0
PLAN = 1

DURACION = "DURACION"

ORIENTACIONES = "ORIENTACIONES"
NOMBRE = 0
CODIGO = 1

CREDITOS_TESIS = "CREDITOS_TESIS"
CREDITOS_TP_PROFESIONAL = "CREDITOS_TP_PROFESIONAL"
CREDITOS_OBLIGATORIAS = "CREDITOS_OBLIGATORIAS"
CREDITOS_ORIENTACION = "CREDITOS_ORIENTACION"
CREDITOS_ELECTIVAS_CON_TP = "CREDITOS_ELECTIVAS_CON_TP"
CREDITOS_ELECTIVAS_CON_TESIS = "CREDITOS_ELECTIVAS_CON_TESIS"
CREDITOS_ELECTIVAS_GENERAL = "CREDITOS_ELECTIVAS_GENERAL"
REQUIERE_SUFICIENCIA_IDIOMA = "REQUIERE_SUFICIENCIA_IDIOMA"


def create_carreras():
    # Create all tables
    db.create_all()

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
    vocales = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u"}

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
        codigo=codigo,
        nombre=titulo,
        plan=plan,
        duracion_estimada_en_cuatrimestres=datos[DURACION],
        requiere_prueba_suficiencia_de_idioma=datos[REQUIERE_SUFICIENCIA_IDIOMA]
    )

    db.session.add(carrera)

    guardar_cantidad_de_creditos(carrera, datos)
    guardar_orientaciones(carrera, datos)

    guardar_materias(carrera, codigo, titulo, plan)

    db.session.commit()


def guardar_orientaciones(carrera, datos):
    orientaciones = datos[ORIENTACIONES]

    for orientacion in orientaciones:
        carrera.orientaciones.append(Orientacion(
            descripcion=orientacion[NOMBRE],
            clave_reducida=orientacion[CODIGO]
        ))


def guardar_cantidad_de_creditos(carrera, datos):
    creditos = Creditos(
        creditos_obligatorias=datos[CREDITOS_OBLIGATORIAS],
        creditos_orientacion=datos[CREDITOS_ORIENTACION],
        creditos_electivas_general=datos[CREDITOS_ELECTIVAS_GENERAL],
        creditos_electivas_con_tp=datos[CREDITOS_ELECTIVAS_CON_TP],
        creditos_electivas_con_tesis=datos[CREDITOS_ELECTIVAS_CON_TESIS],
        creditos_tesis=datos[CREDITOS_TESIS],
        creditos_tp_profesional=datos[CREDITOS_TP_PROFESIONAL]
    )

    if not carrera.creditos:
        carrera.creditos = []

    carrera.creditos.append(creditos)


def cargar_datos_carrera(nombre_arch):
    dir = os.path.dirname(__file__)
    ruta = os.path.join(dir, RUTA_PLANES_INFO + nombre_arch)

    dic_datos = {}
    with open(ruta, 'r') as arch:
        for linea in arch:
            linea = linea.rstrip()

            etiqueta, datos = linea.split(";")
            etiqueta = etiqueta[1:len(etiqueta) - 1]
            datos = datos.split("-")
            datos = [] if len(datos) == 1 and datos[0] == "NULL" else datos

            if len(datos) == 1:  # Salvo las orientaciones, todas son unico valor numerico entero
                dato = datos[0]
                dato = dato[1:len(dato) - 1]
                dic_datos[etiqueta] = int(dato)
            else:
                orientaciones = []
                for dato in datos:
                    orientacion, cod_orientacion = dato.split(":")
                    orientaciones.append((orientacion, cod_orientacion))
                dic_datos[etiqueta] = orientaciones

    return dic_datos


def guardar_materias(carrera, codigo, titulo, plan):
    archivo_carrera = get_nombre_carrera_para_archivo(titulo, plan, "csv")
    materias = cargar_datos_materias(archivo_carrera, carrera)
    carrera.materias = materias


def cargar_datos_materias(nombre_arch, carrera):
    materias = []

    dir = os.path.dirname(__file__)
    ruta = os.path.join(dir, RUTA_PLANES_CSV + nombre_arch)

    dict_correlativas = {}
    with open(ruta, 'r') as arch:
        primera = True
        for linea in arch:

            if primera:
                primera = False
                continue

            materias.append(crear_materia(linea, dict_correlativas, carrera))

    guardar_correlativas(dict_correlativas, carrera)

    return materias


def crear_materia(linea, dict_correlativas, carrera):
    linea = linea.rstrip()

    codigo, nombre, creditos, tipo, cred_minimos, correlativas = linea.split(",")
    creditos = int(creditos)
    cred_minimos = int(cred_minimos)

    correlativas = correlativas.split("-")
    if not correlativas or correlativas[0] == '':
        correlativas = []

    tipo = find_or_create_tipo_materia(tipo)

    materia = Materia(
        codigo=codigo,
        nombre=nombre,
        objetivos="",
        tipo_materia_id=tipo.id,
        creditos_minimos_para_cursarla=cred_minimos,
        creditos=creditos,
        carrera_id=carrera.id
    )

    db.session.add(materia)

    dict_correlativas[codigo] = correlativas

    return materia


def find_or_create_tipo_materia(tipo_materia):
    tipo = TipoMateria.query.filter_by(descripcion=tipo_materia).first()

    if not tipo:
        tipo = TipoMateria(descripcion=tipo_materia)
        db.session.add(tipo)
        db.session.commit()

    return tipo


def find_or_create_correlativa(id_materia_actual, id_materia_correlativa):
    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'))
    materia_correlativa_id = db.Column(db.Integer, db.ForeignKey('materia.id'))

    query = Correlativas.query.filter_by(materia_id=id_materia_actual)
    query = query.filter_by(materia_correlativa_id=id_materia_correlativa)
    correlatividad = query.first()

    if not correlatividad:
        correlatividad = Correlativas(materia_id=id_materia_actual, materia_correlativa_id=id_materia_correlativa)
        db.session.add(correlatividad)


def guardar_correlativas(dic_correlativas, carrera):
    for cod in dic_correlativas:

        materia_actual = Materia.query.filter_by(codigo=cod).filter_by(carrera_id=carrera.id).first()

        for correlativa in dic_correlativas[cod]:
            materia_correlativa = Materia.query.filter(Materia.codigo == correlativa).first()

            if not materia_actual or not materia_correlativa:
                print(materia_actual)
                print(correlativa)
                print(materia_correlativa)
                input()

            find_or_create_correlativa(materia_actual.id, materia_correlativa.id)
