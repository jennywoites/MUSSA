from app import db
from app.DAO.EncuestasDAO import *

class EncuestaAlumno(db.Model):
    __tablename__ = 'encuesta_alumno'

    id = db.Column(db.Integer, primary_key=True)

    alumno_id = db.Column(db.Integer(), db.ForeignKey('alumno.id'), nullable=False)
    materia_alumno_id = db.Column(db.Integer(), db.ForeignKey('materias_alumno.id'), nullable=False)

    cuatrimestre_aprobacion_cursada = db.Column(db.String(1), nullable=False, server_default='')
    anio_aprobacion_cursada = db.Column(db.String(4), nullable=False, server_default='')

    finalizada = db.Column(db.Boolean(), nullable=False, server_default='')

    def __str__(self):
        return "Alumno: {} - Materia: {} - Finalizada: {}".format(self.alumno_id, self.materia, self.finalizada)


class RespuestaEncuestaAlumno(db.Model):
    __tablename__ = 'respuesta_encuesta_alumno'

    id = db.Column(db.Integer, primary_key=True)

    encuesta_alumno_id = db.Column(db.Integer(), db.ForeignKey('encuesta_alumno.id'), nullable=False)
    pregunta_encuesta_id = db.Column(db.Integer(), db.ForeignKey('pregunta_encuesta.id'), nullable=False)

    # Dato redundante con pregunta encuesta. Se completa para simplificar las querys
    tipo_id = db.Column(db.Integer(), db.ForeignKey('tipo_encuesta.id'), nullable=False)


class EstadoPasosEncuestaAlumno(db.Model):
    __tablename__ = 'estado_pasos_encuesta_alumno'

    id = db.Column(db.Integer, primary_key=True)

    encuesta_alumno_id = db.Column(db.Integer(), db.ForeignKey('encuesta_alumno.id'), nullable=False)

    # Los estados son:
    # 0: NO_INICIADO
    # 1: EN_CURSO
    # 2: FINALIZADO

    # ATENCION: Si todos los pasos estan en finalizado podria implicar que el alumno haya indicado ademas
    # finalizar la encuesta. No modificar estos valores manualmente en la base de datos.

    estadoPaso1 = db.Column(db.Integer(), nullable=False, server_default='')
    estadoPaso2 = db.Column(db.Integer(), nullable=False, server_default='')
    estadoPaso3 = db.Column(db.Integer(), nullable=False, server_default='')
    estadoPaso4 = db.Column(db.Integer(), nullable=False, server_default='')
    estadoPaso5 = db.Column(db.Integer(), nullable=False, server_default='')

    def inicializar_pasos(self):
        self.estadoPaso1 = PASO_ENCUESTA_NO_INICIADO
        self.estadoPaso2 = PASO_ENCUESTA_NO_INICIADO
        self.estadoPaso3 = PASO_ENCUESTA_NO_INICIADO
        self.estadoPaso4 = PASO_ENCUESTA_NO_INICIADO
        self.estadoPaso5 = PASO_ENCUESTA_FINALIZADO

    def actualizar_estado_paso(self, numero_paso, finalizado):
        estado = PASO_ENCUESTA_FINALIZADO if finalizado else PASO_ENCUESTA_EN_CURSO

        if numero_paso == 0:
            self.estadoPaso1 = estado
        elif numero_paso == 1:
            self.estadoPaso2 = estado
        elif numero_paso == 2:
            self.estadoPaso3 = estado
        elif numero_paso == 3:
            self.estadoPaso4 = estado
        else:
            self.estadoPaso5 = estado

        db.session.commit()

    def estan_todos_los_pasos_completos(self):
        return (
            self.estadoPaso1 == PASO_ENCUESTA_FINALIZADO and
            self.estadoPaso2 == PASO_ENCUESTA_FINALIZADO and
            self.estadoPaso3 == PASO_ENCUESTA_FINALIZADO and
            self.estadoPaso4 == PASO_ENCUESTA_FINALIZADO and
            self.estadoPaso5 == PASO_ENCUESTA_FINALIZADO
        )

