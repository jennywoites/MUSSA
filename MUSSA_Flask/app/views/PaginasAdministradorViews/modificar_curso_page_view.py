from flask import redirect, render_template
from flask import request, url_for, flash
from flask_user import current_user, login_required, roles_accepted
from werkzeug import secure_filename

from app import db
from app.models.user_models import UserProfileForm

from app.views.base_view import main_blueprint

from app.views.Utils.invocaciones_de_servicios import *

from datetime import datetime
from flask_babel import gettext

from app.utils import frange, get_numero_dos_digitos

HORA_MIN = 7
HORA_MAX = 23

@main_blueprint.route('/admin/curso/<int:idCurso>', methods=['GET'])
@roles_accepted('admin')
def modificar_curso_page(idCurso):
    curso = invocar_buscar_cursos(request.cookies, id_curso=idCurso).pop()
    carreras = invocar_servicio_buscar_carreras(request.cookies)

    carreras_activas = []
    for carrera in curso["carreras"]:
        carreras_activas.append(carrera["codigo"])

    dias = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO"]

    horarios = []
    for i in frange(HORA_MIN, HORA_MAX+0.5, 0.5):
        hora = int(i)
        minutos = "00" if hora == i else "30"
        horarios.append("{}:{}".format(get_numero_dos_digitos(hora), minutos))

    return render_template('pages/modificar_curso_page.html',
                            curso=curso,
                            carreras = carreras,
                            carreras_activas = carreras_activas,
                            dias = dias,
                            hora_desde = horarios[:-1],
                            hora_hasta = horarios[1:])