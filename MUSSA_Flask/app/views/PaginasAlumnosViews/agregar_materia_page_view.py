from flask import redirect, render_template
from flask import request, url_for, flash
from flask_user import login_required
from app.views.base_view import main_blueprint
from app.DAO.MateriasDAO import *
from datetime import datetime
from app.ClienteAPI.ClienteAPI import ClienteAPI
from app.API_Rest.codes import *


@main_blueprint.route('/datos_academicos/agregar_materia', methods=['GET'])
@login_required
def agregar_materia_page():
    cookie = request.cookies

    mis_carreras = ClienteAPI().obtener_carreras_alumno(cookie)

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
                           carreras=mis_carreras,
                           estados=estados,
                           formas_aprobacion=formas_aprobacion,
                           anios=anios)


@main_blueprint.route('/datos_academicos/agregar_materia_save', methods=['POST'])
@login_required
def agregar_materia_page_save():
    response = ClienteAPI().agregar_materia_alumno(
        cookie=request.cookies,
        csrf_token=request.form["csrf_token"],
        idMateriaAlumno=request.form['materia'],
        idCurso=request.form['curso'],
        estado=request.form['estado'],
        cuatrimestre_aprobacion=request.form['cuatrimestre_aprobacion'],
        anio_aprobacion=request.form['anio_aprobacion'],
        fecha_aprobacion=request.form['fecha_aprobacion'],
        forma_aprobacion=request.form['forma_aprobacion'],
        calificacion=request.form['calificacion'],
        acta_resolucion=request.form['acta_resolucion']
    )

    if response == SUCCESS_NO_CONTENT or response == SUCCESS_OK:
        flash("Se agregó la materia satisfactoriamente", 'success')
    else:
        flash(response["Error"], 'error')

    return redirect(url_for("main.datos_academicos_page"))
