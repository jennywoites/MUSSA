from datetime import datetime
from flask_user import login_required
from AsyncTasks.broker_generador_greedy import tarea_generar_plan_greedy
from AsyncTasks.broker_generador_plan_ple import tarea_generar_plan_ple
from app.API_Rest.GeneradorPlanCarreras.Constantes import OBLIGATORIA, ELECTIVA, TRABAJO_FINAL
from app.API_Rest.GeneradorPlanCarreras.ParametrosDTO import Parametros
from app.API_Rest.GeneradorPlanCarreras.modelos.Curso import Curso as Modelo_Curso
from app.API_Rest.GeneradorPlanCarreras.modelos.Horario import Horario as Modelo_Horario
from app.API_Rest.GeneradorPlanCarreras.modelos.Materia import Materia as Modelo_Materia
from app.API_Rest.Services.BaseService import BaseService
from app.API_Rest.codes import *
from app.DAO.MateriasDAO import *
from app.DAO.PlanDeCarreraDAO import *
from app.models.alumno_models import MateriasAlumno
from app.models.carreras_models import Materia, Correlativas, Creditos, TipoMateria, MateriasIncompatibles
from app.models.generadorJSON.plan_de_estudios_generadorJSON import generarJSON_materias_plan_de_estudios
from app.models.horarios_models import Curso, HorarioPorCurso, Horario, CarreraPorCurso
from app.models.palabras_clave_models import TematicaPorMateria, TematicaMateria
from app.models.plan_de_estudios_models import PlanDeEstudios, MateriaPlanDeEstudios


