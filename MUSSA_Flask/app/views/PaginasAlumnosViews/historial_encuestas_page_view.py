from flask import render_template
from flask_user import login_required
from flask import request
from app.views.base_view import main_blueprint
from app.ClienteAPI.ClienteAPI import ClienteAPI


@main_blueprint.route('/mis_encuestas', methods=['GET'])
@login_required
def historial_encuestas_page():
    cookies = request.cookies
    cliente = ClienteAPI()

    pendientes = cliente.obtener_todas_las_encuestas_alumno(cookies, False)
    finalizadas = cliente.obtener_todas_las_encuestas_alumno(cookies, True)

    return render_template('pages/historial_encuestas_page.html',
                           pendientes=pendientes,
                           finalizadas=finalizadas)
