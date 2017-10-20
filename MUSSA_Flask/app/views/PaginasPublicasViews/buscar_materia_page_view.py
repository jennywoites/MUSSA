from app.views.base_view import main_blueprint  

from flask import redirect, render_template
from flask import request, url_for

import requests

from app.views.Utils.invocaciones_de_servicios import *

@main_blueprint.route('/buscar_materias', methods=['GET'])
def buscar_materias_page():
    carreras = invocar_servicio_buscar_carreras()
    return render_template('pages/buscar_materias_page.html',
                carreras= carreras)