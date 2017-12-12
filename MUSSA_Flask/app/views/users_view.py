from flask import redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_accepted
from app.models.user_models import UserProfileForm
from app.views.base_view import main_blueprint

from app.views.PaginasAlumnosViews.datos_academicos_page_view import datos_academicos_page
from app.views.PaginasAlumnosViews.agregar_materia_page_view import agregar_materia_page
from app.views.PaginasAlumnosViews.editar_materia_page_view import editar_materia_page
from app.views.PaginasAlumnosViews.completar_encuestas_view import *
from app.views.PaginasAlumnosViews.historial_encuestas_page_view import historial_encuestas_page


@main_blueprint.route('/member')
@login_required
def member_page():
    return render_template('pages/home_page.html')


@main_blueprint.route('/pages/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.home_page'))

    # Process GET or invalid POST
    return render_template('pages/user_profile_page.html',
                           form=form)
