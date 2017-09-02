from Constantes import *
from Materia import Materia

MATERIAS_1 = {
        "A": Materia("A", "A", 1, "Obligatoria", 0, ["H"]),
        "B": Materia("B", "B", 1, "Obligatoria", 0, ["E"]),
        "C": Materia("C", "C", 1, "Obligatoria", 0, ["F"]),
        "D": Materia("D", "D", 1, "Obligatoria", 0, ["F"]),
        "E": Materia("E", "E", 1, "Obligatoria", 0, ["H"]),
        "F": Materia("B", "B", 1, "Obligatoria", 0, ["G"]),
        "G": Materia("G", "G", 1, "Obligatoria", 0, []),
        "H": Materia("H", "H", 1, "Obligatoria", 0, []),
        "I": Materia("I", "I", 1, "Obligatoria", 7, []),
        "J": Materia("J", "J", 1, "Obligatoria", 0, [])
    }

ADYACENTES_1 = {
        "A": ["H"],
        "B": ["E"],
        "C": ["F"],
        "D": ["F"],
        "E": ["H"],
        "F": ["G"],
        "G": [],
        "H": [],
        "I": [],
        "J": []
    }

MATERIAS_2 = {
        "A": Materia("A", "A", 1, "Obligatoria", 0, []),
        "B": Materia("B", "B", 1, "Obligatoria", 0, []),
        "C": Materia("C", "C", 1, "Obligatoria", 0, [])
    }

ADYACENTES_2 = {
        "A": [],
        "B": [],
        "C": []
    }

MATERIAS_3 = {
        "A": Materia("A", "A", 1, "Obligatoria", 0, []),
        "B": Materia("B", "B", 1, "Obligatoria", 0, []),
        "C": Materia("C", "C", 1, "Obligatoria", 0, [])
    }

ADYACENTES_3 = {
        "A": [],
        "B": [],
        "C": []
    }

def get_materias():
    """Devuelve un diccionario con la clave el codigo de materia y como valor una materia con sus datos"""
    return MATERIAS_1

def get_plan_carrera():
    """Devuelve una lista de adyacencias para un plan de carreras"""
    return ADYACENTES_1
