from app.models.plan_de_estudios_models import EstadoPlanDeEstudios


def generarJSON_plan_de_estudios(plan_de_estudios):
    estado = EstadoPlanDeEstudios.query.get(plan_de_estudios.estado_id)
    fecha = plan_de_estudios.fecha_generacion
    return {
        'id_plan': plan_de_estudios.id,
        'fecha_generacion': "{}/{}/{}".format(fecha.day, fecha.month, fecha.year),
        'estado_id': estado.id,
        'estado_numero': estado.numero,
        'estado': estado.descripcion,
    }
