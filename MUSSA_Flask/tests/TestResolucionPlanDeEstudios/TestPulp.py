import os

from app.API_Rest.GeneradorPlanCarreras.Constantes import *
from app.API_Rest.GeneradorPlanCarreras.GeneradorPLE.GeneradorCodigoPulp import generar_archivo_pulp
from app.API_Rest.GeneradorPlanCarreras.GeneradorPLE.OptimizadorCodigoPulp import optimizar_codigo_pulp
from app.API_Rest.GeneradorPlanCarreras.ParametrosDTO import Parametros
from app.API_Rest.GeneradorPlanCarreras.my_utils import get_str_cuatrimestre

RUTA_EJECUCION_TEST = "resultados_tests/"


class TestPulp:
    def get_nombre_test(self):
        raise Exception("Obligatorio implementar en las clases hijas")

    def get_plan_carrera_test(self):
        plan = {}
        materias = self.get_materias_test()
        for id_materia in materias:
            materia = materias[id_materia]
            if not id_materia in plan:
                plan[id_materia] = []
            for id_correlativa in materia.correlativas:
                correlativas = plan.get(id_correlativa, [])
                correlativas.append(id_materia)
                plan[id_correlativa] = correlativas
        return plan

    def get_materias_test(self):
        raise Exception("Obligatorio implementar en las clases hijas")

    def get_horarios_test(self):
        raise Exception("Obligatorio implementar en las clases hijas")

    def get_nombre_archivo_pulp(self):
        return RUTA_EJECUCION_TEST + self.get_nombre_test() + "_pulp.py"

    def get_nombre_archivo_resultados_pulp(self):
        return RUTA_EJECUCION_TEST + self.get_nombre_test() + "_resultados_pulp.py"

    def get_nombre_archivo_optimizado_pulp(self):
        return RUTA_EJECUCION_TEST + self.get_nombre_test() + "_optimizado_pulp.py"

    def get_dias(self):
        return [LUNES, MARTES, MIERCOLES, JUEVES, VIERNES, SABADO]

    def get_creditos_minimos_electivas(self):
        raise Exception("Obligatorio implementar en las clases hijas")

    def get_franjas_minima_y_maxima(self):
        return 1, 33

    def get_maxima_cantidad_cuatrimestres(self):
        return 10

    def get_maxima_cantidad_materias_por_cuatrimestre(self):
        return 4

    def comienza_en_primer_cuatrimestre(self):
        return True

    def configurar_parametros_test(self):
        parametros = Parametros()

        parametros.plan = self.get_plan_carrera_test()
        parametros.materias = self.get_materias_test()
        parametros.horarios = self.get_horarios_test()
        parametros.horarios_no_permitidos = []
        parametros.creditos_minimos_electivas = self.get_creditos_minimos_electivas()

        parametros.nombre_archivo_pulp = self.get_nombre_archivo_pulp()
        parametros.nombre_archivo_resultados_pulp = self.get_nombre_archivo_resultados_pulp()
        parametros.nombre_archivo_pulp_optimizado = self.get_nombre_archivo_optimizado_pulp()

        minima, maxima = self.get_franjas_minima_y_maxima()
        parametros.set_franjas(minima, maxima)
        parametros.dias = self.get_dias()
        parametros.max_cuatrimestres = self.get_maxima_cantidad_cuatrimestres()
        parametros.max_cant_materias_por_cuatrimestre = self.get_maxima_cantidad_materias_por_cuatrimestre()

        parametros.primer_cuatrimestre_es_impar = self.comienza_en_primer_cuatrimestre()

        return parametros

    def ejecutar_codigo_pulp(self, parametros):
        os.system('python3 ' + parametros.nombre_archivo_pulp_optimizado)

    def obtener_resultados_pulp(self, parametros):
        resultados = {}

        with open(parametros.nombre_archivo_resultados_pulp, 'r') as arch:
            primera = True
            for linea in arch:

                if primera:
                    primera = False
                    continue

                linea = linea.rstrip(ENTER)
                variable, valor = linea.split(";")
                resultados[variable] = int(valor)

        return resultados

    def verificar_resultados(self, parametros, resultados):
        raise Exception("Obligatorio implementar en las clases hijas")

    def imprimir_plan_carrera(self, parametros, resultados):
        print()
        print("Plan de carrera generado:")
        plan_carrera = self.armar_plan(parametros, resultados)
        for cuatrimestre in range(1, len(plan_carrera) + 1):
            msj = "{} Cuatrimestre: [ ".format(cuatrimestre)
            materias = plan_carrera[cuatrimestre]
            for materia in materias:
                msj += materia + " - "
            msj = msj[:-3] + " ]"
            print(msj)

    def armar_plan(self, parametros, resultados):
        VARIABLE = 0
        MATERIA = 1
        CUATRIMESTRE = 2

        plan_carrera = {}
        for variable in resultados:
            valor = resultados[variable]
            if (not "Y_" in variable) or (valor == 0):
                continue
            datos_variable = variable.split("_")

            cuatri = int(datos_variable[CUATRIMESTRE])
            materias = plan_carrera.get(cuatri, [])
            materias.append(datos_variable[MATERIA])
            plan_carrera[cuatri] = materias
        return plan_carrera

    def obtener_todas_las_materias_que_se_cursan(self, parametros, resultados):
        materias_cursadas = set()

        for id_materia in parametros.materias:
            materia = parametros.materias[id_materia]

            cont = 0
            for cuatri in range(1, parametros.max_cuatrimestres + 1):
                variable = "Y_{}_{}".format(materia.id_materia, get_str_cuatrimestre(cuatri))
                cont += resultados[variable]

            if (cont == 1):
                materias_cursadas.add(id_materia)

        return materias_cursadas

    def ejecutar_test(self):
        if not os.path.exists(RUTA_EJECUCION_TEST):
            os.system('mkdir {}'.format(RUTA_EJECUCION_TEST))

        parametros = self.configurar_parametros_test()
        generar_archivo_pulp(parametros)
        optimizar_codigo_pulp(parametros)

        self.ejecutar_codigo_pulp(parametros)
        resultados = self.obtener_resultados_pulp(parametros)
        self.verificar_resultados(parametros, resultados)

        self.imprimir_plan_carrera(parametros, resultados)

    #################################################################
    ##                  Test de uso general                        ##
    #################################################################

    def todas_las_materias_obligatorias_se_hacen(self, parametros, resultados):
        for id_materia in parametros.materias:
            materia = parametros.materias[id_materia]
            if materia.tipo == ELECTIVA:
                continue

            cont = 0
            for cuatri in range(1, parametros.max_cuatrimestres + 1):
                variable = "Y_{}_{}".format(materia.id_materia, get_str_cuatrimestre(cuatri))
                cont += resultados[variable]

            assert (cont == 1)

    def los_cuatrimestres_de_las_correlativas_son_menores(self, parametros, resultados):
        materias_cursadas = self.obtener_todas_las_materias_que_se_cursan(parametros, resultados)

        for id_materia in parametros.materias:
            materia = parametros.materias[id_materia]

            # Si la materia no se cursa no puede tener un numero de cuatrimestre
            if not materia in materias_cursadas:
                continue

            cuatri_actual = "C" + materia.id_materia
            for id_cor_materia in materia.correlativas:
                cuatri_corr = "C" + id_cor_materia
                assert (resultados[cuatri_actual] > resultados[cuatri_corr])

    def los_creditos_en_electivas_cumplen_con_el_minimo(self, parametros, resultados):
        creditos_acumulados = 0
        for id_materia in parametros.materias:
            materia = parametros.materias[id_materia]
            if materia.tipo != ELECTIVA:
                continue

            cont = 0
            for cuatri in range(1, parametros.max_cuatrimestres + 1):
                variable = "Y_{}_{}".format(materia.id_materia, get_str_cuatrimestre(cuatri))
                cont += resultados[variable]

            if (cont == 1):
                creditos_acumulados += materia.creditos
            elif (cont > 1):
                raise Exception("La materia electiva se está cursando en más de un cuatrimestre")

        assert (creditos_acumulados >= parametros.creditos_minimos_electivas)

    def no_se_elige_un_horario_no_disponible_ese_cuatrimestre(self, parametros, resultados):
        for id_materia in parametros.materias:
            for curso in parametros.horarios[id_materia]:
                for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
                    if self.cuatrimestre_no_disponible(curso, parametros, cuatrimestre):
                        variable_H = "H_{}_{}_{}".format(id_materia, curso.id_curso, get_str_cuatrimestre(cuatrimestre))
                        assert (resultados[variable_H] == 0)

    def cuatrimestre_no_disponible(self, curso, parametros, cuatrimestre):
        cuatri = cuatrimestre % 2

        if cuatri == 1:
            return ((not curso.se_dicta_primer_cuatrimestre and parametros.primer_cuatrimestre_es_impar)
                    or (not curso.se_dicta_segundo_cuatrimestre and not parametros.primer_cuatrimestre_es_impar))

        return ((not curso.se_dicta_primer_cuatrimestre and not parametros.primer_cuatrimestre_es_impar)
                or (not curso.se_dicta_segundo_cuatrimestre and parametros.primer_cuatrimestre_es_impar))

    def los_creditos_minimos_acumulados_son_mayores_que_los_necesarios_para_cursar_la_materia(self, parametros,
                                                                                              resultados):
        for id_materia in parametros.materias:
            materia = parametros.materias[id_materia]
            cuatrimestre_cursada = resultados["C{}".format(id_materia)]
            cuatri_anterior = cuatrimestre_cursada - 1
            creditos_acumulados = resultados[
                "CRED{}".format(get_str_cuatrimestre(cuatri_anterior))] if cuatri_anterior > 0 else 0
            assert (creditos_acumulados >= materia.creditos_minimos_aprobados)
