from app.views.base_view import main_blueprint  

from flask import redirect, render_template
from flask import request, url_for

import requests

from app.views.Utils.invocaciones_de_servicios import *

@main_blueprint.route('/materias/<int:idMateria>', methods=['GET'])
def materia_page(idMateria):
    materia = invocar_servicio_obtener_materia(idMateria)

    carreras = invocar_servicio_obtener_carreras_para_una_materia(materia["codigo"])

    correlativas = invocar_servicio_obtener_correlativas(idMateria)

    return render_template('pages/materia_page.html',
                materia=materia,
                carreras=carreras,
                correlativas = correlativas)