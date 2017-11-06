from flask import render_template
from flask_user import roles_accepted
from app.views.base_view import main_blueprint

from app.views.PaginasAdministradorViews.administrar_horario_page_view import administrar_horarios_page, administrar_horarios_upload_file

# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route('/admin')
@roles_accepted('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('pages/admin_page.html')
