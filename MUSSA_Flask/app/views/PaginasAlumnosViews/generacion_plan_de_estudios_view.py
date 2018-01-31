from flask import render_template
from flask_user import login_required
from flask import request
from app.views.base_view import main_blueprint
from app.ClienteAPI.ClienteAPI import ClienteAPI
from app.utils import DIAS, generar_lista_horarios


@main_blueprint.route('/planes_de_estudio', methods=['GET'])
@login_required
def planes_de_estudios_page():
    cookies = request.cookies
    cliente = ClienteAPI()

    return render_template('pages/planes_de_estudio_page.html')


@main_blueprint.route('/planes_de_estudio/nuevo_plan', methods=['GET'])
@login_required
def nuevo_plan_de_estudios_page():
    cookies = request.cookies
    cliente = ClienteAPI()

    mis_carreras = cliente.obtener_carreras_alumno(cookies)
    horarios = generar_lista_horarios()

    return render_template('pages/generar_plan_de_estudios_page.html',
                           carreras=mis_carreras,
                           dias=DIAS,
                           hora_desde=horarios[:-1],
                           hora_hasta=horarios[1:]
                           )
