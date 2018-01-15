
def generarJSON_carrera(carrera):
    return {
        'id_carrera': carrera.id,
        'codigo': carrera.codigo,
        'nombre': carrera.nombre,
        'plan': carrera.plan
    }
