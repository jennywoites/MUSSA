from app import db

class Alumno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apellido = db.Column(db.String(64), unique=False)
    nombre = db.Column(db.String(64), unique=False)
    dni = db.Column(db.String(8), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    padron = db.Column(db.String(8), index=True)
    direccion = db.Column(db.String(200))
    codigo_postal = db.Column(db.String(8))
    telefono = db.Column(db.String(20))

    user = db.relationship("User", uselist=False, back_populates="alumno")

    def __init__(self, nombre, apellido, dni, email, padron='', direccion='', codigo_postal='', telefono=''):
    	self.nombre = nombre
    	self.apellido = apellido
    	self.dni = dni
    	self.email = email
    	self.padron = padron
    	self.direccion = direccion
    	self.codigo_postal = codigo_postal
    	self.telefono = telefono

    def get_nombre_completo(self):
    	return self.nombre + self.apellido

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<Alumno {}>'.format(self.get_nombre_completo())
