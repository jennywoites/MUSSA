import os

from app.API_Rest.GeneradorPlanCarreras.GeneradorCodigoPulp import generar_archivo_pulp
from app.API_Rest.GeneradorPlanCarreras.ParametrosDAO import Parametros
from app.API_Rest.GeneradorPlanCarreras.Constantes import *
from app.API_Rest.GeneradorPlanCarreras.OptimizadorCodigoPulp import optimizar_codigo_pulp
from app.API_Rest.GeneradorPlanCarreras.my_utils import get_str_cuatrimestre

from app.API_Rest.GeneradorPlanCarreras.modelos.Materia import Materia
from app.API_Rest.GeneradorPlanCarreras.modelos.Curso import Curso
from app.API_Rest.GeneradorPlanCarreras.modelos.Horario import Horario

RUTA_EJECUCION_TEST = "resultados_tests/"

class TestPulp:

    def get_nombre_test(self):
        raise Exception("Obligatorio implementar en las clases hijas")


    def get_plan_carrera_test(self):
        raise Exception("Obligatorio implementar en las clases hijas")


    def get_materias_test(self):
        raise Exception("Obligatorio implementar en las clases hijas")


    def get_horarios_test(self):
        raise Exception("Obligatorio implementar en las clases hijas")


    def get_horarios_no_permitidos_test(self):
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


    def configurar_parametros_test(self):
        parametros = Parametros()

        parametros.plan = self.get_plan_carrera_test()
        parametros.materias = self.get_materias_test()
        parametros.horarios = self.get_horarios_test()
        parametros.horarios_no_permitidos = self.get_horarios_no_permitidos_test()
        parametros.creditos_minimos_electivas = self.get_creditos_minimos_electivas()

        parametros.nombre_archivo_pulp = self.get_nombre_archivo_pulp()
        parametros.nombre_archivo_resultados_pulp = self.get_nombre_archivo_resultados_pulp()
        parametros.nombre_archivo_pulp_optimizado = self.get_nombre_archivo_optimizado_pulp()

        minima, maxima = self.get_franjas_minima_y_maxima()
        parametros.set_franjas(minima, maxima)
        parametros.dias = self.get_dias()
        parametros.max_cuatrimestres = self.get_maxima_cantidad_cuatrimestres()
        parametros.max_cant_materias_por_cuatrimestre = self.get_maxima_cantidad_materias_por_cuatrimestre()

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
        for cuatrimestre in range(1, len(plan_carrera) +1):
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

        for codigo in parametros.materias:
            materia = parametros.materias[codigo]

            cont = 0
            for cuatri in range(1, parametros.max_cuatrimestres + 1):
                variable = "Y_{}_{}".format(materia.codigo, get_str_cuatrimestre(cuatri))
                cont += resultados[variable]

            if (cont == 1):
                materias_cursadas.add(codigo)

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
        for codigo in parametros.materias:
            materia = parametros.materias[codigo]
            if materia.tipo == ELECTIVA:
                continue

            cont = 0
            for cuatri in range(1, parametros.max_cuatrimestres + 1):
                variable = "Y_{}_{}".format(materia.codigo, get_str_cuatrimestre(cuatri))
                cont += resultados[variable]

            assert(cont == 1)


    def los_cuatrimestres_de_las_correlativas_son_menores(self, parametros, resultados):
        materias_cursadas = self.obtener_todas_las_materias_que_se_cursan(parametros, resultados)

        for codigo in parametros.materias:
            materia = parametros.materias[codigo]
            
            #Si la materia no se cursa no puede tener un numero de cuatrimestre
            if not materia in materias_cursadas:
                continue

            cod_actual = "C" + materia.codigo
            for cor_materia in materia.correlativas:
                cod_corr = "C" + cor_materia
                assert(resultados[cod_actual] > resultados[cod_corr])