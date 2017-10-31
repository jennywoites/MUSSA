from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request

from app import db
from app.models.carreras_models import Carrera
from app.models.horarios_models import Curso, Horario, HorarioPorCurso, CarreraPorCurso

import logging

from app.API_Rest.CodigoConPulp.app.ParserHorarios import parsear_pdf

class GuardarHorariosDesdeArchivoPDF(Resource):
    def get(self):
        logging.info('Se invoco al servicio Gurdar Horarios Desde Archivo PDF')

        #Validar que el usuario este logueado y sea admin (ver has_role)

        args = request.args

        q_ruta = args["ruta"] if "ruta" in args else None
        q_cuatrimestre = args["cuatrimestre"] if "cuatrimestre" in args else None

        if not q_ruta or not q_cuatrimestre:
            logging.error('El servicio Gurdar Horarios Desde Archivo PDF recibe la ruta del archivo y el cuatrimestre al que pertenece')
            return {'Error': 'Este servicio debe recibir la ruta del archivo y el cuatrimestre al que pertenece'}, CLIENT_ERROR_BAD_REQUEST

        horarios_pdf = parsear_pdf(q_ruta)

        self.guardar_horarios_pdf(horarios_pdf, q_cuatrimestre)

        #Para todos aquellos que no se actualizaron esta vez colocar el cuatrimestre en NO
        #Ya que no se estaria dictando la materia este cuatrimestre

        result = ({'OK': 'Los horarios fueron cargados correctamente'}, SUCCESS_OK) 
        logging.info('Gurdar Horarios Desde Archivo PDF devuelve como resultado: {}'.format(result))
        return result


    def guardar_horarios_pdf(self, horarios_pdf, cuatrimestre):
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
                horarios_materia, cuatrimestre)

            db.session.commit()


    def find_or_create_curso(self, nombre_curso, codigo_materia, docentes, carreras,
        horarios_materia, cuatrimestre):
        curso = Curso.query.filter_by(codigo_materia=codigo_materia).filter_by(codigo=nombre_curso).first()

        if not curso:
            curso = self.crear_curso(nombre_curso, codigo_materia, docentes, horarios_materia)

        print(cuatrimestre)
        if cuatrimestre == 1 or cuatrimestre == '1':
            curso.se_dicta_primer_cuatrimestre = True
        else:
            curso.se_dicta_segundo_cuatrimestre = True
        
        self.agregar_carreras_al_curso(curso, carreras)


    def agregar_carreras_al_curso(self, curso, carreras):
        for codigo in carreras:
            carrera_db = Carrera.query.filter_by(codigo=codigo).first()

            query = CarreraPorCurso.query.filter_by(curso_id=curso.id)
            carrera_por_curso = query.filter_by(carrera_id=carrera_db.id).first()

            if carrera_por_curso:
                continue

            carrera_por_curso = CarreraPorCurso(
                curso_id = curso.id,
                carrera_id = carrera_db.id
            )
            db.session.add(carrera_por_curso)


    def crear_curso(self, nombre_curso, codigo_materia, docentes, horarios_materia):
        curso = Curso(
            codigo_materia = codigo_materia,
            codigo = nombre_curso,
            docentes = docentes,
            cantidad_encuestas_completas = 0,
            puntaje_total_encuestas = 0
        )
        db.session.add(curso)

        for horario_pdf in horarios_materia:
            horario = Horario(
                dia = horario_pdf[0],
                hora_desde = horario_pdf[1],
                hora_hasta = horario_pdf[2]
            )            
            db.session.add(horario)
            db.session.commit()

            horario_por_curso = HorarioPorCurso(
                curso_id = curso.id,
                horario_id = horario.id
            )
            db.session.add(horario_por_curso)
            
        return curso


    def filtrar_solo_carreras_en_sistema(self, carreras_en_sistema, carreras_pdf):
        carreras = []
        for carrera in carreras_pdf:
            if str(carrera) in carreras_en_sistema:                
                carreras.append(carrera)
        return carreras