from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request
from flask_user import current_user, login_required
from app import db
from app.models.respuestas_encuesta_models import *
from app.models.alumno_models import Alumno
from app.models.docentes_models import Docente
from app.models.carreras_models import Materia
from app.models.horarios_models import Horario
from app.models.palabras_clave_models import PalabraClave, TematicaMateria
from app.utils import DIAS, convertir_horario
from app.DAO.EncuestasDAO import *
import logging
import json


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

        try:
            respuestas = json.loads(args["respuestas"])
        except:
            logging.error('El servicio Guardar Respuestas Encuesta Alumno recibió respuestas '
                          'inválidas o éstas no han sido enviadas')
            return {'Error': 'Este servicio recibió respuestas inválidas'
                             ' o éstas no han sido enviadas'}, CLIENT_ERROR_BAD_REQUEST

        son_validas, msj = self.validar_respuestas_recibidas(respuestas, categoria)
        if not son_validas:
            return {'Error': msj}, CLIENT_ERROR_BAD_REQUEST

        self.eliminar_todas_las_respuestas_del_paso_actual(self.obtener_preguntas_encuestas(categoria, True))

        preguntas_categoria_actual = self.obtener_preguntas_encuestas(categoria)
        self.guardar_respuestas(respuestas, id_encuesta, preguntas_categoria_actual)

        self.actualizar_estado_paso_actual(id_encuesta, preguntas_categoria_actual, categoria)

        result = ({'OK': 'Las respuestas fueron guardadas correctamente'}, SUCCESS_OK)
        logging.info('Guardar Respuestas Encuesta Alumno devuelve como resultado: {}'.format(result))
        return result

    def validar_respuestas_recibidas(self, respuestas, categoria):
        ids_respuestas = {}
        ids_respuestas_invalidas = []
        for respuesta in respuestas:
            es_valida, msj = self.respuesta_es_valida(
                respuesta,
                self.obtener_preguntas_encuestas(categoria, True),
                ids_respuestas,
                ids_respuestas_invalidas
            )
            if not es_valida:
                return False, msj

        for id_invalida in ids_respuestas_invalidas:
            if id_invalida in ids_respuestas:
                logging.error('El servicio Guardar Respuestas Encuestas Alumno recibió una subrespuesta inválida')
                return False, msj

        return True, 'OK'

    def eliminar_todas_las_respuestas_del_paso_actual(self, preguntas):
        for id_pregunta in preguntas:
            respuestas_encuestas = RespuestaEncuestaAlumno.query.filter_by(pregunta_encuesta_id=id_pregunta).all()
            self.eliminar_respuestas(respuestas_encuestas)

    def eliminar_respuestas(self, respuestas_encuestas):
        for respuesta_encuesta in respuestas_encuestas:
            tipo_encuesta = TipoEncuesta.query.filter_by(id=respuesta_encuesta.tipo_id).first().tipo
            acciones = {
                PUNTAJE_1_A_5: self.eliminar_respuesta_puntaje,
                TEXTO_LIBRE: self.eliminar_respuesta_texto_libre,
                SI_NO: self.eliminar_respuesta_si_no,
                HORARIO: self.eliminar_respuesta_horario,
                DOCENTE: self.eliminar_respuesta_docente,
                CORRELATIVA: self.eliminar_respuesta_correlativas,
                ESTRELLAS: self.eliminar_respuesta_estrellas,
                NUMERO: self.eliminar_respuesta_numero,
                TAG: self.eliminar_respuesta_tags,
                TEMATICA: self.eliminar_respuesta_tematicas,
            }

            acciones[tipo_encuesta](respuesta_encuesta)

    def eliminar_respuesta_puntaje(self, respuesta_encuesta):
        RespuestaEncuestaPuntaje.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).delete()
        db.session.commit()

    def eliminar_respuesta_texto_libre(self, respuesta_encuesta):
        RespuestaEncuestaTexto.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).delete()
        db.session.commit()

    def eliminar_respuesta_si_no(self, respuesta_encuesta):
        RespuestaEncuestaSiNo.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).delete()
        db.session.commit()

    def eliminar_respuesta_horario(self, respuesta_encuesta):
        ids_horarios_viejos = []
        horarios_viejos = RespuestaEncuestaHorario.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).all()
        for horario_viejo in horarios_viejos:
            ids_horarios_viejos.append(horario_viejo.horario_id)

        if len(ids_horarios_viejos):
            RespuestaEncuestaHorario.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).delete()
            db.session.commit()

            Horario.query.filter(Horario.id.in_(ids_horarios_viejos)).delete(synchronize_session='fetch')
            db.session.commit()

    def eliminar_respuesta_docente(self, respuesta_encuesta):
        RespuestaEncuestaDocente.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).delete()
        db.session.commit()

    def eliminar_respuesta_correlativas(self, respuesta_encuesta):
        RespuestaEncuestaCorrelativa.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).delete()
        db.session.commit()

    def eliminar_respuesta_estrellas(self, respuesta_encuesta):
        RespuestaEncuestaEstrellas.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).delete()
        db.session.commit()

    def eliminar_respuesta_numero(self, respuesta_encuesta):
        RespuestaEncuestaNumero.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).delete()
        db.session.commit()

    def eliminar_respuesta_tags(self, respuesta_encuesta):
        RespuestaEncuestaTags.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).delete()
        db.session.commit()

    def eliminar_respuesta_tematicas(self, respuesta_encuesta):
        RespuestaEncuestaTematica.query.filter_by(rta_encuesta_alumno_id=respuesta_encuesta.id).delete()
        db.session.commit()

    def actualizar_estado_paso_actual(self, id_encuesta, preguntas_categoria_actual, categoria):
        estados_pasos = EstadoPasosEncuestaAlumno.query.filter_by(encuesta_alumno_id=id_encuesta).first()
        numero_paso = GrupoEncuesta.query.filter_by(id=categoria).first().numero_grupo

        finalizado = len(preguntas_categoria_actual) == 0

        #Aunque no hayan respuestas docentes el paso queda finalizado
        if numero_paso == GRUPO_ENCUESTA_DOCENTES:
            finalizado = True

        estados_pasos.actualizar_estado_paso(numero_paso, finalizado)

    def obtener_preguntas_encuestas(self, categoria, agregar_subpreguntas=False):
        encuestas = EncuestaGenerada.query.filter_by(grupo_id=categoria).all()

        preguntas_categoria_actual = {}
        for encuesta in encuestas:
            pregunta = PreguntaEncuesta.query.filter_by(id=encuesta.encuesta_id).first()
            preguntas_categoria_actual[pregunta.id] = pregunta

            if agregar_subpreguntas:
                self.agregar_subpreguntas_si_no(preguntas_categoria_actual, pregunta)

        return preguntas_categoria_actual

    def agregar_subpreguntas_si_no(self, preguntas_categoria_actual, pregunta):
        if pregunta.tipo_id != TipoEncuesta.query.filter_by(tipo=SI_NO).first().id:
            return

        for pregunta_si_no in PreguntaEncuestaSiNo.query.filter_by(encuesta_id=pregunta.id).all():
            if pregunta_si_no.encuesta_id_si:
                subpregunta = PreguntaEncuesta.query.filter_by(id=pregunta_si_no.encuesta_id_si).first()
                preguntas_categoria_actual[subpregunta.id] = subpregunta
            if pregunta_si_no.encuesta_id_no:
                subpregunta = PreguntaEncuesta.query.filter_by(id=pregunta_si_no.encuesta_id_no).first()
                preguntas_categoria_actual[subpregunta.id] = subpregunta


    def respuesta_es_valida(self, respuesta, preguntas_categoria_actual, ids_respuestas, ids_respuestas_invalidas):
        idPregunta = respuesta["idPregunta"]

        if not idPregunta in preguntas_categoria_actual:
            logging.error('El servicio Guardar Respuestas Encuesta Alumno recibió un id de pregunta inválido')
            return False, 'Este servicio recibió un id de pregunta inválido'

        pregunta = preguntas_categoria_actual.pop(idPregunta)
        tipo_encuesta = TipoEncuesta.query.filter_by(id=pregunta.tipo_id).first().tipo

        if not self.validar_respuesta(tipo_encuesta, respuesta, ids_respuestas, ids_respuestas_invalidas):
            logging.error('El servicio Guardar Respuestas Encuesta Alumno recibió una '
                          'respuesta de encuesta inválida')
            return False, 'Este servicio recibió un respuesta de encuesta inválida'

        return True, 'OK'


    def validar_respuesta(self, tipo_encuesta, respuesta, ids_respuestas, ids_respuestas_invalidas):
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
            ids_respuestas[respuesta["idPregunta"]] = respuesta["idPregunta"]
            acciones[tipo_encuesta](respuesta, ids_respuestas_invalidas)
        except:
            return False

        return True

    MIN_PUNTAJE = 1
    MAX_PUNTAJE = 5

    def validar_respuesta_puntaje(self, respuesta, ids_respuestas_invalidas):
        if not str(respuesta["puntaje"]).isdigit():
            raise ValueError("El puntaje debe ser un entero")

        puntaje = int(respuesta["puntaje"])
        if puntaje < self.MIN_PUNTAJE or puntaje > self.MAX_PUNTAJE:
            raise ValueError("El puntaje no esta entre los valores {} - {}".format(self.MIN_PUNTAJE, self.MAX_PUNTAJE))

    MAX_CARACTERES_TEXTO = 250

    def validar_respuesta_texto_libre(self, respuesta, ids_respuestas_invalidas):
        texto = respuesta["texto"]
        self.validar_contenido_y_longitud_texto(1, self.MAX_CARACTERES_TEXTO, texto)

    def validar_respuesta_si_no(self, respuesta, ids_respuestas_invalidas):
        rta = str(respuesta["respuesta"]).upper()
        if not rta == "TRUE" and not rta == "FALSE":
            raise Exception("La respuesta debe ser True o False")

        if rta == "TRUE":
            respuesta["respuesta"] = True
        else:
            respuesta["respuesta"] = False

        for pregunta in PreguntaEncuestaSiNo.query.filter_by(encuesta_id=respuesta["idPregunta"]).all():
            if rta == "TRUE" and pregunta.encuesta_id_no:
                ids_respuestas_invalidas.append(pregunta.encuesta_id_no)
            if rta == "FALSE" and pregunta.encuesta_id_si:
                ids_respuestas_invalidas.append(pregunta.encuesta_id_si)

    def validar_respuesta_horario(self, respuesta, ids_respuestas_invalidas):
        horarios = respuesta["horarios"]
        for horario in horarios:
            dia = horario["dia"].upper()
            if not dia in DIAS:
                raise Exception("El nombre del dia no es válido")

            self.convertir_hora(horario["hora_desde"])
            self.convertir_hora(horario["hora_hasta"])

    def convertir_hora(self, horario):
        horas, minutos = horario.split(":")
        return convertir_horario(horas, minutos)

    def validar_respuesta_docente(self, respuesta, ids_respuestas_invalidas):
        docentes = respuesta["docentes"]
        for docente in docentes:
            idDocente = docente["id_docente"]

            if not Docente.query.filter_by(id=idDocente).first():
                raise ValueError("El id de docente {} es invalido".format(idDocente))

            comentario = docente["comentario"]
            self.validar_contenido_y_longitud_texto(1, self.MAX_CARACTERES_TEXTO, comentario)

    def validar_respuesta_correlativas(self, respuesta, ids_respuestas_invalidas):
        correlativas = respuesta["correlativas"]
        for id_materia_correlativa in correlativas:
            assert (str(id_materia_correlativa).isdigit())
            if not Materia.query.filter_by(id=id_materia_correlativa).first():
                raise ValueError("La materia con id {} que se desea indicar como "
                                 "correlativa no existe".format(id_materia_correlativa))

    MIN_ESTRELLAS = 1
    MAX_ESTRELLAS = 5

    def validar_respuesta_estrellas(self, respuesta, ids_respuestas_invalidas):
        if not str(respuesta["estrellas"]).isdigit():
            raise ValueError("Las estrellas deben ser un número entero")

        estrellas = int(respuesta["estrellas"])
        if estrellas < self.MIN_ESTRELLAS or estrellas > self.MAX_ESTRELLAS:
            raise ValueError("La cantidad de estrellas no está entre "
                             "los valores {} - {}".format(self.MIN_ESTRELLAS, self.MAX_ESTRELLAS))

    MIN_NUMERO = 0
    MAX_NUMERO = 168
    def validar_respuesta_numero(self, respuesta, ids_respuestas_invalidas):
        if not str(respuesta["numero"]).isdigit():
            raise ValueError("El número debe ser un entero")

        numero = int(respuesta["numero"])
        if numero < self.MIN_NUMERO or numero > self.MAX_NUMERO:
            raise ValueError("El número no está entre los "
                             "valores {} - {}".format(self.MIN_NUMERO, self.MAX_NUMERO))

    MAX_CARACTERES_PALABRA_CLAVE_TAG = 30
    MAX_CANTIDAD_PALABRAS_CLAVE = 3

    def validar_respuesta_tags(self, respuesta, ids_respuestas_invalidas):
        palabras_clave = respuesta["palabras_clave"]
        assert (0 < len(palabras_clave) <= self.MAX_CANTIDAD_PALABRAS_CLAVE)
        for palabra in palabras_clave:
            self.validar_contenido_y_longitud_texto(1, self.MAX_CARACTERES_PALABRA_CLAVE_TAG, palabra)

    MAX_CARACTERES_TEMATICA = 40
    MAX_CANTIDAD_TEMATICAS = 10

    def validar_respuesta_tematicas(self, respuesta, ids_respuestas_invalidas):
        tematicas = respuesta["tematicas"]
        assert (0 < len(tematicas) <= self.MAX_CANTIDAD_TEMATICAS)
        for tematica in tematicas:
            self.validar_contenido_y_longitud_texto(1, self.MAX_CARACTERES_TEMATICA, tematica)

    def validar_contenido_y_longitud_texto(self, len_min, len_max, texto):
        for simbolo in "¡!,.-¿?*/+-'[]{}() &%$|@#~¬=;:\n":
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

    def guardar_respuestas(self, respuestas, id_encuesta, preguntas_categoria_actual):
        while len(respuestas) > 0:
            respuesta = respuestas.pop(0)

            # Es una subrespuesta que aun no agrego la pregunta
            if not respuesta["idPregunta"] in preguntas_categoria_actual:
                respuestas.append(respuesta)
                continue

            preguntas_categoria_actual.pop(respuesta["idPregunta"])

            tipo = TipoEncuesta.query.filter_by(tipo=respuesta["tipo_encuesta"]).first()
            respuesta_encuesta = RespuestaEncuestaAlumno(
                encuesta_alumno_id=id_encuesta,
                pregunta_encuesta_id=respuesta["idPregunta"],
                tipo_id=tipo.id
            )
            db.session.add(respuesta_encuesta)
            db.session.commit()

            self.crear_respuesta(respuesta_encuesta, respuesta, respuesta["tipo_encuesta"], preguntas_categoria_actual)
            db.session.commit()

    def crear_respuesta(self, respuesta_encuesta, datos_respuesta, tipo_encuesta, preguntas_categoria_actual):
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

        acciones[tipo_encuesta](respuesta_encuesta, datos_respuesta, preguntas_categoria_actual)

    def generar_respuesta_puntaje(self, respuesta_encuesta, datos_respuesta, preguntas_categoria_actual):
        respuesta = RespuestaEncuestaPuntaje(
            rta_encuesta_alumno_id=respuesta_encuesta.id,
            puntaje=datos_respuesta["puntaje"]
        )
        db.session.add(respuesta)
        db.session.commit()

    def generar_respuesta_texto_libre(self, respuesta_encuesta, datos_respuesta, preguntas_categoria_actual):
        respuesta = RespuestaEncuestaTexto(
            rta_encuesta_alumno_id=respuesta_encuesta.id,
            texto=datos_respuesta["texto"]
        )
        db.session.add(respuesta)
        db.session.commit()

    def generar_respuesta_si_no(self, respuesta_encuesta, datos_respuesta, preguntas_categoria_actual):
        respuesta = RespuestaEncuestaSiNo(
            rta_encuesta_alumno_id=respuesta_encuesta.id,
            respuesta=datos_respuesta["respuesta"]
        )
        db.session.add(respuesta)
        db.session.commit()

        preguntas = PreguntaEncuestaSiNo.query.filter_by(encuesta_id=respuesta_encuesta.pregunta_encuesta_id).all()
        for pregunta in preguntas:
            if datos_respuesta["respuesta"] and pregunta.encuesta_id_si:
                subpregunta = PreguntaEncuesta.query.filter_by(id=pregunta.encuesta_id_si).first()
                preguntas_categoria_actual[pregunta.encuesta_id_si] = subpregunta
            if not datos_respuesta["respuesta"] and pregunta.encuesta_id_no:
                subpregunta = PreguntaEncuesta.query.filter_by(id=pregunta.encuesta_id_no).first()
                preguntas_categoria_actual[pregunta.encuesta_id_no] = subpregunta

    def generar_respuesta_horario(self, respuesta_encuesta, datos_respuesta, preguntas_categoria_actual):
        for datos_horario in datos_respuesta["horarios"]:
            horario = Horario(
                dia=datos_horario["dia"].upper(),
                hora_desde=self.convertir_hora(datos_horario["hora_desde"]),
                hora_hasta=self.convertir_hora(datos_horario["hora_hasta"])
            )
            db.session.add(horario)
            db.session.commit()

            db.session.add(RespuestaEncuestaHorario(
                rta_encuesta_alumno_id=respuesta_encuesta.id,
                horario_id=horario.id
            ))

    def generar_respuesta_docente(self, respuesta_encuesta, datos_respuesta, preguntas_categoria_actual):
        for datos_docente in datos_respuesta["docentes"]:
            db.session.add(RespuestaEncuestaDocente(
                rta_encuesta_alumno_id=respuesta_encuesta.id,
                docente_id=datos_docente["id_docente"],
                comentario=datos_docente["comentario"]
            ))

    def generar_respuesta_correlativas(self, respuesta_encuesta, datos_respuesta, preguntas_categoria_actual):
        for correlativa in datos_respuesta["correlativas"]:
            db.session.add(RespuestaEncuestaCorrelativa(
                rta_encuesta_alumno_id=respuesta_encuesta.id,
                materia_correlativa_id=correlativa
            ))
            db.session.commit()

    def generar_respuesta_estrellas(self, respuesta_encuesta, datos_respuesta, preguntas_categoria_actual):
        respuesta = RespuestaEncuestaEstrellas(
            rta_encuesta_alumno_id=respuesta_encuesta.id,
            estrellas=datos_respuesta["estrellas"]
        )
        db.session.add(respuesta)
        db.session.commit()

    def generar_respuesta_numero(self, respuesta_encuesta, datos_respuesta, preguntas_categoria_actual):
        respuesta = RespuestaEncuestaNumero(
            rta_encuesta_alumno_id=respuesta_encuesta.id,
            numero=datos_respuesta["numero"]
        )
        db.session.add(respuesta)
        db.session.commit()

    def generar_respuesta_tags(self, respuesta_encuesta, datos_respuesta, preguntas_categoria_actual):
        for palabra_clave in datos_respuesta["palabras_clave"]:

            palabra = PalabraClave.query.filter_by(palabra=palabra_clave).first()
            if not palabra:
                palabra = PalabraClave(palabra=palabra_clave)
                db.session.add(palabra)
                db.session.commit()

            db.session.add(RespuestaEncuestaTags(
                rta_encuesta_alumno_id=respuesta_encuesta.id,
                palabra_clave_id=palabra.id
            ))
            db.session.commit()

    def generar_respuesta_tematicas(self, respuesta_encuesta, datos_respuesta, preguntas_categoria_actual):
        for nombre_tematica in datos_respuesta["tematicas"]:

            tematica = TematicaMateria.query.filter_by(tematica=nombre_tematica).first()
            if not tematica:
                tematica = TematicaMateria(tematica=nombre_tematica)
                db.session.add(tematica)
                db.session.commit()

            db.session.add(RespuestaEncuestaTematica(
                rta_encuesta_alumno_id=respuesta_encuesta.id,
                tematica_id=tematica.id
            ))
            db.session.commit()
