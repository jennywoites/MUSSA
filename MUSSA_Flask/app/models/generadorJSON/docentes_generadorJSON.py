from app.models.docentes_models import CursosDocente
from app.models.carreras_models import Materia, Carrera
from app.models.horarios_models import Curso


def generarJSON_docente(docente):
    return {
        "id_docente": docente.id,
        "apellido": docente.apellido,
        "nombre": docente.nombre,
        "nombre_completo": docente.obtener_nombre_completo(),
        "materias_que_dicta": generarJSON_materias_docente(docente)
    }


def generarJSON_materias_docente(docente):
    materias = {}

    cursos_del_docente = CursosDocente.query.filter_by(docente_id=docente.id).all()
    for c in cursos_del_docente:
        curso = Curso.query.get(c.curso_id)
        materia = Materia.query.filter_by(codigo=curso.codigo_materia).first()
        carrera = Carrera.query.get(materia.carrera_id)
        materias[materia.codigo] = {
            "nombre": materia.nombre,
            "id_carrera": materia.carrera_id,
            "carrera": carrera.get_descripcion_carrera()
        }

    return materias
