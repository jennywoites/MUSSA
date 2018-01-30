from app.models.generadorJSON.carreras_generadorJSON import generarJSON_carrera, generarJSON_materia
from app.models.generadorJSON.horarios_generadorJSON import generarJSON_curso, generarJSON_horario
from app.models.carreras_models import Carrera, Materia
from app.models.alumno_models import MateriasAlumno
from app.models.horarios_models import Curso, Horario
from app.models.palabras_clave_models import PalabraClave, TematicaMateria
from app.models.docentes_models import Docente
from app.models.respuestas_encuesta_models import *


def generarJSON_encuesta_alumno(encuesta_alumno):
    materiaAlumno = MateriasAlumno.query.get(encuesta_alumno.materia_alumno_id)
    carrera = Carrera.query.get(materiaAlumno.carrera_id)
    curso = Curso.query.get(materiaAlumno.curso_id)
    materia = Materia.query.get(materiaAlumno.materia_id)

    fecha_aprobacion = '-' if (not encuesta_alumno.cuatrimestre_aprobacion_cursada or
                              not encuesta_alumno.anio_aprobacion_cursada) else\
        "{}C / {}".format(encuesta_alumno.cuatrimestre_aprobacion_cursada, encuesta_alumno.anio_aprobacion_cursada)

    return {
        "id_encuesta_alumno": encuesta_alumno.id,
        "alumno_id": encuesta_alumno.alumno_id,
        "materia_alumno_id": encuesta_alumno.materia_alumno_id,
        "carrera": generarJSON_carrera(carrera),
        "materia": generarJSON_materia(materia),
        "curso": generarJSON_curso(curso),
        "cuatrimestre_aprobacion_cursada": encuesta_alumno.cuatrimestre_aprobacion_cursada,
        "anio_aprobacion_cursada": encuesta_alumno.anio_aprobacion_cursada,
        "fecha_aprobacion": fecha_aprobacion,
        "finalizada": encuesta_alumno.finalizada
    }


def generarJSON_respuesta_pregunta(respuesta_encuesta):
    tipo_encuesta = TipoEncuesta.query.get(respuesta_encuesta.tipo_id).tipo

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

    return acciones[tipo_encuesta](respuesta_encuesta)


def generar_respuesta_puntaje(respuesta_encuesta):
    rta = RespuestaEncuestaPuntaje.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).first()
    return {"puntaje": rta.puntaje} if rta else None


def generar_respuesta_texto_libre(respuesta_encuesta):
    rta = RespuestaEncuestaTexto.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).first()
    return {"texto": rta.texto} if rta else None


def generar_respuesta_si_no(respuesta_encuesta):
    rta = RespuestaEncuestaSiNo.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).first()
    return {"respuesta": rta.respuesta} if rta else None


def generar_respuesta_horario(respuesta_encuesta):
    rtas = RespuestaEncuestaHorario.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).all()
    horarios = []
    for rta in rtas:
        horarios.append(generarJSON_horario(Horario.query.get(rta.horario_id)))

    return {"horarios": horarios} if rtas else None


def generar_respuesta_docente(respuesta_encuesta):
    rtas = RespuestaEncuestaDocente.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).all()
    comentarios_docentes = []
    for rta in rtas:
        docente = Docente.query.get(rta.docente_id)
        comentarios_docentes.append({
            "id_docente": docente.id,
            "apellido": docente.apellido,
            "nombre": docente.nombre,
            "nombre_completo": docente.obtener_nombre_completo(),
            "comentario": rta.comentario
        })

    return {"comentarios_docentes": comentarios_docentes} if rtas else None


def generar_respuesta_correlativas(respuesta_encuesta):
    rtas = RespuestaEncuestaCorrelativa.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).all()
    materias_correlativas = []
    for rta in rtas:
        materia = Materia.query.get(rta.materia_correlativa_id)
        materias_correlativas.append({
            "id_materia": materia.id,
            "codigo": materia.codigo,
            "nombre": materia.nombre
        })

    return {"materias_correlativas": materias_correlativas} if rtas else None


def generar_respuesta_estrellas(respuesta_encuesta):
    rta = RespuestaEncuestaEstrellas.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).first()
    return {"estrellas": rta.estrellas} if rta else None


def generar_respuesta_numero(respuesta_encuesta):
    rta = RespuestaEncuestaNumero.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).first()
    return {"numero": rta.numero} if rta else None


def generar_respuesta_tags(respuesta_encuesta):
    rtas = RespuestaEncuestaTags.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).all()
    palabras_clave = []
    for rta in rtas:
        tag = PalabraClave.query.get(rta.palabra_clave_id)
        palabras_clave.append({
            "id_palabra_clave": tag.id,
            "palabra_clave": tag.palabra
        })

    return {"palabras_clave": palabras_clave} if rtas else None


def generar_respuesta_tematicas(respuesta_encuesta):
    rtas = RespuestaEncuestaTematica.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).all()
    tematicas = []
    for rta in rtas:
        tematica = TematicaMateria.query.get(rta.tematica_id)
        tematicas.append({
            "id_tematica": tematica.id,
            "tematica": tematica.tematica
        })

    return {"tematicas": tematicas} if rtas else None
