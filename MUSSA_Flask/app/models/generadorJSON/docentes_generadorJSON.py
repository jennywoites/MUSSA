from app.models.docentes_models import CursosDocente
from app.models.carreras_models import Materia, Carrera
from app.models.horarios_models import Curso
from app.models.respuestas_encuesta_models import RespuestaEncuestaDocente, EncuestaAlumno, RespuestaEncuestaAlumno
from app.models.alumno_models import MateriasAlumno


def generarJSON_docente(docente):
    return {
        "id_docente": docente.id,
        "apellido": docente.apellido,
        "nombre": docente.nombre,
        "nombre_completo": docente.obtener_nombre_completo(),
        "materias_que_dicta": generarJSON_materias_docente(docente),
        "materias_que_dictaba_con_encuestas": generarJSON_materias_anteriores_con_encuesta_docente(docente)
    }


def generarJSON_materias_docente(docente):
    materias = []

    cursos_del_docente = CursosDocente.query.filter_by(docente_id=docente.id) \
        .filter_by(eliminado=False).all()
    for c in cursos_del_docente:
        curso = Curso.query.get(c.curso_id)
        materia = Materia.query.filter_by(codigo=curso.codigo_materia).first()
        carrera = Carrera.query.get(materia.carrera_id)
        materias.append({
            "codigo": materia.codigo,
            "nombre": materia.nombre,
            "id_carrera": materia.carrera_id,
            "carrera": carrera.get_descripcion_carrera(),
            "curso": curso.codigo,
            "id_curso": curso.id
        })

    return materias


def generarJSON_materias_anteriores_con_encuesta_docente(docente):
    materias = []

    cursos = []

    cursos_viejos = CursosDocente.query.filter_by(docente_id=docente.id) \
        .filter_by(eliminado=True).all()

    respuestas_docentes = RespuestaEncuestaDocente.query.filter_by(docente_id=docente.id).all()
    for respuesta in respuestas_docentes:
        id_curso = MateriasAlumno.query.get(EncuestaAlumno.query.get(
            RespuestaEncuestaAlumno.query.get(respuesta.rta_encuesta_alumno_id)
                .encuesta_alumno_id).materia_alumno_id).curso_id
        for curso_docente in cursos_viejos:
            if id_curso == curso_docente.curso_id:
                cursos.append(curso_docente)
                break

    for c in cursos:
        curso = Curso.query.get(c.curso_id)
        materia = Materia.query.filter_by(codigo=curso.codigo_materia).first()
        carrera = Carrera.query.get(materia.carrera_id)
        materias.append({
            "codigo": materia.codigo,
            "nombre": materia.nombre,
            "id_carrera": materia.carrera_id,
            "carrera": carrera.get_descripcion_carrera(),
            "curso": curso.codigo,
            "id_curso": curso.id
        })

    return materias
