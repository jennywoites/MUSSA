if __name__ == "__main__":
    import sys

    sys.path.append("../..")

from tests.TestResolucionPlanDeEstudios.TestDesdeArchivoCSV import TestDesdeArchivoCSV


class Test_plan_licenciatura_con_unico_horario_por_materia_no_superpuestos_con_materias_electivas(TestDesdeArchivoCSV):
    def get_nombre_test(self):
        return "test_plan_licenciatura_con_unico_horario_por_materia_no_superpuestos_con_materias_electivas"

    def get_materias_test(self):
        return self.materias

    def get_horarios_test(self):
        return self.horarios

    def get_creditos_minimos_electivas(self):
        return 10

    def get_maxima_cantidad_cuatrimestres(self):
        return 12

    def get_maxima_cantidad_materias_por_cuatrimestre(self):
        return 4

    #################################################################
    ##                  Verificacion de resultados                 ##
    #################################################################

    def verificar_resultados(self, parametros, resultados):
        self.todas_las_materias_obligatorias_se_hacen(parametros, resultados)
        self.los_cuatrimestres_de_las_correlativas_son_menores(parametros, resultados)
        self.los_creditos_en_electivas_cumplen_con_el_minimo(parametros, resultados)


if __name__ == "__main__":
    test_a_ejecutar = Test_plan_licenciatura_con_unico_horario_por_materia_no_superpuestos_con_materias_electivas()
    test_a_ejecutar.ejecutar_test()
