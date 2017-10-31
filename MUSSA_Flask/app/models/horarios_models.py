from app import db

class Curso(db.Model):
    __tablename__ = 'curso'

    id = db.Column(db.Integer, primary_key=True)

    codigo_materia = db.Column(db.String(4), nullable=False, server_default='')
    codigo = db.Column(db.String(15), nullable=False, server_default='')
    docentes = db.Column(db.String(250), nullable=True, server_default='')
    se_dicta_primer_cuatrimestre = db.Column(db.Boolean(), nullable=False, server_default='0')
    se_dicta_segundo_cuatrimestre = db.Column(db.Boolean(), nullable=False, server_default='0')
    cantidad_encuestas_completas = db.Column(db.Integer, nullable=False, server_default='0')
    puntaje_total_encuestas = db.Column(db.Integer, nullable=False, server_default='0')

    def __str__(self):
        return "Curso {} de {}".format(self.codigo, self.codigo_materia)


class Horario(db.Model):
    __tablename__ = 'horario'

    id = db.Column(db.Integer, primary_key=True)

    dia = db.Column(db.String(12), nullable=False, server_default='')
    hora_desde = db.Column(db.String(4), nullable=False, server_default='')
    hora_hasta = db.Column(db.String(4), nullable=False, server_default='')

    def __str__(self):
        return "Horario: {} de {} a {}".format(self.dia, self.hora_desde, self.hora_hasta)


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
