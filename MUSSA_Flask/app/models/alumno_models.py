from app import db


class Alumno(db.Model):
    __tablename__ = 'alumno'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    padron = db.Column(db.String(12), nullable=True, server_default='')

    def __str__(self):
        if not self.padron:
            return "Alumno sin padrón asignado"

        return "Alumno con padrón: {}".format(self.padron)

    def get_padron(self):
        return self.padron if self.padron else "sin_padron"


class AlumnosCarreras(db.Model):
    __tablename__ = 'alumnos_carreras'

    id = db.Column(db.Integer(), primary_key=True)

    alumno_id = db.Column(db.Integer(), db.ForeignKey('alumno.id', ondelete='CASCADE'))
    carrera_id = db.Column(db.Integer(), db.ForeignKey('carrera.id', ondelete='CASCADE'))


class MateriasAlumno(db.Model):
    __tablename__ = 'materias_alumno'

    id = db.Column(db.Integer(), primary_key=True)

    alumno_id = db.Column(db.Integer(), db.ForeignKey('alumno.id'))
    materia_id = db.Column(db.Integer(), db.ForeignKey('materia.id'))
    curso_id = db.Column(db.Integer(), db.ForeignKey('curso.id'))
    carrera_id = db.Column(db.Integer(), db.ForeignKey('carrera.id'))

    estado_id = db.Column(db.Integer(), db.ForeignKey('estado_materia.id'))
    calificacion = db.Column(db.Integer, nullable=True)
    fecha_aprobacion = db.Column(db.DateTime)
    cuatrimestre_aprobacion_cursada = db.Column(db.String(1), nullable=True, server_default='')
    anio_aprobacion_cursada = db.Column(db.String(4), nullable=True, server_default='')
    acta_o_resolucion = db.Column(db.String(35), nullable=True, server_default='')
    forma_aprobacion_id = db.Column(db.Integer(), db.ForeignKey('forma_aprobacion_materia.id'), nullable=True)

    def __str__(self):
        string = "Alumno: {}".format(self.alumno_id)
        string += " - Materia: {}".format(self.materia_id)

        curso = self.curso_id if self.curso_id else "Sin designar"
        string += " - Curso: {}".format(curso)

        string += " - Carrera: {}".format(self.carrera_id)
        string += " - Estado: {}".format(self.estado_id)

        string += " - Cuatrimestre: {}".format(self.cuatrimestre_aprobacion_cursada)
        string += " - Año: {}".format(self.anio_aprobacion_cursada)
        return string


class EstadoMateria(db.Model):
    __tablename__ = 'estado_materia'

    id = db.Column(db.Integer(), primary_key=True)
    estado = db.Column(db.String(70), nullable=False, server_default='')


class FormaAprobacionMateria(db.Model):
    __tablename__ = 'forma_aprobacion_materia'

    id = db.Column(db.Integer(), primary_key=True)
    forma = db.Column(db.String(35), nullable=False, server_default='')
