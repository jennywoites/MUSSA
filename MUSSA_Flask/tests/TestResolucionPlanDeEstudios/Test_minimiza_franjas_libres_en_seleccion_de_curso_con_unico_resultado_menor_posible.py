if __name__ == "__main__":
    import sys
    sys.path.append("../..")

from tests.TestResolucionPlanDeEstudios.TestPulp import TestPulp

from app.API_Rest.GeneradorPlanCarreras.GeneradorCodigoPulp import generar_archivo_pulp
from app.API_Rest.GeneradorPlanCarreras.ParametrosDAO import Parametros
from app.API_Rest.GeneradorPlanCarreras.Constantes import *
from app.API_Rest.GeneradorPlanCarreras.my_utils import get_str_cuatrimestre

from app.API_Rest.GeneradorPlanCarreras.modelos.Materia import Materia
from app.API_Rest.GeneradorPlanCarreras.modelos.Curso import Curso
from app.API_Rest.GeneradorPlanCarreras.modelos.Horario import Horario

class Test_minimiza_franjas_libres_en_seleccion_de_curso_con_unico_resultado_menor_posible(TestPulp):

    def get_nombre_test(self):
        return "test_minimiza_franjas_libres_en_seleccion_de_curso_con_unico_resultado_menor_posible"

    def get_plan_carrera_test(self):
        return {
            "A": [],
            "B": []
        }

    def get_materias_test(self):
        return {
            "A": Materia("A", "A", 1, OBLIGATORIA, 0, []),
            "B": Materia("B", "B", 1, OBLIGATORIA, 0, [])
        }

    def get_horarios_test(self):
        return {
            "A": [Curso("A", "Curso1A", [Horario(LUNES, 7, 8.5)], True, True), Curso("A", "Curso2A", [Horario(LUNES, 7.5, 8.5), Horario(LUNES, 9, 10.5)], True, True)],
            "B": [Curso("B", "Curso1B", [Horario(LUNES, 7, 8.5)], True, True), Curso("B", "Curso2B", [Horario(LUNES, 8.5, 9), Horario(LUNES, 11, 11.5)], True, True), Curso("B", "Curso3B", [Horario(LUNES, 10, 12)], True, True), Curso("B", "Curso4B", [Horario(LUNES, 11, 12)], True, True)],
        }

    def get_horarios_no_permitidos_test(self):
        return []

    def get_dias(self):
        return [LUNES]

    def get_creditos_minimos_electivas(self):
        return 0

    def get_franjas_minima_y_maxima(self):
        return 1, 12

    def get_maxima_cantidad_cuatrimestres(self):
        return 1

    def get_maxima_cantidad_materias_por_cuatrimestre(self):
        return 2

    #################################################################
    ##                  Verificacion de resultados                 ##
    #################################################################

    def la_cantidad_de_cuatrimestres_es_optima(self, parametros, resultados):
        assert(resultados["TOTAL_CUATRIMESTRES"] == 1)


    def las_materias_se_hacen_en_el_cuatrimestre_correspondiente(self, parametros, resultados):
        #Materia A
        assert(resultados["CA"] == 1)

        assert(resultados["Y_A_01"] == 1)

        #Materia B
        assert(resultados["CB"] == 1)

        assert(resultados["Y_B_01"] == 1)


    def los_cursos_se_eligieron_correctamente(self, parametros, resultados):
        #Solo hay R de los horarios disponibles, por eso no estan todas las combinaciones

        #Curso 1A
        assert(resultados["H_A_Curso1A_01"] == 0)
        assert(resultados["R_A_Curso1A_LUNES_1_01"] == 0)
        assert(resultados["R_A_Curso1A_LUNES_2_01"] == 0)
        assert(resultados["R_A_Curso1A_LUNES_3_01"] == 0)

        #Curso 2A
        assert(resultados["H_A_Curso2A_01"] == 1)
        assert(resultados["R_A_Curso2A_LUNES_2_01"] == 1)
        assert(resultados["R_A_Curso2A_LUNES_3_01"] == 1)
        assert(resultados["R_A_Curso2A_LUNES_5_01"] == 1)
        assert(resultados["R_A_Curso2A_LUNES_6_01"] == 1)
        assert(resultados["R_A_Curso2A_LUNES_7_01"] == 1)

        #Curso 1B
        assert(resultados["H_B_Curso1B_01"] == 0)
        assert(resultados["R_B_Curso1B_LUNES_1_01"] == 0)
        assert(resultados["R_B_Curso1B_LUNES_2_01"] == 0)
        assert(resultados["R_B_Curso1B_LUNES_3_01"] == 0)

        #Curso 2B
        assert(resultados["H_B_Curso2B_01"] == 1)
        assert(resultados["R_B_Curso2B_LUNES_4_01"] == 1)
        assert(resultados["R_B_Curso2B_LUNES_9_01"] == 1)

        #Curso 3B
        assert(resultados["H_B_Curso3B_01"] == 0)
        assert(resultados["R_B_Curso3B_LUNES_7_01"] == 0)
        assert(resultados["R_B_Curso3B_LUNES_8_01"] == 0)
        assert(resultados["R_B_Curso3B_LUNES_9_01"] == 0)
        assert(resultados["R_B_Curso3B_LUNES_10_01"] == 0)
        
        #Curso 4B
        assert(resultados["H_B_Curso4B_01"] == 0)
        assert(resultados["R_B_Curso4B_LUNES_9_01"] == 0)
        assert(resultados["R_B_Curso4B_LUNES_10_01"] == 0)
 

    def los_creditos_acumulados_son_correctos(self, parametros, resultados):
        materias = parametros.materias

        #Al finalizar el cuatrimestre 1, se acumularon creditos
        creditos_cuatrimestre_1 = 0
        creditos_cuatrimestre_1 += materias["A"].creditos
        creditos_cuatrimestre_1 += materias["B"].creditos
        assert(resultados["CRED01"] == creditos_cuatrimestre_1)


    def las_horas_libres_se_calculan_correctamente(self, parametros, resultados):

        #Los cursos A2-B2 tiene las franjas [2,3] [4] [5,6,7] [9]
        assert(resultados["LUNES_1_01"] == 0)
        assert(resultados["LUNES_2_01"] == 1)
        assert(resultados["LUNES_3_01"] == 1)
        assert(resultados["LUNES_4_01"] == 1)
        assert(resultados["LUNES_5_01"] == 1)
        assert(resultados["LUNES_6_01"] == 1)
        assert(resultados["LUNES_7_01"] == 1)
        assert(resultados["LUNES_8_01"] == 0)
        assert(resultados["LUNES_9_01"] == 1)
        assert(resultados["LUNES_10_01"] == 0)
        assert(resultados["LUNES_11_01"] == 0)
        assert(resultados["LUNES_12_01"] == 0)

        assert(resultados["OCUPADO_LUNES_01"] == 1)
        assert(resultados["MINIMA_FRANJA_LUNES_01"] == 2)        
        assert(resultados["MAXIMA_FRANJA_LUNES_01"] == 9)
        assert(resultados["HORAS_LIBRES_LUNES_01"] == 1)

        #Totales
        assert(resultados["HORAS_LIBRES_TOTALES"] == 1)


    def verificar_resultados(self, parametros, resultados):
        self.la_cantidad_de_cuatrimestres_es_optima(parametros, resultados)
        self.los_cursos_se_eligieron_correctamente(parametros, resultados)
        self.las_materias_se_hacen_en_el_cuatrimestre_correspondiente(parametros, resultados)
        self.los_creditos_acumulados_son_correctos(parametros, resultados)
        self.las_horas_libres_se_calculan_correctamente(parametros, resultados)


if __name__ == "__main__":
    test_a_ejecutar = Test_minimiza_franjas_libres_en_seleccion_de_curso_con_unico_resultado_menor_posible()
    test_a_ejecutar.ejecutar_test()