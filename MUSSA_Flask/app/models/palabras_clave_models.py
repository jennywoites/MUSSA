from app import db


class PalabraClave(db.Model):
    __tablename__ = 'palabra_clave'

    id = db.Column(db.Integer, primary_key=True)

    palabra = db.Column(db.String(30), nullable=False, server_default='')

    def __str__(self):
        return self.palabra


class PalabrasClaveParaMateria(db.Model):
    __tablename__ = 'palabras_clave_para_materias'
    id = db.Column(db.Integer, primary_key=True)

    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'))
    palabra_clave_id = db.Column(db.Integer, db.ForeignKey('palabra_clave.id'))
    cantidad_encuestas_asociadas = db.Column(db.Integer, nullable=False, server_default='0')

    def __str__(self):
        return "La materia {} tiene como plabra clave: {}".format(self.materia_id, self.palabra_clave_id)


class TematicaMateria(db.Model):
    __tablename__ = 'tematica_materia'

    id = db.Column(db.Integer, primary_key=True)

    tematica = db.Column(db.String(40), nullable=False, server_default='')
    verificada = db.Column(db.Boolean(), nullable=False, server_default='0')

    def __str__(self):
        return self.tematica

class TematicaPorMateria(db.Model):
    __tablename__ = 'tematica_por_materia'
    id = db.Column(db.Integer, primary_key=True)

    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'))
    tematica_id = db.Column(db.Integer, db.ForeignKey('tematica_materia.id'))
    cantidad_encuestas_asociadas = db.Column(db.Integer, nullable=False, server_default='0')

    def __str__(self):
        return "La materia {} tiene como temática: {}".format(self.materia_id, self.tematica_id)
