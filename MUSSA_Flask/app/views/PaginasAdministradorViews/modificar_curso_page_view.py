from flask import redirect, render_template
from flask import request, url_for, flash
from flask_user import current_user, login_required, roles_accepted
from app.views.base_view import main_blueprint
from app.views.Utils.invocaciones_de_servicios import *
from app.utils import frange, get_numero_dos_digitos, DIAS
from app.ClienteAPI.ClienteAPI import ClienteAPI

HORA_MIN = 7
HORA_MAX = 23

@main_blueprint.route('/admin/curso/<int:idCurso>', methods=['GET'])
@roles_accepted('admin')
def modificar_curso_page(idCurso):
    client = ClienteAPI()

    cookies = request.cookies
    curso = invocar_buscar_cursos(cookies, id_curso=idCurso).pop()
    docentes_actuales = invocar_obtener_docentes_del_curso(cookies, idCurso)
    docentes = client.obtener_todos_los_docentes(cookies)
    carreras = invocar_servicio_buscar_carreras(cookies)

    carreras_curso = []
    for carrera in carreras:
        activa = "false"
        for c_curso in curso["carreras"]:
            if carrera["codigo"] == c_curso["codigo"]:
                activa = "true"

        carreras_curso.append({
            'id': carrera["id"],
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
                           docentes = docentes,
                           docentes_actuales=docentes_actuales,
                           carreras=carreras_curso,
                           dias=DIAS,
                           hora_desde=horarios[:-1],
                           hora_hasta=horarios[1:])
