from flask import render_template
from flask import request
from flask_user import roles_accepted
from app.views.base_view import main_blueprint
from app.utils import frange, get_numero_dos_digitos, DIAS
from app.ClienteAPI.ClienteAPI import ClienteAPI

HORA_MIN = 7
HORA_MAX = 23


@main_blueprint.route('/admin/curso/<int:idCurso>', methods=['GET'])
@roles_accepted('admin')
def modificar_curso_page(idCurso):
    cookies = request.cookies

    cliente = ClienteAPI()
    curso = cliente.get_curso(cookies, idCurso)
    docentes_actuales = cliente.obtener_docentes_del_curso(cookies, idCurso)
    docentes = cliente.obtener_todos_los_docentes(cookies)
    carreras = cliente.obtener_todas_las_carreras(request.cookies)

    carreras_curso = []
    for carrera in carreras:
        activa = "false"
        for c_curso in curso["carreras"]:
            if carrera["codigo"] == c_curso["codigo"]:
                activa = "true"

        carreras_curso.append({
            'id_carrera': carrera["id_carrera"],
            'codigo': carrera["codigo"],
            'nombre': carrera["nombre"],
            'activa': activa
        })

    horarios = []
    for i in frange(HORA_MIN, HORA_MAX + 0.5, 0.5):
        hora = int(i)
        minutos = "00" if hora == i else "30"
        horarios.append("{}:{}".format(get_numero_dos_digitos(hora), minutos))

    return render_template('pages/modificar_curso_page.html',
                           curso=curso,
                           docentes=docentes,
                           docentes_actuales=docentes_actuales,
                           carreras=carreras_curso,
                           dias=DIAS,
                           hora_desde=horarios[:-1],
                           hora_hasta=horarios[1:])
