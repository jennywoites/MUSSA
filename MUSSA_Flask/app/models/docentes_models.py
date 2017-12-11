from app import db

class Docente(db.Model):
    __tablename__ = 'docente'

    id = db.Column(db.Integer, primary_key=True)

    apellido = db.Column(db.String(35), nullable=False, server_default='')
    nombre = db.Column(db.String(40), nullable=True, server_default='')

    def __str__(self):
        if not self.nombre:
            return self.apellido

        return "{}, {}".format(self.apellido, self.nombre)

    def obtener_nombre_completo(self):
        nombre = self.apellido
        if self.nombre:
            nombre += ", " + self.nombre
        return nombre


class CursosDocente(db.Model):
    __tablename__ = 'cursos_docente'

    id = db.Column(db.Integer, primary_key=True)

    docente_id = db.Column(db.Integer, db.ForeignKey('docente.id'))
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'))
