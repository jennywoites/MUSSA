from app.API_Rest.GeneradorPlanCarreras.Constantes import *
from app.API_Rest.GeneradorPlanCarreras.modelos.Curso import Curso
from app.API_Rest.GeneradorPlanCarreras.modelos.Horario import Horario
from app.API_Rest.GeneradorPlanCarreras.modelos.Materia import Materia
from tests.TestResolucionPlanDeEstudios.TestPulp import TestPulp


class TestDesdeArchivoCSV(TestPulp):
    def __init__(self):
        self.materias = {}
        self.horarios = {}

        self.codigo_a_id = {}
        self.ultimo_id_materia = 0
        self.ultimo_id_curso = 0

        self.cargar_datos_materias()
        self.convertir_codigos_correlativas_por_ids()

    #################################################################
    ##                  Carga de materias desde csv                ##
    #################################################################

    def cargar_datos_materias(self):
        RUTA = "CSV_TestFiles/" + self.get_nombre_test() + ".csv"

        dia = LUNES
        horario = 7  # 7am

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
        if not correlativas or correlativas[0] == '':
            correlativas = []

        tipo = self.obtener_tipo_de_materia(tipo)

        self.ultimo_id_materia += 1

        materia = Materia(
            id_materia=self.ultimo_id_materia,
            codigo=codigo,
            nombre=nombre,
            creditos=creditos,
            tipo=tipo,
            cred_min=cred_minimos,
            correlativas=correlativas,
            tematicas_principales=[],
            medias_horas_extras_cursada=creditos * 2
        )

        self.codigo_a_id[materia.codigo] = materia.id_materia

        self.ultimo_id_curso += 1

        horarios_curso = [Curso(
            id_curso=self.ultimo_id_curso,
            cod_materia=codigo,
            nombre_curso="Curso" + codigo,
            horarios=[Horario(dia, hora, hora + 1)],
            se_dicta_primer_cuatrimestre=True,
            se_dicta_segundo_cuatrimestre=True,
            puntaje=0
        )]

        self.materias[materia.id_materia] = materia
        self.horarios[materia.id_materia] = horarios_curso

        return self.proximo_horario(dia, hora)

    def obtener_tipo_de_materia(self, tipo):
        if tipo == "ELECTIVA":
            return ELECTIVA

        return OBLIGATORIA

    def get_franjas_minima_y_maxima(self):
        return 1, 33

    def proximo_horario(self, dia, franja):
        franja += 1
        if franja >= 23:  # Ultima franja considerada 23hs
            franja = 7  # 7am
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

    def convertir_codigos_correlativas_por_ids(self):
        for id_materia in self.materias:
            materia = self.materias[id_materia]
            ids_correlativas = []
            for codigo_correlativa in materia.correlativas:
                ids_correlativas.append(self.codigo_a_id[codigo_correlativa])
            materia.correlativas = ids_correlativas