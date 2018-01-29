from flask import redirect, render_template
from flask import request, url_for, flash
from flask_user import login_required
from app.views.base_view import main_blueprint
from app.DAO.MateriasDAO import *
from datetime import datetime
from app.ClienteAPI.ClienteAPI import ClienteAPI
from app.API_Rest.codes import *


@main_blueprint.route('/datos_academicos/editar_materia/<int:idMateria>', methods=['GET'])
@login_required
def editar_materia_page(idMateria):
    cookies = request.cookies
    cliente = ClienteAPI()

    materia = cliente.obtener_materia_alumno(cookies, idMateria)

    cursos = cliente.obtener_cursos_con_filtros(cookies, codigo_materia=materia["codigo"],
                                                id_carrera=materia["id_carrera"], filtrar_cursos=True)
    for i in range(len(cursos)):
        texto = ""
        for carrera in cursos[i]["carreras"]:
            texto += "carrera_" + str(carrera["id_carrera"]) + ";"
        cursos[i]["carreras"] = texto[:-1]

    estados = []
    if materia["estado"] == ESTADO_MATERIA[EN_CURSO]:
        estados = [ESTADO_MATERIA[EN_CURSO],
                   ESTADO_MATERIA[FINAL_PENDIENTE],
                   ESTADO_MATERIA[APROBADA],
                   ESTADO_MATERIA[DESAPROBADA]]
    if materia["estado"] == ESTADO_MATERIA[FINAL_PENDIENTE]:
        estados = [ESTADO_MATERIA[FINAL_PENDIENTE], ESTADO_MATERIA[APROBADA], ESTADO_MATERIA[DESAPROBADA]]

    formas_aprobacion = []
    for forma in [EXAMEN, EXAMEN_EQUIVALENCIA, EQUIVALENCIA]:
        formas_aprobacion.append(FORMA_APROBACION[forma])

    MAX_TIEMPO = 10
    hoy = datetime.now().year
    anios = [x for x in range(hoy, hoy - MAX_TIEMPO, -1)]

    return render_template('pages/editar_materia_page.html',
                           materia=materia,
                           cursos=cursos,
                           estados=estados,
                           formas_aprobacion=formas_aprobacion,
                           anios=anios)


@main_blueprint.route('/datos_academicos/editar_materia_save/<int:idMateria>', methods=['POST'])
@login_required
def editar_materia_page_save(idMateria):
    response = ClienteAPI().modificar_materia_alumno(
        cookie=request.cookies,
        csrf_token=request.form["csrf_token"],
        idMateriaAlumno=idMateria,
        estado=request.form['estado'],
        cuatrimestre_aprobacion=request.form['cuatrimestre_aprobacion'],
        anio_aprobacion=request.form['anio_aprobacion'],
        fecha_aprobacion=request.form['fecha_aprobacion'],
        forma_aprobacion=request.form['forma_aprobacion'],
        calificacion=request.form['calificacion'],
        acta_resolucion=request.form['acta_resolucion']
    )

    if response == SUCCESS_NO_CONTENT or response == SUCCESS_OK:
        flash("Se gurdaron los cambios en la materia", 'success')
    else:
        flash(response["Error"], 'error')

    return redirect(url_for("main.datos_academicos_page"))
