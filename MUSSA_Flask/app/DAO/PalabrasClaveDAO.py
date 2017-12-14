from app.models.palabras_clave_models import *
from app import db

def get_tematicas_por_defecto():
    return [
        "DATA MINING",
        "MATEMATICA",
        "GESTION",
        "ADMINISTRACION",
        "ECONOMIA"
    ]

def create_tematicas():
    db.create_all()

    for tematica in get_tematicas_por_defecto():
        find_o_create_tematica(tematica)

    db.session.commit()


def find_o_create_tematica(descripcion):
    tematica = TematicaMateria.query.filter_by(tematica=descripcion).first()

    if not tematica:
        tematica = TematicaMateria(tematica=descripcion)
        db.session.add(tematica)
        db.session.commit()

    return tematica