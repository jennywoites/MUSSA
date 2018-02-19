from app import db

class Carrera(db.Model):
    __tablename__ = 'carrera'

    id = db.Column(db.Integer, primary_key=True)

    codigo = db.Column(db.String(4), nullable=False, unique=True, server_default='')
    nombre = db.Column(db.String(50), nullable=False, server_default='')
    plan = db.Column(db.String(4), nullable=False, server_default='')
    duracion_estimada_en_cuatrimestres = db.Column(db.Integer, nullable=False)
    requiere_prueba_suficiencia_de_idioma = db.Column('requiere_prueba_suficiencia_de_idioma', db.Boolean(), nullable=False)

    creditos = db.relationship('Creditos', backref='carrera', lazy='dynamic')
    materias = db.relationship('Materia', backref='carrera', lazy='dynamic')
    orientaciones = db.relationship('Orientacion', lazy='dynamic')

    def __str__(self):
        return "{} - {}".format(self.codigo, self.nombre)

    def get_descripcion_carrera(self):
        if not self.plan:
            return "{} - {}".format(self.codigo, self.nombre)

        return "{} - {} (Plan {})".format(self.codigo, self.nombre, self.plan)

class Creditos(db.Model):
    __tablename__ = 'creditos'

    id = db.Column(db.Integer, primary_key=True)

    creditos_obligatorias = db.Column(db.Integer, nullable=False)
    creditos_electivas_general = db.Column(db.Integer, nullable=False)
    creditos_orientacion = db.Column(db.Integer, nullable=False)
    creditos_electivas_con_tp = db.Column(db.Integer, nullable=False)
    creditos_electivas_con_tesis = db.Column(db.Integer, nullable=False)
    creditos_tesis = db.Column(db.Integer, nullable=False)
    creditos_tp_profesional = db.Column(db.Integer, nullable=False)

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
    creditos_minimos_para_cursarla = db.Column(db.Integer, nullable=False)
    creditos = db.Column(db.Integer, nullable=False)

    tipo_materia_id = db.Column(db.Integer, db.ForeignKey('tipo_materia.id'))

    carrera_id = db.Column(db.Integer, db.ForeignKey('carrera.id'))

    def __str__(self):
        return "{} - {}".format(self.codigo, self.nombre)


class Correlativas(db.Model):
    """
    Si la materia C tiene como correlativas a A y B,
    significa que A y B deben hacerse antes que C
    """

    __tablename__ = 'correlativas'
    id = db.Column(db.Integer, primary_key=True)

    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'))
    materia_correlativa_id = db.Column(db.Integer, db.ForeignKey('materia.id'))

    def __str__(self):
        return "La materia {} tiene como correlativa a {}".format(self.materia_id, self.materia_correlativa_id)


class MateriasIncompatibles(db.Model):
    __tablename__ = 'materias_incompatibles'
    id = db.Column(db.Integer, primary_key=True)

    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'))
    materia_incompatible_id = db.Column(db.Integer, db.ForeignKey('materia.id'))


class Orientacion(db.Model):
    __tablename__ = 'orientacion'

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(125), nullable=False, server_default='')
    clave_reducida = db.Column(db.String(50), nullable=False, server_default='')

    carrera_id = db.Column(db.Integer, db.ForeignKey('carrera.id'))
