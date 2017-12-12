from app import db

class EncuestaAlumno(db.Model):
    __tablename__ = 'encuesta_alumno'

    id = db.Column(db.Integer, primary_key=True)

    alumno_id = db.Column(db.Integer(), db.ForeignKey('alumno.id'), nullable=False)
    materia_alumno_id = db.Column(db.Integer(), db.ForeignKey('materias_alumno.id'), nullable=False)

    #Datos redundantes: Se los completa para simplificar en las consultas
    carrera = db.Column(db.String(35), nullable=False, server_default='')
    materia = db.Column(db.String(35), nullable=False, server_default='')
    curso = db.Column(db.String(35), nullable=False, server_default='')

    cuatrimestre_aprobacion_cursada = db.Column(db.String(1), nullable=False, server_default='')
    anio_aprobacion_cursada = db.Column(db.String(4), nullable=False, server_default='')

    finalizada = db.Column(db.Boolean(), nullable=False, server_default='')

    def __str__(self):
        return "Alumno: {} - Materia: {} - Finalizada: {}".format(self.alumno_id, self.materia, self.finalizada)
