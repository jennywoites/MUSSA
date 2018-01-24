from app.models.respuestas_encuesta_models import RespuestaEncuestaAlumno


def filtrar_respuesta_encuesta(filtro):
    query = RespuestaEncuestaAlumno.query.filter_by(encuesta_alumno_id=filtro["idEncuestaAlumno"])

    if "ids_preguntas" in filtro:
        query = query.filter(RespuestaEncuestaAlumno.pregunta_encuesta_id.in_(filtro["ids_preguntas"]))

    query = query.order_by(RespuestaEncuestaAlumno.pregunta_encuesta_id.asc())
    return query.order_by(RespuestaEncuestaAlumno.id.asc()).all()
