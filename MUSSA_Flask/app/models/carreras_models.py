from app import db

class Carrera(db.Model):
    __tablename__ = 'carrera'

    id = db.Column(db.Integer, primary_key=True)

    codigo = db.Column(db.String(4), nullable=False, unique=True, server_default='')
    duracion_estimada_en_cuatrimestres = db.Column(db.Integer, nullable=False, server_default=0)
    requiere_prueba_suficiencia_de_idioma = db.Column('requiere_prueba_suficiencia_de_idioma', db.Boolean(), nullable=False, server_default=False)

    creditos = db.relationship('creditos', backref='carrera', lazy='dynamic')
    materias = db.relationship('materia', backref='carrera', lazy='dynamic')
    orientaciones = db.relationship('orientacion', lazy='dynamic')


class Creditos(db.Model):
    __tablename__ = 'creditos'

    id = db.Column(db.Integer, primary_key=True)

    creditos_obligatorias = db.Column(db.Integer, nullable=False, server_default=0)
    creditos_electivas_general = db.Column(db.Integer, nullable=False, server_default=0)
    creditos_orientacion = db.Column(db.Integer, nullable=False, server_default=0)
    creditos_electivas_con_tp = db.Column(db.Integer, nullable=False, server_default=0)
    creditos_electivas_con_tesis = db.Column(db.Integer, nullable=False, server_default=0)
    creditos_tesis = db.Column(db.Integer, nullable=False, server_default=0)
    creditos_tp_profesional = db.Column(db.Integer, nullable=False, server_default=0)

    carrera_id = db.Column(db.Integer, db.ForeignKey('carrera.id'))


class TipoMateria(db.Model):
    __tablename__ = 'tipo_materia'

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50), nullable=False, server_default='')


class Materia(db.Model):
    __tablename__ = 'materia'

    id = db.Column(db.Integer, primary_key=True)

    codigo = db.Column(db.String(4), nullable=False, server_default='')
    nombre = db.Column(db.String(50), nullable=False, server_default='')
    objetivos = db.Column(db.String(250), nullable=True, server_default='')

    tipo_materia_id = db.Column(db.Integer, db.ForeignKey('tipo_materia.id'))

    #Programa sintetico
    #Programa analitico
    #cursos 

    carrera_id = db.Column(db.Integer, db.ForeignKey('carrera.id'))


class Orientacion(db.Model):
    __tablename__ = 'orientacion'

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(125), nullable=False, server_default='')
    clave_reducida = db.Column(db.String(50), nullable=False, server_default='')
