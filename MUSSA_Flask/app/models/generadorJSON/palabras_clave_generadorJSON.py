
def generarJSON_tematica_materia(tematica):
    return {
        "id_tematica": tematica.id,
        "tematica": tematica.tematica,
        "verificada": tematica.verificada
    }
