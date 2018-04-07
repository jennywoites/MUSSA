from app.models.carreras_models import Materia
from app.models.horarios_models import Horario
from app.models.palabras_clave_models import PalabraClave, TematicaMateria
from app.models.docentes_models import Docente
from app.models.respuestas_encuesta_models import *
from app.utils import DIAS, frange
from app.API_Rest.GeneradorPlanCarreras.my_utils import convertir_hora_desde_horario_float


def generar_estructura_respuesta_por_tipo(tipo_id):
    tipo_encuesta = TipoEncuesta.query.get(tipo_id).tipo

    acciones = {
        PUNTAJE_1_A_5: generar_respuesta_puntaje,
        TEXTO_LIBRE: generar_respuesta_texto_libre,
        SI_NO: generar_respuesta_si_no,
        HORARIO: generar_respuesta_horario,
        DOCENTE: generar_respuesta_docente,
        CORRELATIVA: generar_respuesta_correlativas,
        ESTRELLAS: generar_respuesta_estrellas,
        NUMERO: generar_respuesta_numero,
        TAG: generar_respuesta_tags,
        TEMATICA: generar_respuesta_tematicas,
    }

    return acciones[tipo_encuesta]()


def actualizar_respuesta_JSON(rta_encuesta, estructura_respuesta, tipo_id):
    tipo_encuesta = TipoEncuesta.query.get(tipo_id).tipo

    acciones = {
        PUNTAJE_1_A_5: actualizar_respuesta_puntaje,
        TEXTO_LIBRE: actualizar_respuesta_texto_libre,
        SI_NO: actualizar_respuesta_si_no,
        HORARIO: actualizar_respuesta_horario,
        DOCENTE: actualizar_respuesta_docente,
        CORRELATIVA: actualizar_respuesta_correlativas,
        ESTRELLAS: actualizar_respuesta_estrellas,
        NUMERO: actualizar_respuesta_numero,
        TAG: actualizar_respuesta_tags,
        TEMATICA: actualizar_respuesta_tematicas,
    }

    return acciones[tipo_encuesta](rta_encuesta, estructura_respuesta)


####################################################################################################
def generar_respuesta_puntaje():
    return {
        "suma_puntajes": 0,
        "total_encuestas": 0,
        "puntajes": {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0
        }
    }


def actualizar_respuesta_puntaje(rta_encuesta, estructura_respuesta):
    rta = RespuestaEncuestaPuntaje.query.filter_by(rta_encuesta_alumno_id=rta_encuesta.id).first()
    if not rta:
        return

    estructura_respuesta["suma_puntajes"] += rta.puntaje
    estructura_respuesta["total_encuestas"] += 1
    estructura_respuesta["puntajes"][rta.puntaje] += 1


####################################################################################################
def generar_respuesta_texto_libre():
    return {
        "textos": []
    }


def actualizar_respuesta_texto_libre(rta_encuesta, estructura_respuesta):
    rta = RespuestaEncuestaTexto.query.filter_by(rta_encuesta_alumno_id=rta_encuesta.id).first()
    if not rta or not rta.texto:
        return

    estructura_respuesta["textos"].append(rta.texto)


####################################################################################################
def generar_respuesta_si_no():
    return {
        "total_encuestas": 0,
        "SI": 0,
        "NO": 0,
    }


def actualizar_respuesta_si_no(rta_encuesta, estructura_respuesta):
    rta = RespuestaEncuestaSiNo.query.filter_by(rta_encuesta_alumno_id=rta_encuesta.id).first()
    if not rta:
        return

    estructura_respuesta["total_encuestas"] += 1

    if rta.respuesta:
        estructura_respuesta["SI"] += 1
    else:
        estructura_respuesta["NO"] += 1


####################################################################################################
MAX_FRANJA = 33
HORA_ORIGEN = 7


def generar_respuesta_horario():
    lista_horarios = {}
    for dia in DIAS:
        lista_horarios[dia] = ([0] * MAX_FRANJA)

    nombres_franjas_horarios = []
    for i in range(MAX_FRANJA):
        hora = convertir_hora_desde_horario_float(i * 0.5 + HORA_ORIGEN)
        nombres_franjas_horarios.append(hora)

    return {
        "horarios": lista_horarios,
        "nombres_franjas_horarios": nombres_franjas_horarios,
        "total_encuestas": 0
    }


def actualizar_respuesta_horario(rta_encuesta, estructura_respuesta):
    rtas = RespuestaEncuestaHorario.query.filter_by(rta_encuesta_alumno_id=rta_encuesta.id).all()
    if not rtas:
        return

    for rta in rtas:
        horario = Horario.query.get(rta.horario_id)
        for i in horario.get_franjas_utilizadas():
            estructura_respuesta["horarios"][horario.dia][i - 1] += 1
        estructura_respuesta["total_encuestas"] += 1


def ajustar_franjas_respuestas_horarios(estructura_respuesta):
    if not "horarios" in estructura_respuesta:
        return

    min_franja = MAX_FRANJA
    max_franja = 0
    for dia in estructura_respuesta["horarios"]:
        for i in range(len(estructura_respuesta["horarios"][dia])):
            esta_ocupada = estructura_respuesta["horarios"][dia][i]
            min_franja = min(min_franja, i) if esta_ocupada else min_franja
            max_franja = max(max_franja, i) if esta_ocupada else max_franja

    min_franja = min_franja if min_franja == 0 else min_franja - 1
    max_franja = max_franja if max_franja == MAX_FRANJA else max_franja + 1

    for dia in estructura_respuesta["horarios"]:
        estructura_respuesta["horarios"][dia] = estructura_respuesta["horarios"][dia][min_franja:max_franja + 1]

    estructura_respuesta["nombres_franjas_horarios"] = estructura_respuesta["nombres_franjas_horarios"][
                                                       min_franja:max_franja + 1]


