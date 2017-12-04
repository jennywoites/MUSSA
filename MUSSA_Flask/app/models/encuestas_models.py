from app import db

class TipoEncuesta(db.Model):
    __tablename__ = 'tipo_encuesta'

    id = db.Column(db.Integer, primary_key=True)

    tipo = db.Column(db.Integer(), nullable=False, server_default='')
    descripcion = db.Column(db.String(25), nullable=False, server_default='')

    def __str__(self):
        return "{} - {}".format(self.tipo, self.descripcion)


class PreguntaEncuesta(db.Model):
    __tablename__ = 'pregunta_encuesta'

    id = db.Column(db.Integer, primary_key=True)

    pregunta = db.Column(db.String(250), nullable=False, server_default='')
    tipo_id = db.Column(db.Integer(), db.ForeignKey('tipo_encuesta.id'), nullable=False)

    def __str__(self):
        return self.pregunta


class PreguntaEncuestaPuntaje(db.Model):
    __tablename__ = 'pregunta_encuesta_puntaje'

    id = db.Column(db.Integer, primary_key=True)

    encuesta_id = db.Column(db.Integer(), db.ForeignKey('pregunta_encuesta.id'), nullable=False)
    texto_min = db.Column(db.String(25), nullable=False, server_default='')
    texto_max = db.Column(db.String(25), nullable=False, server_default='')

    def __str__(self):
        return "{} - Min: {} - Max: {}".format(self.encuesta_id, self.texto_min, self.texto_max)


class PreguntaEncuestaSiNo(db.Model):
    __tablename__ = 'pregunta_encuesta_si_o_no'

    id = db.Column(db.Integer, primary_key=True)

    encuesta_id = db.Column(db.Integer(), db.ForeignKey('pregunta_encuesta.id'), nullable=False)
    encuesta_id_si = db.Column(db.Integer(), db.ForeignKey('pregunta_encuesta.id'), nullable=True)
    encuesta_id_no = db.Column(db.Integer(), db.ForeignKey('pregunta_encuesta.id'), nullable=True)

    def __str__(self):
        rta_si = self.encuesta_id_si if self.encuesta_id_si else "-"
        rta_no = self.encuesta_id_no if self.encuesta_id_no else "-"
        return "{} - SI: {} - NO: {}".format(self.encuesta_id, rta_si, rta_no)


class GrupoEncuesta(db.Model):
    __tablename__ = 'grupo_encuesta'

    id = db.Column(db.Integer, primary_key=True)
    grupo = db.Column(db.String(35), nullable=False, server_default='')

    def __str__(self):
        return self.grupo


class ExcluirEncuestaSi(db.Model):
    __tablename__ = 'excluir_encuesta_si'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(35), nullable=False, server_default='')

    def __str__(self):
        return self.tipo


class EncuestaGenerada(db.Model):
    __tablename__ = 'encuesta_generada'

    id = db.Column(db.Integer, primary_key=True)

    grupo_id = db.Column(db.Integer(), db.ForeignKey('grupo_encuesta.id'), nullable=False)
    encuesta_id = db.Column(db.Integer(), db.ForeignKey('pregunta_encuesta.id'), nullable=False)
    excluir_si_id = db.Column(db.Integer(), db.ForeignKey('excluir_encuesta_si.id'), nullable=False)
    orden = db.Column(db.Integer(), nullable=False, unique=True)

    def __str__(self):
        return self.tipo
