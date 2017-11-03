from tests.TestResolucionPlanDeEstudios.TestPulp import TestPulp

from app.API_Rest.GeneradorPlanCarreras.GeneradorCodigoPulp import generar_archivo_pulp
from app.API_Rest.GeneradorPlanCarreras.ParametrosDTO import Parametros
from app.API_Rest.GeneradorPlanCarreras.Constantes import *
from app.API_Rest.GeneradorPlanCarreras.my_utils import get_str_cuatrimestre

from app.API_Rest.GeneradorPlanCarreras.modelos.Materia import Materia
from app.API_Rest.GeneradorPlanCarreras.modelos.Curso import Curso
from app.API_Rest.GeneradorPlanCarreras.modelos.Horario import Horario

class TestDesdeArchivoCSV(TestPulp):

    def __init__(self):
        self.materias = {}
        self.plan_carrera = {}
        self.horarios = {}
        self.cargar_datos_materias()

    #################################################################
    ##                  Carga de materias desde csv                ##
    #################################################################

    def cargar_datos_materias(self):
        RUTA = "CSV_TestFiles/" + self.get_nombre_test() + ".csv"

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

        materia = Materia(
            codigo = codigo,
            nombre = nombre,
            creditos = creditos,
            tipo = tipo,
            cred_min = cred_minimos,
            correlativas = correlativas
        )

        horarios_curso = [Curso(codigo, "Curso" + codigo, [Horario(dia, hora, hora + 1)], True, True)]

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


    def get_franjas_minima_y_maxima(self):
        return 1, 33

    def proximo_horario(self, dia, franja):
        franja += 1
        if franja >= 23: #Ultima franja considerada 23hs
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