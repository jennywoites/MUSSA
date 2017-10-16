from TestDesdeArchivoCSV import TestDesdeArchivoCSV

import sys
sys.path.append("../app")

from GeneradorCodigoPulp import generar_archivo_pulp
from ParametrosDAO import Parametros
from Constantes import *
from my_utils import get_str_cuatrimestre

from Materia import Materia
from Curso import Curso
from Horario import Horario

class Test_plan_licenciatura_con_unico_horario_por_materia_no_superpuestos(TestDesdeArchivoCSV):

    def get_nombre_test(self):
        return "test_plan_licenciatura_con_unico_horario_por_materia_no_superpuestos"

    def get_plan_carrera_test(self):
        return self.plan_carrera

    def get_materias_test(self):
        return self.materias

    def get_horarios_test(self):
        return self.horarios

    def get_horarios_no_permitidos_test(self):
        return []

    def get_creditos_minimos_electivas(self):
        return 0

    def get_maxima_cantidad_cuatrimestres(self):
        return 8

    def get_maxima_cantidad_materias_por_cuatrimestre(self):
        return 4

    #################################################################
    ##                  Verificacion de resultados                 ##
    #################################################################

    def verificar_resultados(self, parametros, resultados):
        self.todas_las_materias_obligatorias_se_hacen(parametros, resultados)
        self.los_cuatrimestres_de_las_correlativas_son_menores(parametros,resultados)


if __name__ == "__main__":
    test_a_ejecutar = Test_plan_licenciatura_con_unico_horario_por_materia_no_superpuestos()
    test_a_ejecutar.ejecutar_test()