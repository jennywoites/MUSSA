from TestConHorariosPDF import TestConHorariosPDF

import sys
sys.path.append("../app")

from GeneradorCodigoPulp import generar_archivo_pulp
from ParametrosDAO import Parametros
from Constantes import *
from my_utils import get_str_cuatrimestre

from Materia import Materia
from Curso import Curso
from Horario import Horario

class Test_plan_licenciatura_con_horarios_cargados_desde_pdf_fiuba(TestConHorariosPDF):

    def get_nombre_test(self):
        return "test_plan_licenciatura_con_horarios_cargados_desde_pdf_fiuba"

    def get_plan_carrera_test(self):
        return self.plan_carrera

    def get_materias_test(self):
        return self.materias

    def get_horarios_test(self):
        return self.horarios

    def get_horarios_no_permitidos_test(self):
        return []

    def get_creditos_minimos_electivas(self):
        return 40

    def get_maxima_cantidad_cuatrimestres(self):
        return 18 #Plan tiene 4,5 años == 9 cuatrimestres. Puede llevar hasta el doble: 18

    def get_maxima_cantidad_materias_por_cuatrimestre(self):
        return 4

    #################################################################
    ##                  Verificacion de resultados                 ##
    #################################################################

    def los_creditos_en_electivas_cumplen_con_el_minimo(self, parametros, resultados):
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

        assert(creditos_acumulados >= parametros.creditos_minimos_electivas)       


    def verificar_resultados(self, parametros, resultados):
        self.todas_las_materias_obligatorias_se_hacen(parametros, resultados)
        self.los_cuatrimestres_de_las_correlativas_son_menores(parametros,resultados)
        self.los_creditos_en_electivas_cumplen_con_el_minimo(parametros, resultados)


if __name__ == "__main__":
    test_a_ejecutar = Test_plan_licenciatura_con_horarios_cargados_desde_pdf_fiuba()
    
    #for materia in test_a_ejecutar.horarios:
    #    horarios = "[ "
    #    for horario in test_a_ejecutar.horarios[materia]:
    #        horarios += str(horario) + " - "
    #    print("{} - {}".format(materia, horarios[:-3] + " ]"))

    #for materia in test_a_ejecutar.materias:
    #    if materia not in test_a_ejecutar.horarios:
    #        print(materia)
    #        input("No esta en horarios")

    test_a_ejecutar.ejecutar_test()