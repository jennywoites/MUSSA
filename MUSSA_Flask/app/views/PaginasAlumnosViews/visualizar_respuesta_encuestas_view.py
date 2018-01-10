from flask import render_template
from flask_user import login_required
from flask import request, url_for
from app.views.base_view import main_blueprint
from app.views.Utils.invocaciones_de_servicios import *
from app.DAO.EncuestasDAO import *
from app.utils import frange, get_numero_dos_digitos, DIAS


@main_blueprint.route('/encuestas/visualizar_encuesta/general/<int:idEncuestaAlumno>', methods=['GET'])
@login_required
def visualizar_encuesta_general_page(idEncuestaAlumno):
    return visualizar_encuesta(idEncuestaAlumno, request.cookies, GRUPO_ENCUESTA_GENERAL)


@main_blueprint.route('/encuestas/visualizar_encuesta/contenido/<int:idEncuestaAlumno>', methods=['GET'])
@login_required
def visualizar_encuesta_contenido_page(idEncuestaAlumno):
    return visualizar_encuesta(idEncuestaAlumno, request.cookies, GRUPO_ENCUESTA_CONTENIDO)


@main_blueprint.route(
    '/encuestas/visualizar_encuesta/clases/<int:idEncuestaAlumno>', methods=['GET'])
@login_required
def visualizar_encuesta_clases_page(idEncuestaAlumno):
    return visualizar_encuesta(idEncuestaAlumno, request.cookies, GRUPO_ENCUESTA_CLASES)


@main_blueprint.route('/encuestas/visualizar_encuesta/examenes/<int:idEncuestaAlumno>', methods=['GET'])
@login_required
def visualizar_encuesta_examenes_page(idEncuestaAlumno):
    return visualizar_encuesta(idEncuestaAlumno, request.cookies, GRUPO_ENCUESTA_EXAMENES)


@main_blueprint.route('/encuestas/visualizar_encuesta/docentes/<int:idEncuestaAlumno>', methods=['GET'])
@login_required
def visualizar_encuesta_docentes_page(idEncuestaAlumno):
    return visualizar_encuesta(idEncuestaAlumno, request.cookies, GRUPO_ENCUESTA_DOCENTES)


def visualizar_encuesta(idEncuestaAlumno, cookie, num_categoria):
    preguntas = invocar_servicio_obtener_preguntas_encuesta(cookie, [num_categoria])
    encuesta = invocar_obtener_encuesta_alumno(cookie, idEncuestaAlumno)

    encuesta_esta_completa = invocar_encuesta_alumno_esta_completa(cookie, idEncuestaAlumno)

    respuestas = invocar_obtener_respuestas_encuesta_alumno(cookie, idEncuestaAlumno, preguntas)
    convertir_true_false(respuestas)

    posibles_correlativas = invocar_servicio_buscar_materias(cookie, encuesta["codigo_carrera"])
    for i in range(len(posibles_correlativas)):
        if posibles_correlativas[i]["id"] == encuesta["materia_id"]:
            break
    posibles_correlativas.pop(i)

    docentes = invocar_obtener_docentes_del_curso(cookie, encuesta["id_curso"])

    HORA_MIN = 7
    HORA_MAX = 23
    horarios = []
    for i in frange(HORA_MIN, HORA_MAX + 0.5, 0.5):
        hora = int(i)
        minutos = "00" if hora == i else "30"
        horarios.append("{}:{}".format(get_numero_dos_digitos(hora), minutos))

    tematicas = invocar_obtener_tematicas_materias(cookie)

    titulos = [
        {'url': 'main.visualizar_encuesta_general_page', 'titulo': 'General'},
        {'url': 'main.visualizar_encuesta_contenido_page', 'titulo': 'Contenido'},
        {'url': 'main.visualizar_encuesta_clases_page', 'titulo': 'Clases'},
        {'url': 'main.visualizar_encuesta_examenes_page', 'titulo': 'Exámenes'},
        {'url': 'main.visualizar_encuesta_docentes_page', 'titulo': 'Docentes'}
    ]

    anterior_siguiente = {
        GRUPO_ENCUESTA_GENERAL: [
            '',
            url_for('main.visualizar_encuesta_contenido_page', idEncuestaAlumno=idEncuestaAlumno)
        ],
        GRUPO_ENCUESTA_CONTENIDO: [
            url_for('main.visualizar_encuesta_general_page', idEncuestaAlumno=idEncuestaAlumno),
            url_for('main.visualizar_encuesta_clases_page', idEncuestaAlumno=idEncuestaAlumno),
        ],
        GRUPO_ENCUESTA_CLASES: [
            url_for('main.visualizar_encuesta_contenido_page', idEncuestaAlumno=idEncuestaAlumno),
            url_for('main.visualizar_encuesta_examenes_page', idEncuestaAlumno=idEncuestaAlumno),
        ],
        GRUPO_ENCUESTA_EXAMENES: [
            url_for('main.visualizar_encuesta_clases_page', idEncuestaAlumno=idEncuestaAlumno),
            url_for('main.visualizar_encuesta_docentes_page', idEncuestaAlumno=idEncuestaAlumno),
        ],
        GRUPO_ENCUESTA_DOCENTES: [
            url_for('main.visualizar_encuesta_examenes_page', idEncuestaAlumno=idEncuestaAlumno),
            ''
        ]
    }

    return render_template('pages/visualizar_encuesta_page.html',
                           titulos=titulos,
                           idEncuestaAlumno=idEncuestaAlumno,
                           encuesta=encuesta,
                           paso_activo=num_categoria,
                           preguntas=preguntas,
                           respuestas=respuestas,
                           dias=DIAS,
                           hora_desde=horarios[:-1],
                           hora_hasta=horarios[1:],
                           posibles_correlativas=posibles_correlativas,
                           docentes=docentes,
                           tematicas=tematicas,
                           anterior_siguiente=anterior_siguiente)

def convertir_true_false(respuestas):
    for idPregunta in respuestas:
        if "respuesta" in respuestas[idPregunta]:
            respuestas[idPregunta]["respuesta"] = 'Si' if respuestas[idPregunta]["respuesta"] else 'No'