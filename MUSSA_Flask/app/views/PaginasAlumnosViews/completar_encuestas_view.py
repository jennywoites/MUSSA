from flask import render_template
from flask_user import login_required
from app.views.base_view import main_blueprint
from app.views.Utils.invocaciones_de_servicios import *
from app.DAO.EncuestasDAO import *

#@main_blueprint.route('/encuestas/completar_encuesta/id_materia_alumno', methods=['GET'])
@main_blueprint.route('/encuestas/completar_encuesta', methods=['GET'])
@login_required
def completar_encuesta_page():
    cookie = request.cookies

    preguntas = invocar_servicio_obtener_preguntas_encuesta(cookie, [GRUPO_ENCUESTA_GENERAL])

    return render_template('pages/completar_encuesta_page.html',
                           paso_activo = 1,
                           preguntas = preguntas)
