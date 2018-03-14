from app.API_Rest.GeneradorPlanCarreras.ParserHorarios import parsear_pdf
from app.API_Rest.GeneradorPlanCarreras.modelos.Curso import Curso
from app.API_Rest.GeneradorPlanCarreras.modelos.Horario import Horario
from tests.TestResolucionPlanDeEstudios.TestDesdeArchivoCSV import TestDesdeArchivoCSV


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

        # Los cursos precargados seran eliminados asi que la
        # cuenta se reinicia
        self.ultimo_id_curso = 0

        for horario in horarios:
            id_materia = self.codigo_a_id.get(horario["Codigo"], -1)

            if not id_materia in self.materias:
                continue

            curso = self.transformar_horario(horario)
            cursos = horariosDTO.get(id_materia, [])
            cursos.append(curso)
            horariosDTO[id_materia] = cursos

        return horariosDTO

    def transformar_horario(self, horarioPDF):
        horarios = []
        for horario in horarioPDF["Horarios"]:
            horarios.append(Horario(
                dia=horario[0],
                hora_inicio=horario[1],
                hora_fin=horario[2]
            ))

        self.ultimo_id_curso += 1

        return Curso(
            id_curso=self.ultimo_id_curso,
            cod_materia=horarioPDF["Codigo"],
            nombre_curso="Curso" + horarioPDF["Curso"],
            horarios=horarios,
            se_dicta_primer_cuatrimestre=True,
            se_dicta_segundo_cuatrimestre=True,
            puntaje=0
        )
