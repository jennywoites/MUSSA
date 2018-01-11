from app.views.base_view import main_blueprint
from flask import render_template


@main_blueprint.route('/comisiones_por_carrera')
def comisiones_por_carrera_page():
    comisiones = [
        {
            "NOMBRE": "Casa Informática",
            "CARRERAS": [
                "Ingeniería en Informática",
                "Licenciatura en Análisis de Sistemas"
            ],
            "LINKS": [
                ('Lista de Correo', 'https://groups.google.com/forum/#!forum/casainformatica'),
                ('Facebook', 'https://groups.google.com/forum/#!forum/casainformatica'),
            ]
        },
        {
            "NOMBRE": "ComElec",
            "CARRERAS": [
                "Ingeniería en Electrónica"
            ],
            "LINKS": [
                ('Lista de Correo', 'https://groups.google.com/forum/#!forum/comelec'),
                ('Página Web', 'https://sites.google.com/view/comelecfiuba/p%C3%A1gina-principal'),
            ]
        }
    ]
    return render_template('pages/comisiones_por_carrera_page.html',
                           comisiones=comisiones)
