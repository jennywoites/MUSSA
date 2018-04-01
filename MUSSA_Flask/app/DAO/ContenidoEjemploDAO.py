from app.DAO.UsersDAO import find_or_create_user
import random
from app.models.carreras_models import Carrera, Materia, Correlativas
from app.models.horarios_models import Curso, CarreraPorCurso, HorarioPorCurso, Horario
from app.models.alumno_models import AlumnosCarreras, Alumno, EstadoMateria, MateriasAlumno
from app.models.docentes_models import CursosDocente
from app.models.palabras_clave_models import TematicaMateria
from app.API_Rest.Services.AlumnoServices.CarreraAlumnoService import CarreraAlumnoService
from app.API_Rest.Services.AlumnoServices.MateriaAlumnoService import MateriaAlumnoService
from app.API_Rest.Services.AlumnoServices.EncuestaAlumnoService import EncuestaAlumnoService
from app.API_Rest.Services.AlumnoServices.RespuestasEncuestaAlumnoService import RespuestasEncuestaAlumnoService
from app.models.respuestas_encuesta_models import EncuestaAlumno
from app.DAO.EncuestasDAO import *
from app.utils import get_numero_dos_digitos
from app.DAO.MateriasDAO import ESTADO_MATERIA, PENDIENTE, EN_CURSO, APROBADA, DESAPROBADA, FINAL_PENDIENTE
from datetime import datetime

NOMBRES = [u"Juan", u"Andrea", u"Lucas", u"Rocio", u"Nicolas", u"Julieta", u"Ariel", u"Jennifer", u"Diego", u"Daniela",
           u"Florencia", u"Clara", u"Nestor", u"Gisel", u"Mariel", u"Lorena", u"Alan", u"Aldana", u"Marcelo"]

APELLIDOS = [u"Lopez", u"Woites", u"Essaya", u"Echeverry", u"Cadher", u"Gonzales", u"Ferreira", u"Soto", u"Riesgo",
             u"Noé", u"Pérez"]

TEXTOS_POSIBLES = [
    """Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.""",
    """Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo.""",
    """Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus.""",
    """Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet.""",
    """Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus.""",
    """Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem.""",
    """Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus. Nullam quis ante. Etiam sit amet orci eget eros faucibus tincidunt. Duis leo.""",
    """Sed fringilla mauris sit amet nibh. Donec sodales sagittis magna. Sed consequat, leo eget bibendum sodales, augue velit cursus nunc."""
]

PALABRAS_CLAVE_DISPONIBLES = ["ALGORITMOS", "PROGRAMACION", "OBJETOS", "GREEDY", "PLE", "GRAFOS", "MATEMATICA",
                              "STOCKS", "IDIOMA", "NOVEDOSO", "TECNOLOGIA", "REDES", "CRIPTOGRAFIA", "SEGURIDAD",
                              "INFORMACION", "ADMINISTRACION", "GESTION", "BDD", "PYTHON", "C++", "C", "JAVA", "POO",
                              "DERIVADAS", "INTEGRALES", "MATRICES"]


