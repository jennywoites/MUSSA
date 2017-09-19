import os

import sys
sys.path.append("../app")

from GeneradorCodigoPulp import generar_archivo_pulp
from ParametrosDAO import Parametros
from Constantes import *
from OptimizadorCodigoPulp import optimizar_codigo_pulp

from Materia import Materia
from Curso import Curso
from Horario import Horario

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


    def ejecutar_test(self):
        if not os.path.exists(RUTA_EJECUCION_TEST):
            os.system('mkdir {}'.format(RUTA_EJECUCION_TEST))
    
        parametros = self.configurar_parametros_test()
        generar_archivo_pulp(parametros)
        optimizar_codigo_pulp(parametros)

        self.ejecutar_codigo_pulp(parametros)
        resultados = self.obtener_resultados_pulp(parametros)
        self.verificar_resultados(parametros, resultados)