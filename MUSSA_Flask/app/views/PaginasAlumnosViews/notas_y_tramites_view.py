from flask import render_template
from flask import request
from flask_user import login_required
from app.ClienteAPI.ClienteAPI import ClienteAPI
from app.views.base_view import main_blueprint


@main_blueprint.route('/notas_y_tramites', methods=['GET'])
@login_required
def notas_y_tramites_page():
    return render_template('pages/notas_y_tramites.html')


@main_blueprint.route('/formularios/nota_al_decano', methods=['GET'])
@login_required
def nota_al_decano_page():
    return render_template('pages/nota_al_decano.html')


@main_blueprint.route('/formularios/materias_alumno', methods=['GET'])
@login_required
def formulario_materias_alumno_page():
    cookies = request.cookies
    cliente = ClienteAPI()

    mis_carreras = cliente.obtener_carreras_alumno(cookies)
    return render_template('pages/formulario_materias_alumno.html',
                           carreras=mis_carreras)
