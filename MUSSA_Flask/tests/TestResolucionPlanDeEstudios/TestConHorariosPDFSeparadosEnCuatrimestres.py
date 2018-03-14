from app.API_Rest.GeneradorPlanCarreras.ParserHorarios import parsear_pdf
from app.API_Rest.GeneradorPlanCarreras.modelos.Curso import Curso
from app.API_Rest.GeneradorPlanCarreras.modelos.Horario import Horario
from tests.TestResolucionPlanDeEstudios.TestDesdeArchivoCSV import TestDesdeArchivoCSV


class TestConHorariosPDFSeparadosEnCuatrimestres(TestDesdeArchivoCSV):
    def __init__(self):
        super().__init__()
        self.cargar_horarios_PDF()

    def cargar_horarios_PDF(self):
        # Los cursos precargados seran eliminados asi que la
        # cuenta se reinicia
        self.ultimo_id_curso = 0

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
            id_materia = self.codigo_a_id.get(horario["Codigo"], -1)

            if not id_materia in self.materias:
                continue

            curso = self.transformar_horario(horario, cuatrimestre)
            cursos = horariosDTO.get(id_materia, [])
            cursos.append(curso)
            horariosDTO[id_materia] = cursos

        return horariosDTO

    def transformar_horario(self, horarioPDF, cuatrimestre):
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
            se_dicta_primer_cuatrimestre=(cuatrimestre == 1),
            se_dicta_segundo_cuatrimestre=(cuatrimestre == 2),
            puntaje=0
        )

    def fusionar_horarios(self, horarios_1er_cuatri, horarios_2do_cuatri):
        for id_materia in horarios_1er_cuatri:
            cursos_materia_1C = horarios_1er_cuatri[id_materia]

            if not id_materia in horarios_2do_cuatri:
                continue

            cursos_materia_2c = horarios_2do_cuatri.pop(id_materia)

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

        for id_materia in horarios_1er_cuatri:
            horarios[id_materia] = horarios_1er_cuatri[id_materia]

        for id_materia in horarios_2do_cuatri:
            horarios[id_materia] = horarios_2do_cuatri[id_materia]

        return horarios
