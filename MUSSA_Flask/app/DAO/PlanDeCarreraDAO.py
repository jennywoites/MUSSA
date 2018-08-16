from app import db
from app.models.plan_de_estudios_models import EstadoPlanDeEstudios

PLAN_EN_CURSO = 0
PLAN_FINALIZADO = 1
PLAN_INCOMPATIBLE = 2

ESTADOS_PLAN = {
    PLAN_EN_CURSO: 'En Curso',
    PLAN_FINALIZADO: 'Finalizado',
    PLAN_INCOMPATIBLE: 'Incompatible'
}


def create_estados_plan_de_estudios():
    db.create_all()

    for num_estado in ESTADOS_PLAN:
        find_o_create_estado_plan(num_estado, ESTADOS_PLAN[num_estado])

    db.session.commit()


def find_o_create_estado_plan(num_estado, descripcion):
    estado = EstadoPlanDeEstudios.query.filter_by(numero=num_estado).first()
    if not estado:
        estado = EstadoPlanDeEstudios(
            numero=num_estado,
            descripcion=descripcion
        )
        db.session.add(estado)

    estado.descripcion = descripcion
    db.session.commit()
