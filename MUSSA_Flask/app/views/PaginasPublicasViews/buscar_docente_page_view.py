from app.views.base_view import main_blueprint
from flask import render_template


@main_blueprint.route('/buscar_docentes', methods=['GET'])
def buscar_docentes_page():
    return render_template('pages/buscar_docentes_page.html')
