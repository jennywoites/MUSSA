from app.API_Rest.codes import *
from flask_user import login_required
from app.API_Rest.Services.BaseService import BaseService
from app.DAO.PlanDeCarreraDAO import *
from app.API_Rest.GeneradorPlanCarreras.ParametrosDTO import Parametros
from app.models.carreras_models import Materia, Correlativas, Creditos, TipoMateria
from app.models.alumno_models import MateriasAlumno
from app.models.horarios_models import Curso, HorarioPorCurso, Horario, CarreraPorCurso
from app.DAO.MateriasDAO import *
from app.API_Rest.GeneradorPlanCarreras.Constantes import OBLIGATORIA, ELECTIVA
from app.API_Rest.GeneradorPlanCarreras.modelos.Materia import Materia as Modelo_Materia
from app.API_Rest.GeneradorPlanCarreras.modelos.Curso import Curso as Modelo_Curso
from app.API_Rest.GeneradorPlanCarreras.modelos.Horario import Horario as Modelo_Horario


class PlanDeEstudiosService(BaseService):
    def getNombreClaseServicio(self):
        return "Plan de Estudios Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    @login_required
    def put(self):
        self.logg_parametros_recibidos()

        alumno = self.obtener_alumno_usuario_actual()

        if not alumno:
            msj = "El usuario no tiene ningun alumno asociado"
            self.logg_error(msj)
            return {'Error': msj}, CLIENT_ERROR_NOT_FOUND

        carrera = self.obtener_parametro('carrera')
        max_cant_cuatrimestres = self.obtener_parametro('max_cant_cuatrimestres')
        max_cant_materias = self.obtener_parametro('max_cant_materias')
        max_horas_cursada = self.obtener_parametro('max_horas_cursada')
        max_horas_extras = self.obtener_parametro('max_horas_extras')
        puntaje_minimo_cursos = self.obtener_parametro('puntaje_minimo_cursos')
        cuatrimestre_inicio = self.obtener_parametro('cuatrimestre_inicio')
        anio_inicio = self.obtener_parametro('anio_inicio')
        horarios_invalidos = self.obtener_lista('horarios_invalidos')
        tematicas = self.obtener_lista('tematicas')
        aprobacion_finales = self.obtener_lista('aprobacion_finales')
        cursos_preseleccioandos = self.obtener_lista('cursos_preseleccioandos')
        hace_tesis = self.obtener_booleano('hace_tesis')
        orientacion = self.obtener_texto('orientacion')
        algoritmo = self.obtener_parametro('algoritmo')

        # parametros_son_validos, msj, codigo = self.validar_parametros(dict([
        #     ("idMateriaAlumno", {
        #         self.PARAMETRO: datos_materia["idMateriaAlumno"],
        #         self.ES_OBLIGATORIO: True,
        #         self.FUNCIONES_VALIDACION: []
        #     })
        # ]))
        #
        # if not parametros_son_validos:
        #     self.logg_error(msj)
        #     return {'Error': msj}, codigo

        parametros = Parametros()

        parametros.orientacion = orientacion
        parametros.id_carrera = carrera
        parametros.max_cuatrimestres = max_cant_cuatrimestres
        parametros.max_cant_materias_por_cuatrimestre = max_cant_materias
        parametros.max_horas_cursada = max_horas_cursada
        parametros.max_horas_extras = max_horas_extras
        parametros.tematicas = tematicas

        self.configurar_plan_de_carrera_origen(carrera, hace_tesis, parametros)
        self.actualizar_plan_con_materias_aprobadas(carrera, aprobacion_finales, parametros)
        self.configurar_horarios_y_seleccionar_cursos_obligatorios(horarios_invalidos, cursos_preseleccioandos,
                                                                   puntaje_minimo_cursos, parametros)

        cuatrimestres_de_CBC = 1 if (len(parametros.materias_CBC_pendientes) <= 3) else 2
        parametros.primer_cuatrimestre_es_impar = ((cuatrimestre_inicio + cuatrimestres_de_CBC) % 2 != 0)

        # Validar que los cursos obligatorios hayan quedado con cursos.
        # Si algun curso obligatorio no tiene curso es xq el horario no es compatible con la restriccion
        # (o que no existe ningun curso que la dicte, pero eso no deberia pasar)

        algoritmo = int(algoritmo)
        if algoritmo == ALGORITMO_GREEDY:
            return self.generar_plan_de_cursada_greedy(parametros)

        if algoritmo == ALGORITMO_PROGRAMACION_LINEAL_ENTERA:
            return self.generar_plan_de_cursada_programacion_lineal_entera(parametros)

        result = "El algoritmo introducido no es valido", CLIENT_ERROR_BAD_REQUEST
        self.logg_resultado(result)
        return result

    def configurar_plan_de_carrera_origen(self, id_carrera, hace_tesis, parametros):
        """
        Guarda para el id de carrera especificado en el campo plan de los parámetros, un
        diccionario con el codigo de materia como clave y como valor una lista con los
        códigos de materia que tienen a la materia clave de correlativa.
        Actualiza la cantidad de creditos requeridos en materias electivas.
        """
        parametros.plan = {}
        parametros.materias = {}
        parametros.materias_CBC_pendientes = []

        tipo_CBC = TipoMateria.query.filter_by(descripcion='CBC').first()
        tipo_tesis = TipoMateria.query.filter_by(descripcion='TESIS').first()
        tipo_tp_profesional = TipoMateria.query.filter_by(descripcion='TP_PROFESIONAL').first()

        for materia in Materia.query.filter_by(carrera_id=id_carrera):

            # Las materias del CBC se tratan de forma independiente
            if materia.tipo_materia_id == tipo_CBC.id:
                parametros.materias_CBC_pendientes.append(materia)
                continue

            # Si no hace tesis no guardo la materia de tesis
            if materia.tipo_materia_id == tipo_tesis.id and not hace_tesis:
                continue

            # Si hace tesis no guardo la materia de tp profesional
            if materia.tipo_materia_id == tipo_tp_profesional.id and hace_tesis:
                continue

            # TODO: Si la materia es tesis o tp dividir en dos submaterias

            if not materia.codigo in parametros.plan:
                parametros.plan[materia.codigo] = []

            self.agregar_materia_a_parametros(parametros, materia)

            correlativas_de_materia_actual = Correlativas.query.filter_by(materia_id=materia.id).all()
            for materia_correlativa in correlativas_de_materia_actual:
                correlativa = Materia.query.get(materia_correlativa.materia_correlativa_id)
                correlativas = parametros.plan.get(correlativa.codigo, [])

                if not materia.codigo in correlativas:
                    correlativas.append(materia.codigo)
                parametros.plan[correlativa.codigo] = correlativas

        creditos = Creditos.query.filter_by(carrera_id=id_carrera).first()
        if hace_tesis:
            parametros.creditos_minimos_electivas = creditos.creditos_electivas_con_tesis
        else:
            parametros.creditos_minimos_electivas = creditos.creditos_electivas_con_tp

    def agregar_materia_a_parametros(self, parametros, materia):
        if materia.codigo in parametros.materias:
            return

        # Si la materia es TESIS / TP_PROFESIONAL / OBLIGATORIA / ORIENTACION ELEGIDA --> obligatoria
        # Si la materia es ELECTIVA / ORIENTACION NO ELEGIDA --> electiva
        tipo_original = TipoMateria.query.get(materia.tipo_materia_id).descripcion
        tipo = OBLIGATORIA if tipo_original in ["TESIS", "TP_PROFESIONAL", "OBLIGATORIA", parametros.orientacion] else \
            ELECTIVA

        correlativas = []
        correlativas_de_materia_actual = Correlativas.query.filter_by(materia_id=materia.id).all()
        for correlativa in correlativas_de_materia_actual:
            correlativas.append(Materia.query.get(correlativa.materia_correlativa_id).codigo)

        parametros.materias[materia.codigo] = Modelo_Materia(
            codigo=materia.codigo,
            nombre=materia.nombre,
            creditos=materia.creditos,
            tipo=tipo,
            cred_min=materia.creditos_minimos_para_cursarla,
            correlativas=correlativas
        )

    def actualizar_plan_con_materias_aprobadas(self, carrera, aprobacion_finales, parametros):
        parametros.materias_con_finales_pendientes = aprobacion_finales

        # Borro las materias que se van a dar por aprobadas
        for codigo in aprobacion_finales:
            if aprobacion_finales[codigo] != -1:
                self.quitar_materia_por_codigo(codigo, parametros)

        # Borro las materias que el alumno ya aprobo
        alumno = self.obtener_alumno_usuario_actual()
        estado_aprobado = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[APROBADA]).first()

        materias_aprobadas = MateriasAlumno.query.filter_by(alumno_id=alumno.id).filter_by(carrera_id=carrera). \
            filter_by(estado_id=estado_aprobado.id).all()
        for materia_alumno in materias_aprobadas:
            materia = Materia.query.get(materia_alumno.materia_id)
            self.quitar_materia_por_codigo(materia.codigo, parametros)

    def quitar_materia_por_codigo(self, codigo, parametros):
        if not codigo in parametros.materias:
            return

        materia = parametros.materias.pop(codigo)
        if materia.tipo == ELECTIVA:
            parametros.creditos_minimos_electivas -= materia.creditos

        for cod_materia_que_la_tiene_de_correlativa in parametros.plan[codigo]:
            materia_actual = parametros.materias[cod_materia_que_la_tiene_de_correlativa]
            if codigo in materia_actual.correlativas:
                materia_actual.correlativas.pop(codigo)

        if codigo in parametros.plan:
            del (parametros.plan[codigo])

    def configurar_horarios_y_seleccionar_cursos_obligatorios(self, horarios_invalidos, cursos_preseleccionados,
                                                              puntaje_minimo_cursos, parametros):
        parametros.horarios = {}
        for materia in parametros.materias:
            # Si la materia fue seleccionada, agrego solo el curso correspondiente
            # además, si es una materia electiva se la pasa a obligatoria para forzar
            # que se elija ese curso en algun momento.
            if materia.codigo in cursos_preseleccionados:
                curso_db = Curso.query.get(cursos_preseleccionados[materia.codigo])
                parametros.horarios[materia.codigo] = [self.generar_curso(materia, curso_db)]

                if materia.tipo == ELECTIVA:
                    materia.tipo = OBLIGATORIA
                    parametros.creditos_minimos_electivas -= materia.creditos
            else:
                self.agregar_cursos_materia_con_restricciones(materia, horarios_invalidos, puntaje_minimo_cursos,
                                                              parametros)

    def generar_curso(self, curso_db):
        horarios = []
        for horario_por_curso in HorarioPorCurso.query.filter_by(curso_id=curso_db.id):
            horario = Horario.query.get(horario_por_curso.horario_id)
            horarios.append(Modelo_Horario(
                dia=horario.dia,
                hora_inicio=horario.hora_desde,
                hora_fin=horario.hora_hasta
            ))

        return Modelo_Curso(
            cod_materia=curso_db.codigo_materia,
            nombre_curso=curso_db.codigo,
            horarios=horarios,
            se_dicta_primer_cuatrimestre=curso_db.se_dicta_primer_cuatrimestre,
            se_dicta_segundo_cuatrimestre=curso_db.se_dicta_segundo_cuatrimestre,
            puntaje=curso_db.calcular_puntaje()
        )

    def agregar_cursos_materia_con_restricciones(self, materia, horarios_invalidos, puntaje_minimo_cursos, parametros):
        cursos_db = Curso.query.filter_by(codigo_materia=materia.codigo).filter(CarreraPorCurso.curso_id == Curso.id) \
            .filter(CarreraPorCurso.carrera_id == parametros.id_carrera).all()

        # Posibles cursos que cumplen con la restricción de horarios
        posibles_cursos_materia = []
        for curso in cursos_db:
            if self.curso_tiene_horario_valido(curso, horarios_invalidos):
                posibles_cursos_materia.append((curso.calcular_puntaje(), self.generar_curso(materia, curso)))

        PUNTAJE_POS = 0
        CURSO_POS = 1
        posibles_cursos_materia = sorted(posibles_cursos_materia, key=lambda tupla_curso: tupla_curso[PUNTAJE_POS])

        if not posibles_cursos_materia:
            return

        # Si la materia es obligatoria nos aseguramos de que se agregue el curso de mayor puntaje
        # si no existen cursos que cumplan con la restricción de puntaje minimo
        if materia.tipo == OBLIGATORIA:
            puntaje_mayor_actual = posibles_cursos_materia[-1][PUNTAJE_POS]
            if puntaje_mayor_actual < puntaje_minimo_cursos:
                puntaje_minimo_cursos = puntaje_mayor_actual

        cursos_materia = []
        while posibles_cursos_materia and posibles_cursos_materia[-1][PUNTAJE_POS] >= puntaje_minimo_cursos:
            cursos_materia.append(posibles_cursos_materia.pop()[CURSO_POS])

        if cursos_materia:
            parametros.horarios[materia.codigo] = cursos_materia

    ########################################################################
    ##              Algoritmos de generación de plan de carrera           ##
    ########################################################################

    def generar_plan_de_cursada_greedy(self, parametros):
        pass

    def generar_plan_de_cursada_programacion_lineal_entera(self, parametros):
        # parametros.nombre_archivo_pulp = ARCHIVO_PULP
        # parametros.nombre_archivo_resultados_pulp = ARCHIVO_RESULTADO_PULP
        # parametros.nombre_archivo_pulp_optimizado = ARCHIVO_PULP_OPTIMIZADO

        result = "El algoritmo no ha sido implementado", CLIENT_ERROR_NOT_FOUND
        self.logg_resultado(result)
        return result


#########################################
CLASE = PlanDeEstudiosService
URLS_SERVICIOS = (
    '/api/alumno/planDeEstudios',
)
#########################################
