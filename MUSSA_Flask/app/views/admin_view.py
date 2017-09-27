from flask import redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_accepted

from app import db
from app.models.user_models import UserProfileForm
from app.models.carreras_models import Carrera

from app.views.base_view import main_blueprint

# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route('/admin')
@roles_accepted('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('pages/admin_page.html')


