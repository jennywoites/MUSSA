from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request

from app.models.encuestas_models import *
from app.DAO.EncuestasDAO import *

import logging


class ObtenerPreguntasEncuesta(Resource):
    def get(self):
        args = request.args
        logging.info('Se invoco al servicio Obtener Preguntas Encuesta con los siguientes parametros: {}'.format(args))

        if not self.categorias_son_validas(args):
            logging.error('El servicio Obtener Preguntas Encuesta recibió categorías inválidas')
            return {'Error': 'Este servicio recibió categorías inválidas'}, CLIENT_ERROR_BAD_REQUEST

        query = EncuestaGenerada.query

        categorias = self.obtener_categorias(args)
        if categorias:
            query = query.filter(EncuestaGenerada.grupo_id.in_(categorias))

        encuestas = query.order_by(EncuestaGenerada.orden.asc()).all()

        preguntas_result = []
        for encuesta in encuestas:
            datos = self.generar_estructura_base_encuesta(encuesta)
            pregunta = PreguntaEncuesta.query.filter_by(id=encuesta.encuesta_id).first()
            self.generar_datos_de_encuesta_completa(pregunta, datos)
            preguntas_result.append(datos)

        result = ({'preguntas': preguntas_result}, SUCCESS_OK)
        logging.info('Obtener Preguntas Encuesta devuelve como resultado: {}'.format(result))

        return result

    def generar_datos_de_encuesta_completa(self, pregunta, datos):
        self.generar_datos_pregunta(pregunta, datos)

        if datos["tipo_num"] == PUNTAJE_1_A_5:
            self.generar_datos_encuesta_puntaje(pregunta, datos)

        if datos["tipo_num"] == SI_NO:
            self.generar_datos_encuesta_si_no(pregunta, datos)

    def categorias_son_validas(self, args):
        try:
            self.obtener_categorias(args)
        except:
            return False

        return True

    def obtener_categorias(selfs, args):
        if not "categorias" in args:
            return []

        grupos_id = []
        l_categorias = args["categorias"].split(";")
        for categoria in l_categorias:
            assert (categoria.isdigit())
            grupo = GrupoEncuesta.query.filter_by(numero_grupo=categoria).first()
            assert (grupo is not None)
            grupos_id.append(grupo.id)

        return grupos_id

    def generar_estructura_base_encuesta(self, encuesta):
        return {
            "pregunta_encuesta_id": encuesta.encuesta_id,
            "grupo_id": encuesta.grupo_id,
            "grupo": GrupoEncuesta.query.filter_by(id=encuesta.grupo_id).first().grupo,
            "excluir_si": ExcluirEncuestaSi.query.filter_by(id=encuesta.excluir_si_id).first().tipo,
            "orden": encuesta.orden
        }

    def generar_datos_pregunta(self, pregunta, datos):
        tipo_encuesta = TipoEncuesta.query.filter_by(id=pregunta.tipo_id).first()

        datos["pregunta"] = pregunta.pregunta
        datos["tipo_num"] = tipo_encuesta.tipo
        datos["tipo"] = tipo_encuesta.descripcion

    def generar_datos_encuesta_puntaje(self, pregunta, datos):
        e_puntaje = PreguntaEncuestaPuntaje.query.filter_by(encuesta_id=pregunta.id).first()

        datos["texto_min"] = e_puntaje.texto_min
        datos["texto_max"] = e_puntaje.texto_max

    def generar_datos_encuesta_si_no(self, pregunta, datos):
        encuestas_si_no = PreguntaEncuestaSiNo.query.filter_by(encuesta_id=pregunta.id).all()

        rta_si = []
        rta_no = []
        for e_si_no in encuestas_si_no:
            self.generar_pregunta_agregada_si_no(rta_si, e_si_no.encuesta_id_si)
            self.generar_pregunta_agregada_si_no(rta_no, e_si_no.encuesta_id_no)

        datos["rta_si"] = rta_si
        datos["rta_no"] = rta_no

    def generar_pregunta_agregada_si_no(self, lista_preguntas, id_encuesta):
        if not id_encuesta:
            return

        datos = {}
        pregunta = PreguntaEncuesta.query.filter_by(id=id_encuesta).first()
        self.generar_datos_de_encuesta_completa(pregunta, datos)
        lista_preguntas.append(datos)
