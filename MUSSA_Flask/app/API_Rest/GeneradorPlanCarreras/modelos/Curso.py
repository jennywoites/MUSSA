class Curso:

    def __init__(self, cod_materia, nombre_curso, horarios):
        self.cod = cod_materia
        self.nombre = nombre_curso
        self.horarios = horarios

    def __str__(self):
        horarios = ""
        for h in self.horarios:
            horarios += str(h) + " y "
        horarios = horarios[:-3]
        return self.nombre + " [ " + horarios + " ]"
