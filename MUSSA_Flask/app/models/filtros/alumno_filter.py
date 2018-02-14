from app.models.alumno_models import MateriasAlumno
from app.DAO.MateriasDAO import *


def filtrar_materias_alumno(filtro):
    query = MateriasAlumno.query.filter_by(alumno_id=filtro["id_alumno"])

    if "id_carrera" in filtro:
        query = query.filter_by(carrera_id=filtro["id_carrera"])

    if "estados" in filtro:
        ids_estados = []
        for cod_estado in filtro["estados"]:
            texto = ESTADO_MATERIA[int(cod_estado)]
            estado = EstadoMateria.query.filter_by(estado=texto).first()
            ids_estados.append(estado.id)

        query = query.filter(MateriasAlumno.estado_id.in_(ids_estados))

    if "ids_a_excluir" in filtro:
        query = query.filter(~MateriasAlumno.id.in_(filtro["ids_a_excluir"]))

    return query.all()
