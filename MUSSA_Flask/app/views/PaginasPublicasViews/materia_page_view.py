from app.views.base_view import main_blueprint
from flask import render_template
from flask import request
from app.ClienteAPI.ClienteAPI import ClienteAPI


@main_blueprint.route('/materias/<int:idMateria>', methods=['GET'])
def materia_page(idMateria):
    cookies = request.cookies

    cliente = ClienteAPI()
    materia = cliente.get_materia(cookies, idMateria)
    carreras = cliente.obtener_todas_las_carreras(cookies, materia["codigo"])
    correlativas = cliente.obtener_materias_correlativas(cookies, idMateria)
    cursos = cliente.obtener_cursos_con_filtros(
        cookies,
        codigo_materia=materia["codigo"],
        id_carrera=materia["carrera_id"],
        filtrar_cursos=True
    )

    hay_curso_asterisco = False
    for curso in cursos:
        curso["puntaje"] = "{0:.2f}".format(curso["puntaje"]) if curso["puntaje"] > 0 else 0
        if curso["es_nuevo_curso"] == str(True):
            curso["codigo_curso"] = "* " + curso["codigo_curso"]
            hay_curso_asterisco = True

    return render_template('pages/materia_page.html',
                           materia=materia,
                           carreras=carreras,
                           correlativas=correlativas,
                           cursos=cursos,
                           hay_curso_asterisco=hay_curso_asterisco)
