from app.models.generadorJSON.carreras_generadorJSON import generarJSON_carrera, generarJSON_materia
from app.models.generadorJSON.horarios_generadorJSON import generarJSON_curso
from app.models.carreras_models import Carrera, Materia
from app.models.alumno_models import MateriasAlumno
from app.models.horarios_models import Curso


def generarJSON_encuesta_alumno(encuesta_alumno):
    materiaAlumno = MateriasAlumno.query.get(encuesta_alumno.materia_alumno_id)
    carrera = Carrera.query.get(materiaAlumno.carrera_id)
    curso = Curso.query.get(materiaAlumno.curso_id)
    materia = Materia.query.get(materiaAlumno.materia_id)

    return {
        "id_encuesta_alumno": encuesta_alumno.id,
        "alumno_id": encuesta_alumno.alumno_id,
        "materia_alumno_id": encuesta_alumno.materia_alumno_id,
        "carrera": generarJSON_carrera(carrera),
        "materia": generarJSON_materia(materia),
        "curso": generarJSON_curso(curso),
        "cuatrimestre_aprobacion_cursada": encuesta_alumno.cuatrimestre_aprobacion_cursada,
        "anio_aprobacion_cursada": encuesta_alumno.anio_aprobacion_cursada,
        "fecha_aprobacion": "{}C / {}".format(encuesta_alumno.cuatrimestre_aprobacion_cursada,
                                              encuesta_alumno.anio_aprobacion_cursada),
        "finalizada": encuesta_alumno.finalizada
    }
