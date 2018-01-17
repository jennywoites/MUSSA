from app.models.palabras_clave_models import TematicaMateria

def filtrar_tematica_materia(filtros):
    if "id_tematica" in filtros:
        return TematicaMateria.query.get(filtros["id_tematica"])

    query = TematicaMateria.query

    if "tematicas" in filtros:
        query= query.filter_by(TematicaMateria.tematica._in(filtros["tematicas"]))

    if "solo_verificada" in filtros:
        query= query.filter_by(verificada=filtros["solo_verificada"])

    return query.all()