import datetime
import os

from flask import current_app

from app import db
from app.models.alumno_models import EstadoMateria, FormaAprobacionMateria

#####################################################################
##                      Estados de Materias                        ##
#####################################################################

PENDIENTE = 0
EN_CURSO = 1
FINAL_PENDIENTE = 2
APROBADA = 4
DESAPROBADA = 5

ESTADO_MATERIA = {
    PENDIENTE: "Pendiente de cursar",
    EN_CURSO: "Cursando actualmente",
    FINAL_PENDIENTE: "Final Pendiente",
    APROBADA: "Aprobada",
    DESAPROBADA: "Desaprobada"
}

def create_estados_materia():
    for codigo in ESTADO_MATERIA:
        db.session.add(EstadoMateria(estado=ESTADO_MATERIA[codigo]))

    db.session.commit()


#####################################################################
##                Formas de Aprobación de Materias                 ##
#####################################################################

EXAMEN = 0
EXAMEN_EQUIVALENCIA = 1
EQUIVALENCIA = 2

FORMA_APROBACION = {
    EXAMEN: "Examen",
    EXAMEN_EQUIVALENCIA: "Examen de Equivalencia",
    EQUIVALENCIA: "Equivalencia"
}

def create_forma_aprobacion_materias():
    for codigo in FORMA_APROBACION:
        db.session.add(FormaAprobacionMateria(forma=FORMA_APROBACION[codigo]))

    db.session.commit()
