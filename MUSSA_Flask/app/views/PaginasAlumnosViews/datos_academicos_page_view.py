from flask import redirect, render_template
from flask import request, url_for, flash
from flask_user import login_required
from app.ClienteAPI.ClienteAPI import ClienteAPI
from app.views.base_view import main_blueprint
from app.views.Utils.invocaciones_de_servicios import *
from flask_babel import gettext
from app.API_Rest.codes import *


@main_blueprint.route('/datos_academicos', methods=['GET'])
@login_required
def datos_academicos_page():
    cookie = request.cookies
    cliente = ClienteAPI()

    padron = cliente.obtener_alumno(cookie)["padron"]
    carreras = cliente.obtener_todas_las_carreras(cookie)

    mis_carreras = cliente.obtener_carreras_alumno(cookie)
    carreras_nuevas = filtrar_carreras_no_cursadas(carreras, mis_carreras)

    mis_materias = cliente.obtener_materias_alumno(cookie)

    return render_template('pages/datos_academicos_page.html',
                           padron=padron,
                           carreras=carreras_nuevas,
                           mis_carreras=mis_carreras,
                           mis_materias=mis_materias)


def filtrar_carreras_no_cursadas(carreras, mis_carreras):
    carreras_no_cursadas = []

    cursadas = {}
    for mi_carrera in mis_carreras:
        cursadas[mi_carrera["codigo"]] = True

    for carrera in carreras:
        if carrera["codigo"] not in cursadas:
            carreras_no_cursadas.append(carrera)

    return carreras_no_cursadas


@main_blueprint.route('/datos_academicos/agregar_carrera', methods=['POST'])
@login_required
def datos_academicos_agregar_carrera_page():
    id_carrera = request.form["carrera_a_agregar"]
    csrf_token = request.form['csrf_token']

    response = ClienteAPI().agregar_carrera_alumno(request.cookies, csrf_token, id_carrera)

    if not (response == SUCCESS_NO_CONTENT or response == SUCCESS_OK):
        flash(response["Error"], 'error')

    return redirect(url_for("main.datos_academicos_page"))


@main_blueprint.route('/datos_academicos/eliminar_carrera/<int:idCarrera>/<string:token>', methods=['GET', 'POST'])
@login_required
def datos_academicos_eliminar_carrera_page(idCarrera, token):
    response = ClienteAPI().eliminar_carrera_alumno(request.cookies, token, idCarrera)

    if (response == SUCCESS_NO_CONTENT or response == SUCCESS_OK):
        flash(gettext('Se eliminó la carrera'), 'success')
    else:
        flash(response["Error"], 'error')

    return redirect(url_for("main.datos_academicos_page"))


@main_blueprint.route('/datos_academicos/eliminar_materia/<int:idMateria>/<string:token>', methods=['GET', 'POST'])
@login_required
def datos_academicos_eliminar_materia_page(idMateria, token):
    response = invocar_eliminar_materia_alumno(token, request.cookies, idMateria)

    if 'OK' in response:
        flash(gettext('Se eliminó la materia'), 'success')
    else:
        flash(response["Error"], 'error')

    return redirect(url_for("main.datos_academicos_page"))
