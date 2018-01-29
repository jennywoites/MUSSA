from app.models.carreras_models import Carrera, Materia
from app.models.alumno_models import EstadoMateria, FormaAprobacionMateria
from app.models.docentes_models import Docente, CursosDocente
from app.models.horarios_models import Curso


def generarJSON_alumno(alumno):
    return {
        "padron": alumno.padron
    }

def generarJSON_materia_alumno(materia_alumno):
    materia_carrera = Materia.query.get(materia_alumno.materia_id)
    carrera = Carrera.query.get(materia_alumno.carrera_id)

    return {
        'id_materia_alumno': materia_alumno.id,
        'id_materia': materia_carrera.id,
        'codigo': materia_carrera.codigo,
        'nombre': materia_carrera.nombre,
        'id_carrera': carrera.id,
        'id_curso': materia_alumno.curso_id if materia_alumno.curso_id else '-1',
        'carrera': carrera.get_descripcion_carrera(),
        'curso': get_curso(materia_alumno),
        'estado': EstadoMateria.query.get(materia_alumno.estado_id).estado,
        'aprobacion_cursada': get_aprobacion_cursada(materia_alumno),
        'calificacion': materia_alumno.calificacion if materia_alumno.calificacion else "-",
        'fecha_aprobacion': get_fecha_aprobacion(materia_alumno),
        'acta_o_resolucion': materia_alumno.acta_o_resolucion if materia_alumno.acta_o_resolucion else "-",
        'forma_aprobacion_materia': get_forma_aprobacion_materia(materia_alumno)
    }

def get_fecha_aprobacion(materia_alumno):
    if not materia_alumno.fecha_aprobacion:
        return "-"

    anio, mes, dia = str(materia_alumno.fecha_aprobacion).split(" ")[0].split("-")
    return "{}/{}/{}".format(dia, mes, anio)


def get_forma_aprobacion_materia(materia_alumno):
    if not materia_alumno.forma_aprobacion_id:
        return "-"

    return FormaAprobacionMateria.query.get(materia_alumno.forma_aprobacion_id).forma


def get_aprobacion_cursada(materia_alumno):
    if not (materia_alumno.cuatrimestre_aprobacion_cursada and materia_alumno.anio_aprobacion_cursada):
        return "-"

    return materia_alumno.cuatrimestre_aprobacion_cursada + "C / " + materia_alumno.anio_aprobacion_cursada


def get_curso(materia_alumno):
    if not materia_alumno.curso_id:
        return "Sin designar"

    curso_elegido = Curso.query.get(materia_alumno.curso_id)
    docentes = ""
    for curso_docente in CursosDocente.query.filter_by(curso_id=curso_elegido.id).all():
        docente = Docente.query.get(curso_docente.docente_id)
        docentes += docente.obtener_nombre_completo() + "-"
    return "{} | {}".format(curso_elegido.codigo, docentes[:-1])
