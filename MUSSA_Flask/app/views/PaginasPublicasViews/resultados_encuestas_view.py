from app.views.base_view import main_blueprint
from flask import render_template
from app.ClienteAPI.ClienteAPI import ClienteAPI
from flask import request, url_for
from app.DAO.EncuestasDAO import *


@main_blueprint.route('/materias/encuestas/<int:idCurso>', methods=['GET'])
def resultados_encuestas_por_curso_page(idCurso):
    cookies = request.cookies
    cliente = ClienteAPI()

    curso = cliente.get_curso(cookies, idCurso)
    materia = cliente.obtener_todas_las_materias(cookies, codigo_materia=curso["codigo_materia"]).pop()
    cuatrimestres_con_encuestas = cliente.get_cuatrimestres_con_resultados_encuesta_para_un_curso(cookies, idCurso)

    return render_template('pages/resultados_encuestas_por_curso_page.html',
                           materia=materia,
                           curso=curso,
                           cuatrimestres_con_encuestas=cuatrimestres_con_encuestas)

#######################################################################################################################
@main_blueprint.route('/docentes/encuestas/<int:idDocente>', methods=['GET'])
def resultados_encuestas_por_docente_page(idDocente):
    return "No implementado"

#######################################################################################################################
@main_blueprint.route('/materias/encuestas/<int:idCurso>/resultados/<string:anio>/<int:cuatrimestre>/general',
                      methods=['GET'])
def resultados_encuestas_por_curso_resultados_para_un_cuatrimestre_general_page(idCurso, anio, cuatrimestre):
    return visualizar_resultados_encuesta(idCurso, anio, cuatrimestre, request.cookies, GRUPO_ENCUESTA_GENERAL)


@main_blueprint.route('/materias/encuestas/<int:idCurso>/resultados/<string:anio>/<int:cuatrimestre>/contenido',
                      methods=['GET'])
def resultados_encuestas_por_curso_resultados_para_un_cuatrimestre_contenido_page(idCurso, anio, cuatrimestre):
    return visualizar_resultados_encuesta(idCurso, anio, cuatrimestre, request.cookies, GRUPO_ENCUESTA_CONTENIDO)


@main_blueprint.route('/materias/encuestas/<int:idCurso>/resultados/<string:anio>/<int:cuatrimestre>/clases',
                      methods=['GET'])
def resultados_encuestas_por_curso_resultados_para_un_cuatrimestre_clases_page(idCurso, anio, cuatrimestre):
    return visualizar_resultados_encuesta(idCurso, anio, cuatrimestre, request.cookies, GRUPO_ENCUESTA_CLASES)


@main_blueprint.route('/materias/encuestas/<int:idCurso>/resultados/<string:anio>/<int:cuatrimestre>/examenes',
                      methods=['GET'])
def resultados_encuestas_por_curso_resultados_para_un_cuatrimestre_examenes_page(idCurso, anio, cuatrimestre):
    return visualizar_resultados_encuesta(idCurso, anio, cuatrimestre, request.cookies, GRUPO_ENCUESTA_EXAMENES)


@main_blueprint.route('/materias/encuestas/<int:idCurso>/resultados/<string:anio>/<int:cuatrimestre>/docentes',
                      methods=['GET'])
def resultados_encuestas_por_curso_resultados_para_un_cuatrimestre_docentes_page(idCurso, anio, cuatrimestre):
    return visualizar_resultados_encuesta(idCurso, anio, cuatrimestre, request.cookies, GRUPO_ENCUESTA_DOCENTES)


#######################################################################################################################

@main_blueprint.route('/materias/encuestas/<int:idCurso>/resultados/general', methods=['GET'])
def resultados_encuestas_por_curso_todos_los_resultados_general_page(idCurso):
    return visualizar_resultados_encuesta(idCurso, '', '', request.cookies, GRUPO_ENCUESTA_GENERAL)


@main_blueprint.route('/materias/encuestas/<int:idCurso>/resultados/contenido', methods=['GET'])
def resultados_encuestas_por_curso_todos_los_resultados_contenido_page(idCurso):
    return visualizar_resultados_encuesta(idCurso, '', '', request.cookies, GRUPO_ENCUESTA_CONTENIDO)