####################################################################################################
def generar_respuesta_docente():
    return {"docentes": {}}


def actualizar_respuesta_docente(rta_encuesta, estructura_respuesta):
    rtas = RespuestaEncuestaDocente.query.filter_by(rta_encuesta_alumno_id=rta_encuesta.id).all()
    if not rtas:
        return

    for rta in rtas:
        if not rta.comentario:
            continue

        docente = Docente.query.get(rta.docente_id)
        no_dicta = "" if not docente.eliminado else " (No dicta más clases en este curso)"

        if not docente.id in estructura_respuesta["docentes"]:
            estructura_respuesta["docentes"][docente.id] = {
                "id_docente": docente.id,
                "apellido": docente.apellido,
                "nombre": docente.nombre,
                "nombre_completo": docente.obtener_nombre_completo() + no_dicta,
                "comentarios": []
            }

        estructura_respuesta["docentes"][docente.id]["comentarios"].append(rta.comentario)


####################################################################################################
def generar_respuesta_correlativas():
    return {
        "total_encuestas": 0,
        "materias_correlativas": {}
    }


def actualizar_respuesta_correlativas(rta_encuesta, estructura_respuesta):
    rtas = RespuestaEncuestaCorrelativa.query.filter_by(rta_encuesta_alumno_id=rta_encuesta.id).all()
    if not rtas:
        return

    for rta in rtas:
        materia = Materia.query.get(rta.materia_correlativa_id)

        if not materia.codigo in estructura_respuesta["materias_correlativas"]:
            estructura_respuesta["materias_correlativas"][materia.codigo] = {
                "codigo": materia.codigo,
                "nombre": materia.nombre,
                "total_encuestas": 0
            }

        estructura_respuesta["total_encuestas"] += 1
        estructura_respuesta["materias_correlativas"][materia.codigo]["total_encuestas"] += 1


####################################################################################################
def generar_respuesta_estrellas():
    return {
        "suma_estrellas": 0,
        "total_encuestas": 0,
        "estrellas": {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0
        }
    }


def actualizar_respuesta_estrellas(rta_encuesta, estructura_respuesta):
    rta = RespuestaEncuestaEstrellas.query.filter_by(rta_encuesta_alumno_id=rta_encuesta.id).first()
    if not rta:
        return

    estructura_respuesta["suma_estrellas"] += rta.estrellas
    estructura_respuesta["total_encuestas"] += 1
    estructura_respuesta["estrellas"][rta.estrellas] += 1


####################################################################################################
def generar_respuesta_numero():
    return {
        "suma_numeros": 0,
        "total_encuestas": 0,
        "numeros": {}
    }


def actualizar_respuesta_numero(rta_encuesta, estructura_respuesta):
    rta = RespuestaEncuestaNumero.query.filter_by(rta_encuesta_alumno_id=rta_encuesta.id).first()
    if not rta:
        return

    estructura_respuesta["suma_numeros"] += rta.numero
    estructura_respuesta["total_encuestas"] += 1

    cant_encuestas_con_numero_actual = estructura_respuesta["numeros"].get(rta.numero, 0)
    cant_encuestas_con_numero_actual += 1
    estructura_respuesta["numeros"][rta.numero] = cant_encuestas_con_numero_actual


####################################################################################################
def generar_respuesta_tags():
    return {
        "total_encuestas": 0,
        "palabras_clave": {}
    }


def actualizar_respuesta_tags(rta_encuesta, estructura_respuesta):
    rtas = RespuestaEncuestaTags.query.filter_by(rta_encuesta_alumno_id=rta_encuesta.id).all()
    if not rtas:
        return

    for rta in rtas:
        tag = PalabraClave.query.get(rta.palabra_clave_id)
        if not tag.id in estructura_respuesta["palabras_clave"]:
            estructura_respuesta["palabras_clave"][tag.id] = {
                "id_palabra_clave": tag.id,
                "palabra_clave": tag.palabra,
                "total_encuestas": 0
            }

        estructura_respuesta["total_encuestas"] += 1
        estructura_respuesta["palabras_clave"][tag.id]["total_encuestas"] += 1


####################################################################################################
def generar_respuesta_tematicas():
    return {
        "total_encuestas": 0,
        "tematicas": {}
    }


def actualizar_respuesta_tematicas(rta_encuesta, estructura_respuesta):
    rtas = RespuestaEncuestaTematica.query.filter_by(rta_encuesta_alumno_id=rta_encuesta.id).all()
    if not rtas:
        return

    for rta in rtas:
        tematica = TematicaMateria.query.get(rta.tematica_id)
        if not tematica.id in estructura_respuesta["tematicas"]:
            estructura_respuesta["tematicas"][tematica.id] = {
                "id_tematica": tematica.id,
                "tematica": tematica.tematica,
                "total_encuestas": 0
            }

        estructura_respuesta["total_encuestas"] += 1
        estructura_respuesta["tematicas"][tematica.id]["total_encuestas"] += 1
