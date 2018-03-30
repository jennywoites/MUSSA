from app import db
from app.DAO.UsersDAO import find_or_create_user
import random
from app.models.carreras_models import Carrera, Materia
from app.models.horarios_models import Curso, CarreraPorCurso
from app.models.alumno_models import AlumnosCarreras, Alumno, EstadoMateria, MateriasAlumno
from app.API_Rest.Services.AlumnoServices.AllMateriasAlumnoService import AllMateriasAlumnoService
from app.API_Rest.Services.AlumnoServices.MateriaAlumnoService import MateriaAlumnoService
from app.DAO.MateriasDAO import ESTADO_MATERIA, PENDIENTE, EN_CURSO, APROBADA, DESAPROBADA, FINAL_PENDIENTE
from datetime import datetime

NOMBRES = [u"Juan", u"Andrea", u"Lucas", u"Rocio", u"Nicolas", u"Julieta", u"Ariel", u"Jennifer", u"Diego", u"Daniela",
           u"Florencia", u"Clara", u"Nestor", u"Gisel", u"Mariel", u"Lorena", u"Alan", u"Aldana", u"Marcelo"]
APELLIDOS = [u"Lopez", u"Woites", u"Essaya", u"Echeverry", u"Cadher", u"Gonzales", u"Ferreira", u"Soto", u"Riesgo",
             u"Noé", u"Pérez"]


def crear_datos_de_ejemplo():
    """ Creacion de datos de ejmplo: Usuarios con carreras, materias y encuestas asociadas"""

    # Create all tables
    db.create_all()

    usuarios_ejemplo = crear_usuarios_ejemplo()

    for usuario in usuarios_ejemplo:
        cargar_materias_alumno(usuario)
        # completar_encuestas(usuario)

    # Save to DB
    db.session.commit()


def crear_usuarios_ejemplo():
    usuarios_ejemplo = []
    MAX_USUARIOS = 2000
    for i in range(MAX_USUARIOS):
        nombre = random.choice(NOMBRES)
        apellido = random.choice(APELLIDOS)
        email = u'member{}@example.com'.format(i)
        user = find_or_create_user(nombre, apellido, email, 'Password1')
        usuarios_ejemplo.append(user)
    db.session.commit()
    return usuarios_ejemplo


def encontrar_o_crear_alumno(usuario):
    alumno = Alumno.query.filter_by(user_id=usuario.id).first()
    if not alumno:
        alumno = Alumno(user_id=usuario.id)
        db.session.add(alumno)
        db.session.commit()
    return alumno


def cargar_materias_alumno(usuario):
    alumno = encontrar_o_crear_alumno(usuario)

    carrera = agregar_carrera(alumno)
    cambiar_estados_materias(alumno, carrera)


def cambiar_estados_materias(alumno, carrera):
    """
    Modifica el estado de las materias pendientes a aprobado, desparobado,
    en curso, con final pendiente, o la deja en PENDIENTE con cierta
    probabilidad
    """
    estado_pendiente = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[PENDIENTE]).first()
    materias = MateriasAlumno.query.filter_by(alumno_id=alumno.id).filter_by(estado_id=estado_pendiente).all()
    for materia_alumno in materias:
        if materia_alumno.estado_id != estado_pendiente:
            continue  # Puede suceder que sea incompatible con otra y se haya cambiado su estado

        if random.choice([True, False]):
            datos_materia = obtener_datos_materia(materia_alumno, carrera)
            MateriaAlumnoService().actualizar_materia_alumno(datos_materia)


def obtener_datos_materia(materia_alumno, carrera):
    datos_materia = {}
    datos_materia["idMateriaAlumno"] = materia_alumno.id

    materia = Materia.query.get(materia_alumno.materia_id)
    query_ids_de_cursos_validos = CarreraPorCurso.query.with_entities(CarreraPorCurso.curso_id).filter_by(
        carrera_id=carrera.id)
    cursos = Curso.query.filter_by(codigo_materia=materia.codigo).filter(
        Curso.id.in_(query_ids_de_cursos_validos)).all()
    if not cursos:
        datos_materia["idCurso"] = -1
    else:
        datos_materia["idCurso"] = random.choice(cursos).id

    estado = random.choice([EN_CURSO, FINAL_PENDIENTE, APROBADA, DESAPROBADA])
    datos_materia["estado"] = ESTADO_MATERIA[estado]

    if estado == EN_CURSO:
        return datos_materia

    datos_materia["cuatrimestre_aprobacion"] = random.choice([1, 2])

    anios = []
    MAX_ANIOS = 5
    for i in range(MAX_ANIOS):
        anios.append(datetime.today().year - (i + 1))
    datos_materia["anio_aprobacion"] = random.choice(anios)

    if estado == FINAL_PENDIENTE:
        return datos_materia

    fechas = {
        "1": {
            "dia_inicio": 1,
            "mes_inicio": 1,
            "dia_fin": 30,
            "mes_fin": 6
        },
        "1": {
            "dia_inicio": 1,
            "mes_inicio": 7,
            "dia_fin": 30,
            "mes_fin": 12
        }
    }
    fecha_cuatrimestre = fechas[str(datos_materia["cuatrimestre_aprobacion"])]
    start_date = datetime.today().replace(year=datos_materia["anio_aprobacion"], day=fecha_cuatrimestre["dia_inicio"],
                                          month=fecha_cuatrimestre["mes_inicio"]).toordinal()
    end_date = datetime.today().replace(year=datos_materia["anio_aprobacion"], day=fecha_cuatrimestre["dia_fin"],
                                        month=fecha_cuatrimestre["mes_fin"]).toordinal()
    fecha_aprobacion = datetime.fromordinal(random.randint(start_date, end_date))
    datos_materia["fecha_aprobacion"] = "{}-{}-{}".format(fecha_aprobacion.year, fecha_aprobacion.month,
                                                          fecha_aprobacion.day)

    datos_materia["forma_aprobacion"] = 'Examen'

    if estado == APROBADA:
        datos_materia["calificacion"] = random.choice([x for x in range(4, 10 + 1)])
    else:
        datos_materia["calificacion"] = random.choice([x for x in range(2, 4)])

    acta_resolucion = ""
    for i in range(7):
        acta_resolucion += str(random.randint(0, 9))
    datos_materia["acta_resolucion"] = ""

    return datos_materia


def agregar_carrera(alumno):
    carrera = random.choice(Carrera.query.all())

    carrera_nueva = AlumnosCarreras(alumno_id=alumno.id, carrera_id=carrera.id)
    db.session.add(carrera_nueva)
    db.session.commit()

    AllMateriasAlumnoService().agregar_materias_carrera(alumno.id, carrera.id)
    return carrera
