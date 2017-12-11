from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request
from flask_user import roles_accepted

from app import db
from app.models.carreras_models import Carrera, Materia
from app.models.horarios_models import Curso, Horario, HorarioPorCurso, CarreraPorCurso, HorariosYaCargados
from app.models.docentes_models import Docente, CursosDocente

import logging

from app.API_Rest.GeneradorPlanCarreras.ParserHorarios import parsear_pdf

import datetime


class GuardarHorariosDesdeArchivoPDF(Resource):
    @roles_accepted('admin')
    def post(self):
        logging.info('Se invoco al servicio Gurdar Horarios Desde Archivo PDF')

        args = request.form

        q_ruta = args["ruta"] if "ruta" in args else None
        q_cuatrimestre = args["cuatrimestre"] if "cuatrimestre" in args else None
        q_anio = args["anio"] if "anio" in args else None

        if not q_ruta or not q_cuatrimestre or not q_anio:
            logging.error(
                'El servicio Gurdar Horarios Desde Archivo PDF recibe la ruta del archivo, el cuatrimestre  el año al que pertenece')
            return {
                       'Error': 'Este servicio debe recibir la ruta del archivo, el cuatrimestre y el año al que pertenece'}, CLIENT_ERROR_BAD_REQUEST

        if self.horario_fue_cargado_anteriormente(q_anio, q_cuatrimestre):
            logging.error('Este horario ya fue cargado anteriormente: {} - {}C'.format(q_anio, q_cuatrimestre))
            return {'Error': 'Este horario ya fue cargado anteriormente'}, CLIENT_ERROR_CONFLICT

        if self.ya_hay_horarios_nuevos_cargados(q_anio, q_cuatrimestre):
            logging.error('Este es un horario viejo. Ya hay horarios nuevos cargados en el sistema.')
            return {
                       'Error': 'Este es un horario viejo. Ya hay horarios nuevos cargados en el sistema.'}, CLIENT_ERROR_CONFLICT

        horarios_pdf = parsear_pdf(q_ruta)

        fecha_actualizacion = datetime.datetime.now()

        self.guardar_horarios_pdf(horarios_pdf, q_cuatrimestre, fecha_actualizacion)

        self.guardar_ultima_actualizacion_horarios(q_cuatrimestre, q_anio, fecha_actualizacion)

        result = ({'OK': 'Los horarios fueron cargados correctamente'}, SUCCESS_OK)
        logging.info('Gurdar Horarios Desde Archivo PDF devuelve como resultado: {}'.format(result))
        return result

    def guardar_horarios_pdf(self, horarios_pdf, cuatrimestre, fecha_actualizacion):
        carreras_en_sistema = []
        for carrera in Carrera.query.all():
            carreras_en_sistema.append(carrera.codigo)

        for horario_pdf in horarios_pdf:
            carreras = self.filtrar_solo_carreras_en_sistema(carreras_en_sistema, horario_pdf["Carreras"])
            if not carreras:
                logging.info("Este horario no se procesa: {}".format(horario_pdf))
                continue
            docentes = horario_pdf["Docentes"]
            nombre_curso = horario_pdf["Curso"]
            codigo_materia = horario_pdf["Codigo"]
            horarios_materia = horario_pdf["Horarios"]

            self.find_or_create_curso(nombre_curso, codigo_materia, docentes, carreras,
                                      horarios_materia, cuatrimestre, fecha_actualizacion)

            db.session.commit()

    def find_or_create_curso(self, nombre_curso, codigo_materia, docentes, carreras,
                             horarios_materia, cuatrimestre, fecha_actualizacion):

        # Si la materia no existe, el curso es de una materia no registrada en el sistema
        # (por ejemplo, porque la carrera aun no se ha habilitado) y no tiene sentido
        # guardar dicho curso
        if not Materia.query.filter_by(codigo=codigo_materia).first():
            return

        curso = Curso.query.filter_by(codigo_materia=codigo_materia).filter_by(codigo=nombre_curso).first()

        if not curso:
            curso = self.crear_curso(nombre_curso, codigo_materia, docentes, horarios_materia)

        if cuatrimestre == 1 or cuatrimestre == '1':
            curso.se_dicta_primer_cuatrimestre = True
        else:
            curso.se_dicta_segundo_cuatrimestre = True

        curso.fecha_actualizacion = fecha_actualizacion
        self.agregar_carreras_al_curso(curso, carreras)

    def agregar_carreras_al_curso(self, curso, carreras):
        for codigo in carreras:
            carrera_db = Carrera.query.filter_by(codigo=codigo).first()

            query = CarreraPorCurso.query.filter_by(curso_id=curso.id)
            carrera_por_curso = query.filter_by(carrera_id=carrera_db.id).first()

            if carrera_por_curso:
                continue

            carrera_por_curso = CarreraPorCurso(
                curso_id=curso.id,
                carrera_id=carrera_db.id
            )
            db.session.add(carrera_por_curso)

    def crear_curso(self, nombre_curso, codigo_materia, docentes, horarios_materia):
        curso = Curso(
            codigo_materia=codigo_materia,
            codigo=nombre_curso,
            cantidad_encuestas_completas=0,
            puntaje_total_encuestas=0
        )
        db.session.add(curso)

        self.crear_horario(curso, horarios_materia)
        self.asignar_docentes(curso, docentes)

        return curso

    def crear_horario(self, curso, horarios_materia):
        horarios_materia = self.concatenar_horarios(horarios_materia)

        for horario_pdf in horarios_materia:
            horario = Horario(
                dia=horario_pdf[0],
                hora_desde=horario_pdf[1],
                hora_hasta=horario_pdf[2]
            )
            db.session.add(horario)
            db.session.commit()

            horario_por_curso = HorarioPorCurso(
                curso_id=curso.id,
                horario_id=horario.id
            )
            db.session.add(horario_por_curso)

    def concatenar_horarios(self, horarios_materia):
        concatenados = []
        pares = []
        for i in range(len(horarios_materia)):
            if i in concatenados:
                continue
            horario_pdf_i = horarios_materia[i]
            dia_i = horario_pdf_i[0]
            for j in range(i + 1, len(horarios_materia)):
                if j in concatenados:
                    continue
                horario_pdf_j = horarios_materia[j]
                dia_j = horario_pdf_j[0]
                if dia_i == dia_j:
                    if horario_pdf_i[2] == horario_pdf_j[1]:
                        concatenados.append(i)
                        concatenados.append(j)
                        pares.append((i, j))

        horarios = []
        for i in range(len(horarios_materia)):
            if i not in concatenados:
                horarios.append(horarios_materia[i])

        for i, j in pares:
            horario_i = horarios_materia[i]
            horario_j = horarios_materia[j]
            horarios.append([horario_i[0], horario_i[1], horario_j[2]])

        return horarios

    def filtrar_solo_carreras_en_sistema(self, carreras_en_sistema, carreras_pdf):
        carreras = []
        for carrera in carreras_pdf:
            if str(carrera) in carreras_en_sistema:
                carreras.append(carrera)
        return carreras

    def horario_fue_cargado_anteriormente(self, anio, cuatrimestre):
        query = HorariosYaCargados.query.filter_by(anio=anio).filter_by(cuatrimestre=cuatrimestre)
        ya_cargados = query.all()
        return len(ya_cargados) > 0

    def ya_hay_horarios_nuevos_cargados(self, anio, cuatrimestre):
        query = HorariosYaCargados.query
        query = query.order_by(HorariosYaCargados.anio.desc(), HorariosYaCargados.cuatrimestre.desc())
        ultimo_horario_cargado = query.first()

        if not ultimo_horario_cargado:
            return False

        if ultimo_horario_cargado.anio > anio:
            return True

        if ultimo_horario_cargado.anio < anio:
            return False

        return ultimo_horario_cargado.cuatrimestre > cuatrimestre

    def guardar_ultima_actualizacion_horarios(self, cuatrimestre, anio, fecha_actualizacion):
        db.session.add(HorariosYaCargados(anio=anio, cuatrimestre=cuatrimestre))

        # Actualizar todos los cuatrimestres que no tuvieron update como
        # NO que no se cursa en el cuatrimestre actual.
        cursos = Curso.query.filter(Curso.fecha_actualizacion < fecha_actualizacion).all()
        for curso in cursos:
            if cuatrimestre == 1 or cuatrimestre == '1':
                curso.se_dicta_primer_cuatrimestre = False
            else:
                curso.se_dicta_segundo_cuatrimestre = False

        db.session.commit()

    def asignar_docentes(self, curso, docentes):
        docentes = docentes.split("-")
        for apellido_docente in docentes:
            if apellido_docente.upper() == "A DESIGNAR":
                continue

            docente = Docente(apellido=apellido_docente)
            db.session.add(docente)
            db.session.commit()

            db.session.add(CursosDocente(
                docente_id=docente.id,
                curso_id=curso.id
            ))
