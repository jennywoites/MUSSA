from app.models.encuestas_models import *
from app import db

PUNTAJE_1_A_5 = 0
TEXTO_LIBRE = 1
SI_NO = 2
HORARIO = 3
DOCENTE = 4
CORRELATIVA = 5
ESTRELLAS = 6
NUMERO = 7
TAG = 8
TEMATICA = 9

TIPOS_ENCUESTAS = {
    PUNTAJE_1_A_5: "Puntaje de 1 a 5",
    TEXTO_LIBRE: "Texto Libre",
    SI_NO: "Si o No",
    HORARIO: "Horario",
    DOCENTE: "Docente",
    CORRELATIVA: "Correlativa",
    ESTRELLAS: "Estrellas",
    NUMERO: "Numero",
    TAG: "Tags / Palabras Clave",
    TEMATICA: "Temática de la Materia"
}

GRUPO_ENCUESTA_GENERAL = 0
GRUPO_ENCUESTA_CONTENIDO = 1
GRUPO_ENCUESTA_CLASES = 2
GRUPO_ENCUESTA_EXAMENES = 3
GRUPO_ENCUESTA_DOCENTES = 4

GRUPO_ENCUESTA = {
    GRUPO_ENCUESTA_GENERAL: "Aspectos Generales",
    GRUPO_ENCUESTA_CONTENIDO: "Contenido de la Materia",
    GRUPO_ENCUESTA_CLASES: "Clases",
    GRUPO_ENCUESTA_EXAMENES: "Exámenes",
    GRUPO_ENCUESTA_DOCENTES: "Docentes"
}

EXCLUIR_OBLIGATORIA = 0
EXCLUIR_OBLIGATORIA_CURSO_UNICO = 1
EXCLUIR_ELECTIVA = 2
EXCLUIR_ELECTIVA_CURSO_UNICO = 3
EXCLUIR_NUNCA = 4

EXCLUIR_CUANDO = {
    EXCLUIR_OBLIGATORIA: "Obligatoria",
    EXCLUIR_OBLIGATORIA_CURSO_UNICO: "Obligatoria con curso único",
    EXCLUIR_ELECTIVA: "Electiva",
    EXCLUIR_ELECTIVA_CURSO_UNICO: "Electiva con curso único",
    EXCLUIR_NUNCA: "Nunca"
}

# Estados paso encuesta
PASO_ENCUESTA_NO_INICIADO = 0
PASO_ENCUESTA_EN_CURSO = 1
PASO_ENCUESTA_FINALIZADO = 2


def create_encuestas():
    db.create_all()

    for cod in TIPOS_ENCUESTAS:
        find_o_create_tipo_encuesta(cod, TIPOS_ENCUESTAS[cod])

    for cod in GRUPO_ENCUESTA:
        find_o_create_grupo_encuesta(cod, GRUPO_ENCUESTA[cod])

    for cod in EXCLUIR_CUANDO:
        find_o_categoria_excluir_cuando(EXCLUIR_CUANDO[cod])

    if len(EncuestaGenerada.query.all()) == 0:
        crear_preguntas_encuesta()

    db.session.commit()


def find_o_create_tipo_encuesta(codigo, descripcion):
    query = TipoEncuesta.query.filter_by(tipo=codigo)
    tipo = query.filter_by(descripcion=descripcion).first()

    if not tipo:
        tipo = TipoEncuesta(tipo=codigo, descripcion=descripcion)
        db.session.add(tipo)
        db.session.commit()

    return tipo


def find_o_create_grupo_encuesta(cod, grupo):
    grupo_encuesta = GrupoEncuesta.query.filter_by(numero_grupo=cod).first()

    if not grupo_encuesta:
        grupo_encuesta = GrupoEncuesta(grupo=grupo, numero_grupo=cod)
        db.session.add(grupo_encuesta)
        db.session.commit()

    return grupo_encuesta


def find_o_categoria_excluir_cuando(descripcion):
    categoria = ExcluirEncuestaSi.query.filter_by(tipo=descripcion).first()

    if not categoria:
        categoria = ExcluirEncuestaSi(tipo=descripcion)
        db.session.add(categoria)
        db.session.commit()

    return categoria


def crear_preguntas_encuesta():
    orden = crear_preguntas_categoria_general(0)
    orden = crear_preguntas_categoria_contenido_de_la_materia(orden)
    orden = crear_preguntas_categoria_clases(orden)
    orden = crear_preguntas_categoria_examenes(orden)
    crear_preguntas_categoria_docentes(orden)


