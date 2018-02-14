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

    def __str__(self):
        horarios = ""
        for h in self.horarios:
            horarios += str(h) + " y "
        horarios = horarios[:-3]
        return self.nombre + " [ " + horarios + " ]"
