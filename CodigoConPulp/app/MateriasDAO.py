from Constantes import *
from Materia import Materia

MATERIAS_1 = {
        "A": Materia("A", "A", 1, OBLIGATORIA, 0, ["H"]),
        "B": Materia("B", "B", 1, OBLIGATORIA, 0, ["E"]),
        "C": Materia("C", "C", 1, OBLIGATORIA, 0, ["F"]),
        "D": Materia("D", "D", 1, OBLIGATORIA, 0, ["F"]),
        "E": Materia("E", "E", 1, OBLIGATORIA, 0, ["H"]),
        "F": Materia("B", "B", 1, OBLIGATORIA, 0, ["G"]),
        "G": Materia("G", "G", 1, OBLIGATORIA, 0, []),
        "H": Materia("H", "H", 1, OBLIGATORIA, 0, []),
        "I": Materia("I", "I", 1, OBLIGATORIA, 7, []),
        "J": Materia("J", "J", 1, OBLIGATORIA, 0, [])
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
        "A": Materia("A", "A", 1, OBLIGATORIA, 0, []),
        "B": Materia("B", "B", 1, OBLIGATORIA, 0, []),
        "C": Materia("C", "C", 1, OBLIGATORIA, 0, [])
    }

ADYACENTES_2 = {
        "A": [],
        "B": [],
        "C": []
    }

MATERIAS_3 = {
        "A": Materia("A", "A", 1, OBLIGATORIA, 0, []),
        "B": Materia("B", "B", 1, OBLIGATORIA, 0, []),
        "C": Materia("C", "C", 1, OBLIGATORIA, 0, [])
    }

ADYACENTES_3 = {
        "A": [],
        "B": [],
        "C": []
    }

MATERIAS_4 = {
        "A": Materia("A", "A", 1, OBLIGATORIA, 0, ["H"]),
        "B": Materia("B", "B", 2, OBLIGATORIA, 0, ["E"]),
        "C": Materia("C", "C", 1, OBLIGATORIA, 0, ["F"]),
        "D": Materia("D", "D", 4, OBLIGATORIA, 0, ["F"]),
        "E": Materia("E", "E", 1, OBLIGATORIA, 0, ["H"]),
        "F": Materia("B", "B", 3, OBLIGATORIA, 0, ["G", "K"]),
        "G": Materia("G", "G", 1, OBLIGATORIA, 0, []),
        "H": Materia("H", "H", 4, ELECTIVA, 0, []),
        "I": Materia("I", "I", 1, OBLIGATORIA, 7, []),
        "J": Materia("J", "J", 1, ELECTIVA, 0, []),
        "K": Materia("K", "K", 3, ELECTIVA, 0, []),
        "L": Materia("L", "L", 3, ELECTIVA, 0, []),
        "M": Materia("M", "M", 3, ELECTIVA, 0, []),
        "N": Materia("N", "N", 3, ELECTIVA, 0, [])
    }

ADYACENTES_4 = {
        "A": ["H"],
        "B": ["E"],
        "C": ["F"],
        "D": ["F"],
        "E": ["H"],
        "F": ["G", "K"],
        "G": [],
        "H": [],
        "I": [],
        "J": [],
        "K": [],
        "L": [],
        "M": [],
        "N": []        
    }

MATERIAS_5 = {
        "A": Materia("A", "A", 1, OBLIGATORIA, 0, []),
        "B": Materia("B", "B", 1, OBLIGATORIA, 0, [])
    }

ADYACENTES_5 = {
        "A": [],
        "B": []
    }

POS_MATERIA = 0
POS_ADYACENTE = 1
MATERIAS = {
    1: (MATERIAS_1, ADYACENTES_1),
    2: (MATERIAS_2, ADYACENTES_2),
    3: (MATERIAS_3, ADYACENTES_3),
    4: (MATERIAS_4, ADYACENTES_4),
    5: (MATERIAS_5, ADYACENTES_5)
}

def get_materias(num):
    """Devuelve un diccionario con la clave el codigo de materia y como valor una materia con sus datos"""
    return MATERIAS[num][POS_MATERIA]

def get_plan_carrera(num):
    """Devuelve una lista de adyacencias para un plan de carreras"""
    return MATERIAS[num][POS_ADYACENTE]
