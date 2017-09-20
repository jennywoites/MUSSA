from TestPulp import TestPulp

import sys
sys.path.append("../app")

from GeneradorCodigoPulp import generar_archivo_pulp
from ParametrosDAO import Parametros
from Constantes import *

from Materia import Materia
from Curso import Curso
from Horario import Horario

class Test_creditos_minimos_para_cursar(TestPulp):

    def get_nombre_test(self):
        return "test_creditos_minimos_para_cursar"

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
            "A": Materia("A", "A", 2, OBLIGATORIA, 0, []),
            "B": Materia("B", "B", 3, OBLIGATORIA, 0, []),
            "C": Materia("C", "C", 2, OBLIGATORIA, 0, ["A"]),
            "D": Materia("D", "D", 1, OBLIGATORIA, 0, ["B", "C"]),
            "E": Materia("E", "E", 4, OBLIGATORIA, 7, []),
        }

    def get_horarios_test(self):
        return {
            "A": [Curso("A", "Curso1A", [Horario(LUNES, 7, 10),Horario(MARTES,8,12)]), Curso("A", "Curso2A", [Horario(JUEVES, 8, 15),Horario(SABADO,9,13)])],
            "B": [Curso("B", "Curso1B", [Horario(LUNES, 7, 10),Horario(JUEVES,7,10)])],
            "C": [Curso("C", "Curso1C", [Horario(LUNES, 12, 15),Horario(MIERCOLES,8,12)])],
            "D": [Curso("D", "Curso1D", [Horario(LUNES, 7, 10),Horario(VIERNES,8,12)]), Curso("D", "Curso2D", [Horario(LUNES, 12, 15),Horario(MIERCOLES,8,9)]), Curso("D", "Curso3D", [Horario(JUEVES, 12, 15),Horario(VIERNES,12,15)]), Curso("D", "Curso4D", [Horario(MARTES, 9, 11),Horario(JUEVES,10.5,12.5)])],
            "E": [Curso("E", "Curso1E", [Horario(LUNES, 7, 10),Horario(VIERNES,8,11)]), Curso("E", "Curso2E", [Horario(MARTES, 8, 15)])],
        }

    def get_horarios_no_permitidos_test(self):
        return []

    def get_creditos_minimos_electivas(self):
        return 0

    def get_franjas_minima_y_maxima(self):
        return 1, 33

    def get_maxima_cantidad_cuatrimestres(self):
        return 5

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
            cod_actual = "C" + materia.codigo
            for cor_materia in materia.correlativas:
                cod_corr = "C" + cor_materia
                assert(resultados[cod_actual] > resultados[cod_corr])


    def los_creditos_minimos_acumulados_son_mayores_que_los_necesarios_para_cursar_la_materia(self, parametros, resultados):
        for codigo in parametros.materias:
            materia = parametros.materia[codigo]
            cuatrimestre_cursada = resultados["C{}".format(codigo)]
            cuatri_anterior = cuatrimestre_cursada - 1
            creditos_acumulados  = resultados["CRED{}".format(cuatri_anterior)] if cuatri_anterior > 0 else 0
            assert(creditos_acumulados >= materia.creditos_minimos_aprobados)


    def verificar_resultados(self, parametros, resultados):
        self.todas_las_materias_obligatorias_se_hacen(parametros, resultados)
        self.los_cuatrimestres_de_las_correlativas_son_menores(parametros, resultados)


if __name__ == "__main__":
    test_a_ejecutar = Test_creditos_minimos_para_cursar()
    test_a_ejecutar.ejecutar_test()