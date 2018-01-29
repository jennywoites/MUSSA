from flask import render_template
from flask_user import roles_accepted
from app.forms import AgregarDocente
from app.views.base_view import main_blueprint
import json


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
