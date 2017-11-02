from flask import redirect, render_template
from flask import request, url_for, flash
from flask_user import current_user, login_required, roles_accepted
from werkzeug import secure_filename

from app import db
from app.models.user_models import UserProfileForm

from app.views.base_view import main_blueprint

from app.views.Utils.invocaciones_de_servicios import *

from datetime import datetime

# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route('/admin')
@roles_accepted('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('pages/admin_page.html')


@main_blueprint.route('/admin/administrar_horarios')
@roles_accepted('admin')
def administrar_horarios_page():
    MAX_TIEMPO = 5
    cursos = invocar_buscar_cursos()
    hoy = datetime.now().year
    anios = [x for x in range(hoy, hoy - MAX_TIEMPO, -1)]
    return render_template('pages/administrar_horarios_page.html',
        cursos=cursos,
        anios=anios)


@main_blueprint.route('/admin/administrar_horarios/uploader', methods = ['POST'])
@roles_accepted('admin')
def administrar_horarios_upload_file():
    if request.method == 'POST':
        f = request.files['file']
        ruta = 'app/tmp/' + secure_filename(f.filename)
        f.save(ruta)

        print(request.files)
        #cuatrimestre = request.files['numero_cuatrimestre']
        invocar_guardar_horarios_desde_PDF(ruta, 2)

        flash("Los horarios han sido guardados")
        return redirect(url_for("main.administrar_horarios_page"))