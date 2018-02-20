from app.API_Rest.codes import *
from flask_user import login_required
from flask import url_for
from app.API_Rest.Services.BaseService import BaseService
from app.DAO.PlanDeCarreraDAO import *
from app.API_Rest.GeneradorPlanCarreras.ParametrosDTO import Parametros
from app.models.carreras_models import Materia, Correlativas, Creditos, TipoMateria, MateriasIncompatibles
from app.models.alumno_models import MateriasAlumno
from app.models.horarios_models import Curso, HorarioPorCurso, Horario, CarreraPorCurso
from app.models.plan_de_estudios_models import PlanDeEstudios, MateriaPlanDeEstudios
from app.models.palabras_clave_models import TematicaPorMateria, TematicaMateria
from app.DAO.MateriasDAO import *
from app.API_Rest.GeneradorPlanCarreras.Constantes import OBLIGATORIA, ELECTIVA, TRABAJO_FINAL
from app.API_Rest.GeneradorPlanCarreras.modelos.Materia import Materia as Modelo_Materia
from app.API_Rest.GeneradorPlanCarreras.modelos.Curso import Curso as Modelo_Curso
from app.API_Rest.GeneradorPlanCarreras.modelos.Horario import Horario as Modelo_Horario
from datetime import datetime
from app.models.generadorJSON.plan_de_estudios_generadorJSON import generarJSON_materias_plan_de_estudios
from app.API_Rest.GeneradorPlanCarreras.GeneradorPlanGreedy import generar_plan_greedy


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
                    (self.plan_pertenece_al_alumno, [])
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
            result = msj, CLIENT_ERROR_BAD_REQUEST
            self.logg_resultado(result)
            return result

        self.eliminar_materias_sin_cursos(parametros)

        electivas_cubren_creditos_requeridos, msj = self.validar_creditos_requeridos_electivas(parametros)
        if not electivas_cubren_creditos_requeridos:
            result = msj, CLIENT_ERROR_BAD_REQUEST
            self.logg_resultado(result)
            return result

        self.actualizar_horarios_con_franjas_minimas_y_maximas(parametros)

        plan_de_estudios = self.alta_nuevo_plan_de_estudios(parametros)

        if algoritmo == ALGORITMO_GREEDY:
            return self.generar_plan_de_cursada_greedy(parametros, plan_de_estudios)

        if algoritmo == ALGORITMO_PROGRAMACION_LINEAL_ENTERA:
            return self.generar_plan_de_cursada_programacion_lineal_entera(parametros, plan_de_estudios)

        result = "El algoritmo introducido no es valido", CLIENT_ERROR_BAD_REQUEST
        self.logg_resultado(result)
        return result

    def cargar_materias_incompatibles(self, parametros):
        parametros.materias_incompatibles = {}

        for cod_materia in parametros.materias:
            incompatibles = MateriasIncompatibles.query. \
                filter_by(materia_id=parametros.materias[cod_materia].id_materia).all()
            if not incompatibles:
                continue

            parametros.materias_incompatibles[cod_materia] = []
            for grupo_materia_incompatible in incompatibles:
                materia_incompatible = Materia.query.get(grupo_materia_incompatible.materia_incompatible_id)
                parametros.materias_incompatibles[cod_materia].append(materia_incompatible.codigo)

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
        diccionario con el codigo de materia como clave y como valor una lista con los
        códigos de materia que tienen a la materia clave de correlativa.
        Actualiza la cantidad de creditos requeridos en materias electivas.
        """
        parametros.plan = {}
        parametros.materias = {}
        parametros.materias_CBC_pendientes = []

        for materia in Materia.query.filter_by(carrera_id=id_carrera).all():
            if not materia.codigo in parametros.plan:
                parametros.plan[materia.codigo] = []

            self.agregar_materia_a_parametros(parametros, materia)

            correlativas_de_materia_actual = Correlativas.query.filter_by(materia_id=materia.id).all()
            for materia_correlativa in correlativas_de_materia_actual:
                materia_correlativa_db = Materia.query.get(materia_correlativa.materia_correlativa_id)
                materias_correlativas = parametros.plan.get(materia_correlativa_db.codigo, [])

                if not materia.codigo in materias_correlativas:
                    materias_correlativas.append(materia.codigo)
                parametros.plan[materia_correlativa_db.codigo] = materias_correlativas

    def filtrar_materias_CBC_y_trabajos_finales(self, trabajo_final, parametros):
        # Las materias del CBC se trabajan de forma independiente
        tipo_CBC = TipoMateria.query.filter_by(descripcion='CBC').first().id
        for materia in Materia.query.filter_by(carrera_id=parametros.id_carrera).filter_by(tipo_materia_id=tipo_CBC):
            if materia.codigo in parametros.materias:
                parametros.materias_CBC_pendientes.append(materia)
                parametros.quitar_materia_por_codigo(materia.codigo, True)

        tipo_tesis = TipoMateria.query.filter_by(descripcion='TESIS').first().id
        tesis = Materia.query.filter_by(carrera_id=parametros.id_carrera).filter_by(tipo_materia_id=tipo_tesis) \
            .first()

        # Si no hace tesis, quitar la materia de tesis
        if trabajo_final != "TESIS" and tesis:
            parametros.quitar_materia_por_codigo(tesis.codigo, False)

        tipo_tp_profesional = TipoMateria.query.filter_by(descripcion='TP_PROFESIONAL').first().id
        tp = Materia.query.filter_by(carrera_id=parametros.id_carrera) \
            .filter_by(tipo_materia_id=tipo_tp_profesional).first()

        # Si no hace trabajo profesional, quitar la materia de trabajo profesional
        if trabajo_final != "TP_PROFESIONAL" and tp:
            parametros.quitar_materia_por_codigo(tp.codigo, False)

        # Los trabajos finales se trabajan de forma independiente
        codigo = ''
        if trabajo_final == "TESIS":
            codigo = tesis.codigo
        if trabajo_final == "TP_PROFESIONAL":
            codigo = tp.codigo

        if codigo and codigo in parametros.materias:
            materia_trabajo_final_parte_1 = parametros.materias[codigo]
            codigo_parte_1 = materia_trabajo_final_parte_1.codigo + '_PARTE_A'

            materia_trabajo_final_parte_1.medias_horas_extras_cursada /= 2

            materia_trabajo_final_parte_2 = Modelo_Materia(
                id_materia=materia_trabajo_final_parte_1.id_materia,
                codigo=materia_trabajo_final_parte_1.codigo + '_PARTE_B',
                nombre=materia_trabajo_final_parte_1.nombre,
                creditos=materia_trabajo_final_parte_1.creditos,
                tipo=materia_trabajo_final_parte_1.tipo,
                cred_min=materia_trabajo_final_parte_1.creditos_minimos_aprobados,
                correlativas=materia_trabajo_final_parte_1.correlativas[:] + [codigo_parte_1],
                tematicas_principales=materia_trabajo_final_parte_1.tematicas_principales[:],
                medias_horas_extras_cursada=materia_trabajo_final_parte_1.medias_horas_extras_cursada
            )

            materia_trabajo_final_parte_1.codigo = codigo_parte_1

            parametros.quitar_materia_por_codigo(codigo, False)
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
        if materia.codigo in parametros.materias:
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
            correlativas.append(Materia.query.get(correlativa.materia_correlativa_id).codigo)

        tematicas_principales = []
        MAX_TEMATICAS = 3
        tematicas_por_materia = TematicaPorMateria.query.filter_by(materia_id=materia.id) \
            .order_by(TematicaPorMateria.cantidad_encuestas_asociadas.desc()).limit(MAX_TEMATICAS).all()
        for tematica in tematicas_por_materia:
            tematicas_principales.append(tematica.tematica_id)

        # TODO: Si se tienen suficientes encuestas modificar para que las horas extras se saquen con ese valor
        medias_horas_extra_cursada = materia.creditos * 2  # Se multiplica por dos para obtener las medias horas

        parametros.materias[materia.codigo] = Modelo_Materia(
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
        for codigo in aprobacion_finales:
            cuatrimestre = int(aprobacion_finales[codigo])
            self.setear_cuatrimestre_minimo_correlativas(codigo, cuatrimestre, parametros)
            if cuatrimestre > -1:
                parametros.quitar_materia_por_codigo(codigo, True)

        materias_aprobadas = MateriasAlumno.query.filter_by(alumno_id=alumno.id).filter_by(carrera_id=carrera). \
            filter_by(estado_id=estado_aprobado.id).all()
        for materia_alumno in materias_aprobadas:
            materia = Materia.query.get(materia_alumno.materia_id)
            parametros.quitar_materia_por_codigo(materia.codigo, True)

    def setear_cuatrimestre_minimo_correlativas(self, codigo, cuatrimestre, parametros):
        if cuatrimestre <= 0 or not codigo in parametros.plan:
            return

        # Si la materia es del CBC no modifica los cuatrimestres de inicio
        tipo_CBC = TipoMateria.query.filter_by(descripcion='CBC').first().id
        if Materia.query.filter_by(carrera_id=parametros.id_carrera).filter_by(codigo=codigo) \
                .filter_by(tipo_materia_id=tipo_CBC).first():
            return

        materias_que_la_tienen_de_correlativa = parametros.plan[codigo]
        for cod_materia in materias_que_la_tienen_de_correlativa:
            cuatri_actual = parametros.cuatrimestre_minimo_para_materia.get(cod_materia, cuatrimestre)
            parametros.cuatrimestre_minimo_para_materia[cod_materia] = max(cuatri_actual, cuatrimestre)

    def configurar_horarios_y_seleccionar_cursos_obligatorios(self, horarios_invalidos, cursos_preseleccionados,
                                                              puntaje_minimo_cursos, parametros):

        horarios_invalidos = self.normalizar_dias_y_franjas_invalidas(horarios_invalidos)

        parametros.horarios = {}
        for cod in parametros.materias:
            materia = parametros.materias[cod]

            # Si la materia fue seleccionada, agrego solo el curso correspondiente
            # además, si es una materia electiva se la pasa a obligatoria para forzar
            # que se elija ese curso en algun momento.
            if materia.codigo in cursos_preseleccionados:
                curso_db = Curso.query.get(cursos_preseleccionados[materia.codigo])
                parametros.horarios[materia.codigo] = [self.generar_curso(curso_db)]

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
            parametros.horarios[materia.codigo] = cursos_materia

    def curso_tiene_horario_valido(self, curso, horarios_invalidos):
        for horario_curso in HorarioPorCurso.query.filter_by(curso_id=curso.id).all():
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
        for codigo in parametros.plan:
            materia = parametros.materias[codigo]
            if materia.tipo == OBLIGATORIA and not codigo in parametros.horarios:
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
        codigos_plan = list(parametros.plan.keys())
        for cod_materia in codigos_plan:
            if not cod_materia in parametros.horarios:
                self.eliminar_materia_y_correlativas_recursivo(cod_materia, parametros)

    def eliminar_materia_y_correlativas_recursivo(self, cod_materia, parametros):
        correlativas = parametros.plan[cod_materia] if cod_materia in parametros.plan else []
        parametros.quitar_materia_por_codigo(cod_materia, False)

        for cod_correlativa in correlativas:
            self.eliminar_materia_y_correlativas_recursivo(cod_correlativa, parametros)

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
        for cod_materia in parametros.horarios:
            for curso in parametros.horarios[cod_materia]:
                for horario in curso.horarios:
                    if horario.dia not in dias:
                        dias.append(horario.dia)
                    franjas = horario.get_franjas_utilizadas()
                    min_inicio = min(min_inicio, min(franjas))
                    max_inicio = max(max_inicio, min(franjas))

        parametros.franja_minima = min_inicio
        parametros.franja_maxima = max_inicio + 1
        parametros.dias = dias

        for cod_materia in parametros.horarios:
            for curso in parametros.horarios[cod_materia]:
                for horario in curso.horarios:
                    hora_maxima = horario.convertir_franja_a_hora(parametros.franja_maxima)
                    if horario.hora_fin > hora_maxima:
                        horario.hora_fin = hora_maxima

    def validar_creditos_requeridos_electivas(self, parametros):
        creditos_tematicas = parametros.creditos_minimos_tematicas.copy()
        creditos = 0
        for cod_materia in parametros.materias:
            materia = parametros.materias[cod_materia]
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

    def actualizar_plan(self, plan_de_estudios, nuevo_estado):
        estado = EstadoPlanDeEstudios.query.filter_by(numero=nuevo_estado).first()

        plan_de_estudios.fecha_ultima_actualizacion = datetime.today()
        plan_de_estudios.estado_id = estado.id

        db.session.commit()

    def agregar_materia_al_plan(self, plan_de_estudios, id_materia, id_curso, cuatrimestre):
        materia_plan = MateriaPlanDeEstudios(
            plan_estudios_id=plan_de_estudios.id,
            materia_id=id_materia,
            orden=cuatrimestre
        )

        if id_curso:
            materia_plan.curso_id = id_curso

        db.session.add(materia_plan)
        db.session.commit()

    def agregar_materias_CBC_al_plan_generado(self, parametros):
        if not parametros.materias_CBC_pendientes:
            return

        grupos_CBC = []
        grupo_actual = {}
        for index, materia in enumerate(parametros.materias_CBC_pendientes):
            grupo_actual[materia.codigo] = {
                "id_materia": materia.id,
                "id_curso": None
            }
            if (index + 1) % 3 == 0:
                grupos_CBC.append(grupo_actual)
                grupo_actual = {}

        if grupo_actual: #En caso de tener menos materias por cuatrimestre
            grupos_CBC.append(grupo_actual)

        for i in range(len(grupos_CBC)-1,-1,-1):
            grupo_cuatrimestre = grupos_CBC[i]
            parametros.plan_generado.insert(0, grupo_cuatrimestre)

    def agregar_materias_generadas_al_plan(self, parametros, plan_de_estudios):
        self.agregar_materias_CBC_al_plan_generado(parametros)

        for cuatrimestre, grupo_materias in enumerate(parametros.plan_generado):
            for cod_materia in grupo_materias:
                id_materia = grupo_materias[cod_materia]["id_materia"]
                id_curso = grupo_materias[cod_materia]["id_curso"]
                self.agregar_materia_al_plan(plan_de_estudios, id_materia, id_curso, cuatrimestre)

    ########################################################################
    ##              Algoritmos de generación de plan de carrera           ##
    ########################################################################

    def generar_plan_de_cursada_greedy(self, parametros, plan_de_estudios):
        se_genero_plan_compatible = generar_plan_greedy(parametros)

        if not se_genero_plan_compatible:
            self.actualizar_plan(plan_de_estudios, PLAN_INCOMPATIBLE)
            result = 'No es posible generar un plan con todas las restricciones impuestas.<br />' \
                     'Flexibilizá algunas condiciones o seleccioná algunos cursos manualmente y' \
                     'luego volvé a generar el plan de estudios.', CLIENT_ERROR_BAD_REQUEST
            self.logg_resultado(result)
            return result

        self.agregar_materias_generadas_al_plan(parametros, plan_de_estudios)
        self.actualizar_plan(plan_de_estudios, PLAN_FINALIZADO)

        url = url_for('main.visualizar_plan_de_estudios_page', idPlanEstudios=plan_de_estudios.id)
        result = url, SUCCESS_OK
        self.logg_resultado(result)
        return result

    def generar_plan_de_cursada_programacion_lineal_entera(self, parametros, plan_de_estudios):
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
    '/api/alumno/planDeEstudios/<int:idPlanDeEstudios>',
)
#########################################
