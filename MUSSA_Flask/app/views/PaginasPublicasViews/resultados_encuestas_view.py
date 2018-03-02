from app.views.base_view import main_blueprint
from flask import render_template
from flask import request
from app.ClienteAPI.ClienteAPI import ClienteAPI


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

@main_blueprint.route('/materias/encuestas/<int:idCurso>/resultados', methods=['GET'])
def resultados_encuestas_por_curso_todos_los_resultados_page(idCurso):
    return "No implementada"

@main_blueprint.route('/materias/encuestas/<int:idCurso>/resultados/<string:anio>/<int:cuatrimestre>', methods=['GET'])
def resultados_encuestas_por_curso_resultados_para_un_cuatrimestre_page(idCurso, anio, cuatrimestre):
    return "No implementada"