@main_blueprint.route('/materias/encuestas/<int:idCurso>/resultados/clases', methods=['GET'])
def resultados_encuestas_por_curso_todos_los_resultados_clases_page(idCurso):
    return visualizar_resultados_encuesta(idCurso, '', '', request.cookies, GRUPO_ENCUESTA_CLASES)


@main_blueprint.route('/materias/encuestas/<int:idCurso>/resultados/examenes', methods=['GET'])
def resultados_encuestas_por_curso_todos_los_resultados_examenes_page(idCurso):
    return visualizar_resultados_encuesta(idCurso, '', '', request.cookies, GRUPO_ENCUESTA_EXAMENES)


@main_blueprint.route('/materias/encuestas/<int:idCurso>/resultados/docentes', methods=['GET'])
def resultados_encuestas_por_curso_todos_los_resultados_docentes_page(idCurso):
    return visualizar_resultados_encuesta(idCurso, '', '', request.cookies, GRUPO_ENCUESTA_DOCENTES)


#######################################################################################################################

def get_titulos_con_cuatrimestre_especifico(idCurso, anio, cuatrimestre):
    return [
        {'url': url_for('main.resultados_encuestas_por_curso_resultados_para_un_cuatrimestre_general_page',
                        idCurso=idCurso, cuatrimestre=cuatrimestre, anio=anio), 'titulo': 'General'},
        {'url': url_for('main.resultados_encuestas_por_curso_resultados_para_un_cuatrimestre_contenido_page',
                        idCurso=idCurso, cuatrimestre=cuatrimestre, anio=anio), 'titulo': 'Contenido'},
        {'url': url_for('main.resultados_encuestas_por_curso_resultados_para_un_cuatrimestre_clases_page',
                        idCurso=idCurso, cuatrimestre=cuatrimestre, anio=anio), 'titulo': 'Clases'},
        {'url': url_for('main.resultados_encuestas_por_curso_resultados_para_un_cuatrimestre_examenes_page',
                        idCurso=idCurso, cuatrimestre=cuatrimestre, anio=anio), 'titulo': 'Exámenes'},
        {'url': url_for('main.resultados_encuestas_por_curso_resultados_para_un_cuatrimestre_docentes_page',
                        idCurso=idCurso, cuatrimestre=cuatrimestre, anio=anio), 'titulo': 'Docentes'},
    ]


def get_titulos(idCurso):
    return [
        {'url': url_for('main.resultados_encuestas_por_curso_todos_los_resultados_general_page', idCurso=idCurso),
         'titulo': 'General'},
        {'url': url_for('main.resultados_encuestas_por_curso_todos_los_resultados_contenido_page', idCurso=idCurso),
         'titulo': 'Contenido'},
        {'url': url_for('main.resultados_encuestas_por_curso_todos_los_resultados_clases_page', idCurso=idCurso),
         'titulo': 'Clases'},
        {'url': url_for('main.resultados_encuestas_por_curso_todos_los_resultados_examenes_page', idCurso=idCurso),
         'titulo': 'Exámenes'},
        {'url': url_for('main.resultados_encuestas_por_curso_todos_los_resultados_docentes_page', idCurso=idCurso),
         'titulo': 'Docentes'},
    ]


