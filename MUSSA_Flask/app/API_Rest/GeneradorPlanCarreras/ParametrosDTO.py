from app.API_Rest.GeneradorPlanCarreras.Constantes import *

CREDITOS_MINIMOS_ELECTIVAS = 5
NUM_EJEMPLO_MATERIAS = 4

ARCHIVO_PULP = "pulp_generado.py"
ARCHIVO_PULP_OPTIMIZADO = "pulp_optimizado.py"
ARCHIVO_RESULTADO_PULP = "resultados_pulp_001.csv"

DIAS = [LUNES, MARTES, MIERCOLES, JUEVES, VIERNES, SABADO]

FRANJA_MIN = 1 #Corresponde al horario de 07:00 a 07:30 --> 1
FRANJA_MAX = 33 #Corresponde al horario de 23:00 a 23:30 --> 33

MAX_CUATRIMESTRES_TOTALES = 10
MAX_CANTIDAD_MATERIAS_POR_CUATRIMESTRE = 3

class Parametros:

    def __init__(self):
        self.set_valores_default()

    def set_valores_default(self):
        # Si el primer cuatrimestre es 1 entonces es True.
        # Si el primer cuatrimestres es 2 entonces es False
        self.primer_cuatrimestre_es_impar = True

        self.plan = {}
        self.materias = {}
        self.horarios = {}
        self.horarios_no_permitidos = []
        self.creditos_minimos_electivas = CREDITOS_MINIMOS_ELECTIVAS

        self.nombre_archivo_pulp = ARCHIVO_PULP
        self.nombre_archivo_resultados_pulp = ARCHIVO_RESULTADO_PULP
        self.nombre_archivo_pulp_optimizado = ARCHIVO_PULP_OPTIMIZADO

        self.set_franjas(FRANJA_MIN, FRANJA_MAX)
        self.dias = DIAS
        self.max_cuatrimestres = MAX_CUATRIMESTRES_TOTALES
        self.max_cant_materias_por_cuatrimestre = MAX_CANTIDAD_MATERIAS_POR_CUATRIMESTRE

        #Nuevos parametros a agregar

        self.materias_CBC_pendientes = []
        self.orientacion = ''
        self.id_carrera = ''
        self.max_horas_cursada = 0
        self.max_horas_extras = 0
        self.cuatrimestre_minimo_para_materia = {}
        self.tematicas = {}
        self.cuatrimestre_inicio = 1
        self.anio_inicio = '2018'

        #Estas materias son largas y se las divide en dos cuatrimestres pero es la misma materia
        self.materia_trabajo_final = []


    def set_franjas(self, minima, maxima):
        self.franja_minima = minima
        self.franja_maxima = maxima