def crear_preguntas_categoria_general(orden):
    grupo = GrupoEncuesta.query.filter_by(grupo=GRUPO_ENCUESTA[GRUPO_ENCUESTA_GENERAL]).first()

    ##########################################################################################
    pregunta = "¿Qué te pareció el curso en general?"
    pregunta_resultados = "Calificación del curso"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, ESTRELLAS)
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)
    ##########################################################################################

    ##########################################################################################
    pregunta = "¿Te aportó algo el curso por sobre tus conocimientos previos?"
    pregunta_resultados = "¿Cuánto aportó la materia a los alumnos sobre sus conocimientos" \
                          " previos?"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, PUNTAJE_1_A_5)
    crear_pregunta_encuesta_puntaje(encuesta, "Nada", "Mucho")
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)
    ##########################################################################################

    ##########################################################################################
    pregunta = "¿Se superponen los temas con los de otras materias? " \
               "Si es así, indicar qué temas y con cuáles asignaturas."
    pregunta_resultados = "¿Los temas se superponían con otras asignaturas?"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, TEXTO_LIBRE)
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)
    ##########################################################################################

    ##########################################################################################
    pregunta = """¿Tenías los conocimientos previos suficientes para realizar esta materia?"""
    pregunta_resultados = "Al cursar la materia, el alumno ¿tenía los conocimientos previos " \
                          "necesarios para poder cursarla?"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, SI_NO)
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)

    pregunta_rta_no = "¿Qué conocimientos crees que hubiese sido bueno tener antes de comenzar" \
                      " a cursar la materia?"
    pregunta_resultados_rta_no = "Conocimientos que los alumnos creen que son necesarios tener" \
                                 " antes de cursar esta materia."
    encuestas_no = [crear_pregunta_encuesta(pregunta_rta_no, pregunta_resultados_rta_no, TEXTO_LIBRE)]
    crear_pregunta_encuesta_si_no(encuesta, [], encuestas_no)
    ##########################################################################################

    ##########################################################################################
    pregunta = """¿Cuáles crees que deberían ser las materias correlativas de esta materia?"""
    pregunta_resultados = "Materias que los alumnos creen que deberían ser cursadas " \
                          "antes de cursar esta materia."
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, CORRELATIVA)
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)
    ##########################################################################################

    ##########################################################################################
    pregunta = """¿Cuál es la temática de la materia?"""
    pregunta_resultados = "Temáticas de la materia"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, TEMATICA)
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)
    ##########################################################################################

    ##########################################################################################
    pregunta = """¿Cuál es el horario real de cursada de la materia?"""
    pregunta_resultados = "Horario real de cursada"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, HORARIO)
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)
    ##########################################################################################

    ##########################################################################################
    pregunta = "¿Cuántas horas dedicabas a estudiar la materia fuera de las horas de clases " \
               "semanalmente? Incluye horas para realizar trabajos prácticos, guías, estudiar " \
               "para exámenes."
    pregunta_resultados = "Horas de dedicación semanal de los alumnos extras al horario de " \
                          "cursada (Trabajos prácticos, guías, horas de estudio, etc)"
    MAX_HORAS_SEMANA = 24 * 7  # 24hs x 7 dias
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, NUMERO)
    crear_pregunta_encuesta_numerica(encuesta, 0, MAX_HORAS_SEMANA)
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)
    ##########################################################################################

    ##########################################################################################
    pregunta = "¿Cuál es la dificultad de la materia?"
    pregunta_resultados = "Nivel de dificultad de la materia"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, PUNTAJE_1_A_5)
    crear_pregunta_encuesta_puntaje(encuesta, "Muy difícil", "Muy fácil")
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)
    ##########################################################################################

    ##########################################################################################
    pregunta = "¿Qué tan amenos o llevaderos te resultaron los temas de la materia?"
    pregunta_resultados = "¿Qué tan amenos o llevaderos resultaron los temas de la materia" \
                          " para los alumnos?"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, PUNTAJE_1_A_5)
    crear_pregunta_encuesta_puntaje(encuesta, "Muy aburridos", "Atrapantes")
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)
    ##########################################################################################

    ##########################################################################################
    pregunta = """¿Por qué te anotaste en este curso?"""
    pregunta_resultados = "Motivos por los cuáles los alumnos se anotan en este curso"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, TEXTO_LIBRE)
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_OBLIGATORIA_CURSO_UNICO, orden)
    ##########################################################################################

    ##########################################################################################
    pregunta = """¿La materia es promocionable?"""
    pregunta_resultados = "¿La materia es promocionable?"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, SI_NO)
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)

    pregunta_rta_si = """¿Cuál es el régimen de promoción?"""
    pregunta_resultados_rta_si = "Explicación del régimen de promoción"
    encuestas_si = [crear_pregunta_encuesta(pregunta_rta_si, pregunta_resultados_rta_si, TEXTO_LIBRE)]
    crear_pregunta_encuesta_si_no(encuesta, encuestas_si, [])
    ##########################################################################################

    ##########################################################################################
    pregunta = "Escribí hasta tres palabras clave con las cuales podrías relacionar la materia " \
               "para facilitar búsquedas futuras (TAGS)"
    pregunta_resultados = "Palabras clave con las que se identifica a la materia"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, TAG)
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)
    ##########################################################################################

    ##########################################################################################
    pregunta = "Por favor, indicá todas las cosas buenas o positivas que se deberían seguir " \
               "haciendo en el curso y/o que se están haciendo poco y se deberían hacer más."
    pregunta_resultados = "Cosas buenas o positivas que se deberían seguir haciendo en el " \
                          "curso y/o que se están haciendo poco y se deberían hacer más"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, TEXTO_LIBRE)
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)
    ##########################################################################################

    ##########################################################################################
    pregunta = "Por favor, indicá todas las cosas malas o negativas que se deberían cambiar " \
               "o mejorar."
    pregunta_resultados = "Cosas malas o negativas que se deberían cambiar o mejorar"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, TEXTO_LIBRE)
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)
    ##########################################################################################

    return orden


