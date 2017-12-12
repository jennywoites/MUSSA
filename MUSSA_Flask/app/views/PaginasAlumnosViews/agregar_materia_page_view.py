from flask import redirect, render_template
from flask import request, url_for, flash
from flask_user import login_required

from app.views.base_view import main_blueprint

from app.views.Utils.invocaciones_de_servicios import *

from app.DAO.MateriasDAO import *

from datetime import datetime

@main_blueprint.route('/datos_academicos/agregar_materia', methods=['GET'])
@login_required
def agregar_materia_page():
    cookie = request.cookies

    mis_carreras = invocar_obtener_carreras_alumno(cookie)

    materias = invocar_obtener_materias_alumno(cookie, [PENDIENTE])

    cursos = invocar_servicio_obtener_curso(cookie)
    for i in range(len(cursos)):
        texto = ""
        for carrera in cursos[i]["carreras"]:
            texto += "carrera_" + str(carrera["id_carrera"]) + ";"
        cursos[i]["carreras"] = texto[:-1]

    estados = []
    for estado in [EN_CURSO, FINAL_PENDIENTE, APROBADA, DESAPROBADA]:
        estados.append(ESTADO_MATERIA[estado])

    formas_aprobacion = []
    for forma in [EXAMEN, EXAMEN_EQUIVALENCIA, EQUIVALENCIA]:
        formas_aprobacion.append(FORMA_APROBACION[forma])

    MAX_TIEMPO = 10
    hoy = datetime.now().year
    anios = [x for x in range(hoy, hoy - MAX_TIEMPO, -1)]

    return render_template('pages/agregar_materia_page.html',
        carreras = mis_carreras,
        materias = materias,
        cursos = cursos,
        estados = estados,
        formas_aprobacion = formas_aprobacion,
        anios = anios)


@main_blueprint.route('/datos_academicos/agregar_materia_save', methods=['POST'])
@login_required
def agregar_materia_page_save():
    parametros = {
        'id_carrera': request.form['carrera'],
        'id_materia': request.form['materia'],
        'id_curso': request.form['curso'],
        'estado': request.form['estado'],
        'cuatrimestre_aprobacion': request.form['cuatrimestre_aprobacion'],
        'anio_aprobacion': request.form['anio_aprobacion'],
        'fecha_aprobacion': request.form['fecha_aprobacion'],
        'forma_aprobacion': request.form['forma_aprobacion'],
        'calificacion': request.form['calificacion'],
        'acta_resolucion': request.form['acta_resolucion']
    }

    response = invocar_agregar_materia_alumno(request.form["csrf_token"], request.cookies, parametros)

    if 'OK' in response:
        flash("Se agregó la materia satisfactoriamente", 'success')
    else:   
        flash(response["Error"], 'error')

    return redirect(url_for("main.datos_academicos_page"))