def get_anterior_siguiente_con_cuatrimestre_especifico(idCurso, anio, cuatrimestre):
    return {
        GRUPO_ENCUESTA_GENERAL: [
            '',
            url_for('main.resultados_encuestas_por_curso_resultados_para_un_cuatrimestre_contenido_page',
                    idCurso=idCurso, cuatrimestre=cuatrimestre, anio=anio)
        ],
        GRUPO_ENCUESTA_CONTENIDO: [
            url_for('main.resultados_encuestas_por_curso_resultados_para_un_cuatrimestre_general_page', idCurso=idCurso,
                    cuatrimestre=cuatrimestre, anio=anio),
            url_for('main.resultados_encuestas_por_curso_resultados_para_un_cuatrimestre_clases_page', idCurso=idCurso,
                    cuatrimestre=cuatrimestre, anio=anio),
        ],
        GRUPO_ENCUESTA_CLASES: [
            url_for('main.resultados_encuestas_por_curso_resultados_para_un_cuatrimestre_contenido_page',
                    idCurso=idCurso, cuatrimestre=cuatrimestre, anio=anio),
            url_for('main.resultados_encuestas_por_curso_resultados_para_un_cuatrimestre_examenes_page',
                    idCurso=idCurso, cuatrimestre=cuatrimestre, anio=anio),
        ],
        GRUPO_ENCUESTA_EXAMENES: [
            url_for('main.resultados_encuestas_por_curso_resultados_para_un_cuatrimestre_clases_page', idCurso=idCurso,
                    cuatrimestre=cuatrimestre, anio=anio),
            url_for('main.resultados_encuestas_por_curso_resultados_para_un_cuatrimestre_docentes_page',
                    idCurso=idCurso, cuatrimestre=cuatrimestre, anio=anio),
        ],
        GRUPO_ENCUESTA_DOCENTES: [
            url_for('main.resultados_encuestas_por_curso_resultados_para_un_cuatrimestre_examenes_page',
                    idCurso=idCurso, cuatrimestre=cuatrimestre, anio=anio),
            ''
        ]
    }


def get_anterior_siguiente(idCurso):
    return {
        GRUPO_ENCUESTA_GENERAL: [
            '',
            url_for('main.resultados_encuestas_por_curso_todos_los_resultados_contenido_page', idCurso=idCurso)
        ],
        GRUPO_ENCUESTA_CONTENIDO: [
            url_for('main.resultados_encuestas_por_curso_todos_los_resultados_general_page', idCurso=idCurso),
            url_for('main.resultados_encuestas_por_curso_todos_los_resultados_clases_page', idCurso=idCurso),
        ],
        GRUPO_ENCUESTA_CLASES: [
            url_for('main.resultados_encuestas_por_curso_todos_los_resultados_contenido_page', idCurso=idCurso),
            url_for('main.resultados_encuestas_por_curso_todos_los_resultados_examenes_page', idCurso=idCurso),
        ],
        GRUPO_ENCUESTA_EXAMENES: [
            url_for('main.resultados_encuestas_por_curso_todos_los_resultados_clases_page', idCurso=idCurso),
            url_for('main.resultados_encuestas_por_curso_todos_los_resultados_docentes_page', idCurso=idCurso),
        ],
        GRUPO_ENCUESTA_DOCENTES: [
            url_for('main.resultados_encuestas_por_curso_todos_los_resultados_examenes_page', idCurso=idCurso),
            ''
        ]
    }


def visualizar_resultados_encuesta(idCurso, anio, cuatrimestre, cookies, num_categoria):
    cliente = ClienteAPI()

    curso = cliente.get_curso(cookies, idCurso)
    materia = cliente.obtener_todas_las_materias(cookies, codigo_materia=curso["codigo_materia"]).pop()

    preguntas = cliente.obtener_preguntas_resultados_encuesta(cookies, [num_categoria])

    respuestas = cliente.obtener_repuestas_resultados_encuesta(cookies, idCurso, num_categoria, anio, cuatrimestre)

    titulos = get_titulos(idCurso) if (not cuatrimestre or not anio) else get_titulos_con_cuatrimestre_especifico(
        idCurso, anio, cuatrimestre)

    anterior_siguiente = get_anterior_siguiente(idCurso) if (
        not cuatrimestre or not anio) else get_anterior_siguiente_con_cuatrimestre_especifico(idCurso, anio,
                                                                                              cuatrimestre)

    return render_template('pages/respuestas_encuesta_por_curso_page.html',
                           curso=curso,
                           materia=materia,
                           anio=anio,
                           cuatrimestre=cuatrimestre,
                           titulos=titulos,
                           paso_activo=num_categoria,
                           preguntas=preguntas,
                           respuestas=respuestas,
                           anterior_siguiente=anterior_siguiente)
