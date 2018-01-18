from flask import render_template
from flask_user import login_required
from flask import request, url_for, redirect
from app.views.base_view import main_blueprint
from app.views.Utils.invocaciones_de_servicios import *
from app.DAO.EncuestasDAO import *
from app.utils import frange, get_numero_dos_digitos, DIAS
from app.ClienteAPI.ClienteAPI import ClienteAPI
from app.API_Rest.codes import *

@main_blueprint.route('/encuestas/visualizar_encuesta/general/<int:idEncuestaAlumno>', methods=['GET'])
@login_required
def visualizar_encuesta_general_page(idEncuestaAlumno):
    return visualizar_encuesta(idEncuestaAlumno, request.cookies, GRUPO_ENCUESTA_GENERAL)


@main_blueprint.route('/encuestas/visualizar_encuesta/contenido/<int:idEncuestaAlumno>', methods=['GET'])
@login_required
def visualizar_encuesta_contenido_page(idEncuestaAlumno):
    return visualizar_encuesta(idEncuestaAlumno, request.cookies, GRUPO_ENCUESTA_CONTENIDO)


@main_blueprint.route(
    '/encuestas/visualizar_encuesta/clases/<int:idEncuestaAlumno>', methods=['GET'])
@login_required
def visualizar_encuesta_clases_page(idEncuestaAlumno):
    return visualizar_encuesta(idEncuestaAlumno, request.cookies, GRUPO_ENCUESTA_CLASES)


@main_blueprint.route('/encuestas/visualizar_encuesta/examenes/<int:idEncuestaAlumno>', methods=['GET'])
@login_required
def visualizar_encuesta_examenes_page(idEncuestaAlumno):
    return visualizar_encuesta(idEncuestaAlumno, request.cookies, GRUPO_ENCUESTA_EXAMENES)


@main_blueprint.route('/encuestas/visualizar_encuesta/docentes/<int:idEncuestaAlumno>', methods=['GET'])
@login_required
def visualizar_encuesta_docentes_page(idEncuestaAlumno):
    return visualizar_encuesta(idEncuestaAlumno, request.cookies, GRUPO_ENCUESTA_DOCENTES)


def visualizar_encuesta(idEncuestaAlumno, cookie, num_categoria):
    preguntas = invocar_servicio_obtener_preguntas_encuesta(cookie, [num_categoria])
    encuesta = invocar_obtener_encuesta_alumno(cookie, idEncuestaAlumno)

    if not encuesta["finalizada"]:
        return redirect(url_for('main.historial_encuestas_page'), code=REDIRECTION_FOUND)

    respuestas = invocar_obtener_respuestas_encuesta_alumno(cookie, idEncuestaAlumno, preguntas)
    convertir_true_false(respuestas)

    titulos = [
        {'url': 'main.visualizar_encuesta_general_page', 'titulo': 'General'},
        {'url': 'main.visualizar_encuesta_contenido_page', 'titulo': 'Contenido'},
        {'url': 'main.visualizar_encuesta_clases_page', 'titulo': 'Clases'},
        {'url': 'main.visualizar_encuesta_examenes_page', 'titulo': 'Exámenes'},
        {'url': 'main.visualizar_encuesta_docentes_page', 'titulo': 'Docentes'}
    ]

    anterior_siguiente = {
        GRUPO_ENCUESTA_GENERAL: [
            '',
            url_for('main.visualizar_encuesta_contenido_page', idEncuestaAlumno=idEncuestaAlumno)
        ],
        GRUPO_ENCUESTA_CONTENIDO: [
            url_for('main.visualizar_encuesta_general_page', idEncuestaAlumno=idEncuestaAlumno),
            url_for('main.visualizar_encuesta_clases_page', idEncuestaAlumno=idEncuestaAlumno),
        ],
        GRUPO_ENCUESTA_CLASES: [
            url_for('main.visualizar_encuesta_contenido_page', idEncuestaAlumno=idEncuestaAlumno),
            url_for('main.visualizar_encuesta_examenes_page', idEncuestaAlumno=idEncuestaAlumno),
        ],
        GRUPO_ENCUESTA_EXAMENES: [
            url_for('main.visualizar_encuesta_clases_page', idEncuestaAlumno=idEncuestaAlumno),
            url_for('main.visualizar_encuesta_docentes_page', idEncuestaAlumno=idEncuestaAlumno),
        ],
        GRUPO_ENCUESTA_DOCENTES: [
            url_for('main.visualizar_encuesta_examenes_page', idEncuestaAlumno=idEncuestaAlumno),
            ''
        ]
    }

    return render_template('pages/visualizar_encuesta_page.html',
                           titulos=titulos,
                           idEncuestaAlumno=idEncuestaAlumno,
                           encuesta=encuesta,
                           paso_activo=num_categoria,
                           preguntas=preguntas,
                           respuestas=respuestas,
                           anterior_siguiente=anterior_siguiente)


def convertir_true_false(respuestas):
    for idPregunta in respuestas:
        if "respuesta" in respuestas[idPregunta]:
            respuestas[idPregunta]["respuesta"] = 'Si' if respuestas[idPregunta]["respuesta"] else 'No'
