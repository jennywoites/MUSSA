class Curso:
    def __init__(self, id_curso, cod_materia, nombre_curso, horarios, se_dicta_primer_cuatrimestre,
                 se_dicta_segundo_cuatrimestre, puntaje=0):
        self.id_curso = id_curso
        self.cod = cod_materia
        self.nombre = nombre_curso
        self.horarios = horarios
        self.se_dicta_primer_cuatrimestre = se_dicta_primer_cuatrimestre
        self.se_dicta_segundo_cuatrimestre = se_dicta_segundo_cuatrimestre
        self.puntaje = puntaje

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

    def __str__(self):
        horarios = ""
        for h in self.horarios:
            horarios += str(h) + " y "
        horarios = horarios[:-3]
        return self.nombre + " [ " + horarios + " ]"
