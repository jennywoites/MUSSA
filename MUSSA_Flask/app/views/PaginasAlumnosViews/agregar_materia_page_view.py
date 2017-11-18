from flask import redirect, render_template
from flask import request, url_for, flash
from flask_user import current_user, login_required, roles_accepted

from app.views.base_view import main_blueprint

from app.views.Utils.invocaciones_de_servicios import *

from flask_babel import gettext
from app.DAO.MateriasDAO import *


@main_blueprint.route('/datos_academicos/agregar_materia', methods=['GET'])
@login_required
def agregar_materia_page():
    cookie = request.cookies

    mis_carreras = invocar_obtener_carreras_alumno(cookie)

    materias = invocar_obtener_materias_alumno(cookie, [PENDIENTE])

    estados = []
    for estado in [EN_CURSO, FINAL_PENDIENTE, APROBADA, DESAPROBADA]:
        estados.append(ESTADO_MATERIA[estado])

    formas_aprobacion = []
    for forma in [EXAMEN, EXAMEN_EQUIVALENCIA, EQUIVALENCIA]:
        formas_aprobacion.append(FORMA_APROBACION[forma])

    return render_template('pages/agregar_materia_page.html',
        carreras = mis_carreras,
        materias = materias,
        estados = estados,
        formas_aprobacion = formas_aprobacion)


@main_blueprint.route('/datos_academicos/agregar_materia_save', methods=['POST'])
@login_required
def agregar_materia_page_save():    
    #if not 'OK' in response:
    #    flash(response["Error"], 'error')

    flash("Lalal", 'error')

    return redirect(url_for("main.datos_academicos_page"))