class PlanDeEstudiosService(BaseService):
    def getNombreClaseServicio(self):
        return "Plan de Estudios Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    @login_required
    def get(self, idPlanDeEstudios):
        self.logg_parametros_recibidos()

        alumno = self.obtener_alumno_usuario_actual()

        if not alumno:
            msj = "El usuario no tiene ningun alumno asociado"
            self.logg_error(msj)
            return {'Error': msj}, CLIENT_ERROR_NOT_FOUND

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            ("idPlanDeEstudios", {
                self.PARAMETRO: idPlanDeEstudios,
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: [
                    (self.id_es_valido, []),
                    (self.existe_id, [PlanDeEstudios]),
                    (self.plan_pertenece_al_alumno, [])
                ]
            })
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        plan_json = generarJSON_materias_plan_de_estudios(PlanDeEstudios.query.get(idPlanDeEstudios))

        result = ({"plan_de_estudio": plan_json}, SUCCESS_OK)
        self.logg_resultado(result)

        return result

    @login_required
    def delete(self, idPlanDeEstudios):
        self.logg_parametros_recibidos()

        alumno = self.obtener_alumno_usuario_actual()

        if not alumno:
            msj = "El usuario no tiene ningun alumno asociado"
            self.logg_error(msj)
            return {'Error': msj}, CLIENT_ERROR_NOT_FOUND

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            ("idPlanDeEstudios", {
                self.PARAMETRO: idPlanDeEstudios,
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: [
                    (self.id_es_valido, []),
                    (self.existe_id, [PlanDeEstudios]),
                    (self.plan_pertenece_al_alumno, []),
                    (self.plan_no_se_encuentra_en_curso, [])
                ]
            })
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        MateriaPlanDeEstudios.query.filter_by(plan_estudios_id=idPlanDeEstudios).delete()
        db.session.commit()

        PlanDeEstudios.query.filter_by(id=idPlanDeEstudios).delete()
        db.session.commit()

        result = SUCCESS_NO_CONTENT
        self.logg_resultado(result)
        return result

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
        cursos_preseleccionados = self.obtener_lista('cursos_preseleccionados')
        trabajo_final = self.obtener_texto('trabajo_final')
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

        carrera = int(carrera)
        max_cant_cuatrimestres = int(max_cant_cuatrimestres)
        max_cant_materias = int(max_cant_materias)
        max_horas_cursada = int(max_horas_cursada)
        max_horas_extras = int(max_horas_extras)
        puntaje_minimo_cursos = int(puntaje_minimo_cursos)
        cuatrimestre_inicio = int(cuatrimestre_inicio)
        algoritmo = int(algoritmo)

        parametros = Parametros()

        parametros.orientacion = orientacion
        parametros.id_carrera = carrera
        parametros.max_cuatrimestres = max_cant_cuatrimestres
        parametros.max_cant_materias_por_cuatrimestre = max_cant_materias
        parametros.max_horas_cursada = max_horas_cursada * 2
        parametros.max_horas_extras = max_horas_extras * 2
        parametros.cuatrimestre_inicio = cuatrimestre_inicio
        parametros.anio_inicio = anio_inicio

        self.configurar_plan_de_carrera_origen(carrera, parametros)
        self.actualizar_creditos(carrera, trabajo_final, parametros)

        self.actualizar_plan_con_materias_aprobadas(carrera, aprobacion_finales, parametros)

        # Se separan en otras categorias las materias de trabajo final y CBC que aun no estan aprobadas
        self.filtrar_materias_CBC_y_trabajos_finales(trabajo_final, parametros)

        self.configurar_horarios_y_seleccionar_cursos_obligatorios(horarios_invalidos, cursos_preseleccionados,
                                                                   puntaje_minimo_cursos, parametros)

        self.actualizar_creditos_minimos_por_tematica(parametros, tematicas)

        cuatrimestres_de_CBC = 1 if (len(parametros.materias_CBC_pendientes) <= 3) else 2
        parametros.primer_cuatrimestre_es_impar = ((cuatrimestre_inicio + cuatrimestres_de_CBC) % 2 != 0)

        self.cargar_materias_incompatibles(parametros)

        obligatorias_tienen_cursos, msj = self.validar_cursos_materias_obligatorias(parametros)
        if not obligatorias_tienen_cursos:
            result = {"mensaje": msj}, CLIENT_ERROR_BAD_REQUEST
            self.logg_resultado(result)
            return result

        self.eliminar_materias_sin_cursos(parametros)

        electivas_cubren_creditos_requeridos, msj = self.validar_creditos_requeridos_electivas(parametros)
        if not electivas_cubren_creditos_requeridos:
            result = {"mensaje": msj}, CLIENT_ERROR_BAD_REQUEST
            self.logg_resultado(result)
            return result

        self.actualizar_horarios_con_franjas_minimas_y_maximas(parametros)

        ALGORITMOS_VALIDOS = {
            ALGORITMO_GREEDY: tarea_generar_plan_greedy,
            ALGORITMO_PROGRAMACION_LINEAL_ENTERA: tarea_generar_plan_ple
        }

        if algoritmo in ALGORITMOS_VALIDOS:
            return self.crear_tarea_para_generar_plan_de_estudios(ALGORITMOS_VALIDOS[algoritmo], parametros)

        result = {"mensaje": "El algoritmo introducido no es valido"}, CLIENT_ERROR_BAD_REQUEST
        self.logg_resultado(result)
        return result

    def crear_tarea_para_generar_plan_de_estudios(self, tarea_algoritmo, parametros):
        plan_de_estudios = self.alta_nuevo_plan_de_estudios(parametros)

        parametros.id_plan_estudios = plan_de_estudios.id
        tarea = tarea_algoritmo.delay(parametros.generar_parametros_json())

        if not tarea:
            result = {"mensaje": "No se pudo enviar a generar el plan."
                                 " Por favor, intentá nuevamente"}, CLIENT_ERROR_BAD_REQUEST
            self.logg_resultado(result)
            return result

        result = SUCCESS_NO_CONTENT
        self.logg_resultado(result)
        return result

    def cargar_materias_incompatibles(self, parametros):
        parametros.materias_incompatibles = {}

        for id_materia in parametros.materias:
            incompatibles = MateriasIncompatibles.query.filter_by(materia_id=id_materia).all()
            if not incompatibles:
                continue

            parametros.materias_incompatibles[id_materia] = []
            for grupo_materia_incompatible in incompatibles:
                parametros.materias_incompatibles[id_materia].append(grupo_materia_incompatible.materia_incompatible_id)

    def actualizar_creditos_minimos_por_tematica(self, parametros, tematicas):
        parametros.creditos_minimos_tematicas = {}
        for nombre_tematica in tematicas:
            tematica = TematicaMateria.query.filter_by(tematica=nombre_tematica).first()
            porcentaje = int(tematicas[nombre_tematica]) / 100
            creditos = round(porcentaje * parametros.creditos_minimos_electivas)
            parametros.creditos_minimos_tematicas[tematica.id] = creditos

    def configurar_plan_de_carrera_origen(self, id_carrera, parametros):
        """
        Guarda para el id de carrera especificado en el campo plan de los parámetros, un
        diccionario con el id de materia como clave y como valor una lista con los
        ids de materia que tienen a la materia clave de correlativa.
        Actualiza la cantidad de creditos requeridos en materias electivas.
        """
        parametros.plan = {}
        parametros.materias = {}
        parametros.materias_CBC_pendientes = []

        for materia in Materia.query.filter_by(carrera_id=id_carrera).all():
            if not materia.id in parametros.plan:
                parametros.plan[materia.id] = []

            self.agregar_materia_a_parametros(parametros, materia)

            correlativas_de_materia_actual = Correlativas.query.filter_by(materia_id=materia.id).all()
            for materia_correlativa in correlativas_de_materia_actual:
                id_correlativa = materia_correlativa.materia_correlativa_id
                materias_correlativas = parametros.plan.get(id_correlativa, [])

                if not materia.id in materias_correlativas:
                    materias_correlativas.append(materia.id)

                parametros.plan[id_correlativa] = materias_correlativas

    def filtrar_materias_CBC_y_trabajos_finales(self, trabajo_final, parametros):
        # Las materias del CBC se trabajan de forma independiente
        tipo_CBC = TipoMateria.query.filter_by(descripcion='CBC').first().id
        for materia in Materia.query.filter_by(carrera_id=parametros.id_carrera).filter_by(tipo_materia_id=tipo_CBC):
            if materia.id in parametros.materias:
                parametros.materias_CBC_pendientes.append(materia.id)
                parametros.quitar_materia_por_id(materia.id, True)

        tipo_tesis = TipoMateria.query.filter_by(descripcion='TESIS').first().id
        tesis = Materia.query.filter_by(carrera_id=parametros.id_carrera).filter_by(tipo_materia_id=tipo_tesis) \
            .first()

        # Si no hace tesis, quitar la materia de tesis
        if trabajo_final != "TESIS" and tesis:
            parametros.quitar_materia_por_id(tesis.id, False)

        tipo_tp_profesional = TipoMateria.query.filter_by(descripcion='TP_PROFESIONAL').first().id
        tp = Materia.query.filter_by(carrera_id=parametros.id_carrera) \
            .filter_by(tipo_materia_id=tipo_tp_profesional).first()

        # Si no hace trabajo profesional, quitar la materia de trabajo profesional
        if trabajo_final != "TP_PROFESIONAL" and tp:
            parametros.quitar_materia_por_id(tp.id, False)

        # Los trabajos finales se trabajan de forma independiente
        id_trabajo = ''
        if trabajo_final == "TESIS":
            id_trabajo = tesis.id
        if trabajo_final == "TP_PROFESIONAL":
            id_trabajo = tp.id

        if id_trabajo and id_trabajo in parametros.materias:
            materia_trabajo_final_parte_1 = parametros.materias[id_trabajo]
            codigo_parte_1 = materia_trabajo_final_parte_1.codigo + '_PARTE_A'

            materia_trabajo_final_parte_1.medias_horas_extras_cursada /= 2

            materia_trabajo_final_parte_2 = Modelo_Materia(
                id_materia=materia_trabajo_final_parte_1.id_materia,
                codigo=materia_trabajo_final_parte_1.codigo + '_PARTE_B',
                nombre=materia_trabajo_final_parte_1.nombre,
                creditos=materia_trabajo_final_parte_1.creditos,
                tipo=materia_trabajo_final_parte_1.tipo,
                cred_min=materia_trabajo_final_parte_1.creditos_minimos_aprobados,
                correlativas=materia_trabajo_final_parte_1.correlativas[:],
                tematicas_principales=materia_trabajo_final_parte_1.tematicas_principales[:],
                medias_horas_extras_cursada=materia_trabajo_final_parte_1.medias_horas_extras_cursada
            )

            materia_trabajo_final_parte_1.codigo = codigo_parte_1

            parametros.quitar_materia_por_id(materia_trabajo_final_parte_1.id_materia, False)
            parametros.materia_trabajo_final.append(materia_trabajo_final_parte_1)
            parametros.materia_trabajo_final.append(materia_trabajo_final_parte_2)

    def actualizar_creditos(self, id_carrera, trabajo_final, parametros):
        creditos = Creditos.query.filter_by(carrera_id=id_carrera).first()

        if trabajo_final == "TESIS":
            parametros.creditos_minimos_electivas = creditos.creditos_electivas_con_tesis
        elif trabajo_final == "TP_PROFESIONAL":
            parametros.creditos_minimos_electivas = creditos.creditos_electivas_con_tp
        else:
            parametros.creditos_minimos_electivas = creditos.creditos_electivas_general

    def agregar_materia_a_parametros(self, parametros, materia):
        if materia.id in parametros.materias:
            return

        # Si la materia es TESIS / TP_PROFESIONAL --> TRABAJO_FINAL
        # Si la materia es OBLIGATORIA / ORIENTACION ELEGIDA --> obligatoria
        # Si la materia es ELECTIVA / ORIENTACION NO ELEGIDA --> electiva
        tipo_original = TipoMateria.query.get(materia.tipo_materia_id).descripcion
        tipo = ELECTIVA
        if tipo_original in ["OBLIGATORIA", parametros.orientacion]:
            tipo = OBLIGATORIA
        if tipo_original in ["TESIS", "TP_PROFESIONAL"]:
            tipo = TRABAJO_FINAL

        correlativas = []
        correlativas_de_materia_actual = Correlativas.query.filter_by(materia_id=materia.id).all()
        for correlativa in correlativas_de_materia_actual:
            correlativas.append(correlativa.materia_correlativa_id)

        tematicas_principales = []
        MAX_TEMATICAS = 3
        tematicas_por_materia = TematicaPorMateria.query.filter_by(materia_id=materia.id) \
            .order_by(TematicaPorMateria.cantidad_encuestas_asociadas.desc()).limit(MAX_TEMATICAS).all()
        for tematica in tematicas_por_materia:
            tematicas_principales.append(tematica.tematica_id)

        # TODO: Si se tienen suficientes encuestas modificar para que las horas extras se saquen con ese valor
        medias_horas_extra_cursada = materia.creditos * 2  # Se multiplica por dos para obtener las medias horas

        parametros.materias[materia.id] = Modelo_Materia(
            id_materia=materia.id,
            codigo=materia.codigo,
            nombre=materia.nombre,
            creditos=materia.creditos,
            tipo=tipo,
            cred_min=materia.creditos_minimos_para_cursarla,
            correlativas=correlativas,
            tematicas_principales=tematicas_principales,
            medias_horas_extras_cursada=medias_horas_extra_cursada
        )

    def actualizar_plan_con_materias_aprobadas(self, carrera, aprobacion_finales, parametros):
        parametros.cuatrimestre_minimo_para_materia = {}

        # Borro las materias que el alumno ya aprobo
        alumno = self.obtener_alumno_usuario_actual()
        estado_aprobado = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[APROBADA]).first()

        # Borro las materias que se van a dar por aprobadas
        for id_materia in aprobacion_finales:
            cuatrimestre = int(aprobacion_finales[id_materia])
            self.setear_cuatrimestre_minimo_correlativas(id_materia, cuatrimestre, parametros)
            if cuatrimestre > -1:
                parametros.quitar_materia_por_id(id_materia, True)

        materias_aprobadas = MateriasAlumno.query.filter_by(alumno_id=alumno.id).filter_by(carrera_id=carrera). \
            filter_by(estado_id=estado_aprobado.id).all()
        for materia_alumno in materias_aprobadas:
            parametros.quitar_materia_por_id(materia_alumno.materia_id, True)

    def setear_cuatrimestre_minimo_correlativas(self, id_materia, cuatrimestre, parametros):
        if cuatrimestre <= 0 or not id_materia in parametros.plan:
            return

        materia = Materia.query.get(id_materia)

        # Si la materia es del CBC no modifica los cuatrimestres de inicio
        tipo_CBC = TipoMateria.query.filter_by(descripcion='CBC').first().id
        if materia.tipo_materia_id == tipo_CBC:
            return

        materias_que_la_tienen_de_correlativa = parametros.plan[id_materia]
        for id_materia_q_tiene_de_correlativa in materias_que_la_tienen_de_correlativa:
            cuatri_actual = parametros.cuatrimestre_minimo_para_materia.get(id_materia_q_tiene_de_correlativa,
                                                                            cuatrimestre)
            parametros.cuatrimestre_minimo_para_materia[id_materia_q_tiene_de_correlativa] = max(cuatri_actual,
                                                                                                 cuatrimestre)

    def configurar_horarios_y_seleccionar_cursos_obligatorios(self, horarios_invalidos, cursos_preseleccionados,
                                                              puntaje_minimo_cursos, parametros):

        horarios_invalidos = self.normalizar_dias_y_franjas_invalidas(horarios_invalidos)

        parametros.horarios = {}
        for id_materia in parametros.materias:
            materia = parametros.materias[id_materia]

            # Si la materia fue seleccionada, agrego solo el curso correspondiente
            # además, si es una materia electiva se la pasa a obligatoria para forzar
            # que se elija ese curso en algun momento.
            if materia.id_materia in cursos_preseleccionados:
                curso_db = Curso.query.get(cursos_preseleccionados[materia.id_materia])
                parametros.horarios[materia.id_materia] = [self.generar_curso(curso_db)]

                if materia.tipo == ELECTIVA:
                    materia.tipo = OBLIGATORIA
                    parametros.creditos_minimos_electivas -= materia.creditos
            else:
                self.agregar_cursos_materia_con_restricciones(materia, horarios_invalidos, puntaje_minimo_cursos,
                                                              parametros)

    def generar_curso(self, curso_db):
        horarios = []
        for horario_por_curso in HorarioPorCurso.query.filter_by(curso_id=curso_db.id).filter_by(
                es_horario_activo=True).all():
            horario = Horario.query.get(horario_por_curso.horario_id)
            horarios.append(Modelo_Horario(
                dia=horario.dia,
                hora_inicio=float(horario.hora_desde),
                hora_fin=float(horario.hora_hasta)
            ))

        return Modelo_Curso(
            id_curso=curso_db.id,
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
                posibles_cursos_materia.append((curso.calcular_puntaje(), self.generar_curso(curso)))

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
            parametros.horarios[materia.id_materia] = cursos_materia

    def curso_tiene_horario_valido(self, curso, horarios_invalidos):
        for horario_curso in HorarioPorCurso.query.filter_by(curso_id=curso.id).filter_by(es_horario_activo=True).all():
            horario = Horario.query.get(horario_curso.horario_id)
            if not horario.dia in horarios_invalidos:
                continue

            horario = Modelo_Horario(
                dia=horario.dia,
                hora_inicio=float(horario.hora_desde),
                hora_fin=float(horario.hora_hasta)
            )
            franjas = horario.get_franjas_utilizadas()
            for franja in franjas:
                if franja in horarios_invalidos[horario.dia]:
                    return False

        return True

    def validar_cursos_materias_obligatorias(self, parametros):
        materias_obligatorias_sin_curso = []
        for id_materia in parametros.plan:
            materia = parametros.materias[id_materia]
            if materia.tipo == OBLIGATORIA and not id_materia in parametros.horarios:
                materias_obligatorias_sin_curso.append(materia)

        if not materias_obligatorias_sin_curso:
            return True, 'OK'

        msj = "El plan no se ha generado <br />"

        if len(materias_obligatorias_sin_curso) == 1:
            materia = materias_obligatorias_sin_curso[0]
            return False, msj + "La materia {} - {} es obligatoria pero no tiene horarios compatibles. Por favor " \
                                "elige un curso manualmente y vuelve a generar el " \
                                "plan".format(materia.codigo, materia.nombre)

        msj += "Las siguientes materias son obligatorias pero no tienen horarios compatibles con los seleccionados. " \
               "<br /> Por favor, elige un curso manualmente y vuelve a generar el plan. <br />"
        for materia in materias_obligatorias_sin_curso:
            msj += "* {} - {}<br />".format(materia.codigo, materia.nombre)
        msj = msj[:-6]  # Elimino el ultimo <br />
        return False, msj

    def eliminar_materias_sin_cursos(self, parametros):
        ids_plan = list(parametros.plan.keys())
        for id_materia in ids_plan:
            if not id_materia in parametros.horarios:
                self.eliminar_materia_y_correlativas_recursivo(id_materia, parametros)

    def eliminar_materia_y_correlativas_recursivo(self, id_materia, parametros):
        correlativas = parametros.plan[id_materia] if id_materia in parametros.plan else []
        parametros.quitar_materia_por_id(id_materia, False)

        for id_correlativa in correlativas:
            self.eliminar_materia_y_correlativas_recursivo(id_correlativa, parametros)

    def normalizar_dias_y_franjas_invalidas(self, horarios_invalidos):
        horarios_normalizados = {}
        for datos_horario in horarios_invalidos:
            franjas = horarios_normalizados.get(datos_horario["dia"], [])

            horario = Modelo_Horario(
                dia=datos_horario["dia"],
                hora_inicio=self.get_hora_numerica(datos_horario["hora_desde"]),
                hora_fin=self.get_hora_numerica(datos_horario["hora_hasta"])
            )

            for franja in horario.get_franjas_utilizadas():
                if not franja in franjas:
                    franjas.append(franja)

            horarios_normalizados[datos_horario["dia"]] = franjas

        return horarios_normalizados

    def get_hora_numerica(self, hora):
        horas, minutos = hora.split(':')
        horas, minutos = int(horas), int(minutos)
        if minutos == 30:
            horas += 0.5
        return horas

    def actualizar_horarios_con_franjas_minimas_y_maximas(self, parametros):
        min_inicio = 33
        max_inicio = 1
        dias = []
        for id_materia in parametros.horarios:
            for curso in parametros.horarios[id_materia]:
                for horario in curso.horarios:
                    if horario.dia not in dias:
                        dias.append(horario.dia)
                    franjas = horario.get_franjas_utilizadas()
                    min_inicio = min(min_inicio, min(franjas))
                    max_inicio = max(max_inicio, min(franjas))

        parametros.franja_minima = min_inicio
        parametros.franja_maxima = max_inicio + 1
        parametros.dias = dias

        for id_materia in parametros.horarios:
            for curso in parametros.horarios[id_materia]:
                for horario in curso.horarios:
                    hora_maxima = horario.convertir_franja_a_hora(parametros.franja_maxima)
                    if horario.hora_fin > hora_maxima:
                        horario.hora_fin = hora_maxima

    def validar_creditos_requeridos_electivas(self, parametros):
        creditos_tematicas = parametros.creditos_minimos_tematicas.copy()
        creditos = 0
        for id_materia in parametros.materias:
            materia = parametros.materias[id_materia]
            if materia.tipo == ELECTIVA:
                creditos += materia.creditos
                self.actualizar_creditos_tematicas(creditos_tematicas, materia)

        es_valido = (creditos >= parametros.creditos_minimos_electivas) and not creditos_tematicas
        return es_valido, ('OK' if es_valido else 'Las materias electivas disponibles que cumplen con las '
                                                  'restricciones impuestas no son suficientes para completar la '
                                                  'cantidad de créditos mínimos necesarios o la proporción de créditos'
                                                  ' para las temáticas elegidas. Modifica las restricciones '
                                                  'o elige algunas materias electivas especificas que desees.')

    def actualizar_creditos_tematicas(self, creditos_tematicas, materia):
        for id_tematica in materia.tematicas_principales:
            if id_tematica in creditos_tematicas:
                creditos_tematicas[id_tematica] -= materia.creditos
                if creditos_tematicas[id_tematica] <= 0:
                    creditos_tematicas.pop(id_tematica)

    def alta_nuevo_plan_de_estudios(self, parametros):
        estado_en_curso = EstadoPlanDeEstudios.query.filter_by(numero=PLAN_EN_CURSO).first()
        alumno = self.obtener_alumno_usuario_actual()

        plan_de_estudios = PlanDeEstudios(
            alumno_id=alumno.id,
            fecha_generacion=datetime.today(),
            fecha_ultima_actualizacion=datetime.today(),
            estado_id=estado_en_curso.id,
            cuatrimestre_inicio_plan=parametros.cuatrimestre_inicio,
            anio_inicio_plan=parametros.anio_inicio
        )
        db.session.add(plan_de_estudios)
        db.session.commit()

        return plan_de_estudios

    def plan_pertenece_al_alumno(self, nombre_parametro, valor, es_obligatorio):
        alumno = self.obtener_alumno_usuario_actual()
        plan = PlanDeEstudios.query.filter_by(id=valor).filter_by(alumno_id=alumno.id).first()
        if not plan:
            return False, 'El plan indicado no existe o no pertenece al alumno', CLIENT_ERROR_NOT_FOUND
        return self.mensaje_OK(nombre_parametro)

    def plan_no_se_encuentra_en_curso(self, nombre_parametro, valor, es_obligatorio):
        plan = PlanDeEstudios.query.get(valor)
        estado_en_curso = EstadoPlanDeEstudios.query.filter_by(numero=PLAN_EN_CURSO).first()

        if plan.estado_id == estado_en_curso.id:
            return False, 'El plan indicado no puede eliminarse porque se encuentra en curso', CLIENT_ERROR_NOT_FOUND

        return self.mensaje_OK(nombre_parametro)


#########################################
CLASE = PlanDeEstudiosService
URLS_SERVICIOS = (
    '/api/alumno/planDeEstudios',
    '/api/alumno/planDeEstudios/<int:idPlanDeEstudios>',
)
#########################################
