from app import db


class PlanDeEstudios(db.Model):
    __tablename__ = 'plan_de_estudios'

    id = db.Column(db.Integer, primary_key=True)

    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'))
    fecha_generacion = db.Column(db.DateTime)
    fecha_ultima_actualizacion = db.Column(db.DateTime)
    estado_id = db.Column(db.Integer, db.ForeignKey('estado_plan_de_estudios.id'))

    cuatrimestre_inicio_plan = db.Column(db.Integer, nullable=False, server_default='0')
    anio_inicio_plan = db.Column(db.String(30), nullable=False, server_default='')

    def __str__(self):
        return "Plan de Estudios {}".format(self.id)


class EstadoPlanDeEstudios(db.Model):
    __tablename__ = 'estado_plan_de_estudios'

    id = db.Column(db.Integer, primary_key=True)

    numero = db.Column(db.Integer, nullable=False, server_default='0')
    descripcion = db.Column(db.String(30), nullable=False, server_default='')


class MateriaPlanDeEstudios(db.Model):
    __tablename__ = 'materia_plan_de_estudios'
    id = db.Column(db.Integer, primary_key=True)

    plan_estudios_id = db.Column(db.Integer, db.ForeignKey('plan_de_estudios.id'))
    carrera_id = db.Column(db.Integer, db.ForeignKey('carrera.id'))
    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'))

    # El orden representa el cuatrimestre en la que se va a cursar la materia. Por ejemplo,
    # la materia A con orden 1 se cursa en el primer cuatrimestre y la materia B de orden 2,
    # se cursa en el cuatrimestre siguiente a la materia A.
    orden = db.Column(db.Integer, nullable=False, server_default='0')


class PreferenciasGeneracionPlanDeEstudios(db.Model):
    __tablename__ = 'preferencias_generacion_plan_de_estudios'
    id = db.Column(db.Integer, primary_key=True)

    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'))

    cant_cuatrimestres_max = db.Column(db.Integer, nullable=False, server_default='0')
    hs_cursada_por_semana_max = db.Column(db.Integer, nullable=False, server_default='0')
    hs_extras_por_semana_max = db.Column(db.Integer, nullable=False, server_default='0')

    # Horarios que el alumno no puede cursar
    # indicados en HorarioPreferenciasGeneracionPlanDeEstudios

    # Si el porcentaje de las materias no suma el 100%, el porcentaje restante corresponde
    # a cualquier temática de forma de no restringir tan fuertemente el valor.
    # Tematicas y porcentajes seleccionados por el alumno
    # indicados en TematicaPreferenciasGeneracionPlanDeEstudios

    puntaje_minimo_cursos = db.Column(db.Integer, nullable=False, server_default='0')

    # Momento estimado de aprobacion de las materias con final pendiente. Tener en cuenta
    # que las materias pendientes pueden haberse modificado desde la ultima selección de
    # preferencias
    # indicados en AprobacionFinalesPreferenciasGeneracionPlanDeEstudios


class HorarioPreferenciasGeneracionPlanDeEstudios(db.Model):
    __tablename__ = 'horario_preferencias_generacion_plan_de_estudios'
    id = db.Column(db.Integer, primary_key=True)

    preferencias_id = db.Column(db.Integer, db.ForeignKey('preferencias_generacion_plan_de_estudios.id'))
    horario_id = db.Column(db.Integer, db.ForeignKey('horario.id'))


class TematicaPreferenciasGeneracionPlanDeEstudios(db.Model):
    __tablename__ = 'tematica_preferencias_generacion_plan_de_estudios'
    id = db.Column(db.Integer, primary_key=True)

    preferencias_id = db.Column(db.Integer, db.ForeignKey('preferencias_generacion_plan_de_estudios.id'))
    tematica_id = db.Column(db.Integer, db.ForeignKey('tematica_materia.id'))
    porcentaje = db.Column(db.Integer, nullable=False, server_default='0')


class AprobacionFinalesPreferenciasGeneracionPlanDeEstudios(db.Model):
    __tablename__ = 'aprobacion_finales_preferencias_generacion_plan_de_estudios'
    id = db.Column(db.Integer, primary_key=True)

    preferencias_id = db.Column(db.Integer, db.ForeignKey('preferencias_generacion_plan_de_estudios.id'))

    # Numero de cuatrimestre en que se espera tener el final aprobado
    # 0 equivale a suponer que a partir del primer cuatrimestre del plan el final ya va a estar aprobado
    # 1 equivale a suponer que luego del primer cuatrimestre del plan el final va a estar aprobado, etc.
    num_cuatrimestre_aprobacion = db.Column(db.Integer, nullable=False, server_default='0')

    # Los ids no se vinculan como foreign key ya que pueden dejar de existir y no se desea mantenerlos
    # vinculados. Si deja de existir el id, no considerar el final correspondiente.
    carrera_id = db.Column(db.Integer, nullable=False, server_default='0')
    materia_alumno_id = db.Column(db.Integer, nullable=False, server_default='0')
