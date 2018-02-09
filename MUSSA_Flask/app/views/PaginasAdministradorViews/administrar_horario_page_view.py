from flask import redirect, render_template
from flask import request, url_for, flash
from flask_user import roles_accepted
from werkzeug import secure_filename
from app.ClienteAPI.ClienteAPI import ClienteAPI
from app.views.base_view import main_blueprint
from app.API_Rest.codes import *
from flask_babel import gettext
from app.utils import generar_lista_anios


@main_blueprint.route('/admin/administrar_cursos')
@roles_accepted('admin')
def administrar_cursos_page():
    cursos = ClienteAPI().obtener_todos_los_cursos_existentes(request.cookies)
    cursos = cursos if cursos else []

    return render_template('pages/administrar_cursos_page.html', cursos=cursos)


@main_blueprint.route('/admin/cargar_horarios')
@roles_accepted('admin')
def administrar_horarios_page():
    anios = generar_lista_anios()
    return render_template('pages/administrar_horarios_page.html', anios=anios)


@main_blueprint.route('/admin/cargar_horarios/uploader', methods=['POST'])
@roles_accepted('admin')
def administrar_horarios_upload_file():
    f = request.files['file']
    cuatrimestre = request.form['numero_cuatrimestre']
    anio = request.form['anio']
    ruta = 'app/tmp/' + secure_filename('Horarios_' + anio + "_" + cuatrimestre + "C.pdf")
    f.save(ruta)

    csrf_token = request.form['csrf_token']
    response = ClienteAPI().guardar_horarios_PDF(request.cookies, csrf_token, ruta, anio, cuatrimestre)

    if (response == SUCCESS_NO_CONTENT or response == SUCCESS_OK):
        flash(gettext('Los horarios han sido guardados satisfactoriamente'), 'success')
    else:
        flash(response["Error"], 'error')

    return redirect(url_for("main.administrar_horarios_page"))
