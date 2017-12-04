from app import db
from flask_script import Command

from app.DAO.UsersDAO import create_users
from app.DAO.CarrerasDAO import create_carreras
from app.DAO.MateriasDAO import create_estados_materia, create_forma_aprobacion_materias
from app.DAO.EncuestasDAO import create_encuestas

class InitDbCommand(Command):
    """ Initialize the database."""

    def run(self):
        init_db()


def init_db():
    """ Initialize the database."""
    db.drop_all()
    db.create_all()

    create_users()
    create_carreras()
    create_estados_materia()
    create_forma_aprobacion_materias()
    create_encuestas()