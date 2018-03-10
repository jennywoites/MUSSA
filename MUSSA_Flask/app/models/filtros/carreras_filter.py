from app.models.carreras_models import Carrera, Materia
from app.models.palabras_clave_models import PalabrasClaveParaMateria, PalabraClave


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


def filtrar_materia(filtros):
    query = Materia.query

    if "codigo" in filtros:
        query = query.filter(Materia.codigo.like(filtros["codigo"] + "%"))

    if "nombre" in filtros:
        query = query.filter(Materia.nombre.like("%" + filtros["nombre"] + "%"))

    if "ids_carreras" in filtros:
        query = query.filter(Materia.carrera.has(Carrera.id.in_(filtros["ids_carreras"])))

    if "palabras_clave" in filtros:
        query_ids_materias_con_palabras = PalabrasClaveParaMateria.query \
            .with_entities(PalabrasClaveParaMateria.materia_id) \
            .filter(PalabrasClaveParaMateria.palabra_clave_id.in_(
            PalabraClave.query.with_entities(PalabraClave.id)
                .filter(PalabraClave.palabra.in_(filtros["palabras_clave"]))
        ))
        query = query.filter(Materia.id.in_(query_ids_materias_con_palabras))

    return query.order_by(Materia.codigo.asc()).all()
