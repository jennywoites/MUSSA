from app.API_Rest.GeneradorPlanCarreras.modelos.Curso import Curso
from app.API_Rest.GeneradorPlanCarreras.modelos.Materia import Materia
from app.API_Rest.GeneradorPlanCarreras.modelos.Horario import Horario
from app.API_Rest.GeneradorPlanCarreras.ParametrosDTO import OBLIGATORIA, ELECTIVA
from app.API_Rest.GeneradorPlanCarreras.Constantes import *

#############################################
##              Horarios                   ##
#############################################

LUNES_7_7y5 = Horario(
    dia=LUNES,
    hora_inicio=7,
    hora_fin=7.5
)

LUNES_7y5_8 = Horario(
    dia=LUNES,
    hora_inicio=7.5,
    hora_fin=8
)

LUNES_7_8 = Horario(
    dia=LUNES,
    hora_inicio=7,
    hora_fin=8
)

LUNES_8_8y5 = Horario(
    dia=LUNES,
    hora_inicio=8,
    hora_fin=8.5
)

LUNES_8_9 = Horario(
    dia=LUNES,
    hora_inicio=8,
    hora_fin=9
)

LUNES_8y5_9 = Horario(
    dia=LUNES,
    hora_inicio=8.5,
    hora_fin=9
)

LUNES_9_9y5 = Horario(
    dia=LUNES,
    hora_inicio=9,
    hora_fin=9.5
)

LUNES_9_10 = Horario(
    dia=LUNES,
    hora_inicio=9,
    hora_fin=10
)

MARTES_7_8 = Horario(
    dia=MARTES,
    hora_inicio=7,
    hora_fin=8
)

MARTES_8_9 = Horario(
    dia=MARTES,
    hora_inicio=8,
    hora_fin=9
)

#############################################
##              Materias                   ##
#############################################

MATERIA_A_OBLIGATORIA = Materia(
    id_materia='1',
    codigo='A',
    nombre='Materia A',
    creditos=6,
    tipo=OBLIGATORIA,
    cred_min=0,
    correlativas=[],
    tematicas_principales=[],
    medias_horas_extras_cursada=12
)

CURSO_1_MATERIA_A = Curso(
    id_curso='1',
    cod_materia='A',
    nombre_curso='1A',
    horarios=[LUNES_7_8],
    se_dicta_primer_cuatrimestre=True,
    se_dicta_segundo_cuatrimestre=False,
    puntaje=0
)

CURSO_2_MATERIA_A = Curso(
    id_curso='2',
    cod_materia='A',
    nombre_curso='2A',
    horarios=[MARTES_7_8],
    se_dicta_primer_cuatrimestre=False,
    se_dicta_segundo_cuatrimestre=True,
    puntaje=0
)

CURSO_3_MATERIA_A = Curso(
    id_curso='6',
    cod_materia='A',
    nombre_curso='3A',
    horarios=[LUNES_7_7y5],
    se_dicta_primer_cuatrimestre=True,
    se_dicta_segundo_cuatrimestre=True,
    puntaje=0
)

##################################################
MATERIA_B_OBLIGATORIA = Materia(
    id_materia='2',
    codigo='B',
    nombre='Materia B',
    creditos=6,
    tipo=OBLIGATORIA,
    cred_min=0,
    correlativas=[],
    tematicas_principales=[],
    medias_horas_extras_cursada=12
)

CURSO_1_MATERIA_B = Curso(
    id_curso='3',
    cod_materia='B',
    nombre_curso='1B',
    horarios=[LUNES_8_9],
    se_dicta_primer_cuatrimestre=False,
    se_dicta_segundo_cuatrimestre=True,
    puntaje=0
)

CURSO_2_MATERIA_B = Curso(
    id_curso='4',
    cod_materia='B',
    nombre_curso='2B',
    horarios=[MARTES_8_9],
    se_dicta_primer_cuatrimestre=True,
    se_dicta_segundo_cuatrimestre=False,
    puntaje=0
)

CURSO_3_MATERIA_B = Curso(
    id_curso='7',
    cod_materia='B',
    nombre_curso='3B',
    horarios=[LUNES_7y5_8],
    se_dicta_primer_cuatrimestre=True,
    se_dicta_segundo_cuatrimestre=True,
    puntaje=0
)
##############################################
MATERIA_C_OBLIGATORIA = Materia(
    id_materia='3',
    codigo='C',
    nombre='Materia C',
    creditos=6,
    tipo=OBLIGATORIA,
    cred_min=0,
    correlativas=[MATERIA_A_OBLIGATORIA.id_materia],
    tematicas_principales=[],
    medias_horas_extras_cursada=12
)

CURSO_1_MATERIA_C = Curso(
    id_curso='5',
    cod_materia='C',
    nombre_curso='1C',
    horarios=[LUNES_9_10],
    se_dicta_primer_cuatrimestre=True,
    se_dicta_segundo_cuatrimestre=True,
    puntaje=0
)

CURSO_2_MATERIA_C = Curso(
    id_curso='8',
    cod_materia='C',
    nombre_curso='2C',
    horarios=[LUNES_8_8y5],
    se_dicta_primer_cuatrimestre=True,
    se_dicta_segundo_cuatrimestre=True,
    puntaje=0
)
#############################################
MATERIA_D_OBLIGATORIA = Materia(
    id_materia='4',
    codigo='D',
    nombre='Materia D',
    creditos=6,
    tipo=OBLIGATORIA,
    cred_min=0,
    correlativas=[MATERIA_B_OBLIGATORIA.id_materia, MATERIA_C_OBLIGATORIA.id_materia],
    tematicas_principales=[],
    medias_horas_extras_cursada=12
)

CURSO_1_MATERIA_D = Curso(
    id_curso='9',
    cod_materia='D',
    nombre_curso='1D',
    horarios=[LUNES_8y5_9],
    se_dicta_primer_cuatrimestre=True,
    se_dicta_segundo_cuatrimestre=True,
    puntaje=0
)
##############################################
MATERIA_E_OBLIGATORIA = Materia(
    id_materia='5',
    codigo='E',
    nombre='Materia E',
    creditos=6,
    tipo=OBLIGATORIA,
    cred_min=0,
    correlativas=[],
    tematicas_principales=[],
    medias_horas_extras_cursada=12
)

CURSO_1_MATERIA_E = Curso(
    id_curso='10',
    cod_materia='E',
    nombre_curso='1E',
    horarios=[LUNES_9_9y5],
    se_dicta_primer_cuatrimestre=True,
    se_dicta_segundo_cuatrimestre=True,
    puntaje=0
)
