from TestPulp import TestPulp

import sys
sys.path.append("../app")

from GeneradorCodigoPulp import generar_archivo_pulp
from ParametrosDAO import Parametros
from Constantes import *

from Materia import Materia
from Curso import Curso
from Horario import Horario

COMBINACION_CURSOS_A3_B1 = 0
COMBINACION_CURSOS_A3_B3 = 1

class Test_minimiza_franjas_libres_en_seleccion_de_curso_con_dos_posibles_resultados(TestPulp):

    def get_nombre_test(self):
        return "test_minimiza_franjas_libres_en_seleccion_de_curso_con_dos_posibles_resultados"

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
        "A": [Curso("A", "Curso1A", [Horario(LUNES, 7, 8.5)]), Curso("A", "Curso2A", [Horario(LUNES, 7.5, 8.5), Horario(LUNES, 9, 10.5)]), Curso("A", "Curso3A", [Horario(LUNES, 8.5, 10)])],
        "B": [Curso("B", "Curso1B", [Horario(LUNES, 7, 8.5)]), Curso("B", "Curso2B", [Horario(LUNES, 8.5, 9), Horario(LUNES, 11, 11.5)]), Curso("B", "Curso3B", [Horario(LUNES, 10, 12)]), Curso("B", "Curso4B", [Horario(LUNES, 11, 12)])],
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

    def numero_combinacion_seleccionada(self, resultados):
        if resultados["H_A_Curso3A_1"] and resultados["H_B_Curso1B_1"] :
            return COMBINACION_CURSOS_A3_B1

        if resultados["H_A_Curso3A_1"] and resultados["H_B_Curso3B_1"] :
            return COMBINACION_CURSOS_A3_B3

        return -1


    def la_cantidad_de_cuatrimestres_es_optima(self, parametros, resultados):
        assert(resultados["TOTAL_CUATRIMESTRES"] == 1)


    def las_materias_se_hacen_en_el_cuatrimestre_correspondiente(self, parametros, resultados):
        #Materia A
        assert(resultados["CA"] == 1)

        assert(resultados["Y_A_1"] == 1)

        #Materia B
        assert(resultados["CB"] == 1)

        assert(resultados["Y_B_1"] == 1)


    def los_cursos_se_eligieron_correctamente(self, parametros, resultados):
        combinacion = self.numero_combinacion_seleccionada(resultados)

        if combinacion == COMBINACION_CURSOS_A3_B1:
            self.los_cursos_se_eligieron_correctamente_A3_B1(parametros, resultados)
        elif combinacion == COMBINACION_CURSOS_A3_B3:
            self.los_cursos_se_eligieron_correctamente_A3_B3(parametros, resultados)
        else:
            raise Exception("No se eligieron las opciones correctas")


    def los_cursos_se_eligieron_correctamente_A3_B1(self, parametros, resultados):
        #Solo hay R de los horarios disponibles, por eso no estan todas las combinaciones

        #Curso 1A
        assert(resultados["H_A_Curso1A_1"] == 0)
        assert(resultados["R_A_Curso1A_LUNES_1_1"] == 0)
        assert(resultados["R_A_Curso1A_LUNES_2_1"] == 0)
        assert(resultados["R_A_Curso1A_LUNES_3_1"] == 0)

        #Curso 2A
        assert(resultados["H_A_Curso2A_1"] == 0)
        assert(resultados["R_A_Curso2A_LUNES_2_1"] == 0)
        assert(resultados["R_A_Curso2A_LUNES_3_1"] == 0)
        assert(resultados["R_A_Curso2A_LUNES_5_1"] == 0)
        assert(resultados["R_A_Curso2A_LUNES_6_1"] == 0)
        assert(resultados["R_A_Curso2A_LUNES_7_1"] == 0)

        #Curso 3A
        assert(resultados["H_A_Curso3A_1"] == 1)
        assert(resultados["R_A_Curso3A_LUNES_4_1"] == 1)
        assert(resultados["R_A_Curso3A_LUNES_5_1"] == 1)
        assert(resultados["R_A_Curso3A_LUNES_6_1"] == 1)

        #Curso 1B
        assert(resultados["H_B_Curso1B_1"] == 1)
        assert(resultados["R_B_Curso1B_LUNES_1_1"] == 1)
        assert(resultados["R_B_Curso1B_LUNES_2_1"] == 1)
        assert(resultados["R_B_Curso1B_LUNES_3_1"] == 1)

        #Curso 2B
        assert(resultados["H_B_Curso2B_1"] == 0)
        assert(resultados["R_B_Curso2B_LUNES_4_1"] == 0)
        assert(resultados["R_B_Curso2B_LUNES_9_1"] == 0)

        #Curso 3B
        assert(resultados["H_B_Curso3B_1"] == 0)
        assert(resultados["R_B_Curso3B_LUNES_7_1"] == 0)
        assert(resultados["R_B_Curso3B_LUNES_8_1"] == 0)
        assert(resultados["R_B_Curso3B_LUNES_9_1"] == 0)
        assert(resultados["R_B_Curso3B_LUNES_10_1"] == 0)
        
        #Curso 4B
        assert(resultados["H_B_Curso4B_1"] == 0)
        assert(resultados["R_B_Curso4B_LUNES_9_1"] == 0)
        assert(resultados["R_B_Curso4B_LUNES_10_1"] == 0)

 
    def los_cursos_se_eligieron_correctamente_A3_B3(self, parametros, resultados):
        #Solo hay R de los horarios disponibles, por eso no estan todas las combinaciones

        #Curso 1A
        assert(resultados["H_A_Curso1A_1"] == 0)
        assert(resultados["R_A_Curso1A_LUNES_1_1"] == 0)
        assert(resultados["R_A_Curso1A_LUNES_2_1"] == 0)
        assert(resultados["R_A_Curso1A_LUNES_3_1"] == 0)

        #Curso 2A
        assert(resultados["H_A_Curso2A_1"] == 0)
        assert(resultados["R_A_Curso2A_LUNES_2_1"] == 0)
        assert(resultados["R_A_Curso2A_LUNES_3_1"] == 0)
        assert(resultados["R_A_Curso2A_LUNES_5_1"] == 0)
        assert(resultados["R_A_Curso2A_LUNES_6_1"] == 0)
        assert(resultados["R_A_Curso2A_LUNES_7_1"] == 0)

        #Curso 3A
        assert(resultados["H_A_Curso3A_1"] == 1)
        assert(resultados["R_A_Curso3A_LUNES_4_1"] == 1)
        assert(resultados["R_A_Curso3A_LUNES_5_1"] == 1)
        assert(resultados["R_A_Curso3A_LUNES_6_1"] == 1)

        #Curso 1B
        assert(resultados["H_B_Curso1B_1"] == 1)
        assert(resultados["R_B_Curso1B_LUNES_1_1"] == 1)
        assert(resultados["R_B_Curso1B_LUNES_2_1"] == 1)
        assert(resultados["R_B_Curso1B_LUNES_3_1"] == 1)

        #Curso 2B
        assert(resultados["H_B_Curso2B_1"] == 0)
        assert(resultados["R_B_Curso2B_LUNES_4_1"] == 0)
        assert(resultados["R_B_Curso2B_LUNES_9_1"] == 0)

        #Curso 3B
        assert(resultados["H_B_Curso3B_1"] == 1)
        assert(resultados["R_B_Curso3B_LUNES_7_1"] == 1)
        assert(resultados["R_B_Curso3B_LUNES_8_1"] == 1)
        assert(resultados["R_B_Curso3B_LUNES_9_1"] == 1)
        assert(resultados["R_B_Curso3B_LUNES_10_1"] == 1)

        #Curso 4B
        assert(resultados["H_B_Curso4B_1"] == 0)
        assert(resultados["R_B_Curso4B_LUNES_9_1"] == 0)
        assert(resultados["R_B_Curso4B_LUNES_10_1"] == 0)


    def los_creditos_acumulados_son_correctos(self, parametros, resultados):
        materias = parametros.materias

        #El cuatrimetre inicial siempre acumula 0:
        assert(resultados["CRED0"] == 0)

        #Al finalizar el cuatrimestre 1, se acumularon creditos
        creditos_cuatrimestre_1 = 0
        creditos_cuatrimestre_1 += materias["A"].creditos
        creditos_cuatrimestre_1 += materias["B"].creditos
        assert(resultados["CRED1"] == creditos_cuatrimestre_1)


    def las_horas_libres_se_calculan_correctamente(self, parametros, resultados):
        combinacion = self.numero_combinacion_seleccionada(resultados)

        if combinacion == COMBINACION_CURSOS_A3_B1:
            self.las_horas_libres_se_calculan_correctamente_A3_B1(parametros, resultados)
        elif combinacion == COMBINACION_CURSOS_A3_B3:
            self.las_horas_libres_se_calculan_correctamente_A3_B3(parametros, resultados)
        else:
            raise Exception("No se eligieron las opciones correctas")


    def las_horas_libres_se_calculan_correctamente_A3_B1(self, parametros, resultados):
        #Los cursos A3-B3 tiene las franjas [4,5,6] [1,2,3]
        assert(resultados["LUNES_1_1"] == 1)
        assert(resultados["LUNES_2_1"] == 1)
        assert(resultados["LUNES_3_1"] == 1)
        assert(resultados["LUNES_4_1"] == 1)
        assert(resultados["LUNES_5_1"] == 1)
        assert(resultados["LUNES_6_1"] == 1)
        assert(resultados["LUNES_7_1"] == 0)
        assert(resultados["LUNES_8_1"] == 0)
        assert(resultados["LUNES_9_1"] == 0)
        assert(resultados["LUNES_10_1"] == 0)
        assert(resultados["LUNES_11_1"] == 0)
        assert(resultados["LUNES_12_1"] == 0)

        assert(resultados["OCUPADO_LUNES_1"] == 1)
        assert(resultados["MINIMA_FRANJA_LUNES_1"] == 1)        
        assert(resultados["MAXIMA_FRANJA_LUNES_1"] == 6)
        assert(resultados["HORAS_LIBRES_LUNES_1"] == 0)

        #Totales
        assert(resultados["HORAS_LIBRES_TOTALES"] == 0)


    def las_horas_libres_se_calculan_correctamente_A3_B3(self, parametros, resultados):
        #Los cursos A3-B3 tiene las franjas [4,5,6] [7,8,9,10]
        assert(resultados["LUNES_1_1"] == 0)
        assert(resultados["LUNES_2_1"] == 0)
        assert(resultados["LUNES_3_1"] == 0)
        assert(resultados["LUNES_4_1"] == 1)
        assert(resultados["LUNES_5_1"] == 1)
        assert(resultados["LUNES_6_1"] == 1)
        assert(resultados["LUNES_7_1"] == 1)
        assert(resultados["LUNES_8_1"] == 1)
        assert(resultados["LUNES_9_1"] == 1)
        assert(resultados["LUNES_10_1"] == 1)
        assert(resultados["LUNES_11_1"] == 0)
        assert(resultados["LUNES_12_1"] == 0)

        assert(resultados["OCUPADO_LUNES_1"] == 1)
        assert(resultados["MINIMA_FRANJA_LUNES_1"] == 4)        
        assert(resultados["MAXIMA_FRANJA_LUNES_1"] == 10)
        assert(resultados["HORAS_LIBRES_LUNES_1"] == 0)

        #Totales
        assert(resultados["HORAS_LIBRES_TOTALES"] == 0)


    def verificar_resultados(self, parametros, resultados):
        self.la_cantidad_de_cuatrimestres_es_optima(parametros, resultados)
        self.los_cursos_se_eligieron_correctamente(parametros, resultados)
        self.las_materias_se_hacen_en_el_cuatrimestre_correspondiente(parametros, resultados)
        self.los_creditos_acumulados_son_correctos(parametros, resultados)
        self.las_horas_libres_se_calculan_correctamente(parametros, resultados)


if __name__ == "__main__":
    test_a_ejecutar = Test_minimiza_franjas_libres_en_seleccion_de_curso_con_dos_posibles_resultados()
    test_a_ejecutar.ejecutar_test()