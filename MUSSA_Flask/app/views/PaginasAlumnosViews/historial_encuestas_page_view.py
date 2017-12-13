from flask import render_template
from flask_user import login_required
from flask import request
from app.views.base_view import main_blueprint

from app.views.Utils.invocaciones_de_servicios import *


@main_blueprint.route('/mis_encuestas', methods=['GET'])
@login_required
def historial_encuestas_page():
    pendientes = invocar_obtener_encuestas_alumno(request.cookies, False)
    finalizadas = invocar_obtener_encuestas_alumno(request.cookies, True)
    return render_template('pages/historial_encuestas_page.html',
                           pendientes=pendientes,
                           finalizadas=finalizadas)
