if __name__ == "__main__":
    import sys
    sys.path.append("../..")

from tests.TestResolucionPlanDeEstudios.TestPulp import TestPulp
from tests.TestResolucionPlanDeEstudios.MateriasDAOMock import *

class Test_creditos_minimos_para_cursar(TestPulp):

    def get_nombre_test(self):
        return "test_creditos_minimos_para_cursar"

    def get_materias_test(self):
        return {
            MATERIA_A_OBLIGATORIA.id_materia: MATERIA_A_OBLIGATORIA,
            MATERIA_B_OBLIGATORIA.id_materia: MATERIA_B_OBLIGATORIA,
            MATERIA_C_OBLIGATORIA.id_materia: MATERIA_C_OBLIGATORIA,
            MATERIA_D_OBLIGATORIA.id_materia: MATERIA_D_OBLIGATORIA,
            MATERIA_E_OBLIGATORIA_CREDITOS_MINIMOS.id_materia: MATERIA_E_OBLIGATORIA_CREDITOS_MINIMOS
        }

    def get_horarios_test(self):
        return {
            MATERIA_A_OBLIGATORIA.id_materia: [CURSO_3_MATERIA_A],
            MATERIA_B_OBLIGATORIA.id_materia: [CURSO_3_MATERIA_B],
            MATERIA_C_OBLIGATORIA.id_materia: [CURSO_2_MATERIA_C],
            MATERIA_D_OBLIGATORIA.id_materia: [CURSO_1_MATERIA_D],
            MATERIA_E_OBLIGATORIA.id_materia: [CURSO_1_MATERIA_E]
        }

    def get_creditos_minimos_electivas(self):
        return 0

    def get_franjas_minima_y_maxima(self):
        return 1, 20

    def get_maxima_cantidad_cuatrimestres(self):
        return 4

    def get_maxima_cantidad_materias_por_cuatrimestre(self):
        return 3

    #################################################################
    ##                  Verificacion de resultados                 ##
    #################################################################

    def verificar_resultados(self, parametros, resultados):
        self.todas_las_materias_obligatorias_se_hacen(parametros, resultados)
        self.los_cuatrimestres_de_las_correlativas_son_menores(parametros, resultados)
        self.los_creditos_minimos_acumulados_son_mayores_que_los_necesarios_para_cursar_la_materia(parametros, resultados)

if __name__ == "__main__":
    test_a_ejecutar = Test_creditos_minimos_para_cursar()
    test_a_ejecutar.ejecutar_test()