class RespuestaEncuestaPuntaje(db.Model):
    __tablename__ = 'rta_encuesta_puntaje'

    id = db.Column(db.Integer, primary_key=True)

    rta_encuesta_alumno_id = db.Column(db.Integer(), db.ForeignKey('respuesta_encuesta_alumno.id'), nullable=False)
    puntaje = db.Column(db.Integer(), nullable=False, server_default='')


class RespuestaEncuestaTexto(db.Model):
    __tablename__ = 'rta_encuesta_texto'

    id = db.Column(db.Integer, primary_key=True)

    rta_encuesta_alumno_id = db.Column(db.Integer(), db.ForeignKey('respuesta_encuesta_alumno.id'), nullable=False)
    texto = db.Column(db.String(250), nullable=False, server_default='')


class RespuestaEncuestaSiNo(db.Model):
    __tablename__ = 'rta_encuesta_si_no'

    id = db.Column(db.Integer, primary_key=True)

    rta_encuesta_alumno_id = db.Column(db.Integer(), db.ForeignKey('respuesta_encuesta_alumno.id'), nullable=False)
    respuesta = db.Column(db.Boolean(), nullable=False)


class RespuestaEncuestaHorario(db.Model):
    __tablename__ = 'rta_encuesta_horario'

    id = db.Column(db.Integer, primary_key=True)

    rta_encuesta_alumno_id = db.Column(db.Integer(), db.ForeignKey('respuesta_encuesta_alumno.id'), nullable=False)
    horario_id = db.Column(db.Integer(), db.ForeignKey('horario.id'), nullable=False)


class RespuestaEncuestaDocente(db.Model):
    __tablename__ = 'rta_encuesta_docente'

    id = db.Column(db.Integer, primary_key=True)

    rta_encuesta_alumno_id = db.Column(db.Integer(), db.ForeignKey('respuesta_encuesta_alumno.id'), nullable=False)
    docente_id = db.Column(db.Integer(), db.ForeignKey('docente.id'), nullable=False)
    comentario = db.Column(db.String(250), nullable=False, server_default='')


class RespuestaEncuestaCorrelativa(db.Model):
    __tablename__ = 'rta_encuesta_correlativa'

    id = db.Column(db.Integer, primary_key=True)

    rta_encuesta_alumno_id = db.Column(db.Integer(), db.ForeignKey('respuesta_encuesta_alumno.id'), nullable=False)
    materia_correlativa_id = db.Column(db.Integer(), db.ForeignKey('materia.id'), nullable=False)


class RespuestaEncuestaEstrellas(db.Model):
    __tablename__ = 'rta_encuesta_estrellas'

    id = db.Column(db.Integer, primary_key=True)

    rta_encuesta_alumno_id = db.Column(db.Integer(), db.ForeignKey('respuesta_encuesta_alumno.id'), nullable=False)
    estrellas = db.Column(db.Integer(), nullable=False, server_default='')


class RespuestaEncuestaNumero(db.Model):
    __tablename__ = 'rta_encuesta_numero'

    id = db.Column(db.Integer, primary_key=True)

    rta_encuesta_alumno_id = db.Column(db.Integer(), db.ForeignKey('respuesta_encuesta_alumno.id'), nullable=False)
    numero = db.Column(db.Integer(), nullable=False, server_default='')


class RespuestaEncuestaTags(db.Model):
    __tablename__ = 'rta_encuesta_tags'

    id = db.Column(db.Integer, primary_key=True)

    rta_encuesta_alumno_id = db.Column(db.Integer(), db.ForeignKey('respuesta_encuesta_alumno.id'), nullable=False)
    palabra_clave_id = db.Column(db.Integer(), db.ForeignKey('palabra_clave.id'), nullable=False)


class RespuestaEncuestaTematica(db.Model):
    __tablename__ = 'rta_encuesta_tematica'

    id = db.Column(db.Integer, primary_key=True)

    rta_encuesta_alumno_id = db.Column(db.Integer(), db.ForeignKey('respuesta_encuesta_alumno.id'), nullable=False)
    tematica_id = db.Column(db.Integer(), db.ForeignKey('tematica_materia.id'), nullable=False)
