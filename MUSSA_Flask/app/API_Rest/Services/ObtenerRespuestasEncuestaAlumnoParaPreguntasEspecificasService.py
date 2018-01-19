from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request
from flask_user import current_user, login_required

from app.models.respuestas_encuesta_models import *
from app.models.alumno_models import Alumno
from app.models.docentes_models import Docente
from app.models.carreras_models import Materia
from app.models.horarios_models import Horario
from app.models.palabras_clave_models import PalabraClave, TematicaMateria
from app.DAO.EncuestasDAO import *

import logging


class ObtenerRespuestasEncuestaAlumnoParaPreguntasEspecificas(Resource):
    @login_required
    def get(self):
        args = request.args
        logging.info('Se invoco al servicio Obtener Respuestas Encuesta Alumno'
                     'para preguntas específicas con los siguientes parametros: {}'.format(args))

        alumno = Alumno.query.filter_by(user_id=current_user.id).first()

        id_encuesta = args["id_encuesta"] if "id_encuesta" in args else None

        if not id_encuesta or not self.id_encuesta_es_valido(id_encuesta, alumno):
            logging.error('El servicio Obtener Respuestas Encuesta Alumno'
                          'para preguntas específicas recibió un id de encuesta invalido')
            return {'Error': 'Este servicio recibió un id de encuesta invalido o no perteneciente'
                             'al alumno'}, CLIENT_ERROR_BAD_REQUEST

        if not self.ids_preguntas_son_validas(args):
            logging.error('El servicio Obtener Respuestas Encuesta Alumno'
                          'para preguntas específicas recibió uno o más ids de preguntas inválidos')
            return {'Error': 'Este servicio recibió uno o más ids de preguntas inválidos'}, CLIENT_ERROR_BAD_REQUEST

        query = RespuestaEncuestaAlumno.query.filter_by(encuesta_alumno_id=id_encuesta)

        ids_preguntas = args["ids_preguntas"].split(";") if "ids_preguntas" in args and args["ids_preguntas"] else None
        if ids_preguntas:
            query = query.filter(RespuestaEncuestaAlumno.pregunta_encuesta_id.in_(ids_preguntas))

        query = query.order_by(RespuestaEncuestaAlumno.pregunta_encuesta_id.asc())
        respuestas_encuesta = query.order_by(RespuestaEncuestaAlumno.id.asc()).all()

        preguntas_result = {}
        for respuesta_encuesta in respuestas_encuesta:
            datos = self.generar_respuesta_pregunta(respuesta_encuesta)
            if datos:
                preguntas_result[respuesta_encuesta.pregunta_encuesta_id] = datos

        result = ({'respuestas_encuestas': preguntas_result}, SUCCESS_OK)
        logging.info('Obtener Respuestas Encuesta Alumno para preguntas específicas: {}'.format(result))

        return result

    def ids_preguntas_son_validas(self, args):
        if not "ids_preguntas" in args or not args["ids_preguntas"]:
            return True

        ids_preguntas = args["ids_preguntas"].split(";")
        for id_pregunta in ids_preguntas:
            if not id_pregunta.isdigit() or not PreguntaEncuesta.query.get(id_pregunta):
                return False
        return True

    def id_encuesta_es_valido(self, id_encuesta, alumno):
        if not id_encuesta.isdigit():
            return False
        return EncuestaAlumno.query.filter_by(id=id_encuesta).filter_by(alumno_id=alumno.id).first()

    def generar_respuesta_pregunta(self, respuesta_encuesta):
        tipo_encuesta = TipoEncuesta.query.get(respuesta_encuesta.tipo_id).tipo

        acciones = {
            PUNTAJE_1_A_5: self.generar_respuesta_puntaje,
            TEXTO_LIBRE: self.generar_respuesta_texto_libre,
            SI_NO: self.generar_respuesta_si_no,
            HORARIO: self.generar_respuesta_horario,
            DOCENTE: self.generar_respuesta_docente,
            CORRELATIVA: self.generar_respuesta_correlativas,
            ESTRELLAS: self.generar_respuesta_estrellas,
            NUMERO: self.generar_respuesta_numero,
            TAG: self.generar_respuesta_tags,
            TEMATICA: self.generar_respuesta_tematicas,
        }

        return acciones[tipo_encuesta](respuesta_encuesta)

    def generar_respuesta_puntaje(self, respuesta_encuesta):
        rta = RespuestaEncuestaPuntaje.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).first()
        return {"puntaje": rta.puntaje} if rta else None

    def generar_respuesta_texto_libre(self, respuesta_encuesta):
        rta = RespuestaEncuestaTexto.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).first()
        return {"texto": rta.texto} if rta else None

    def generar_respuesta_si_no(self, respuesta_encuesta):
        rta = RespuestaEncuestaSiNo.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).first()
        return {"respuesta": rta.respuesta} if rta else None

    def generar_respuesta_horario(self, respuesta_encuesta):
        rtas = RespuestaEncuestaHorario.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).all()
        horarios = []
        for rta in rtas:
            horario = Horario.query.get(rta.horario_id)
            horarios.append({
                "dia": horario.dia,
                "hora_desde": horario.hora_desde,
                "hora_hasta": horario.hora_hasta
            })

        return {"horarios": horarios} if rtas else None

    def generar_respuesta_docente(self, respuesta_encuesta):
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

    def generar_respuesta_correlativas(self, respuesta_encuesta):
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

    def generar_respuesta_estrellas(self, respuesta_encuesta):
        rta = RespuestaEncuestaEstrellas.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).first()
        return {"estrellas": rta.estrellas} if rta else None

    def generar_respuesta_numero(self, respuesta_encuesta):
        rta = RespuestaEncuestaNumero.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).first()
        return {"numero": rta.numero} if rta else None

    def generar_respuesta_tags(self, respuesta_encuesta):
        rtas = RespuestaEncuestaTags.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).all()
        palabras_clave = []
        for rta in rtas:
            tag = PalabraClave.query.get(rta.palabra_clave_id)
            palabras_clave.append({
                "id_palabra_clave": tag.id,
                "palabra_clave": tag.palabra
            })

        return {"palabras_clave": palabras_clave} if rtas else None

    def generar_respuesta_tematicas(self, respuesta_encuesta):
        rtas = RespuestaEncuestaTematica.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).all()
        tematicas = []
        for rta in rtas:
            tematica = TematicaMateria.query.get(rta.tematica_id)
            tematicas.append({
                "id_tematica": tematica.id,
                "tematica": tematica.tematica
            })

        return {"tematicas": tematicas} if rtas else None
