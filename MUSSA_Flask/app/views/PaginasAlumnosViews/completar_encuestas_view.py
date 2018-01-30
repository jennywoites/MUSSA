from flask import render_template
from flask_user import login_required
from flask import request, url_for, redirect
from app.views.base_view import main_blueprint
from app.DAO.EncuestasDAO import *
from app.utils import frange, get_numero_dos_digitos, DIAS
from app.ClienteAPI.ClienteAPI import ClienteAPI
from app.API_Rest.codes import *

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
    cliente = ClienteAPI()
    preguntas = cliente.obtener_preguntas_encuesta(cookie, [num_categoria])
    encuesta = cliente.obtener_encuesta_alumno(cookie, idEncuestaAlumno)

    if encuesta["finalizada"]:
        return redirect(url_for('main.historial_encuestas_page'), code=REDIRECTION_FOUND)

    encuesta_esta_completa = cliente.encuesta_alumno_esta_completa(cookie, idEncuestaAlumno)

    respuestas = cliente.obtener_respuestas_encuesta_alumno(cookie, idEncuestaAlumno, preguntas)
    convertir_true_false(respuestas)

    posibles_correlativas = cliente.obtener_todas_las_materias(
        cookie,
        ids_carreras=[encuesta["carrera"]["id_carrera"]]
    )

    for i in range(len(posibles_correlativas)):
        if posibles_correlativas[i]["id_materia"] == encuesta["materia"]["id_materia"]:
            break
    posibles_correlativas.pop(i)

    docentes = ClienteAPI().obtener_docentes_del_curso(cookie, encuesta["curso"]["id_curso"])

    HORA_MIN = 7
    HORA_MAX = 23
    horarios = []
    for i in frange(HORA_MIN, HORA_MAX + 0.5, 0.5):
        hora = int(i)
        minutos = "00" if hora == i else "30"
        horarios.append("{}:{}".format(get_numero_dos_digitos(hora), minutos))

    tematicas = ClienteAPI().obtener_todas_las_tematicas(cookie)

    titulos = [
        {'url': 'main.completar_encuesta_general_page', 'titulo': 'General'},
        {'url': 'main.completar_encuesta_contenido_page', 'titulo': 'Contenido'},
        {'url': 'main.completar_encuesta_clases_page', 'titulo': 'Clases'},
        {'url': 'main.completar_encuesta_examenes_page', 'titulo': 'Exámenes'},
        {'url': 'main.completar_encuesta_docentes_page', 'titulo': 'Docentes'}
    ]

    anterior_siguiente = {
        GRUPO_ENCUESTA_GENERAL: [
            '',
            url_for('main.completar_encuesta_contenido_page', idEncuestaAlumno=idEncuestaAlumno)
        ],
        GRUPO_ENCUESTA_CONTENIDO: [
            url_for('main.completar_encuesta_general_page', idEncuestaAlumno=idEncuestaAlumno),
            url_for('main.completar_encuesta_clases_page', idEncuestaAlumno=idEncuestaAlumno),
        ],
        GRUPO_ENCUESTA_CLASES: [
            url_for('main.completar_encuesta_contenido_page', idEncuestaAlumno=idEncuestaAlumno),
            url_for('main.completar_encuesta_examenes_page', idEncuestaAlumno=idEncuestaAlumno),
        ],
        GRUPO_ENCUESTA_EXAMENES: [
            url_for('main.completar_encuesta_clases_page', idEncuestaAlumno=idEncuestaAlumno),
            url_for('main.completar_encuesta_docentes_page', idEncuestaAlumno=idEncuestaAlumno),
        ],
        GRUPO_ENCUESTA_DOCENTES: [
            url_for('main.completar_encuesta_examenes_page', idEncuestaAlumno=idEncuestaAlumno),
            ''
        ]
    }

    return render_template('pages/completar_encuesta_page.html',
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
                           anterior_siguiente=anterior_siguiente,
                           encuesta_esta_completa=encuesta_esta_completa)


def convertir_true_false(respuestas):
    for idPregunta in respuestas:
        if "respuesta" in respuestas[idPregunta]:
            respuestas[idPregunta]["respuesta"] = 'Si' if respuestas[idPregunta]["respuesta"] else 'No'