from Constantes import *
from Curso import Curso
from Horario import Horario

HORARIOS_1 = {
        "A": [Curso("A", "Curso1A", [Horario(LUNES, 7, 10),Horario(MARTES,8,12)]), Curso("A", "Curso2A", [Horario(JUEVES, 8, 15),Horario(SABADO,9,13)]), Curso("A", "Curso3A", [Horario(MARTES, 17, 21)])],
        "B": [Curso("B", "Curso1B", [Horario(LUNES, 7, 10),Horario(JUEVES,7,10)])],
        "C": [Curso("C", "Curso1C", [Horario(LUNES, 12, 15),Horario(MIERCOLES,8,12)])],
        "D": [Curso("D", "Curso1D", [Horario(LUNES, 7, 10),Horario(VIERNES,8,12)]), Curso("D", "Curso2D", [Horario(LUNES, 12, 15),Horario(MIERCOLES,8,9)]), Curso("D", "Curso3D", [Horario(JUEVES, 12, 15),Horario(VIERNES,12,15)]), Curso("D", "Curso4D", [Horario(MARTES, 9, 11),Horario(JUEVES,10.5,12.5)])],
        "E": [Curso("E", "Curso1E", [Horario(LUNES, 7, 10),Horario(VIERNES,8,11)]), Curso("E", "Curso2E", [Horario(MARTES, 8, 15)])],
        "F": [Curso("F", "Curso1F", [Horario(VIERNES, 8, 13)]), Curso("F", "Curso2F", [Horario(VIERNES, 15, 20)])],
        "G": [Curso("G", "Curso1G", [Horario(VIERNES, 8, 13)])],
        "H": [Curso("H", "Curso1H", [Horario(SABADO, 15, 21)])],
        "I": [Curso("I", "Curso1I", [Horario(SABADO, 21, 21.5)])],
        "J": [Curso("J", "Curso1J", [Horario(SABADO, 22, 23)])],
    }

HORARIOS_2 = {
        "A": [Curso("A", "Curso1A", [Horario(LUNES, 9, 12)]), Curso("A", "Curso2A", [Horario(MARTES, 8, 13)])],
        "B": [Curso("B", "Curso1B", [Horario(LUNES, 9, 12)]), Curso("B", "Curso2B", [Horario(MIERCOLES, 13, 16)])],
        "C": [Curso("C", "Curso1C", [Horario(JUEVES, 9, 14)])],
    }

HORARIOS_3 = {
        "A": [Curso("A", "Curso1A", [Horario(LUNES, 9, 10)])],
        "B": [Curso("B", "Curso1B", [Horario(LUNES, 10.5, 11)])],
        "C": [Curso("C", "Curso1C", [Horario(LUNES, 9, 11)]), Curso("C", "Curso2C", [Horario(LUNES, 9, 10)])],
    }

HORARIOS_4 = {
        "A": [Curso("A", "Curso1A", [Horario(LUNES, 7, 10),Horario(MARTES,8,12)]), Curso("A", "Curso2A", [Horario(JUEVES, 8, 15),Horario(SABADO,9,13)]), Curso("A", "Curso3A", [Horario(MARTES, 17, 21)])],
        "B": [Curso("B", "Curso1B", [Horario(LUNES, 7, 10),Horario(JUEVES,7,10)])],
        "C": [Curso("C", "Curso1C", [Horario(LUNES, 12, 15),Horario(MIERCOLES,8,12)])],
        "D": [Curso("D", "Curso1D", [Horario(LUNES, 7, 10),Horario(VIERNES,8,12)]), Curso("D", "Curso2D", [Horario(LUNES, 12, 15),Horario(MIERCOLES,8,9)]), Curso("D", "Curso3D", [Horario(JUEVES, 12, 15),Horario(VIERNES,12,15)]), Curso("D", "Curso4D", [Horario(MARTES, 9, 11),Horario(JUEVES,10.5,12.5)])],
        "E": [Curso("E", "Curso1E", [Horario(LUNES, 7, 10),Horario(VIERNES,8,11)]), Curso("E", "Curso2E", [Horario(MARTES, 8, 15)])],
        "F": [Curso("F", "Curso1F", [Horario(VIERNES, 8, 13)]), Curso("F", "Curso2F", [Horario(VIERNES, 15, 20)])],
        "G": [Curso("G", "Curso1G", [Horario(VIERNES, 8, 13)])],
        "H": [Curso("H", "Curso1H", [Horario(SABADO, 15, 21)])],
        "I": [Curso("I", "Curso1I", [Horario(SABADO, 21, 21.5)])],
        "J": [Curso("J", "Curso1J", [Horario(SABADO, 22, 23)])],
        "K": [Curso("K", "Curso1K", [Horario(MIERCOLES, 9, 12)])],
        "L": [Curso("L", "Curso1L", [Horario(MIERCOLES, 9, 12)])],
        "M": [Curso("M", "Curso1M", [Horario(MIERCOLES, 9, 12)])],
        "N": [Curso("N", "Curso1N", [Horario(MIERCOLES, 9, 12)])],
    }

HORARIOS = {
    1: HORARIOS_1,
    2: HORARIOS_2,
    3: HORARIOS_3,
    4: HORARIOS_4
}

def get_horarios_no_permitidos(num=0):
    """
    Devuelve una lista de horarios en los que el alumno no puede cursar por motivos personales.
    """
    return []


def get_horarios(num):
    return HORARIOS[num]

