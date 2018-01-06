from flask import redirect, render_template
from flask import request, url_for, flash
from flask_user import current_user, login_required, roles_accepted
from werkzeug import secure_filename
import json
from app import db
from app.models.docentes_models import  Docente
from app.forms import AgregarDocente

from app.views.base_view import main_blueprint

from app.views.Utils.invocaciones_de_servicios import *

from datetime import datetime
from flask_babel import gettext


@main_blueprint.route('/admin/editar_docente/<int:idDocente>')
@roles_accepted('admin')
def editar_docente_page(idDocente):
    form = AgregarDocente()
    return render_template('pages/editar_docente_page.html',
                           form=form,
                           tabla_materias_columnas=json.dumps(form.tabla_materias_columnas),
                           id_docente=idDocente)

@main_blueprint.route('/admin/administrar_docentes')
@roles_accepted('admin')
def administrar_docentes_page():
    columnas_tabla = [
        {
            "field": "id_docente",
            "title": "id_docente",
            "visible": False,
        },
        {
            "field": "apellido",
            "title": "Apellido",
            "sortable": True,
        },
        {
            "field": "nombre",
            "title": "Nombre",
            "sortable": True,
        },
        {
            "field": "materias",
            "title": "Materias que dicta",
            "sortable": True,
        },
        {
            "field": "acciones",
            "title": "Acciones",
            "sortable": True,
            "align": "center"
        },
        {
            "field": "state",
            "checkbox": True,
        }
    ]
    return render_template('pages/administrar_docentes_page.html',
                           tabla_docentes_columnas=columnas_tabla)