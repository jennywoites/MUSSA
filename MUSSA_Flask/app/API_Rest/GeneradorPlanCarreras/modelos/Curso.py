from app.API_Rest.GeneradorPlanCarreras.modelos.Horario import Horario


class Curso:
    def inicializar_con_JSON(self, datos_json):
        self.id_curso = datos_json["id_curso"]
        self.cod = datos_json["cod"]
        self.nombre = datos_json["nombre"]

        horarios = []
        for datos_horario in datos_json["horarios"]:
            horarios.append(Horario(datos_JSON=datos_horario))
        self.horarios = horarios

        self.se_dicta_primer_cuatrimestre = datos_json["se_dicta_primer_cuatrimestre"]
        self.se_dicta_segundo_cuatrimestre = datos_json["se_dicta_segundo_cuatrimestre"]
        self.puntaje = datos_json["puntaje"]

    def __init__(self, id_curso='', cod_materia='', nombre_curso='', horarios=[], se_dicta_primer_cuatrimestre=False,
                 se_dicta_segundo_cuatrimestre=False, puntaje=0, datos_JSON=''):
        if datos_JSON:
            return self.inicializar_con_JSON(datos_JSON)

        self.id_curso = id_curso
        self.cod = cod_materia
        self.nombre = nombre_curso
        self.horarios = horarios
        self.se_dicta_primer_cuatrimestre = se_dicta_primer_cuatrimestre
        self.se_dicta_segundo_cuatrimestre = se_dicta_segundo_cuatrimestre
        self.puntaje = puntaje

    def __str__(self):
        SALTO = "\n"
        curso = "Curso: {" + SALTO
        curso += "id_curso:" + str(self.id_curso) + SALTO
        curso += "cod:" + str(self.cod) + SALTO
        curso += "nombre:" + str(self.nombre) + SALTO

        curso += "horarios: [" + SALTO
        for horario in self.horarios:
            curso += str(horario)
        curso += "]"

        curso += "se_dicta_primer_cuatrimestre:" + str(self.se_dicta_primer_cuatrimestre) + SALTO
        curso += "se_dicta_segundo_cuatrimestre:" + str(self.se_dicta_segundo_cuatrimestre) + SALTO
        curso += "puntaje:" + str(self.puntaje) + SALTO
        curso += "}:" + SALTO
        return curso

    def generar_JSON(self):
        horarios = []
        for horario in self.horarios:
            horarios.append(horario.generar_JSON())

        return {
            "id_curso": self.id_curso,
            "cod": self.cod,
            "nombre": self.nombre,
            "horarios": horarios,
            "se_dicta_primer_cuatrimestre": self.se_dicta_primer_cuatrimestre,
            "se_dicta_segundo_cuatrimestre": self.se_dicta_segundo_cuatrimestre,
            "puntaje": self.puntaje
        }

    def copia_profunda(self):
        horarios = []
        for horario in self.horarios:
            horarios.append(horario.copia_profunda())

        return Curso(
            id_curso=self.id_curso,
            cod_materia=self.cod,
            nombre_curso=self.nombre,
            horarios=horarios,
            se_dicta_primer_cuatrimestre=self.se_dicta_primer_cuatrimestre,
            se_dicta_segundo_cuatrimestre=self.se_dicta_segundo_cuatrimestre,
            puntaje=self.puntaje
        )

    def obtener_franjas_curso(self):
        franjas_totales = {}
        total_horas = 0
        for horario in self.horarios:
            franjas = horario.get_franjas_utilizadas()
            franjas_dia = franjas_totales.get(horario.dia, [])
            for franja in franjas:
                franjas_dia.append(franja)
            franjas_totales[horario.dia] = franjas_dia
            total_horas += len(franjas_dia)

        return franjas_totales, total_horas