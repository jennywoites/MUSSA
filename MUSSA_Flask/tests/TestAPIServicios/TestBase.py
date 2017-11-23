from flask import Flask
from flask_testing import LiveServerTestCase
import unittest
import requests
import app

from flask_testing import TestCase
from flask import url_for
from app import create_app, db

from app.DAO.UsersDAO import create_users
from app.DAO.MateriasDAO import create_estados_materia, create_forma_aprobacion_materias

from app.models.user_models import User


class TestBase(TestCase):
    def get_test_db_name(self):
        return "sqlite:///tmp/" + self.get_test_name() + ".sql"


    def get_test_name(self):
        return "test_base"


    def create_app(self):
        settings = {}
        settings['SQLALCHEMY_DATABASE_URI'] = self.get_test_db_name()
        self.app = app.create_app(extra_config_settings=settings)
        return self.app


    def loguear_usuario(self):
        client = self.app.test_client()
        response = client.post(url_for('user.login'), follow_redirects=True,
                    data=dict(email='member@example.com', password='Password1'))
        print(response)
        assert(response.status_code==200)


    def loguear_administrador(self):
        client = self.app.test_client()
        response = client.post(url_for('user.login'), follow_redirects=True,
                    data=dict(email='admin@example.com', password='Password1'))
        assert(response.status_code==200)


    def get_usuario(self):
        return User.query.filter_by(email='member@example.com').first()


    def get_administrador(self):
        return User.query.filter_by(email='admin@example.com').first()


    def setUp(self):
        db.create_all()
        create_users()
        create_estados_materia()
        create_forma_aprobacion_materias()
        self.crear_datos_bd()
        db.session.commit()


    def crear_datos_bd(self):
        raise Exception("Debe implementarse en las clases hijas")


    def tearDown(self):
        db.session.remove()
        db.drop_all()
