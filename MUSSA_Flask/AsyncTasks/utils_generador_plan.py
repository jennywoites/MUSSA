from app import db
from app.models.plan_de_estudios_models import EstadoPlanDeEstudios, MateriaPlanDeEstudios
from app.models.carreras_models import Materia
from datetime import datetime

def actualizar_plan(plan_de_estudios, nuevo_estado):
    estado = EstadoPlanDeEstudios.query.filter_by(numero=nuevo_estado).first()

    plan_de_estudios.fecha_ultima_actualizacion = datetime.today()
    plan_de_estudios.estado_id = estado.id

    db.session.commit()

def agregar_materia_al_plan(plan_de_estudios, id_materia, id_curso, cuatrimestre):
    materia_plan = MateriaPlanDeEstudios(
        plan_estudios_id=plan_de_estudios.id,
        materia_id=id_materia,
        orden=cuatrimestre
    )

    if id_curso:
        materia_plan.curso_id = id_curso

    db.session.add(materia_plan)
    db.session.commit()

def agregar_materias_CBC_al_plan_generado(parametros):
    if not parametros.materias_CBC_pendientes:
        return

    grupos_CBC = []
    grupo_actual = {}
    for index, id_materia in enumerate(parametros.materias_CBC_pendientes):
        materia = Materia.query.get(id_materia)
        grupo_actual[materia.codigo] = {
            "id_materia": materia.id,
            "id_curso": None
        }
        if (index + 1) % 3 == 0:
            grupos_CBC.append(grupo_actual)
            grupo_actual = {}

    if grupo_actual: #En caso de tener menos materias por cuatrimestre
        grupos_CBC.append(grupo_actual)

    for i in range(len(grupos_CBC)-1,-1,-1):
        grupo_cuatrimestre = grupos_CBC[i]
        parametros.plan_generado.insert(0, grupo_cuatrimestre)

def agregar_materias_generadas_al_plan(parametros, plan_de_estudios):
    agregar_materias_CBC_al_plan_generado(parametros)

    for cuatrimestre, grupo_materias in enumerate(parametros.plan_generado):
        for cod_materia in grupo_materias:
            id_materia = grupo_materias[cod_materia]["id_materia"]
            id_curso = grupo_materias[cod_materia]["id_curso"]
            agregar_materia_al_plan(plan_de_estudios, id_materia, id_curso, cuatrimestre)