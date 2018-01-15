from app.views.base_view import main_blueprint
from flask import render_template
from flask import request
from app.ClienteAPI.ClienteAPI import ClienteAPI
from app.views.Utils.invocaciones_de_servicios import *


@main_blueprint.route('/materias/<int:idMateria>', methods=['GET'])
def materia_page(idMateria):
    materia = invocar_servicio_obtener_materia(request.cookies, idMateria)

    carreras = ClienteAPI().obtener_todas_las_carreras(request.cookies, materia["codigo"])

    correlativas = invocar_servicio_obtener_correlativas(request.cookies, idMateria)

    cursos = invocar_servicio_obtener_curso(request.cookies, materia["codigo"], materia["carrera_id"])

    return render_template('pages/materia_page.html',
                           materia=materia,
                           carreras=carreras,
                           correlativas=correlativas,
                           cursos=cursos)
