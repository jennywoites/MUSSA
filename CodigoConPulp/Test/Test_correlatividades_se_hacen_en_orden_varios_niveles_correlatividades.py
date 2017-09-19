from TestPulp import TestPulp

import sys
sys.path.append("../app")

from GeneradorCodigoPulp import generar_archivo_pulp
from ParametrosDAO import Parametros
from Constantes import *

from Materia import Materia
from Curso import Curso
from Horario import Horario

class Test_correlatividades_se_hacen_en_orden_varios_niveles_correlatividades(TestPulp):

    def get_nombre_test(self):
        return "test_correlatividades_se_hacen_en_orden_varios_niveles_correlatividades"

    def get_plan_carrera_test(self):
        return {
        "A": ["C"],
        "B": ["D"],
        "C": ["D"],
        "D": [],
        "E": [],
    }

    def get_materias_test(self):
        return {
        "A": Materia("A", "A", 1, OBLIGATORIA, 0, ["C"]),
        "B": Materia("B", "B", 1, OBLIGATORIA, 0, ["D"]),
        "C": Materia("C", "C", 1, OBLIGATORIA, 0, ["D"]),
        "D": Materia("D", "D", 1, OBLIGATORIA, 0, []),
        "E": Materia("E", "E", 1, OBLIGATORIA, 0, []),
    }

    def get_horarios_test(self):
        return {
        "A": [Curso("A", "Curso1A", [Horario(LUNES, 7, 7.5)])],
        "B": [Curso("B", "Curso1B", [Horario(LUNES, 7.5, 8)])],
        "C": [Curso("C", "Curso1C", [Horario(LUNES, 8, 8.5)])],
        "D": [Curso("D", "Curso1D", [Horario(LUNES, 8.5, 9)])],
        "E": [Curso("E", "Curso1E", [Horario(LUNES, 9, 9.5)])],
    }

    def get_horarios_no_permitidos_test(self):
        return []

    def get_dias(self):
        return [LUNES]

    def get_creditos_minimos_electivas(self):
        return 0

    def get_franjas_minima_y_maxima(self):
        return 1, 6

    def get_maxima_cantidad_cuatrimestres(self):
        return 3

    def get_maxima_cantidad_materias_por_cuatrimestre(self):
        return 3

    #################################################################
    ##                  Verificacion de resultados                 ##
    #################################################################

    def todas_las_materias_obligatorias_se_hacen(self, parametros, resultados):
        for codigo in parametros.materias:
            materia = parametros.materias[codigo]
            if materia.tipo == ELECTIVA:
                continue

            cont = 0
            for cuatri in range(1, parametros.max_cuatrimestres + 1):
                variable = "Y_{}_{}".format(materia.codigo, cuatri)
                cont += resultados[variable]

            assert(cont == 1)


    def los_cuatrimestres_de_las_correlativas_son_menores(self, parametros, resultados):
        for codigo in parametros.materias:
            materia = parametros.materias[codigo]
            var_codigo_menor = "C" + materia.codigo
            me_tienen_como_correltiva = materia.correlativas
            for cor_materia in me_tienen_como_correltiva:
                var_cod_corr = "C" + cor_materia
                assert(resultados[var_codigo_menor] < resultados[var_cod_corr])


    def verificar_resultados(self, parametros, resultados):
        self.todas_las_materias_obligatorias_se_hacen(parametros, resultados)
        self.los_cuatrimestres_de_las_correlativas_son_menores(parametros, resultados)


if __name__ == "__main__":
    test_a_ejecutar = Test_correlatividades_se_hacen_en_orden_varios_niveles_correlatividades()
    test_a_ejecutar.ejecutar_test()