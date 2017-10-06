from flask import redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_accepted

from app.views.base_view import main_blueprint

from app.views.paginas_publicas_view import *
from app.views.admin_view import *
from app.views.users_view import *

from app.API_Rest.server import *

from app.models.carreras_models import Carrera

@main_blueprint.route('/test_sql_page')
def test_sql_page():
    carreras = Carrera.query.all()
    return render_template("pages/test_sql_page.html",
                           carreras=carreras)