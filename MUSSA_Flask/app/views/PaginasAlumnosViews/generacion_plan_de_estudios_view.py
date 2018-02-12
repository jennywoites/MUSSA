from flask import render_template
from flask_user import login_required
from flask import request
from app.views.base_view import main_blueprint
from app.ClienteAPI.ClienteAPI import ClienteAPI
from app.utils import DIAS, generar_lista_horarios, generar_lista_anios
from app.DAO.MateriasDAO import FINAL_PENDIENTE
from datetime import datetime


@main_blueprint.route('/planes_de_estudio', methods=['GET'])
@login_required
def planes_de_estudios_page():
    cookies = request.cookies
    cliente = ClienteAPI()

    planes = cliente.obtener_planes_de_estudio_alumno(cookies)

    return render_template('pages/planes_de_estudio_page.html', planes=planes)


@main_blueprint.route('/planes_de_estudio/nuevo_plan', methods=['GET'])
@login_required
def nuevo_plan_de_estudios_page():
    cookies = request.cookies
    cliente = ClienteAPI()

    hoy = datetime.today()
    primer_cuatri_valido = 1 if hoy.month <= 7 else 2

    mis_carreras = cliente.obtener_carreras_alumno(cookies)
    horarios = generar_lista_horarios()
    tematicas = cliente.obtener_todas_las_tematicas(cookies)
    anios = generar_lista_anios()

    materias_con_final_pendiente = cliente.obtener_materias_alumno(cookies, [FINAL_PENDIENTE])

    return render_template('pages/generar_plan_de_estudios_page.html',
                           carreras=mis_carreras,
                           dias=DIAS,
                           hora_desde=horarios[:-1],
                           hora_hasta=horarios[1:],
                           tematicas=tematicas,
                           anios=anios,
                           materias_con_final_pendiente=materias_con_final_pendiente,
                           primer_cuatri_valido=primer_cuatri_valido
                           )

@main_blueprint.route('/planes_de_estudio/mis_planes/<int:idPlanEstudios>', methods=['GET'])
@login_required
def visualizar_plan_de_estudios_page(idPlanEstudios):
    cookies = request.cookies
    cliente = ClienteAPI()

    return "No se ha implementado esta pagina"
