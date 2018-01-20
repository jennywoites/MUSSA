from app.models.carreras_models import TipoMateria


def generarJSON_carrera(carrera):
    return {
        'id_carrera': carrera.id,
        'codigo': carrera.codigo,
        'nombre': carrera.nombre,
        'plan': carrera.plan,
        'descripcion': carrera.get_descripcion_carrera()
    }


def generarJSON_materia(materia):
    return {
        "id_materia": materia.id,
        "codigo": materia.codigo,
        "nombre": materia.nombre,
        "objetivos": materia.objetivos,
        "creditos": materia.creditos,
        "creditos_minimos_para_cursarla": materia.creditos_minimos_para_cursarla,
        "tipo_materia_id": materia.tipo_materia_id,
        "tipo_materia": TipoMateria.query.get(materia.tipo_materia_id).descripcion,
        "carrera_id": materia.carrera.id,
        "carrera": materia.carrera.get_descripcion_carrera()
    }