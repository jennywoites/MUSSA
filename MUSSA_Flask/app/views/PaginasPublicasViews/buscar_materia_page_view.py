from app.views.base_view import main_blueprint
from flask import render_template
from flask import request
from app.ClienteAPI.ClienteAPI import ClienteAPI


@main_blueprint.route('/buscar_materias', methods=['GET'])
def buscar_materias_page():
    carreras = ClienteAPI().obtener_todas_las_carreras(request.cookies)
    return render_template('pages/buscar_materias_page.html',
                           carreras=carreras)
