from TestPulp import TestPulp

import sys
sys.path.append("../app")

from GeneradorCodigoPulp import generar_archivo_pulp
from ParametrosDAO import Parametros
from Constantes import *
from my_utils import get_str_cuatrimestre

from Materia import Materia
from Curso import Curso
from Horario import Horario

class Test_plan_licenciatura_con_unico_horario_por_materia_no_superpuestos(TestPulp):

    def __init__(self):
        self.materias = {}
        self.plan_carrera = {}
        self.horarios = {}
        self.cargar_datos_materias()

    def get_nombre_test(self):
        return "test_plan_licenciatura_con_unico_horario_por_materia_no_superpuestos"

    def get_plan_carrera_test(self):
        return self.plan_carrera

    def get_materias_test(self):
        return self.materias

    def get_horarios_test(self):
        return self.horarios

    def get_dias(self):
        return [LUNES, MARTES, MIERCOLES, JUEVES]

    def get_horarios_no_permitidos_test(self):
        return []

    def get_creditos_minimos_electivas(self):
        return 0

    def get_maxima_cantidad_cuatrimestres(self):
        return 6

    def get_maxima_cantidad_materias_por_cuatrimestre(self):
        return 4

    #################################################################
    ##                  Carga de materias desde csv                ##
    #################################################################

    def cargar_datos_materias(self):
        RUTA = "CSV_TestFiles/Test_plan_licenciatura_con_unico_horario_por_materia_no_superpuestos.csv"

        dia = LUNES
        horario = 7 #7am

        primera = True
        with open(RUTA, 'r') as f:
            for linea in f:
                if primera:
                    primera = False
                    continue

                linea = linea.rstrip()
                dia, horario = self.procesar_materia(linea, dia, horario)


    def procesar_materia(self, linea, dia, hora):
        codigo, nombre, creditos, tipo, cred_minimos, correlativas = linea.split(",")

        creditos = int(creditos)
        cred_minimos = int(cred_minimos)

        correlativas = correlativas.split("-")
        if not correlativas or correlativas[0]=='':
            correlativas = []

        tipo = self.obtener_tipo_de_materia(tipo)

        if tipo == ELECTIVA: #No se consideran las materias electivas
            return dia, hora

        materia = Materia(
            codigo = codigo,
            nombre = nombre,
            creditos = creditos,
            tipo = tipo,
            cred_min = cred_minimos,
            correlativas = correlativas
        )

        horarios_curso = [Curso(codigo, "Curso" + codigo, [Horario(dia, hora, hora + 1)])]

        self.materias[codigo] = materia
        self.horarios[codigo] = horarios_curso
        
        if codigo not in self.plan_carrera:
            self.plan_carrera[codigo] = []

        for correlativa in correlativas:
            l_adyacentes = self.plan_carrera.get(correlativa, [])
            l_adyacentes.append(codigo)
            self.plan_carrera[correlativa] = l_adyacentes

        return self.proximo_horario(dia, hora)


    def obtener_tipo_de_materia(self, tipo):
        if tipo == "ELECTIVA":
            return ELECTIVA
        
        return OBLIGATORIA


    def proximo_horario(self, dia, franja):
        franja += 1
        if franja >= 21: #Ultima franja considerada 21hs
            franja = 7 #7am
            dia = self.avanzar_dia(dia)
        return dia, franja


    def avanzar_dia(self, dia):
        siguientes = {
            LUNES: MARTES,
            MARTES: MIERCOLES,
            MIERCOLES: JUEVES,
            JUEVES: VIERNES,
            VIERNES: SABADO,
            SABADO: LUNES
        }
        return siguientes[dia]


    #################################################################
    ##                  Verificacion de resultados                 ##
    #################################################################

    def verificar_todas_las_materias_obligatorias_se_hacen(self, parametros, resultados):
        for codigo in parametros.materias:
            materia = parametros.materias[codigo]
            if materia.tipo == ELECTIVA:
                continue

            cont = 0
            for cuatri in range(1, parametros.max_cuatrimestres + 1):
                variable = "Y_{}_{}".format(materia.codigo, get_str_cuatrimestre(cuatri))
                cont += resultados[variable]

            assert(cont == 1)


    def los_cuatrimestres_de_las_correlativas_son_menores(self, parametros, resultados):
        for codigo in parametros.materias:
            materia = parametros.materias[codigo]
            cod_actual = "C" + materia.codigo
            for cor_materia in materia.correlativas:
                cod_corr = "C" + cor_materia
                assert(resultados[cod_actual] > resultados[cod_corr])


    def verificar_resultados(self, parametros, resultados):
        self.verificar_todas_las_materias_obligatorias_se_hacen(parametros, resultados)
        self.los_cuatrimestres_de_las_correlativas_son_menores(parametros,resultados)


if __name__ == "__main__":
    test_a_ejecutar = Test_plan_licenciatura_con_unico_horario_por_materia_no_superpuestos()
    test_a_ejecutar.ejecutar_test()