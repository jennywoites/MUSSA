from flask import render_template
from flask_user import login_required
from app.views.base_view import main_blueprint
from app.views.Utils.invocaciones_de_servicios import *
from app.DAO.EncuestasDAO import *

#@main_blueprint.route('/encuestas/completar_encuesta/id_materia_alumno', methods=['GET'])
@main_blueprint.route('/encuestas/completar_encuesta/general', methods=['GET'])
@login_required
def completar_encuesta_general_page():
    return completar_encuesta(request.cookies, GRUPO_ENCUESTA_GENERAL)


@main_blueprint.route('/encuestas/completar_encuesta/contenido', methods=['GET'])
@login_required
def completar_encuesta_contenido_page():
    return completar_encuesta(request.cookies, GRUPO_ENCUESTA_CONTENIDO)


@main_blueprint.route('/encuestas/completar_encuesta/clases', methods=['GET'])
@login_required
def completar_encuesta_clases_page():
    return completar_encuesta(request.cookies, GRUPO_ENCUESTA_CLASES)


@main_blueprint.route('/encuestas/completar_encuesta/examenes', methods=['GET'])
@login_required
def completar_encuesta_examenes_page():
    return completar_encuesta(request.cookies, GRUPO_ENCUESTA_EXAMENES)


@main_blueprint.route('/encuestas/completar_encuesta/docentes', methods=['GET'])
@login_required
def completar_encuesta_docentes_page():
    return completar_encuesta(request.cookies, GRUPO_ENCUESTA_DOCENTES)


def completar_encuesta(cookie, num_categoria):
    preguntas = invocar_servicio_obtener_preguntas_encuesta(cookie, [num_categoria])

    return render_template('pages/completar_encuesta_page.html',
                           paso_activo = num_categoria,
                           preguntas = preguntas)