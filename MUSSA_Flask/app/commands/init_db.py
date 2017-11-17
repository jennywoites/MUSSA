# This file defines command line commands for manage.py
#
# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>
# Modify: Jennifer Woites

from app import db
from flask_script import Command

from app.DAO.UsersDAO import create_users
from app.DAO.CarrerasDAO import create_carreras
from app.DAO.MateriasDAO import create_estados_materia, create_forma_aprobacion_materias

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