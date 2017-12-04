from app import db

class Docente(db.Model):
    __tablename__ = 'docente'

    id = db.Column(db.Integer, primary_key=True)

    apellido = db.Column(db.String(25), nullable=False, server_default='')
    nombre = db.Column(db.String(25), nullable=False, server_default='')
    email = db.Column(db.String(30), nullable=True, server_default='')

    def __str__(self):
        return "{}, {}".format(self.apellido.upper(), self.nombre)