def crear_preguntas_categoria_contenido_de_la_materia(orden):
    grupo = GrupoEncuesta.query.filter_by(grupo=GRUPO_ENCUESTA[GRUPO_ENCUESTA_CONTENIDO]).first()

    ##########################################################################################
    pregunta = """¿Cómo te resultaron los temas de la materia en general?"""
    pregunta_resultados = "Cómo resultaron a los alumnos los temas de la materia en general."
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, TEXTO_LIBRE)
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)
    ##########################################################################################

    ##########################################################################################
    pregunta = """¿Cuáles temas te resultaron más fáciles? ¿Por qué?"""
    pregunta_resultados = "Temas que resultaron más fáciles"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, TEXTO_LIBRE)
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)
    ##########################################################################################

    ##########################################################################################
    pregunta = """¿Cuáles temas te resultaron más difícles? ¿Por qué?"""
    pregunta_resultados = "Temas que resultaron más difíciles"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, TEXTO_LIBRE)
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)
    ##########################################################################################

    ##########################################################################################
    pregunta = """¿Te parece que hubo algún tema demás?"""
    pregunta_resultados = "Temas que estuvieron demás"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, TEXTO_LIBRE)
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)
    ##########################################################################################

    ##########################################################################################
    pregunta = """¿Te parece que hubo algún tema al que se le haya dedicado muy poco tiempo?"""
    pregunta_resultados = "Temas a los que se le dedicó muy poco tiempo"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, TEXTO_LIBRE)
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)
    ##########################################################################################

    ##########################################################################################
    pregunta = """¿Te parece que hubo algún tema al que se le haya dedicado demasiado tiempo?"""
    pregunta_resultados = "Temas a los que se le dedicó demasiado tiempo"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, TEXTO_LIBRE)
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)
    ##########################################################################################

    return orden


def crear_preguntas_categoria_clases(orden):
    grupo = GrupoEncuesta.query.filter_by(grupo=GRUPO_ENCUESTA[GRUPO_ENCUESTA_CLASES]).first()

    ##########################################################################################
    pregunta = """¿Qué te parecieron las clases teóricas?"""
    pregunta_resultados = "Opiniones sobre las clases teóricas"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, TEXTO_LIBRE)
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)
    ##########################################################################################

    ##########################################################################################
    pregunta = """¿Qué te parecieron las clases prácticas?"""
    pregunta_resultados = "Opiniones sobre las clases prácticas"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, TEXTO_LIBRE)
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)
    ##########################################################################################

    ##########################################################################################
    pregunta = "¿Cómo fue la disponibilidad de los ayudantes y docentes en general para" \
               "responder consultas?"
    pregunta_resultados = "Disponibilidad de los ayudantes y docentes en general para responser consultas"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, PUNTAJE_1_A_5)
    crear_pregunta_encuesta_puntaje(encuesta, "Muy mala", "Excelente")
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)
    ##########################################################################################

    ##########################################################################################
    pregunta = "¿Cómo fue la comunicación y coordinación entre los docentes de las clases " \
               "teóricas y prácticas?"
    pregunta_resultados = "Nivel de coordinación entre los docentes de las clases teóricas y prácticas"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, PUNTAJE_1_A_5)
    crear_pregunta_encuesta_puntaje(encuesta, "Muy mala", "Excelente")
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)
    ##########################################################################################

    ##########################################################################################
    pregunta = "¿Qué opinas sobre el material provisto por el curso? ¿Era de fácil acceso? " \
               "Incluye material entregado en clases, diapositivas, lecturas adicionales, " \
               "lecturas recomendadas, etc."
    pregunta_resultados = "Opiniones sobre el material provisto por el curso"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, TEXTO_LIBRE)
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)
    ##########################################################################################

    return orden


