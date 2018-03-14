if __name__ == "__main__":
    import sys

    sys.path.append("../..")

from tests.TestResolucionPlanDeEstudios.TestPulp import TestPulp
from tests.TestResolucionPlanDeEstudios.MateriasDAOMock import *


class Test_correlatividades_se_hacen_en_orden(TestPulp):
    def get_nombre_test(self):
        return "test_correlatividades_se_hacen_en_orden"

    def get_materias_test(self):
        return {
            MATERIA_A_OBLIGATORIA.id_materia: MATERIA_A_OBLIGATORIA,
            MATERIA_B_OBLIGATORIA.id_materia: MATERIA_B_OBLIGATORIA,
            MATERIA_C_OBLIGATORIA.id_materia: MATERIA_C_OBLIGATORIA,
        }

    def get_horarios_test(self):
        return {
            MATERIA_A_OBLIGATORIA.id_materia: [CURSO_1_MATERIA_A, CURSO_2_MATERIA_A],
            MATERIA_B_OBLIGATORIA.id_materia: [CURSO_1_MATERIA_B, CURSO_2_MATERIA_B],
            MATERIA_C_OBLIGATORIA.id_materia: [CURSO_1_MATERIA_C],
        }

    def get_horarios_no_permitidos_test(self):
        return []

    def get_dias(self):
        return [LUNES]

    def get_creditos_minimos_electivas(self):
        return 0

    def get_franjas_minima_y_maxima(self):
        return 1, 10

    def get_maxima_cantidad_cuatrimestres(self):
        return 3

    def get_maxima_cantidad_materias_por_cuatrimestre(self):
        return 3

    #################################################################
    ##                  Verificacion de resultados                 ##
    #################################################################

    def verificar_resultados(self, parametros, resultados):
        self.todas_las_materias_obligatorias_se_hacen(parametros, resultados)
        self.los_cuatrimestres_de_las_correlativas_son_menores(parametros, resultados)


if __name__ == "__main__":
    test_a_ejecutar = Test_correlatividades_se_hacen_en_orden()
    test_a_ejecutar.ejecutar_test()
