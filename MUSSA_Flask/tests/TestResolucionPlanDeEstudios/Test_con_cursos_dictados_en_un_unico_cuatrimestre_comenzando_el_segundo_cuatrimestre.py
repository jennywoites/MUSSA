if __name__ == "__main__":
    import sys
    sys.path.append("../..")

from tests.TestResolucionPlanDeEstudios.TestPulp import TestPulp

from app.API_Rest.GeneradorPlanCarreras.GeneradorCodigoPulp import generar_archivo_pulp
from app.API_Rest.GeneradorPlanCarreras.ParametrosDTO import Parametros
from app.API_Rest.GeneradorPlanCarreras.Constantes import *
from app.API_Rest.GeneradorPlanCarreras.my_utils import get_str_cuatrimestre

from app.API_Rest.GeneradorPlanCarreras.modelos.Materia import Materia
from app.API_Rest.GeneradorPlanCarreras.modelos.Curso import Curso
from app.API_Rest.GeneradorPlanCarreras.modelos.Horario import Horario

class Test_con_cursos_dictados_en_un_unico_cuatrimestre_comenzando_el_segundo_cuatrimestre(TestPulp):

    def get_nombre_test(self):
        return "test_con_cursos_dictados_en_un_unico_cuatrimestre_comenzando_el_segundo_cuatrimestre"

    def get_plan_carrera_test(self):
        return {
        "A": ["C"],
        "B": [],
        "C": [],
    }

    def get_materias_test(self):
        return {
        "A": Materia("A", "A", 1, OBLIGATORIA, 0, []),
        "B": Materia("B", "B", 1, OBLIGATORIA, 0, []),
        "C": Materia("C", "C", 1, OBLIGATORIA, 0, ["A"]),
    }

    def get_horarios_test(self):
        return {
        "A": [Curso("A", "Curso1A", [Horario(LUNES, 7, 8)], True, False), Curso("A", "Curso2A", [Horario(MARTES, 7, 8)], False, True)],
        "B": [Curso("B", "Curso1B", [Horario(LUNES, 8, 9)], False, True), Curso("B", "Curso2B", [Horario(MARTES, 8, 9)], True, False)],
        "C": [Curso("C", "Curso1C", [Horario(LUNES, 9, 10)], True, True)],
    }

    def get_horarios_no_permitidos_test(self):
        return []

    def get_dias(self):
        return [LUNES, MARTES]

    def get_creditos_minimos_electivas(self):
        return 0

    def get_franjas_minima_y_maxima(self):
        return 1, 10

    def get_maxima_cantidad_cuatrimestres(self):
        return 4

    def get_maxima_cantidad_materias_por_cuatrimestre(self):
        return 2

    def comienza_en_primer_cuatrimestre(self):
        return False


    #################################################################
    ##                  Verificacion de resultados                 ##
    #################################################################

    def no_se_elige_un_horario_no_disponible_ese_cuatrimestre(self, parametros, resultados):
        assert(resultados["H_A_Curso1A_01"] == 0)
        assert(resultados["H_B_Curso2B_01"] == 0)
        
        assert(resultados["H_A_Curso2A_02"] == 0)
        assert(resultados["H_B_Curso1B_02"] == 0)

        assert(resultados["H_A_Curso1A_03"] == 0)
        assert(resultados["H_B_Curso2B_03"] == 0)

        assert(resultados["H_A_Curso2A_04"] == 0)
        assert(resultados["H_B_Curso1B_04"] == 0)


    def verificar_resultados(self, parametros, resultados):
        self.todas_las_materias_obligatorias_se_hacen(parametros, resultados)
        self.los_cuatrimestres_de_las_correlativas_son_menores(parametros, resultados)
        self.no_se_elige_un_horario_no_disponible_ese_cuatrimestre(parametros, resultados)


if __name__ == "__main__":
    test_a_ejecutar = Test_con_cursos_dictados_en_un_unico_cuatrimestre_comenzando_el_segundo_cuatrimestre()
    test_a_ejecutar.ejecutar_test()