def crear_preguntas_categoria_examenes(orden):
    grupo = GrupoEncuesta.query.filter_by(grupo=GRUPO_ENCUESTA[GRUPO_ENCUESTA_EXAMENES]).first()

    ##########################################################################################
    pregunta = """¿Cómo está estructurado el parcial / parciales de la materia?"""
    pregunta_resultados = "Estructura del parcial / los parciales de la materia"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, TEXTO_LIBRE)
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)
    ##########################################################################################

    ##########################################################################################
    pregunta = """¿Cómo son los trabajos prácticos de la materia?"""
    pregunta_resultados = "Trabajos prácticos de la materia"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, TEXTO_LIBRE)
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)
    ##########################################################################################

    ##########################################################################################
    pregunta = """¿Cómo es el final o coloquio de la materia?"""
    pregunta_resultados = "Final o coloquio de la materia"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, TEXTO_LIBRE)
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)
    ##########################################################################################

    ##########################################################################################
    pregunta = "¿Crees que las calificaciones de los exámenes y trabajos prácticos fueron " \
               "justas?"
    pregunta_resultados = "¿Las califiaciones de los exámenes y trabajos prácticos fueron justas?"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, SI_NO)
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)

    pregunta_rta_no = """Si no lo crees, explicá por qué no."""
    pregunta_resultados = "Motivos por los que los alumnos no consideraron justas las calificaciones de " \
                          "los exámenes y/o trabajos prácticos"
    encuestas_no = [crear_pregunta_encuesta(pregunta_rta_no, pregunta_resultados, TEXTO_LIBRE)]
    crear_pregunta_encuesta_si_no(encuesta, [], encuestas_no)
    ##########################################################################################

    return orden


def crear_preguntas_categoria_docentes(orden):
    grupo = GrupoEncuesta.query.filter_by(grupo=GRUPO_ENCUESTA[GRUPO_ENCUESTA_DOCENTES]).first()

    ##########################################################################################
    pregunta = "Si así lo deseas, puedes dejar un comentario sobre los docentes de la materia."
    pregunta_resultados = "Comentarios realizados a los docentes del curso"
    encuesta = crear_pregunta_encuesta(pregunta, pregunta_resultados, DOCENTE)
    orden = crear_entrada_encuesta_generada(encuesta, grupo, EXCLUIR_NUNCA, orden)
    ##########################################################################################

    return orden


def crear_pregunta_encuesta(pregunta, pregunta_resultados, tipo_codigo):
    tipo = TipoEncuesta.query.filter_by(tipo=tipo_codigo).first()

    pregunta_encuesta = PreguntaEncuesta(
        pregunta=pregunta,
        tipo_id=tipo.id
    )
    db.session.add(pregunta_encuesta)
    db.session.commit()

    db.session.add(PreguntaResultadoEncuesta(
        pregunta=pregunta_resultados,
        pregunta_encuesta_id=pregunta_encuesta.id
    ))
    db.session.commit()

    return pregunta_encuesta


def crear_entrada_encuesta_generada(encuesta, grupo, motivo_exclusion, orden):
    excluir_si = ExcluirEncuestaSi.query.filter_by(tipo=EXCLUIR_CUANDO[motivo_exclusion]).first()

    db.session.add(EncuestaGenerada(
        grupo_id=grupo.id,
        encuesta_id=encuesta.id,
        excluir_si_id=excluir_si.id,
        orden=orden
    ))
    db.session.commit()

    orden += 1
    return orden


def crear_pregunta_encuesta_puntaje(encuesta, texto_min, texto_max):
    db.session.add(PreguntaEncuestaPuntaje(
        encuesta_id=encuesta.id,
        texto_min=texto_min,
        texto_max=texto_max
    ))
    db.session.commit()


def crear_pregunta_encuesta_numerica(encuesta, numero_min, numero_max):
    db.session.add(PreguntaEncuestaNumero(
        encuesta_id=encuesta.id,
        numero_min=numero_min,
        numero_max=numero_max
    ))
    db.session.commit()


def crear_pregunta_encuesta_si_no(encuesta, lista_si, lista_no):
    i = 0
    for i in range(len(lista_si)):
        pregunta = PreguntaEncuestaSiNo(encuesta_id=encuesta.id)
        pregunta.encuesta_id_si = lista_si[i].id
        if i < len(lista_no):
            pregunta.encuesta_id_no = lista_no[i].id
        db.session.add(pregunta)
        db.session.commit()

    for j in range(i, len(lista_no)):
        db.session.add(PreguntaEncuestaSiNo(
            encuesta_id=encuesta.id,
            encuesta_id_no=lista_no[j].id)
        )
        db.session.commit()
