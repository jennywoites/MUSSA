from app.models.carreras_models import TipoMateria, Creditos


def generarJSON_carrera(carrera):
    return {
        'id_carrera': carrera.id,
        'codigo': carrera.codigo,
        'nombre': carrera.nombre,
        'plan': carrera.plan,
        'descripcion': carrera.get_descripcion_carrera(),
        'orientaciones': generarJSON_orientaciones(carrera.orientaciones.all()),
        'trabajos_finales_carrera': generarJSON_trabajo_final_carrera(carrera)
    }


def generarJSON_trabajo_final_carrera(carrera):
    creditos = Creditos.query.get(carrera.id)
    trabajos = []

    if creditos.creditos_tesis > 0:
        trabajos.append({
            "codigo": "TESIS",
            "descripcion": "Tesis"
        })

    if creditos.creditos_tesis > 0:
        trabajos.append({
            "codigo": "TP_PROFESIONAL",
            "descripcion": "Trabajo Profesional"
        })

    return trabajos


def generarJSON_orientaciones(orientaciones):
    json_orientaciones = []
    for orientacion in orientaciones:
        json_orientaciones.append({
            "descripcion": orientacion.descripcion,
            "clave_reducida": orientacion.clave_reducida
        })
    return json_orientaciones


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
