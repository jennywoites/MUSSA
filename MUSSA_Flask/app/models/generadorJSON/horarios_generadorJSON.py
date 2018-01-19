from app.models.carreras_models import Carrera
from app.models.horarios_models import CarreraPorCurso, Horario, HorarioPorCurso
from app.models.docentes_models import Docente, CursosDocente
from app.models.generadorJSON.carreras_generadorJSON import generarJSON_carrera
from app.models.generadorJSON.docentes_generadorJSON import generarJSON_docente


def generarJSON_curso(curso):
    carreras_response = obtener_carreras_response(curso)
    docentes, docentes_response = obtener_docentes_response(curso)
    return generarJSON_curso_con_filtros(curso, carreras_response, docentes, docentes_response)


def generarJSON_curso_con_filtros(curso, carreras_response, docentes, docentes_response):
    return {
        'id_curso': curso.id,
        'codigo_curso': curso.codigo,
        'codigo_materia': curso.codigo_materia,
        'se_dicta_primer_cuatri': curso.se_dicta_primer_cuatrimestre,
        'se_dicta_segundo_cuatri': curso.se_dicta_segundo_cuatrimestre,
        'cuatrimestre': curso.mensaje_cuatrimestre(),
        'carreras': carreras_response,
        'horarios': obtener_horarios_response(curso),
        'docentes': docentes,
        'datos_docentes': docentes_response,
        'puntaje': curso.calcular_puntaje(),
        'cantidad_encuestas_completas': curso.cantidad_encuestas_completas,
        'puntaje_total_encuestas': curso.puntaje_total_encuestas
    }

def obtener_horarios_response(curso):
    horarios_response = []
    horarios_por_curso = HorarioPorCurso.query.filter_by(curso_id=curso.id).all()
    for horario in horarios_por_curso:
        horario_db = Horario.query.get(horario.horario_id)
        horarios_response.append(generarJSON_horario(horario_db))
    return horarios_response

def obtener_carreras_response(curso, idCarrera=None):
    carreras_response = []
    query = CarreraPorCurso.query.filter_by(curso_id=curso.id)

    if idCarrera:
        query = query.filter_by(carrera_id=idCarrera)

    for carrera in query.all():
        carrera_db = Carrera.query.get(carrera.carrera_id)
        carreras_response.append(generarJSON_carrera(carrera_db))

    return carreras_response

def obtener_docentes_response(curso):
    docentes = ""
    docentes_response = []

    docentes_del_curso = CursosDocente.query.filter_by(curso_id=curso.id).all()
    for doc in docentes_del_curso:
        docente_db = Docente.query.get(doc.docente_id)
        docentes += docente_db.obtener_nombre_completo() + "-"
        docentes_response.append(generarJSON_docente(docente_db))
    docentes = docentes[:-1]

    return docentes, docentes_response

def generarJSON_horario(horario):
    return {
        'dia': horario.dia,
        'hora_desde': horario.convertir_hora(horario.hora_desde),
        'hora_hasta': horario.convertir_hora(horario.hora_hasta)
    }
