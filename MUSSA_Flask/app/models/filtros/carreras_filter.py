from app.models.carreras_models import Carrera, Materia


def filtrar_carrera(filtros):
    if "id_carrera" in filtros:
        return Carrera.query.get(filtros["id_carrera"])

    query = Carrera.query

    if "codigo" in filtros:
        query = query.filter_by(codigo=(filtros["codigo"]))

    if "nombre" in filtros:
        query = query.filter_by(nombre=(filtros["nombre"]))

    if "codigo_materia" in filtros:
        query = query.join(Carrera.materias).filter(Materia.codigo == filtros["codigo_materia"])

    query = query.order_by(Carrera.codigo.asc()).order_by(Carrera.plan.desc())

    return query.all()
