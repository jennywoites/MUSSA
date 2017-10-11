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

class Test_plan_licenciatura_con_unico_horario_por_materia_no_superpuestos_con_materias_electivas(TestDesdeArchivoCSV):

    def get_nombre_test(self):
        return "test_plan_licenciatura_con_unico_horario_por_materia_no_superpuestos_con_materias_electivas"

    def get_plan_carrera_test(self):
        return self.plan_carrera

    def get_materias_test(self):
        return self.materias

    def get_horarios_test(self):
        return self.horarios

    def get_horarios_no_permitidos_test(self):
        return []

    def get_creditos_minimos_electivas(self):
        return 10

    def get_maxima_cantidad_cuatrimestres(self):
        return 12

    def get_maxima_cantidad_materias_por_cuatrimestre(self):
        return 4

    #################################################################
    ##                  Verificacion de resultados                 ##
    #################################################################

    def verificar_todas_las_materias_obligatorias_se_hacen(self, parametros, resultados):
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
        for codigo in parametros.materias:
            materia = parametros.materias[codigo]
            cod_actual = "C" + materia.codigo
            for cor_materia in materia.correlativas:
                cod_corr = "C" + cor_materia
                assert(resultados[cod_actual] > resultados[cod_corr])


    def los_creditos_en_electivas_cumplen_con_el_minimo(parametros, resultados):
        creditos_acumulados = 0
        for codigo in parametros.materias:
            materia = parametros.materias[codigo]
            if materia.tipo != ELECTIVA:
                continue

            cont = 0
            for cuatri in range(1, parametros.max_cuatrimestres + 1):
                variable = "Y_{}_{}".format(materia.codigo, get_str_cuatrimestre(cuatri))
                cont += resultados[variable]

            if (cont == 1):
                creditos_acumulados += materia.creditos
            elif (cont > 1):
                raise Exception("La materia electiva se está cursando en más de un cuatrimestre")

        print(creditos_acumulados)
        assert(creditos_acumulados >= parametros.creditos_minimos_electivas)       


    def verificar_resultados(self, parametros, resultados):
        self.verificar_todas_las_materias_obligatorias_se_hacen(parametros, resultados)
        self.los_cuatrimestres_de_las_correlativas_son_menores(parametros,resultados)
        self.los_creditos_en_electivas_cumplen_con_el_minimo(parametros, resultados)


if __name__ == "__main__":
    test_a_ejecutar = Test_plan_licenciatura_con_unico_horario_por_materia_no_superpuestos_con_materias_electivas()
    test_a_ejecutar.ejecutar_test()