def crear_datos_de_ejemplo():
    """ Creacion de datos de ejmplo: Usuarios con carreras, materias y encuestas asociadas"""

    # Create all tables
    db.create_all()

    usuarios_ejemplo = crear_usuarios_ejemplo()

    for usuario in usuarios_ejemplo:
        cargar_materias_alumno(usuario)
        completar_encuestas(usuario)

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
    materias = MateriasAlumno.query.filter_by(alumno_id=alumno.id).filter_by(estado_id=estado_pendiente.id).all()
    for materia_alumno in materias:
        if materia_alumno.estado_id != estado_pendiente.id:
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
        datos_materia["idCurso"] = "-1"
    else:
        datos_materia["idCurso"] = random.choice(cursos).id

    estado = random.choice([EN_CURSO, FINAL_PENDIENTE, APROBADA, DESAPROBADA])
    datos_materia["estado"] = ESTADO_MATERIA[estado]

    datos_materia["cuatrimestre_aprobacion"] = None
    datos_materia["anio_aprobacion"] = None
    datos_materia["fecha_aprobacion"] = None
    datos_materia["forma_aprobacion"] = None
    datos_materia["calificacion"] = None
    datos_materia["acta_resolucion"] = None

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
        "2": {
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

    CarreraAlumnoService().agregar_materias_carrera(alumno.id, carrera.id)
    db.session.commit()
    return carrera


def completar_encuestas(usuario):
    alumno = encontrar_o_crear_alumno(usuario)

    encuestas = EncuestaAlumno.query.filter_by(alumno_id=alumno.id).all()
    for encuesta in encuestas:
        for numero_grupo in [GRUPO_ENCUESTA_CLASES, GRUPO_ENCUESTA_GENERAL, GRUPO_ENCUESTA_EXAMENES,
                             GRUPO_ENCUESTA_DOCENTES, GRUPO_ENCUESTA_CONTENIDO]:
            completar_encuesta(encuesta, numero_grupo)
        finalizar_encuesta(encuesta)


def completar_encuesta(encuesta, numero_grupo):
    categoria = GrupoEncuesta.query.filter_by(numero_grupo=numero_grupo).first().id

    servicio = RespuestasEncuestaAlumnoService()
    preguntas_categoria_actual = servicio.obtener_preguntas_encuestas(categoria, True)

    respuestas = []
    for id_pregunta in preguntas_categoria_actual:
        agregar_respuesta_para_pregunta(encuesta, respuestas, preguntas_categoria_actual[id_pregunta])

    servicio.guardar_respuestas(respuestas, encuesta.id, preguntas_categoria_actual)

    servicio.actualizar_estado_paso_actual(encuesta.id, preguntas_categoria_actual, categoria)


def agregar_respuesta_para_pregunta(encuesta, respuestas, pregunta):
    tipo_pregunta = TipoEncuesta.query.get(pregunta.tipo_id).tipo

    datos = {}
    datos["idPregunta"] = pregunta.id
    datos["tipo_encuesta"] = tipo_pregunta

    if tipo_pregunta == TEXTO_LIBRE:
        return generar_respuesta_texto_libre(respuestas, datos)

    if tipo_pregunta == PUNTAJE_1_A_5:
        return generar_respuesta_puntaje(respuestas, datos)

    if tipo_pregunta == NUMERO:
        return generar_respuesta_numero(respuestas, datos)

    if tipo_pregunta == HORARIO:
        return generar_respuesta_horario(respuestas, datos, encuesta)

    if tipo_pregunta == DOCENTE:
        return generar_respuesta_docentes(respuestas, datos, encuesta)

    if tipo_pregunta == CORRELATIVA:
        return generar_respuesta_correlativas(respuestas, datos, encuesta)

    if tipo_pregunta == ESTRELLAS:
        return generar_respuesta_estrellas(respuestas, datos)

    if tipo_pregunta == TEMATICA:
        return generar_respuesta_tematicas(respuestas, datos)

    if tipo_pregunta == TAG:
        return generar_respuesta_palabras_clave(respuestas, datos)

    if tipo_pregunta == SI_NO:
        return generar_respuesta_si_o_no(respuestas, datos)


def generar_respuesta_horario(respuestas, datos, encuesta):
    materia_alumno = MateriasAlumno.query.get(encuesta.materia_alumno_id)

    horarios_curso = HorarioPorCurso.query.filter_by(curso_id=materia_alumno.curso_id) \
        .filter_by(es_horario_activo=True).all()

    horarios = []
    for horario_curso in horarios_curso:
        horario = Horario.query.get(horario_curso.horario_id)
        horarios.append({
            "dia": horario.dia,
            "hora_desde": horario_reloj_aproximado(horario.hora_desde),
            "hora_hasta": horario_reloj_aproximado(horario.hora_hasta)
        })

    datos["horarios"] = horarios
    respuestas.append(datos)


def horario_reloj_aproximado(horario_decimal):
    horario_decimal = float(horario_decimal)
    horario_decimal += random.choice([0, 0.5, -0.5])

    MIN_HORA = 7
    MAX_HORA = 23
    if horario_decimal < MIN_HORA:
        horario_decimal = MIN_HORA
    elif horario_decimal > MAX_HORA:
        horario_decimal = MAX_HORA

    hora = int(horario_decimal)
    minutos = "00" if hora == horario_decimal else "30"
    return "{}:{}".format(get_numero_dos_digitos(hora), minutos)


def generar_respuesta_palabras_clave(respuestas, datos):
    palabras = []

    MAX_PALABRAS = 3
    for i in range(MAX_PALABRAS):
        palabra = random.choice(PALABRAS_CLAVE_DISPONIBLES)
        if not palabra in palabras:
            palabras.append(palabra)

    datos["palabras_clave"] = palabras
    respuestas.append(datos)


def generar_respuesta_tematicas(respuestas, datos):
    tematicas = []

    MAX_TEMATICAS = 8
    tematicas_disponibles = [tematica.tematica for tematica in TematicaMateria.query.all()]
    for i in range(MAX_TEMATICAS):
        tematica = random.choice(tematicas_disponibles)
        if not tematica in tematicas:
            tematicas.append(tematica)

    datos["tematicas"] = tematicas
    respuestas.append(datos)


def generar_respuesta_docentes(respuestas, datos, encuesta):
    materia_alumno = MateriasAlumno.query.get(encuesta.materia_alumno_id)
    docentes_curso = CursosDocente.query.filter_by(curso_id=materia_alumno.curso_id).all()

    docentes = []
    for docente in docentes_curso:
        docentes.append({
            "id_docente": docente.docente_id,
            "comentario": random.choice(TEXTOS_POSIBLES)
        })
    datos["docentes"] = docentes
    respuestas.append(datos)


def generar_respuesta_texto_libre(respuestas, datos):
    datos["texto"] = random.choice(TEXTOS_POSIBLES)
    respuestas.append(datos)


def generar_respuesta_si_o_no(respuestas, datos):
    datos["respuesta"] = random.choice([True, False])
    respuestas.append(datos)


def generar_respuesta_correlativas(respuestas, datos, encuesta):
    materia_alumno = MateriasAlumno.query.get(encuesta.materia_alumno_id)
    materia = Materia.query.get(materia_alumno.materia_id)

    correlativas = []
    for correlativa in Correlativas.query.filter_by(materia_id=materia.id).all():
        correlativas.append(correlativa.materia_correlativa_id)

    datos["correlativas"] = correlativas
    respuestas.append(datos)


def generar_respuesta_puntaje(respuestas, datos):
    MIN_PUNTAJE = 1
    MAX_PUNTAJE = 5
    datos["puntaje"] = random.choice([x for x in range(MIN_PUNTAJE, MAX_PUNTAJE + 1)])
    respuestas.append(datos)


def generar_respuesta_numero(respuestas, datos):
    MAX_NUMERO = 24 * 7  # 24hs 7 dias
    datos["numero"] = random.choice([x for x in range(MAX_NUMERO + 1)])
    respuestas.append(datos)


def generar_respuesta_estrellas(respuestas, datos):
    MIN_ESTRELLAS = 1
    MAX_ESTRELLAS = 5
    datos["estrellas"] = random.choice([x for x in range(MIN_ESTRELLAS, MAX_ESTRELLAS + 1)])
    respuestas.append(datos)


def finalizar_encuesta(encuesta):
    encuesta.finalizada = True
    db.session.commit()

    materiaAlumno = MateriasAlumno.query.get(encuesta.materia_alumno_id)

    servicio = EncuestaAlumnoService()
    servicio.agregarPalabrasClavesALasMaterias(encuesta, materiaAlumno.materia_id)
    servicio.agregarTematicasALasMaterias(encuesta, materiaAlumno.materia_id)
    servicio.actualizar_puntaje_y_cantidad_encuestas_curso(encuesta, materiaAlumno.curso_id)

    db.session.commit()
