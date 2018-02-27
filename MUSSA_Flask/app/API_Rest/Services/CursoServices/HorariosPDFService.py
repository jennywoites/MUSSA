from app.API_Rest.Services.BaseService import BaseService
from app.API_Rest.codes import *
from flask_user import roles_accepted
from app import db
from app.models.carreras_models import Carrera, Materia
from app.models.horarios_models import Curso, Horario, HorarioPorCurso, CarreraPorCurso, HorariosYaCargados
from app.models.docentes_models import Docente, CursosDocente
from app.API_Rest.GeneradorPlanCarreras.ParserHorarios import parsear_pdf
import datetime


class HorariosPDFService(BaseService):
    def getNombreClaseServicio(self):
        return "Horarios PDF Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    @roles_accepted('admin')
    def post(self):
        self.logg_parametros_recibidos()

        ruta = self.obtener_texto("ruta")
        cuatrimestre = self.obtener_parametro("cuatrimestre")
        anio = self.obtener_parametro("anio")

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            ("ruta", {
                self.PARAMETRO: ruta,
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: [
                    (self.validar_contenido_y_longitud_texto, [1, 250])
                ]
            }),
            ("cuatrimestre", {
                self.PARAMETRO: cuatrimestre,
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: [
                    (self.es_numero_valido, [])
                ]
            }),
            ("anio", {
                self.PARAMETRO: anio,
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: [
                    (self.es_numero_valido, []),
                    (self.el_horario_no_fue_cargado, [cuatrimestre]),
                    (self.no_hay_horarios_nuevos_cargados, [cuatrimestre])
                ]
            })
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        self.generar_horarios_desde_PDF(ruta, cuatrimestre, anio)

        result = SUCCESS_NO_CONTENT
        self.logg_resultado(result)

        return result

    def generar_horarios_desde_PDF(self, ruta, cuatrimestre, anio):
        horarios_pdf = parsear_pdf(ruta)

        fecha_actualizacion = datetime.datetime.now()
        self.guardar_horarios_pdf(horarios_pdf, cuatrimestre, fecha_actualizacion)
        self.guardar_ultima_actualizacion_horarios(cuatrimestre, anio, fecha_actualizacion)

    def el_horario_no_fue_cargado(self, nombre_parametro, anio, obligatorio, cuatrimestre):
        horarios = HorariosYaCargados.query.filter_by(anio=anio).filter_by(cuatrimestre=cuatrimestre).all()
        return (False, 'El horario ya fue cargado anteriormente', CLIENT_ERROR_BAD_REQUEST) if len(horarios) > 0 else \
            self.mensaje_OK(nombre_parametro)

    def no_hay_horarios_nuevos_cargados(self, nombre_parametro, anio, obligatorio, cuatrimestre):
        query = HorariosYaCargados.query
        query = query.order_by(HorariosYaCargados.anio.desc(), HorariosYaCargados.cuatrimestre.desc())
        ultimo_horario_cargado = query.first()

        if not ultimo_horario_cargado:
            return self.mensaje_OK(nombre_parametro)

        if ultimo_horario_cargado.anio > anio:
            return False, 'Ya hay un horario de un año mayor cargado', CLIENT_ERROR_BAD_REQUEST

        if ultimo_horario_cargado.anio < anio:
            return self.mensaje_OK(nombre_parametro)

        ultimo_horario_cuatri_mayor = ultimo_horario_cargado.cuatrimestre > cuatrimestre
        return self.mensaje_OK(nombre_parametro) if not ultimo_horario_cuatri_mayor else \
            (False, 'Ya hay un horario de el año {} pero de un '
                    'cuatrimestre posterior'.format(anio), CLIENT_ERROR_BAD_REQUEST)

    def guardar_horarios_pdf(self, horarios_pdf, cuatrimestre, fecha_actualizacion):
        carreras_en_sistema = []
        for carrera in Carrera.query.all():
            carreras_en_sistema.append(int(carrera.codigo))

        for horario_pdf in horarios_pdf:
            carreras = self.filtrar_solo_carreras_en_sistema(carreras_en_sistema, horario_pdf["Carreras"])
            if not carreras:
                self.logg_info("Este horario no se procesa: {}".format(horario_pdf))
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
            curso = self.crear_curso(nombre_curso, codigo_materia, docentes, cuatrimestre)

        self.crear_o_actualizar_horarios(curso, horarios_materia, fecha_actualizacion)

        if cuatrimestre == 1 or cuatrimestre == '1':
            curso.se_dicta_primer_cuatrimestre = True
            curso.primer_cuatrimestre_actualizado = True
        else:
            curso.se_dicta_segundo_cuatrimestre = True
            curso.segundo_cuatrimestre_actualizado = True

        curso.fecha_actualizacion = fecha_actualizacion
        self.agregar_carreras_al_curso(curso, carreras)

    def agregar_carreras_al_curso(self, curso, carreras):
        for codigo in carreras:
            codigo = codigo if len(str(codigo)) > 1 else '0' + str(codigo)
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

    def crear_curso(self, nombre_curso, codigo_materia, docentes, cuatrimestre):
        """
        Cuando se crea el curso se lo crea habilitado para ambos cuatrimestres,
        pero como horario nuevo, es decir, solo con el chequeo del cuatrimestre
        que corresponde. Cuando se cargue el siguiente cuatrimestre, se marcara
        si corresponde a ambos cuatrimestres o solo se dicta en uno de ellos.
        """
        curso = Curso(
            codigo_materia=codigo_materia,
            codigo=nombre_curso,
            cantidad_encuestas_completas=0,
            puntaje_total_encuestas=0,
            se_dicta_primer_cuatrimestre=True,
            se_dicta_segundo_cuatrimestre=True,
            primer_cuatrimestre_actualizado=(cuatrimestre == '1'),
            segundo_cuatrimestre_actualizado=(cuatrimestre == '2'),
        )
        db.session.add(curso)

        self.asignar_docentes(curso, docentes)

        return curso

    def desactualizar_horarios_anteriores(self, curso):
        horarios_por_curso = HorarioPorCurso.query.filter_by(curso_id=curso.id).all()

        for horario in horarios_por_curso:
            horario.es_horario_activo = False

        db.session.commit()

    def crear_o_actualizar_horarios(self, curso, horarios_materia, fecha_actualizacion):
        self.desactualizar_horarios_anteriores(curso)

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
                horario_id=horario.id,
                fecha_actualizacion=fecha_actualizacion,
                es_horario_activo=True
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
            if carrera in carreras_en_sistema:
                carreras.append(carrera)
        return carreras

    def guardar_ultima_actualizacion_horarios(self, cuatrimestre, anio, fecha_actualizacion):
        db.session.add(HorariosYaCargados(anio=anio, cuatrimestre=cuatrimestre))

        # Actualizar todos los cuatrimestres que no tuvieron update como
        # NO que no se cursa en el cuatrimestre actual. Ademas se marca a todos
        # los cursos como que han tenido el chequeo del cuatrimestre 1 o 2 segun
        # corresponda
        cursos = Curso.query.filter(Curso.fecha_actualizacion < fecha_actualizacion).all()
        for curso in cursos:
            if cuatrimestre == 1 or cuatrimestre == '1':
                curso.se_dicta_primer_cuatrimestre = False
                curso.primer_cuatrimestre_actualizado = True
            else:
                curso.se_dicta_segundo_cuatrimestre = False
                curso.segundo_cuatrimestre_actualizado = True

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


#########################################
CLASE = HorariosPDFService
URLS_SERVICIOS = (
    '/api/curso/all/horarios/uploadPDF',
)
#########################################
