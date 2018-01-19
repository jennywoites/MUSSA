from app.DAO.EncuestasDAO import *
from app.models.encuestas_models import PreguntaEncuesta, GrupoEncuesta, ExcluirEncuestaSi, TipoEncuesta


def generarJSON_encuesta(encuesta):
    datos = generarJSON_base_encuesta(encuesta)
    pregunta = PreguntaEncuesta.query.get(encuesta.encuesta_id)
    agregarJSON_datos_de_encuesta_completa(pregunta, datos)
    return datos


######################################################################################
##                      Generadores y Funciones Auxiliares                          ##
######################################################################################

def generarJSON_base_encuesta(encuesta):
    return {
        "pregunta_encuesta_id": encuesta.encuesta_id,
        "grupo_id": encuesta.grupo_id,
        "grupo": GrupoEncuesta.query.get(encuesta.grupo_id).grupo,
        "excluir_si": ExcluirEncuestaSi.query.get(encuesta.excluir_si_id).tipo,
        "orden": encuesta.orden
    }


def agregarJSON_datos_de_encuesta_completa(pregunta, datos):
    agregarJSON_datos_pregunta(pregunta, datos)

    if datos["tipo_num"] == PUNTAJE_1_A_5:
        agregarJSON_datos_encuesta_puntaje(pregunta, datos)

    if datos["tipo_num"] == SI_NO:
        agregarJSON_datos_encuesta_si_no(pregunta, datos)

    if datos["tipo_num"] == NUMERO:
        agregarJSON_datos_encuesta_numerica(pregunta, datos)


def agregarJSON_datos_pregunta(pregunta, datos):
    tipo_encuesta = TipoEncuesta.query.get(pregunta.tipo_id)

    datos["pregunta_id"] = pregunta.id
    datos["pregunta"] = pregunta.pregunta
    datos["tipo_num"] = tipo_encuesta.tipo
    datos["tipo"] = tipo_encuesta.descripcion


def agregarJSON_datos_encuesta_puntaje(pregunta, datos):
    e_puntaje = PreguntaEncuestaPuntaje.query.filter_by(encuesta_id=pregunta.id).first()

    datos["texto_min"] = e_puntaje.texto_min
    datos["texto_max"] = e_puntaje.texto_max


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
    agregarJSON_datos_pregunta(pregunta, datos)
    agregarJSON_datos_de_encuesta_completa(pregunta, datos)
    lista_preguntas.append(datos)


def agregarJSON_datos_encuesta_numerica(pregunta, datos):
    e_numerica = PreguntaEncuestaNumero.query.filter_by(encuesta_id=pregunta.id).first()

    datos["numero_min"] = e_numerica.numero_min
    datos["numero_max"] = e_numerica.numero_max
