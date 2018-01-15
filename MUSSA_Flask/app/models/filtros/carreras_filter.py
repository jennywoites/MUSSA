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
        materias = Materia.query.filter_by(codigo=filtros["codigo_materia"]).all()
        l_ids = [materia.id for materia in materias]
        query = query.filter_by(Carrera.materias.in_(l_ids))

    query = query.order_by(Carrera.codigo.asc()).order_by(Carrera.plan.desc())

    return query.all()
