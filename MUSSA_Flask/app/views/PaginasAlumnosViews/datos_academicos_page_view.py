from flask import redirect, render_template
from flask import request, url_for, flash
from flask_user import login_required

from app.views.base_view import main_blueprint

from app.views.Utils.invocaciones_de_servicios import *

from flask_babel import gettext
from app.DAO.MateriasDAO import *
import functools

@main_blueprint.route('/datos_academicos', methods=['GET'])
@login_required
def datos_academicos_page():
    cookie = request.cookies
    padron = invocar_obtener_padron_alumno(cookie)
    carreras = invocar_servicio_buscar_carreras(cookie)

    mis_carreras = invocar_obtener_carreras_alumno(cookie)
    carreras_nuevas = filtrar_carreras_no_cursadas(carreras, mis_carreras)

    estados = [EN_CURSO, FINAL_PENDIENTE, APROBADA, DESAPROBADA]
    mis_materias = invocar_obtener_materias_alumno(cookie, estados)
    mis_materias = sorted(mis_materias, key=functools.cmp_to_key(cmp_materias_result))

    return render_template('pages/datos_academicos_page.html',
        padron = padron,
        carreras = carreras_nuevas,
        mis_carreras = mis_carreras,
        mis_materias = mis_materias)


def filtrar_carreras_no_cursadas(carreras, mis_carreras):
    carreras_no_cursadas = []

    cursadas = {}
    for mi_carrera in mis_carreras:
        cursadas[mi_carrera["codigo"]] = True

    for carrera in carreras:
        if carrera["codigo"] not in cursadas:
            carreras_no_cursadas.append(carrera)

    return carreras_no_cursadas


def cmp_materias_result(materia1, materia2):
    codigo1 = convertir_codigo(materia1)
    codigo2 = convertir_codigo(materia2)

    estado1 = materia1["estado"]
    estado2 = materia2["estado"]

    if estado1 == ESTADO_MATERIA[EN_CURSO]:
        if estado2 != ESTADO_MATERIA[EN_CURSO]:
            return 1
        return cmp_codigo(codigo1, codigo2)

    if estado2 == ESTADO_MATERIA[EN_CURSO]:
        return -1

    if estado1 == ESTADO_MATERIA[FINAL_PENDIENTE]:
        if estado2 != ESTADO_MATERIA[FINAL_PENDIENTE]:
            return 1
        return cmp_codigo(codigo1, codigo2)

    if estado2 == ESTADO_MATERIA[FINAL_PENDIENTE]:
        return -1

    if materia1["fecha_aprobacion"] < materia2["fecha_aprobacion"]:
        return -1
    elif materia1["fecha_aprobacion"] > materia2["fecha_aprobacion"]:
        return 1

    return cmp_codigo(codigo1, codigo2)


def cmp_codigo(codigo1, codigo2):
    if codigo1 < codigo2:
        return -1
    elif codigo1 > codigo2:
        return 1
    return 0


def convertir_codigo(materia):
    LONGITUD_CODIGO = 4
    codigo = materia["codigo"]
    return "0"*(LONGITUD_CODIGO - len(codigo)) + codigo

@main_blueprint.route('/datos_academicos/agregar_carrera', methods=['POST'])
@login_required
def datos_academicos_agregar_carrera_page():
    id_carrera = request.form["carrera_a_agregar"]
    csrf_token = request.form['csrf_token']

    response = invocar_agregar_carrera_alumno(csrf_token, request.cookies, id_carrera)

    if not 'OK' in response:
        flash(response["Error"], 'error')

    return redirect(url_for("main.datos_academicos_page"))


@main_blueprint.route('/datos_academicos/eliminar_carrera/<int:idCarrera>/<string:token>', methods=['GET', 'POST'])
@login_required
def datos_academicos_eliminar_carrera_page(idCarrera, token):
    response = invocar_eliminar_carrera_alumno(token, request.cookies, idCarrera)

    if 'OK' in response:
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