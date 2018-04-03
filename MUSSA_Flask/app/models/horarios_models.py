from app import db
from app.API_Rest.GeneradorPlanCarreras.my_utils import convertir_hora_desde_horario_float


# FIXME: Eliminar cuando se encuentre una mejor manera de trabajar con los cursos de modelos I con teoricas de horario opcional
class AjustadoCursoModelosI(db.Model):
    __tablename__ = 'ajustado_curso_modelos_I'

    id = db.Column(db.Integer, primary_key=True)
    actualizado = db.Column(db.Boolean(), nullable=False, server_default='0')


class Curso(db.Model):
    __tablename__ = 'curso'

    id = db.Column(db.Integer, primary_key=True)

    codigo_materia = db.Column(db.String(4), nullable=False, server_default='')
    codigo = db.Column(db.String(15), nullable=False, server_default='')
    se_dicta_primer_cuatrimestre = db.Column(db.Boolean(), nullable=False, server_default='0')
    se_dicta_segundo_cuatrimestre = db.Column(db.Boolean(), nullable=False, server_default='0')
    cantidad_encuestas_completas = db.Column(db.Integer, nullable=False, server_default='0')
    puntaje_total_encuestas = db.Column(db.Integer, nullable=False, server_default='0')
    fecha_actualizacion = db.Column(db.DateTime)

    # Indican si el curso fue actualizado por primera vez un primer y un segundo cuatrimestre respectivamente
    # es decir, para cada curso nuevo se verificó su horario y si era dictado en ambos cuatrimestres.
    primer_cuatrimestre_actualizado = db.Column(db.Boolean(), nullable=False, server_default='0')
    segundo_cuatrimestre_actualizado = db.Column(db.Boolean(), nullable=False, server_default='0')

    def __str__(self):
        return "Curso {} de {}".format(self.codigo, self.codigo_materia)

    def mensaje_cuatrimestre(self):
        if not self.se_dicta_primer_cuatrimestre and not self.se_dicta_segundo_cuatrimestre:
            return "No se dicta actualmente"
        if self.se_dicta_primer_cuatrimestre and self.se_dicta_segundo_cuatrimestre:
            return "Ambos cuatrimestres"
        if self.se_dicta_primer_cuatrimestre:
            return "Solo el 1º cuatrimestre"
        return "Solo el 2º cuatrimestre"

    def calcular_puntaje(self):
        if self.cantidad_encuestas_completas == 0:
            return 0
        return "{0:.2f}".format(self.puntaje_total_encuestas / self.cantidad_encuestas_completas)


class Horario(db.Model):
    __tablename__ = 'horario'

    id = db.Column(db.Integer, primary_key=True)

    dia = db.Column(db.String(12), nullable=False, server_default='')
    hora_desde = db.Column(db.String(4), nullable=False, server_default='')
    hora_hasta = db.Column(db.String(4), nullable=False, server_default='')

    def __str__(self):
        return "Horario: {} de {} a {}".format(self.dia, self.hora_desde, self.hora_hasta)

    def convertir_hora(self, horario):
        return convertir_hora_desde_horario_float(horario)

    def convertir_a_franja(self, hora):
        hora = float(hora)
        base = 1
        hora_origen = 7
        if (round(hora) != hora):
            base += 1
            hora = int(hora - 0.5)
        return int((hora - hora_origen) * 2 + base)

    def get_franjas_utilizadas(self):
        """
        Las franjas horarias van cada media hora desde las 7am hasta las 23:30
        07:00 a 07:30 --> 1
        07:30 a 08:00 --> 2
        08:00 a 08:30 --> 3
        ...
        Devuelve una lista con los numeros de las franjas horarias desde hora_desde hasta hora_hasta
        """
        franja_inicio = self.convertir_a_franja(self.hora_desde)
        franja_final = self.convertir_a_franja(self.hora_hasta)
        return [x for x in range(franja_inicio, franja_final)]

class HorarioPorCurso(db.Model):
    __tablename__ = 'horario_por_curso'
    id = db.Column(db.Integer, primary_key=True)

    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'))
    horario_id = db.Column(db.Integer, db.ForeignKey('horario.id'))
    es_horario_activo = db.Column(db.Boolean(), nullable=False, server_default='0')
    fecha_actualizacion = db.Column(db.DateTime)

    def __str__(self):
        return "El curso {} tiene este horario: {}".format(self.curso_id, self.horario_id)


class CarreraPorCurso(db.Model):
    __tablename__ = 'carrera_por_curso'
    id = db.Column(db.Integer, primary_key=True)

    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'))
    carrera_id = db.Column(db.Integer, db.ForeignKey('carrera.id'))

    def __str__(self):
        return "El curso con id {} es de esta carrera: {}".format(self.curso_id, self.carrera_id)


class HorariosYaCargados(db.Model):
    __tablename__ = 'horarios_ya_cargados'
    id = db.Column(db.Integer, primary_key=True)

    anio = db.Column(db.String(4), nullable=False, server_default='')
    cuatrimestre = db.Column(db.String(1), nullable=False, server_default='')

    def __str__(self):
        return "Año: {} - {}C".format(self.anio, self.cuatrimestre)
