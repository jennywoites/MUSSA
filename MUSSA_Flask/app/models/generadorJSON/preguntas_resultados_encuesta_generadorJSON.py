from app.DAO.EncuestasDAO import *
from app.models.encuestas_models import PreguntaEncuesta, GrupoEncuesta, ExcluirEncuestaSi, TipoEncuesta


def generarJSON_pregunta_resultados(encuesta):
    pregunta = PreguntaEncuesta.query.get(encuesta.encuesta_id)
    pregunta_resultado = PreguntaResultadoEncuesta.query.filter_by(pregunta_encuesta_id=pregunta.id).first()

    datos = generarJSON_base_encuesta(encuesta)
    agregarJSON_datos_de_encuesta_completa(pregunta, pregunta_resultado, datos)
    return datos


######################################################################################
##                      Generadores y Funciones Auxiliares                          ##
######################################################################################

def generarJSON_base_encuesta(encuesta):
    return {
        "grupo_id": encuesta.grupo_id,
        "grupo": GrupoEncuesta.query.get(encuesta.grupo_id).grupo,
        "excluir_si": ExcluirEncuestaSi.query.get(encuesta.excluir_si_id).tipo,
        "orden": encuesta.orden
    }


def agregarJSON_datos_de_encuesta_completa(pregunta, pregunta_resultado, datos):
    agregarJSON_datos_pregunta(pregunta, pregunta_resultado, datos)

    if datos["tipo_num"] == PUNTAJE_1_A_5:
        agregarJSON_datos_encuesta_puntaje(pregunta_resultado, datos)

    if datos["tipo_num"] == SI_NO:
        agregarJSON_datos_encuesta_si_no(pregunta, datos)


def agregarJSON_datos_pregunta(pregunta, pregunta_resultado, datos):
    tipo_encuesta = TipoEncuesta.query.get(pregunta.tipo_id)

    datos["pregunta_id"] = pregunta_resultado.id
    datos["pregunta"] = pregunta_resultado.pregunta
    datos["tipo_num"] = tipo_encuesta.tipo
    datos["tipo"] = tipo_encuesta.descripcion


def agregarJSON_datos_encuesta_puntaje(pregunta_resultado, datos):
    e_puntaje = PreguntaResultadoEncuestaPuntaje.query.filter_by(pregunta_resultado_id=pregunta_resultado.id).first()
    datos["textos"] = [e_puntaje.texto_1, e_puntaje.texto_2, e_puntaje.texto_3, e_puntaje.texto_4, e_puntaje.texto_5]


def agregarJSON_datos_encuesta_si_no(pregunta, datos):
    encuestas_si_no = PreguntaEncuestaSiNo.query.filter_by(encuesta_id=pregunta.id).all()

    rta_si = []
    rta_no = []
    for e_si_no in encuestas_si_no:
        generar_pregunta_agregada_si_no(rta_si, e_si_no.encuesta_id_si)
        generar_pregunta_agregada_si_no(rta_no, e_si_no.encuesta_id_no)

    datos["rta_si"] = rta_si
    datos["rta_no"] = rta_no


def generar_pregunta_agregada_si_no(lista_preguntas, id_encuesta):
    if not id_encuesta:
        return

    datos = {}
    pregunta = PreguntaEncuesta.query.get(id_encuesta)
    pregunta_resultado = PreguntaResultadoEncuesta.query.filter_by(pregunta_encuesta_id=pregunta.id).first()

    agregarJSON_datos_pregunta(pregunta, pregunta_resultado, datos)
    agregarJSON_datos_de_encuesta_completa(pregunta, pregunta_resultado, datos)
    lista_preguntas.append(datos)
