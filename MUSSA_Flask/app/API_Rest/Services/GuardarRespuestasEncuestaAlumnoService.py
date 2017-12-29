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


class GuardarRespuestasEncuestaAlumno(Resource):
    @login_required
    def get(self):
        args = request.args
        logging.info('Se invoco al servicio Guardar Respuestas Encuesta Alumno con los siguientes '
                     'parametros: {}'.format(args))

        alumno = Alumno.query.filter_by(user_id=current_user.id).first()

        id_encuesta = args["id_encuesta"] if "id_encuesta" in args else None

        if not id_encuesta or not self.id_encuesta_es_valido(id_encuesta, alumno):
            logging.error('El servicio Guardar Respuestas Encuesta Alumno recibió un id de encuesta '
                          'inválido, no perteneciente al alumno o de una encuesta ya finalizada')
            return {'Error': 'Este servicio recibió un id de inválido, no perteneciente al alumno o de'
                             'una encuesta ya finalizada'}, CLIENT_ERROR_BAD_REQUEST

        if not self.categoria_es_valida(args):
            logging.error('El servicio Guardar Respuestas Encuesta Alumno recibió una categoría inválida')
            return {'Error': 'Este servicio  recibió una categoría inválida'}, CLIENT_ERROR_BAD_REQUEST

        categoria = self.obtener_categoria(args)
        preguntas_categoria_actual = self.obtener_preguntas_encuestas(categoria)

        respuestas = self.convertir_respuestas(args)

        for respuesta in respuestas:
            es_valida, msj = self.respuesta_es_valida(respuesta, preguntas_categoria_actual)
            if not es_valida:
                return {'Error': msj}, CLIENT_ERROR_BAD_REQUEST

        self.guardar_respuestas(respuestas)

        self.actualizar_estado_paso_actual(id_encuesta, preguntas_categoria_actual, categoria)

        result = ({'OK': 'Las respuestas fueron guardadas correctamente'}, SUCCESS_OK)
        logging.info('Guardar Respuestas Encuesta Alumno devuelve como resultado: {}'.format(result))
        return result

    def actualizar_estado_paso_actual(self, id_encuesta, preguntas_categoria_actual, categoria):
        estados_pasos = EstadoPasosEncuestaAlumno.query.filter_by(encuesta_alumno_id=id_encuesta).first()
        numero_paso = GrupoEncuesta.query.filter_by(id=categoria).first().numero_grupo

        finalizado = len(preguntas_categoria_actual) == 0
        estados_pasos.actualizar_estado_paso(numero_paso, finalizado)

    def obtener_preguntas_encuestas(self, categoria):
        encuestas = EncuestaGenerada.query.filter_by(grupo_id=categoria).all()

        preguntas_categoria_actual = {}
        for encuesta in encuestas:
            pregunta = PreguntaEncuesta.query.filter_by(id=encuesta.encuesta_id).first()
            preguntas_categoria_actual[pregunta.id] = pregunta

        return preguntas_categoria_actual

    def convertir_respuestas(self, args):
        # TODO
        print(args)
        pass
        # convertir el diccionario correspondiente

    def respuesta_es_valida(self, respuesta, preguntas_categoria_actual):
        idPregunta = respuesta["idPregunta"]

        if not idPregunta in preguntas_categoria_actual:
            logging.error('El servicio Guardar Respuestas Encuesta Alumno recibió un id de pregunta inválido')
            return False, 'Este servicio recibió un id de pregunta inválido'

        pregunta = preguntas_categoria_actual.pop(idPregunta)
        tipo_encuesta = TipoEncuesta.query.filter_by(id=pregunta.tipo_id).first().tipo

        if not self.validar_respuesta(preguntas_categoria_actual, pregunta, tipo_encuesta, respuesta):
            logging.error('El servicio Guardar Respuestas Encuesta Alumno recibió una '
                          'respuesta de encuesta inválida')
            return False, 'Este servicio recibió un respuesta de encuesta inválida'

        return True

    def validar_respuesta(self, preguntas_categoria_actual, pregunta, tipo_encuesta, respuesta):
        acciones = {
            PUNTAJE_1_A_5: self.validar_respuesta_puntaje,
            TEXTO_LIBRE: self.validar_respuesta_texto_libre,
            SI_NO: self.validar_respuesta_si_no,
            HORARIO: self.validar_respuesta_horario,
            DOCENTE: self.validar_respuesta_docente,
            CORRELATIVA: self.validar_respuesta_correlativas,
            ESTRELLAS: self.validar_respuesta_estrellas,
            NUMERO: self.validar_respuesta_numero,
            TAG: self.validar_respuesta_tags,
            TEMATICA: self.validar_respuesta_tematicas,
        }

        try:
            acciones[tipo_encuesta](preguntas_categoria_actual, pregunta, respuesta)
        except:
            return False

        return True

    MIN_PUNTAJE = 1
    MAX_PUNTAJE = 5

    def validar_respuesta_puntaje(self, preguntas_categoria_actual, pregunta, respuesta):
        puntaje = int(respuesta["puntaje"])
        if puntaje < self.MIN_PUNTAJE or puntaje > self.MAX_PUNTAJE:
            raise ValueError("El puntaje no esta entre los valores {} - {}".format(self.MIN_PUNTAJE, self.MAX_PUNTAJE))

    MAX_CARACTERES_TEXTO = 250

    def validar_respuesta_texto_libre(self, preguntas_categoria_actual, pregunta, respuesta):
        texto = respuesta["texto"]
        self.validar_contenido_y_longitud_texto(1, self.MAX_CARACTERES_TEXTO, texto)

    def validar_respuesta_si_no(self, preguntas_categoria_actual, pregunta, respuesta):
        respuesta = respuesta["respuesta"]

        for pregunta_si_no in PreguntaEncuestaSiNo.query.filter_by(encuesta_id=pregunta.id).all():
            id_nueva_pregunta = None
            if respuesta and pregunta_si_no.rta_si:
                id_nueva_pregunta = pregunta_si_no.rta_si
            elif not respuesta and pregunta_si_no.rta_no:
                id_nueva_pregunta = pregunta_si_no.rta_no

            if id_nueva_pregunta:
                nueva_pregunta = PreguntaEncuesta.query.filter_by(id=id_nueva_pregunta).first()
                preguntas_categoria_actual[id_nueva_pregunta] = nueva_pregunta

    def validar_respuesta_horario(self, preguntas_categoria_actual, pregunta, respuesta):
        horarios = respuesta["horarios"]
        for horario in horarios:
            dia = horario["dia"]
            hora_desde = horario["hora_desde"]
            hora_hasta = horario["hora_hasta"]
            # TODO
            raise NotImplementedError("Ver como validar el horario")

    def validar_respuesta_docente(self, preguntas_categoria_actual, pregunta, respuesta):
        docentes = respuesta["docentes"]
        for docente in docentes:
            idDocente = docente["id_docente"]

            if not Docente.query.filter_by(id=idDocente).first():
                raise ValueError("El id de docente {} es invalido".format(idDocente))

            comentario = docente["comentario"]
            self.validar_contenido_y_longitud_texto(1, self.MAX_CARACTERES_TEXTO, comentario)

    def validar_respuesta_correlativas(self, preguntas_categoria_actual, pregunta, respuesta):
        correlativas = respuesta["correlativas"]
        for id_materia_correlativa in correlativas:
            assert (id_materia_correlativa.isdigit())
            if not Materia.query.filter_by(id=id_materia_correlativa).first():
                raise ValueError("La materia con id {} que se desea indicar como "
                                 "correlativa no existe".format(id_materia_correlativa))

    MIN_ESTRELLAS = 1
    MAX_ESTRELLAS = 5

    def validar_respuesta_estrellas(self, preguntas_categoria_actual, pregunta, respuesta):
        estrellas = int(respuesta["estrellas"])
        if estrellas < self.MIN_ESTRELLAS or estrellas > self.MAX_ESTRELLAS:
            raise ValueError("La cantidad de estrellas no está entre "
                             "los valores {} - {}".format(self.MIN_ESTRELLAS, self.MAX_ESTRELLAS))

    def validar_respuesta_numero(self, preguntas_categoria_actual, pregunta, respuesta):
        numero = int(respuesta["numero"])

    MAX_CARACTERES_PALABRA_CLAVE_TAG = 30
    MAX_CANTIDAD_PALABRAS_CLAVE = 3

    def validar_respuesta_tags(self, preguntas_categoria_actual, pregunta, respuesta):
        palabras_clave = respuesta["palabras_clave"]
        assert (0 < len(palabras_clave) <= self.MAX_CANTIDAD_PALABRAS_CLAVE)
        for palabra in palabras_clave:
            self.validar_contenido_y_longitud_texto(1, self.MAX_CARACTERES_PALABRA_CLAVE_TAG, palabra)

    MAX_CARACTERES_TEMATICA = 40
    MAX_CANTIDAD_TEMATICAS = 10

    def validar_respuesta_tematicas(self, preguntas_categoria_actual, pregunta, respuesta):
        tematicas = respuesta["tematicas"]
        assert (0 < len(tematicas) <= self.MAX_CANTIDAD_TEMATICAS)
        for tematica in tematicas:
            self.validar_contenido_y_longitud_texto(1, self.MAX_CARACTERES_TEMATICA, tematica)

    def validar_contenido_y_longitud_texto(self, len_min, len_max, texto):
        for simbolo in "¡!,.-¿?*/+-'[]{}() ":
            texto = texto.replace(simbolo, '')
        if len(texto) < len_min or len(texto) > len_max:
            raise ValueError("El texto debe tener al menos {} caracteres, y tener una logitud menor"
                             "a {} caracteres".format(len_min, len_max))

    def id_encuesta_es_valido(self, id_encuesta, alumno):
        if not id_encuesta.isdigit():
            return False

        query = EncuestaAlumno.query.filter_by(id=id_encuesta).filter_by(alumno_id=alumno.id)
        query = query.filter_by(finalizada=False)
        return query.first()

    def obtener_categoria(self, args):
        categoria = args["categoria"] if "categoria" in args else None
        assert (categoria.isdigit())

        grupo = GrupoEncuesta.query.filter_by(numero_grupo=categoria).first()
        assert (grupo is not None)

        return grupo.id

    def categoria_es_valida(self, args):
        try:
            self.obtener_categoria(args)
        except:
            return False
        return True

    def guardar_respuestas(self, respuestas):
        raise NotImplementedError("Implementar guardar respuestas")
