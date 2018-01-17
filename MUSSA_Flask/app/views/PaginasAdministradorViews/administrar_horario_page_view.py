from flask import redirect, render_template
from flask import request, url_for, flash
from flask_user import roles_accepted
from werkzeug import secure_filename
from app.ClienteAPI.ClienteAPI import ClienteAPI
from app.views.base_view import main_blueprint
from app.views.Utils.invocaciones_de_servicios import *
from datetime import datetime
from flask_babel import gettext


@main_blueprint.route('/admin/administrar_horarios')
@roles_accepted('admin')
def administrar_horarios_page():
    MAX_TIEMPO = 5

    cursos = ClienteAPI().obtener_todos_los_cursos_existentes(request.cookies)

    hoy = datetime.now().year
    anios = [x for x in range(hoy, hoy - MAX_TIEMPO, -1)]
    return render_template('pages/administrar_horarios_page.html',
        cursos=cursos,
        anios=anios)


@main_blueprint.route('/admin/administrar_horarios/uploader', methods = ['POST'])
@roles_accepted('admin')
def administrar_horarios_upload_file():
    f = request.files['file']
    cuatrimestre = request.form['numero_cuatrimestre']
    anio = request.form['anio']
    ruta = 'app/tmp/' + secure_filename('Horarios_' + anio + "_" + cuatrimestre + "C.pdf") 
    f.save(ruta)

    csrf_token = request.form['csrf_token']
    response = invocar_guardar_horarios_desde_PDF(csrf_token, request.cookies, ruta, anio, cuatrimestre)

    if 'OK' in response:
        flash(gettext('Los horarios han sido guardados satisfactoriamente'), 'success')
    else:
        flash(response["Error"], 'error')

    return redirect(url_for("main.administrar_horarios_page"))