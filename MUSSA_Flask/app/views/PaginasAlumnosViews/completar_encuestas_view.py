from flask import render_template
from flask_user import login_required
from flask import request
from app.views.base_view import main_blueprint
from app.views.Utils.invocaciones_de_servicios import *
from app.DAO.EncuestasDAO import *
from app.utils import frange, get_numero_dos_digitos, DIAS


@main_blueprint.route('/encuestas/completar_encuesta/general/<int:idEncuestaAlumno>', methods=['GET'])
@login_required
def completar_encuesta_general_page(idEncuestaAlumno):
    return completar_encuesta(idEncuestaAlumno, request.cookies, GRUPO_ENCUESTA_GENERAL)


@main_blueprint.route('/encuestas/completar_encuesta/contenido/<int:idEncuestaAlumno>', methods=['GET'])
@login_required
def completar_encuesta_contenido_page(idEncuestaAlumno):
    return completar_encuesta(idEncuestaAlumno, request.cookies, GRUPO_ENCUESTA_CONTENIDO)


@main_blueprint.route(
    '/encuestas/completar_encuesta/clases/<int:idEncuestaAlumno>', methods=['GET'])
@login_required
def completar_encuesta_clases_page(idEncuestaAlumno):
    return completar_encuesta(idEncuestaAlumno, request.cookies, GRUPO_ENCUESTA_CLASES)


@main_blueprint.route('/encuestas/completar_encuesta/examenes/<int:idEncuestaAlumno>', methods=['GET'])
@login_required
def completar_encuesta_examenes_page(idEncuestaAlumno):
    return completar_encuesta(idEncuestaAlumno, request.cookies, GRUPO_ENCUESTA_EXAMENES)


@main_blueprint.route('/encuestas/completar_encuesta/docentes/<int:idEncuestaAlumno>', methods=['GET'])
@login_required
def completar_encuesta_docentes_page(idEncuestaAlumno):
    return completar_encuesta(idEncuestaAlumno, request.cookies, GRUPO_ENCUESTA_DOCENTES)


def completar_encuesta(idEncuestaAlumno, cookie, num_categoria):
    preguntas = invocar_servicio_obtener_preguntas_encuesta(cookie, [num_categoria])
    encuesta = invocar_obtener_encuesta_alumno(cookie, idEncuestaAlumno)

    posibles_correlativas = invocar_servicio_buscar_materias(cookie, encuesta["codigo_carrera"])
    # filtrar la materia actual ya que no es correlativa

    docentes = invocar_obtener_docentes_del_curso(cookie, encuesta["id_curso"])

    HORA_MIN = 7
    HORA_MAX = 23
    horarios = []
    for i in frange(HORA_MIN, HORA_MAX + 0.5, 0.5):
        hora = int(i)
        minutos = "00" if hora == i else "30"
        horarios.append("{}:{}".format(get_numero_dos_digitos(hora), minutos))

    titulos = [
        {'url': 'main.completar_encuesta_general_page', 'titulo': 'General'},
        {'url': 'main.completar_encuesta_contenido_page', 'titulo': 'Contenido'},
        {'url': 'main.completar_encuesta_clases_page', 'titulo': 'Clases'},
        {'url': 'main.completar_encuesta_examenes_page', 'titulo': 'Exámenes'},
        {'url': 'main.completar_encuesta_docentes_page', 'titulo': 'Docentes'}
    ]

    return render_template('pages/completar_encuesta_page.html',
                           titulos= titulos,
                           idEncuestaAlumno=idEncuestaAlumno,
                           encuesta = encuesta,
                           paso_activo=num_categoria,
                           preguntas=preguntas,
                           dias=DIAS,
                           hora_desde=horarios[:-1],
                           hora_hasta=horarios[1:],
                           posibles_correlativas=posibles_correlativas,
                           docentes=docentes)
