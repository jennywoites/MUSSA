from tests.TestResolucionPlanDeEstudios.TestDesdeArchivoCSV import TestDesdeArchivoCSV

from app.API_Rest.GeneradorPlanCarreras.GeneradorCodigoPulp import generar_archivo_pulp
from app.API_Rest.GeneradorPlanCarreras.ParametrosDTO import Parametros
from app.API_Rest.GeneradorPlanCarreras.Constantes import *
from app.API_Rest.GeneradorPlanCarreras.my_utils import get_str_cuatrimestre
from app.API_Rest.GeneradorPlanCarreras.ParserHorarios import parsear_pdf

from app.API_Rest.GeneradorPlanCarreras.modelos.Materia import Materia
from app.API_Rest.GeneradorPlanCarreras.modelos.Curso import Curso
from app.API_Rest.GeneradorPlanCarreras.modelos.Horario import Horario


class TestConHorariosPDF(TestDesdeArchivoCSV):

    def __init__(self):
        super().__init__()
        self.cargar_horarios_PDF()


    def cargar_horarios_PDF(self):
        RUTA = "Horarios_TestFiles/" + self.get_nombre_test() + ".pdf"
        self.horarios = self.horarios_PDF_to_horarios_DTO(RUTA)
        

    def horarios_PDF_to_horarios_DTO(self, ruta):
        horariosDTO = {}
        horarios = parsear_pdf(ruta)

        for horario in horarios:
            codigo = horario["Codigo"]

            if not codigo in self.materias:
                continue

            curso = self.transformar_horario(horario)
            cursos = horariosDTO.get(codigo, [])
            cursos.append(curso)
            horariosDTO[codigo] = cursos

        return horariosDTO


    def transformar_horario(self, horarioPDF):
        horarios = []
        for horario in horarioPDF["Horarios"]:
            horarios.append(Horario(
                dia = horario[0],
                hora_inicio = horario[1],
                hora_fin = horario[2]
            ))

        return Curso(
                cod_materia = horarioPDF["Codigo"],
                nombre_curso = "Curso" + horarioPDF["Curso"],
                horarios = horarios,
                se_dicta_primer_cuatrimestre = True,
                se_dicta_segundo_cuatrimestre = True
            )