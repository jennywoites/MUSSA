import os
from app.models.horarios_models import HorariosYaCargados, Curso, AjustadoCursoModelosI, HorarioPorCurso, Horario, \
    CarreraPorCurso
from app.API_Rest.Services.CursoServices.HorariosPDFService import HorariosPDFService
from app.models.docentes_models import CursosDocente
from app import db
from app.utils import MIERCOLES, JUEVES


def create_horarios_y_cursos_desde_PDF():
    servicio = HorariosPDFService()

    DIR_HORARIOS = os.path.join('..', 'PlanesdeEstudio', 'Horarios')

    # Los nombres de archivo estan ordenados de mas viejo a mas nuevo con el formato:
    # Horario_anio_cuatrimestre.pdf
    # Por ejemplo, el Horario_2017_2.pdf corresponde al horario del año 2017, 2º cuatrimestre
    for archivo in sorted(os.listdir(DIR_HORARIOS)):
        ruta, extension = archivo.split('.')
        horarios, anio, cuatrimestre = ruta.split('_')

        # Si ya fue cargado el cuatrimestre, no lo cargo nuevamente
        if HorariosYaCargados.query.filter_by(anio=anio).filter_by(cuatrimestre=cuatrimestre).first():
            continue

        ruta = os.path.join(DIR_HORARIOS, archivo)
        servicio.generar_horarios_desde_PDF(ruta, cuatrimestre, anio)

    # FIXME: Eliminar esto cuando se encuentre una mejor forma de lidiar con la materia de Modelos I que tiene horarios opcionales
    if not AjustadoCursoModelosI.query.first():
        ajustar_horarios_materia_modelos_1()


def ajustar_horarios_materia_modelos_1():
    CODIGO_MODELOS_1 = '7114'
    cursos_a_duplicar = Curso.query.filter_by(codigo_materia=CODIGO_MODELOS_1).all()
    for curso in cursos_a_duplicar:
        nuevo_curso = Curso(
            codigo_materia=curso.codigo_materia,
            codigo=curso.codigo + 'OpTeorica2',
            se_dicta_primer_cuatrimestre=curso.se_dicta_primer_cuatrimestre,
            se_dicta_segundo_cuatrimestre=curso.se_dicta_segundo_cuatrimestre,
            cantidad_encuestas_completas=curso.cantidad_encuestas_completas,
            puntaje_total_encuestas=curso.puntaje_total_encuestas,
            fecha_actualizacion=curso.fecha_actualizacion,
            primer_cuatrimestre_actualizado=curso.primer_cuatrimestre_actualizado,
            segundo_cuatrimestre_actualizado=curso.segundo_cuatrimestre_actualizado
        )
        db.session.add(nuevo_curso)
        db.session.commit()

        for carrera_curso in CarreraPorCurso.query.filter_by(curso_id=curso.id).all():
            db.session.add(CarreraPorCurso(
                curso_id=nuevo_curso.id,
                carrera_id=carrera_curso.carrera_id
            ))
            db.session.commit()

        for docente_curso in CursosDocente.query.filter_by(curso_id=curso.id).all():
            db.session.add(CursosDocente(
                curso_id=nuevo_curso.id,
                docente_id=docente_curso.docente_id
            ))
            db.session.commit()

        horarios = HorarioPorCurso.query.filter_by(curso_id=curso.id).filter_by(es_horario_activo=True).all()
        for horario_por_curso in horarios:
            horario_a_copiar = Horario.query.get(horario_por_curso.horario_id)

            # Si el horario es el de la torica obligatoria de MIERCOLES de 18:30 a 21:30 no lo copio en el nuevo horario
            if (horario_a_copiar.dia == MIERCOLES and
                        horario_a_copiar.hora_desde == '18.5' and horario_a_copiar.hora_hasta == '21.5'):
                continue

            nuevo_horario = Horario(
                dia=horario_a_copiar.dia,
                hora_desde=horario_a_copiar.hora_desde,
                hora_hasta=horario_a_copiar.hora_hasta
            )
            db.session.add(nuevo_horario)
            db.session.commit()

            db.session.add(HorarioPorCurso(
                curso_id=nuevo_curso.id,
                horario_id=nuevo_horario.id,
                es_horario_activo=True,
                fecha_actualizacion=horario_por_curso.fecha_actualizacion
            ))

            # Si el horario es el de la torica obligatoria de los JUEVES de 09:00 a 11:30 lo elimino del horario viejo
            # (lo marco como no activo)
            if (horario_a_copiar.dia == JUEVES and
                        horario_a_copiar.hora_desde == '9' and horario_a_copiar.hora_hasta == '11.5'):
                horario_por_curso.es_horario_activo = False

            db.session.commit()

        curso.codigo = curso.codigo + 'OpTeorica1'
        db.session.commit()

    db.session.add(AjustadoCursoModelosI(actualizado=True))
    db.session.commit()
