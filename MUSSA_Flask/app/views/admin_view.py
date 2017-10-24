from flask import redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_accepted
from werkzeug import secure_filename

from app import db
from app.models.user_models import UserProfileForm
from app.models.carreras_models import Carrera

from app.views.base_view import main_blueprint

# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route('/admin')
@roles_accepted('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('pages/admin_page.html')


@main_blueprint.route('/admin/administrar_horarios')
@roles_accepted('admin')
def administrar_horarios_page():
   return render_template('pages/administrar_horarios_page.html')


@main_blueprint.route('/admin/administrar_horarios/uploader', methods = ['POST'])
@roles_accepted('admin')
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        ruta = 'app/tmp/' + secure_filename(f.filename)
        f.save(ruta)

        #Guardar los horarios que esten en el archivo
        #invocando al servicio correspondiente con la ruta del archivo

        return 'file uploaded successfully'