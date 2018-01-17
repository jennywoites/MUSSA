from app import db

class Curso(db.Model):
    __tablename__ = 'curso'

    id = db.Column(db.Integer, primary_key=True)

    codigo_materia = db.Column(db.String(4), nullable=False, server_default='')
    codigo = db.Column(db.String(15), nullable=False, server_default='')
    se_dicta_primer_cuatrimestre = db.Column(db.Boolean(), nullable=False, server_default='0')
    se_dicta_segundo_cuatrimestre = db.Column(db.Boolean(), nullable=False, server_default='0')
    cantidad_encuestas_completas = db.Column(db.Integer, nullable=False, server_default='0')
    puntaje_total_encuestas = db.Column(db.Integer, nullable=False, server_default='0')
    fecha_actualizacion = db.Column(db.DateTime)

    def __str__(self):
        return "Curso {} de {}".format(self.codigo, self.codigo_materia)

    def mensaje_cuatrimestre(self):
        if not self.se_dicta_primer_cuatrimestre and not self.se_dicta_segundo_cuatrimestre:
            return "No se dicta actualmente"
        if self.se_dicta_primer_cuatrimestre and self.se_dicta_segundo_cuatrimestre:
            return "Ambos cuatrimestres"
        if self.se_dicta_primer_cuatrimestre:
            return "Solo el 1º cuatrimestre"
        return "Solo el 2º cuatrimestre"

    def calcular_puntaje(self):
        if self.cantidad_encuestas_completas == 0:
            return 0
        return (self.puntaje_total_encuestas / self.cantidad_encuestas_completas)

class Horario(db.Model):
    __tablename__ = 'horario'

    id = db.Column(db.Integer, primary_key=True)

    dia = db.Column(db.String(12), nullable=False, server_default='')
    hora_desde = db.Column(db.String(4), nullable=False, server_default='')
    hora_hasta = db.Column(db.String(4), nullable=False, server_default='')

    def __str__(self):
        return "Horario: {} de {} a {}".format(self.dia, self.hora_desde, self.hora_hasta)

    def convertir_hora(self, horario):
        l_horario = str(horario).split(".")
        hora = l_horario[0]

        if (0 <= int(hora) < 10):
            hora = "0" + hora

        if len(l_horario) == 1:
            return hora + ":00"
        return hora + ":30"

class HorarioPorCurso(db.Model):
    __tablename__ = 'horario_por_curso'
    id = db.Column(db.Integer, primary_key=True)

    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'))
    horario_id = db.Column(db.Integer, db.ForeignKey('horario.id'))

    def __str__(self):
        return "El curso {} tiene este horario: {}".format(self.curso_id, self.horario_id)


class CarreraPorCurso(db.Model):
    __tablename__ = 'carrera_por_curso'
    id = db.Column(db.Integer, primary_key=True)

    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'))
    carrera_id = db.Column(db.Integer, db.ForeignKey('carrera.id'))

    def __str__(self):
        return "El curso con id {} es de esta carrera: {}".format(self.curso_id, self.carrera_id)


class HorariosYaCargados(db.Model):
    __tablename__ = 'horarios_ya_cargados'
    id = db.Column(db.Integer, primary_key=True)

    anio = db.Column(db.String(4), nullable=False, server_default='')
    cuatrimestre = db.Column(db.String(1), nullable=False, server_default='')

    def __str__(self):
        return "Año: {} - {}C".format(self.anio, self.cuatrimestre)