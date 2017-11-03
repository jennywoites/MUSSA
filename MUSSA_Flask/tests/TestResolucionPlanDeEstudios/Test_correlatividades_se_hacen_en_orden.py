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

class Test_correlatividades_se_hacen_en_orden(TestPulp):

    def get_nombre_test(self):
        return "test_correlatividades_se_hacen_en_orden"

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
        "A": [Curso("A", "Curso1A", [Horario(LUNES, 7, 8)], True, True)],
        "B": [Curso("B", "Curso1B", [Horario(LUNES, 8, 9)], True, True)],
        "C": [Curso("C", "Curso1C", [Horario(LUNES, 9, 10)], True, True)],
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