from app.API_Rest.GeneradorPlanCarreras.ParserHorarios import parsear_pdf
from app.API_Rest.GeneradorPlanCarreras.modelos.Curso import Curso
from app.API_Rest.GeneradorPlanCarreras.modelos.Horario import Horario
from tests.TestResolucionPlanDeEstudios.TestDesdeArchivoCSV import TestDesdeArchivoCSV


class TestConHorariosPDFSeparadosEnCuatrimestres(TestDesdeArchivoCSV):

    def __init__(self):
        super().__init__()
        self.cargar_horarios_PDF()


    def cargar_horarios_PDF(self):
        horarios_1er_cuatri = self.horarios_PDF_to_horarios_DTO(1)
        horarios_2do_cuatri = self.horarios_PDF_to_horarios_DTO(2)

        self.horarios = self.fusionar_horarios(horarios_1er_cuatri, horarios_2do_cuatri)


    def horarios_PDF_to_horarios_DTO(self, cuatrimestre):
        CARPETA = "Horarios_TestFiles/"
        NOMBRE_ARCHIVO = self.get_nombre_test() + "-" + str(cuatrimestre) + "C"
        RUTA = CARPETA + NOMBRE_ARCHIVO + ".pdf"

        horariosDTO = {}
        horarios = parsear_pdf(RUTA)

        for horario in horarios:
            codigo = horario["Codigo"]

            if not codigo in self.materias:
                continue

            curso = self.transformar_horario(horario, cuatrimestre)
            cursos = horariosDTO.get(codigo, [])
            cursos.append(curso)
            horariosDTO[codigo] = cursos

        return horariosDTO


    def transformar_horario(self, horarioPDF, cuatrimestre):
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
                se_dicta_primer_cuatrimestre = (cuatrimestre == 1),
                se_dicta_segundo_cuatrimestre = (cuatrimestre == 2)
            )

    def fusionar_horarios(self, horarios_1er_cuatri, horarios_2do_cuatri):
        for codigo_materia in horarios_1er_cuatri:
            cursos_materia_1C = horarios_1er_cuatri[codigo_materia]

            if not codigo_materia in horarios_2do_cuatri:
                continue

            cursos_materia_2c = horarios_2do_cuatri.pop(codigo_materia)

            for curso_1C in cursos_materia_1C:
                cod_curso_1C = curso_1C.nombre

                pos_curso = -1
                for i in range(len(cursos_materia_2c)):
                    curso_2C = cursos_materia_2c[i]
                    if curso_2C.nombre == cod_curso_1C:
                        pos_curso = i
                        break

                if pos_curso == -1:
                    continue
                    
                curso_2c = cursos_materia_2c.pop(pos_curso)
                curso_1C.horarios = curso_2c.horarios
                curso_1C.se_dicta_primer_cuatrimestre = True
                curso_1C.se_dicta_segundo_cuatrimestre = True

        horarios = {}

        for codigo_materia in horarios_1er_cuatri:
            horarios[codigo_materia] = horarios_1er_cuatri[codigo_materia]

        for codigo_materia in horarios_2do_cuatri:
            horarios[codigo_materia] = horarios_2do_cuatri[codigo_materia]

        return horarios