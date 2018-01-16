from app.views.base_view import main_blueprint
from flask import render_template
from flask import request
from app.ClienteAPI.ClienteAPI import ClienteAPI
from app.views.Utils.invocaciones_de_servicios import *


@main_blueprint.route('/materias/<int:idMateria>', methods=['GET'])
def materia_page(idMateria):
    cookies = request.cookies

    materia = ClienteAPI().get_materia(cookies, idMateria)
    carreras = ClienteAPI().obtener_todas_las_carreras(cookies, materia["codigo"])
    correlativas = ClienteAPI().obtener_materias_correlativas(cookies, idMateria)
    cursos = invocar_servicio_obtener_curso(cookies, materia["codigo"], materia["carrera_id"])

    return render_template('pages/materia_page.html',
                           materia=materia,
                           carreras=carreras,
                           correlativas=correlativas,
                           cursos=cursos)
